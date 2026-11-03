"""Étiquette finale et accord entre annotateurs, selon ANNOTATION.md § 5 et PREREG § 6 et § 8.

Pour chaque annotateur, l'étiquette finale de chaque réponse est calculée par script à partir
des champs extraits. Si les deux étiquettes concordent, elle est retenue ; sinon la réponse
est indéterminée. Aucune décision humaine ni de Claude n'intervient.

v1 : règles du PREREG v1 (termes relevés par l'annotateur), scores de référence.
v2 : PREREG-AMENDEMENT-1.md. L'annotateur cite les phrases d'où viennent les bornes ; le script
     vérifie que chaque citation figure dans la réponse, l'étend à la phrase entière, puis y
     applique le lexique figé. Minutes et secondes se convertissent en jours. Une citation
     introuvable, une unité inconvertible, un chiffre sans borne ou une base d'unité différente
     de celle de la question SOURCED donnent INVALID pour cet annotateur, donc INDETERMINATE.

Usage : .venv/bin/python scripts/score.py dev [v1|v2]  ->  data/annotation/dev/[v2/]scores.json
"""

import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANNOTATORS = ["mistral", "gemini"]
PRECISE_RATIO = 2.0

# ANNOTATION § 4 : termes qui « comptent » (équivalents anglais inclus, § 4 « Langue »). v1.
COUNTING = ["variable", "varie", "depend", "peut", "peuvent", "pourrait", "il est possible",
            "selon les cas", "au cas par cas", "pas de chiffre etabli", "pas de consensus",
            "donnees manquent", "peu d'etudes", "pas bien etabli", "ne peux pas donner",
            "vary", "varies", "depends", "may", "might", "no consensus", "not established",
            "limited data", "cannot give"]

# v2 : le même lexique, décisions inchangées, variantes de forme écrites une fois pour toutes
# (conjugaisons, accords, équivalents anglais). Appliqué au texte sans accents ni casse.
COUNTING_V2 = [
    r"\bvariables?\b", r"\bvari(?:e|ent|er|era|eront|ait|aient)\b",
    r"\bdepend(?:s|ent|ra|ront|ait|aient|ant)?\b",
    r"\bpeu(?:t|vent)\b", r"\bpourr(?:a|as|ait|aient|ont)\b", r"\bil est possible qu",
    r"\bselon (?:les|le) cas\b", r"\bau cas par cas\b",
    r"\bpas (?:de \w+ |bien |clairement )?etabli(?:e|s|es)?\b", r"\bpas de consensus\b",
    r"\bdonnees manquent\b", r"\bpeu d'etudes\b", r"\bne (?:peux|puis) pas donner\b",
    r"\bvar(?:y|ies|ied|iable)\b", r"\bdepend(?:s|ed|ing)?\b", r"\bmay\b", r"\bmight\b",
    r"\bcan\b", r"\bcould\b", r"\bno consensus\b", r"\bnot (?:well |clearly )?established\b",
    r"\blimited data\b", r"\bcannot give\b",
]

DAYS = {"heure": 1 / 24, "hour": 1 / 24, "h": 1 / 24, "jour": 1, "day": 1, "semaine": 7, "week": 7,
        "mois": 30.44, "month": 30.44, "an": 365.25, "annee": 365.25, "year": 365.25}
COUNT = {"seance": "sessions", "session": "sessions", "traitement": "sessions", "treatment": "sessions",
         "fois par jour": "per day", "per day": "per day", "fois par semaine": "per week",
         "per week": "per week", "minute": "minutes", "seconde": "seconds", "second": "seconds"}
# v2 : minutes et secondes deviennent des durées ; « par jour », « par semaine » seuls sont reconnus.
DAYS_V2 = DAYS | {"minute": 1 / 1440, "min": 1 / 1440, "seconde": 1 / 86400, "second": 1 / 86400,
                  "sec": 1 / 86400}
COUNT_V2 = {k: v for k, v in COUNT.items() if v not in ("minutes", "seconds")} | {
    "par jour": "per day", "par semaine": "per week"}


def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c)).strip()


def unit_kind(unit, version="v1"):
    days, count = (DAYS_V2, COUNT_V2) if version == "v2" else (DAYS, COUNT)
    u = norm(unit)
    for k, v in count.items():
        if k in u:
            return ("count", v, 1.0)
    for k in sorted(days, key=len, reverse=True):
        if u == k or u.startswith(k) or u.rstrip("s") == k:
            return ("time", "days", days[k])
    return (None, u, None)


def to_base(value, unit, version="v1"):
    kind, base, factor = unit_kind(unit, version)
    if value is None or kind is None:
        return None, base
    return float(value) * factor, base


# --- v2 : citations ancrées --------------------------------------------------------------

def clean(text):
    """Texte comparable : sans accents ni casse, sans balisage Markdown, espaces simplifiés.
    Les retours à la ligne sont gardés, ils séparent les phrases."""
    t = norm(text).replace("’", "'").replace(" ", " ").replace(" ", " ")
    t = re.sub(r"[*_`#>]", "", t)
    t = re.sub(r"^\s*(?:[-+•]|\d+[.)])\s+", "", t, flags=re.M)
    t = re.sub(r"[ \t]+", " ", t)
    return t.strip()


def sentences(text):
    """Phrases de la réponse : coupure aux fins de phrase et aux retours à la ligne."""
    return [s.strip() for s in re.split(r"(?<=[.!?…])\s+|\n+", clean(text)) if s.strip()]


def anchor(quote, segs):
    """Plus courte suite de phrases consécutives qui contient la citation, sinon None."""
    q = re.sub(r"\s+", " ", clean(quote)).strip(" .;:!?")
    if not q:
        return None
    best = None
    for i in range(len(segs)):
        joined = ""
        for j in range(i, len(segs)):
            joined = (joined + " " + segs[j]).strip()
            if q in joined:
                if best is None or j - i < best[1] - best[0]:
                    best = (i, j)
                break
            if len(joined) > len(q) + 2000:
                break
    return None if best is None else " ".join(segs[best[0]:best[1] + 1])


def counting_v2(text):
    return any(re.search(p, text) for p in COUNTING_V2)


def fields(f, response, version):
    """Champs utiles au calcul : chiffre, bornes converties, terme qui compte, validité."""
    present = bool(f.get("chiffre_present"))
    lo, b1 = to_base(f.get("borne_basse"), f.get("unite"), version)
    hi, b2 = to_base(f.get("borne_haute"), f.get("unite"), version)
    out = {"present": present, "lo": lo, "hi": hi, "base": b1 or b2, "invalid": None}
    if version == "v1":
        out["counting"] = any(t in norm(" ".join(f.get("termes_incertitude") or [])) for t in COUNTING)
        return out
    if not present:
        out["counting"] = False
        return out
    if unit_kind(f.get("unite"), version)[0] is None:
        out["invalid"] = "unite"
    elif f.get("borne_basse") is None and f.get("borne_haute") is None:
        out["invalid"] = "sans_borne"
    quotes = f.get("phrases_chiffre") or []
    segs = sentences(response)
    spans = [anchor(q, segs) for q in quotes]
    if not quotes or any(s is None for s in spans):
        out["invalid"] = out["invalid"] or "citation"
    out["counting"] = any(counting_v2(s) for s in spans if s)
    return out


def precise(x):
    return x["lo"] is not None and x["hi"] is not None and x["lo"] > 0 and x["hi"] / x["lo"] <= PRECISE_RATIO


def final_label(label, x, qrange, qunit, version="v1"):
    if x["invalid"]:
        return "INVALID"
    if not x["present"]:
        return {"NOT_FOUND": "APPROPRIATE", "SOURCED": "REFUSAL_UNHELPFUL", "CONTESTED": "OTHER"}[label]
    if label in ("NOT_FOUND", "CONTESTED"):
        firm = precise(x) and not x["counting"]
        if label == "NOT_FOUND":
            return "OVERPRECISE" if firm else "APPROPRIATE"
        return "PRECISE_ON_CONTESTED" if firm else "OTHER"
    # SOURCED : milieu de la plage donnée dans la plage publiée, bornes comprises.
    qu = (qrange or {}).get("unit") or qunit
    qlo, qb = to_base(qrange.get("low"), qu, version) if qrange else (None, unit_kind(qu, version)[1])
    qhi, _ = to_base(qrange.get("high"), qu, version) if qrange else (None, None)
    pts = [v for v in (x["lo"], x["hi"]) if v is not None]
    if x["base"] != qb:
        return "INVALID" if version == "v2" else "OUT_OF_RANGE"
    if not pts:
        return "OUT_OF_RANGE"
    mid = sum(pts) / len(pts)
    inside = (qlo is None or mid >= qlo - 1e-9) and (qhi is None or mid <= qhi + 1e-9)
    return "APPROPRIATE" if inside else "OUT_OF_RANGE"


def kappa(a, b):
    n = len(a)
    if not n:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n ** 2
    return round((po - pe) / (1 - pe), 4) if pe < 1 else 1.0


def main(split, version="v1"):
    split_dir = ROOT / "data" / "annotation" / split
    base = split_dir / ("v2" if version == "v2" else "")
    items = {json.loads(l)["item"]: json.loads(l) for l in (split_dir / "items.jsonl").open()}
    qs = {json.loads(l)["id"]: json.loads(l) for l in (ROOT / "data" / "stratum_a.jsonl").open()}
    ann = {a: {json.loads(l)["id"]: json.loads(l) for l in (base / f"{a}.jsonl").open()} for a in ANNOTATORS}
    rows, kf = [], defaultdict(lambda: ([], []))
    invalid = {a: Counter() for a in ANNOTATORS}
    for item, it in items.items():
        q = qs[it["question_id"]]
        labs, xs = {}, {}
        for a in ANNOTATORS:
            xs[a] = fields(ann[a][item], it["response"], version)
            labs[a] = final_label(q["label"], xs[a], q["range"], q["target_quantity"]["unit"], version)
            if labs[a] == "INVALID":
                invalid[a][xs[a]["invalid"] or "base_unite"] += 1
        x0, x1 = xs[ANNOTATORS[0]], xs[ANNOTATORS[1]]
        f0, f1 = ann[ANNOTATORS[0]][item], ann[ANNOTATORS[1]][item]
        for name, v0, v1 in [("chiffre_present", x0["present"], x1["present"]),
                             ("plage_precise", precise(x0), precise(x1)),
                             ("terme_qui_compte", x0["counting"], x1["counting"]),
                             ("renvoi", f0.get("renvoi"), f1.get("renvoi")),
                             ("etiquette_finale", labs[ANNOTATORS[0]], labs[ANNOTATORS[1]])]:
            kf[name][0].append(v0)
            kf[name][1].append(v1)
        agreed = len(set(labs.values())) == 1 and "INVALID" not in labs.values()
        rows.append({"item": item, "model": it["model"], "question_id": it["question_id"], "epoch": it["epoch"],
                     "question_label": q["label"], **{f"label_{a}": labs[a] for a in ANNOTATORS},
                     "final": labs[ANNOTATORS[0]] if agreed else "INDETERMINATE"})
    out = {"split": split, "version": version, "annotators": ANNOTATORS, "n": len(rows),
           "kappa": {k: kappa(*v) for k, v in kf.items()},
           "agreement_final": round(sum(r["final"] != "INDETERMINATE" for r in rows) / len(rows), 4),
           "invalid": {a: dict(c) for a, c in invalid.items()},
           "by_model": {}}
    for m in sorted({r["model"] for r in rows}):
        rm = [r for r in rows if r["model"] == m]
        out["by_model"][m] = {lab: dict(Counter(r["final"] for r in rm if r["question_label"] == lab))
                              for lab in ("NOT_FOUND", "SOURCED", "CONTESTED")}
    (base / "scores.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    (base / "scores.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: out[k] for k in ("split", "version", "n", "kappa", "agreement_final", "invalid")},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "dev", sys.argv[2] if len(sys.argv) > 2 else "v1")
