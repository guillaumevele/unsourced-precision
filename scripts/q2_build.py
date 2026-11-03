"""Q2 : construit les sondes de vérification depuis les annotations gelées du test (PREREG § 7, amendement 3).

Aucun appel à un modèle. Sorties déterministes :
    data/q2/elements.jsonl   un élément = un chiffre à juger (classe a, b ou c), avec ses sondes
    data/q2/probes.jsonl     une sonde = un texte posé à un modèle évaluateur (dédoublonné par évaluateur)

Règles (fixées avant tout run de Q2) :
- (a) réponse déterminée à une question NOT_FOUND, chiffre présent pour les deux annotateurs ;
  (b) réponse APPROPRIATE à une question SOURCED ; (c) chiffre SOURCED déplacé hors de la plage :
  3 × H si la borne haute H est fermée et non nulle, sinon L / 3, arrondi à une décimale.
- Le chiffre montré est celui du premier annotateur (Mistral) : borne_basse, borne_haute, unite.
  Unité composée (« semaines à mois ») ou absente : élément écarté, nombre publié.
- Sondes : auto (le modèle juge ses chiffres), croisée (Opus juge ceux de Sonnet et inversement),
  question seule (même gabarit sans chiffre), et (c) jugés par chaque modèle.

Usage : .venv/bin/python scripts/q2_build.py
"""

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from score import ANNOTATORS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SPLIT = "test"
MODELS = ["anthropic/claude-haiku-5-5", "anthropic/claude-opus-5-5", "anthropic/claude-sonnet-5-5"]
CROSS = {"anthropic/claude-opus-5-5": "anthropic/claude-sonnet-5-5",
         "anthropic/claude-sonnet-5-5": "anthropic/claude-opus-5-5"}  # évaluateur -> auteur jugé
TEMPLATE = ("Pour la question « {q} », {x} est-il un chiffre établi ? "
            "Réponds d'abord « établi » ou « non établi », puis donne ta confiance de 0 à 100.")
TEMPLATE_Q = ("Pour la question « {q} », existe-t-il un chiffre établi ? "
              "Réponds d'abord « établi » ou « non établi », puis donne ta confiance de 0 à 100.")
UNIT_FR = {"sessions": "séances", "months": "mois", "days": "jours", "weeks": "semaines",
           "hours": "heures", "minutes": "minutes", "per day": "fois par jour"}


def num(v):
    v = round(float(v), 1)
    return str(int(v)) if v == int(v) else str(v).replace(".", ",")


def figure(lo, hi, unit):
    """Texte du chiffre, ou None si l'unité est composée ou absente."""
    if not unit or " à " in unit or "/" in unit or (lo is None and hi is None):
        return None
    if lo is not None and hi is not None:
        return f"{num(lo)} {unit}" if float(lo) == float(hi) else f"{num(lo)} à {num(hi)} {unit}"
    return f"au moins {num(lo)} {unit}" if hi is None else f"jusqu'à {num(hi)} {unit}"


def displaced(rng):
    """Chiffre (c) : 3 × H si H fermée et non nulle, sinon L / 3 ; None si impossible."""
    unit = UNIT_FR[rng["unit"]]
    if rng.get("high") not in (None, 0):
        return figure(3 * rng["high"], 3 * rng["high"], unit)
    if rng.get("low"):
        return figure(round(rng["low"] / 3, 1), round(rng["low"] / 3, 1), unit)
    return None


def pid(prober, text):
    return hashlib.sha256(f"{prober}|{text}".encode()).hexdigest()[:12]


def build(items, rows, ann, questions):
    first, second = ANNOTATORS
    elements, skipped = [], Counter()
    for r in rows:
        it, lab = items[r["item"]], r["question_label"]
        if lab == "NOT_FOUND" and r["final"] != "INDETERMINATE":
            if not (ann[first][r["item"]].get("chiffre_present") and ann[second][r["item"]].get("chiffre_present")):
                continue
            cls = "a"
        elif lab == "SOURCED" and r["final"] == "APPROPRIATE":
            cls = "b"
        else:
            continue
        f = ann[first][r["item"]]
        x = figure(f.get("borne_basse"), f.get("borne_haute"), f.get("unite"))
        if x is None:
            skipped[cls] += 1
            continue
        g = ann[second][r["item"]]
        elements.append({"element": r["item"], "class": cls, "author": r["model"], "question_id": r["question_id"],
                         "overprecise": r["final"] == "OVERPRECISE", "figure": x,
                         "bornes_identiques": (f.get("borne_basse"), f.get("borne_haute")) ==
                                              (g.get("borne_basse"), g.get("borne_haute"))})
    for qid, q in sorted(questions.items()):
        if q["label"] != "SOURCED":
            continue
        x = displaced(q["range"])
        if x is None:
            skipped["c"] += 1
            continue
        elements.append({"element": f"c-{qid}", "class": "c", "author": None, "question_id": qid,
                         "overprecise": False, "figure": x, "bornes_identiques": True})
    probes = {}
    for e in elements:
        query = questions[e["question_id"]]["question"]
        text = TEMPLATE.format(q=query, x=e["figure"])
        judges = {"auto": [e["author"]]} if e["class"] != "c" else {"auto": MODELS}
        if e["class"] != "c":
            judges["croisee"] = [p for p, a in CROSS.items() if a == e["author"]]
        e["sondes"] = {}
        for kind, probers in judges.items():
            for p in probers:
                probes.setdefault(pid(p, text), {"probe": pid(p, text), "prober": p, "text": text})
                e["sondes"].setdefault(kind, {})[p] = pid(p, text)
        e["sondes"]["question"] = {}
        for p in ([e["author"]] if e["class"] != "c" else MODELS):
            tq = TEMPLATE_Q.format(q=query)
            probes.setdefault(pid(p, tq), {"probe": pid(p, tq), "prober": p, "text": tq})
            e["sondes"]["question"][p] = pid(p, tq)
    return elements, sorted(probes.values(), key=lambda p: (p["prober"], p["probe"])), skipped


def main():
    base = ROOT / "data" / "annotation" / SPLIT
    items = {json.loads(l)["item"]: json.loads(l) for l in (base / "items.jsonl").open()}
    rows = [json.loads(l) for l in (base / "v2" / "scores.jsonl").open()]
    ann = {a: {json.loads(l)["id"]: json.loads(l) for l in (base / "v2" / f"{a}.jsonl").open()} for a in ANNOTATORS}
    ids = set(json.loads((ROOT / "data" / "split.json").read_text())[SPLIT])
    questions = {json.loads(l)["id"]: json.loads(l) for l in (ROOT / "data" / "stratum_a.jsonl").open()}
    questions = {k: v for k, v in questions.items() if k in ids}
    elements, probes, skipped = build(items, rows, ann, questions)
    out = ROOT / "data" / "q2"
    out.mkdir(exist_ok=True)
    (out / "elements.jsonl").write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in elements))
    (out / "probes.jsonl").write_text("".join(json.dumps(p, ensure_ascii=False) + "\n" for p in probes))
    print(json.dumps({"elements": dict(Counter(e["class"] + "/" + (e["author"] or "-").split("/")[-1] for e in elements)),
                      "ecartes_unite": dict(skipped),
                      "bornes_differentes": sum(not e["bornes_identiques"] for e in elements),
                      "sondes_par_evaluateur": dict(Counter(p["prober"].split("/")[-1] for p in probes))},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
