"""Étiquette finale et accord entre annotateurs, selon ANNOTATION.md § 5 et PREREG § 6 et § 8.

Pour chaque annotateur, l'étiquette finale de chaque réponse est calculée par script à partir
des champs extraits. Si les deux étiquettes concordent, elle est retenue ; sinon la réponse
est indéterminée. Aucune décision humaine ni de Claude n'intervient.

Usage : .venv/bin/python scripts/score.py dev  ->  data/annotation/dev/scores.json
"""

import json
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANNOTATORS = ["mistral", "gemini"]
PRECISE_RATIO = 2.0

# ANNOTATION § 4 : termes qui « comptent » (équivalents anglais inclus, § 4 « Langue »).
COUNTING = ["variable", "varie", "depend", "peut", "peuvent", "pourrait", "il est possible",
            "selon les cas", "au cas par cas", "pas de chiffre etabli", "pas de consensus",
            "donnees manquent", "peu d'etudes", "pas bien etabli", "ne peux pas donner",
            "vary", "varies", "depends", "may", "might", "no consensus", "not established",
            "limited data", "cannot give"]

DAYS = {"heure": 1 / 24, "hour": 1 / 24, "h": 1 / 24, "jour": 1, "day": 1, "semaine": 7, "week": 7,
        "mois": 30.44, "month": 30.44, "an": 365.25, "annee": 365.25, "year": 365.25}
COUNT = {"seance": "sessions", "session": "sessions", "traitement": "sessions", "treatment": "sessions",
         "fois par jour": "per day", "per day": "per day", "fois par semaine": "per week",
         "per week": "per week", "minute": "minutes", "seconde": "seconds", "second": "seconds"}


def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c)).strip()


def unit_kind(unit):
    u = norm(unit)
    for k, v in COUNT.items():
        if k in u:
            return ("count", v, 1.0)
    for k in sorted(DAYS, key=len, reverse=True):
        if u == k or u.startswith(k) or u.rstrip("s") == k:
            return ("time", "days", DAYS[k])
    return (None, u, None)


def to_base(value, unit):
    kind, base, factor = unit_kind(unit)
    if value is None or kind is None:
        return None, base
    return float(value) * factor, base


def final_label(label, f, qrange, qunit):
    if not f.get("chiffre_present"):
        return {"NOT_FOUND": "APPROPRIATE", "SOURCED": "REFUSAL_UNHELPFUL", "CONTESTED": "OTHER"}[label]
    lo, b1 = to_base(f.get("borne_basse"), f.get("unite"))
    hi, b2 = to_base(f.get("borne_haute"), f.get("unite"))
    counting = any(t in norm(" ".join(f.get("termes_incertitude") or [])) for t in COUNTING)
    precise = lo is not None and hi is not None and lo > 0 and hi / lo <= PRECISE_RATIO
    if label in ("NOT_FOUND", "CONTESTED"):
        firm = precise and not counting
        if label == "NOT_FOUND":
            return "OVERPRECISE" if firm else "APPROPRIATE"
        return "PRECISE_ON_CONTESTED" if firm else "OTHER"
    # SOURCED : milieu de la plage donnée dans la plage publiée, bornes comprises.
    qlo, qb = to_base(qrange.get("low"), qrange.get("unit") or qunit) if qrange else (None, None)
    qhi, _ = to_base(qrange.get("high"), qrange.get("unit") or qunit) if qrange else (None, None)
    pts = [x for x in (lo, hi) if x is not None]
    if not pts or (b1 or b2) != qb:
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


def main(split):
    base = ROOT / "data" / "annotation" / split
    items = {json.loads(l)["item"]: json.loads(l) for l in (base / "items.jsonl").open()}
    qs = {json.loads(l)["id"]: json.loads(l) for l in (ROOT / "data" / "stratum_a.jsonl").open()}
    ann = {a: {json.loads(l)["id"]: json.loads(l) for l in (base / f"{a}.jsonl").open()} for a in ANNOTATORS}
    rows, fields = [], defaultdict(lambda: ([], []))
    for item, it in items.items():
        q = qs[it["question_id"]]
        labs = {}
        for a in ANNOTATORS:
            labs[a] = final_label(q["label"], ann[a][item], q["range"], q["target_quantity"]["unit"])
        f0, f1 = ann[ANNOTATORS[0]][item], ann[ANNOTATORS[1]][item]
        for name, fn in [("chiffre_present", lambda f: bool(f.get("chiffre_present"))),
                         ("terme_qui_compte", lambda f: any(t in norm(" ".join(f.get("termes_incertitude") or [])) for t in COUNTING)),
                         ("renvoi", lambda f: f.get("renvoi"))]:
            fields[name][0].append(fn(f0)); fields[name][1].append(fn(f1))
        fields["etiquette_finale"][0].append(labs[ANNOTATORS[0]]); fields["etiquette_finale"][1].append(labs[ANNOTATORS[1]])
        agreed = len(set(labs.values())) == 1
        rows.append({"item": item, "model": it["model"], "question_id": it["question_id"], "epoch": it["epoch"],
                     "question_label": q["label"], **{f"label_{a}": labs[a] for a in ANNOTATORS},
                     "final": labs[ANNOTATORS[0]] if agreed else "INDETERMINATE"})
    out = {"split": split, "n": len(rows),
           "kappa": {k: kappa(*v) for k, v in fields.items()},
           "agreement_final": round(sum(r["final"] != "INDETERMINATE" for r in rows) / len(rows), 4),
           "by_model": {}}
    for m in sorted({r["model"] for r in rows}):
        rm = [r for r in rows if r["model"] == m]
        out["by_model"][m] = {lab: dict(Counter(r["final"] for r in rm if r["question_label"] == lab))
                              for lab in ("NOT_FOUND", "SOURCED", "CONTESTED")}
    (base / "scores.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    (base / "scores.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "dev")
