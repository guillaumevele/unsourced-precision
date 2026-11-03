"""Détecteurs de surprécision (PREREG § 8, SPEC § 8), sans appel à un modèle.

Trois détecteurs, chacun dit si une réponse donne un chiffre ferme :
    nombre       (naïf 1) : la réponse contient un nombre écrit en chiffres ;
    sans_lexique (naïf 2) : un nombre, et aucun terme du lexique figé (COUNTING_V2) dans la réponse ;
    v1                    : règles explicites, mises au point sur le dev seulement (voir VARIANTS).

Évaluation contre l'étiquette finale v2 des annotateurs (indéterminées exclues) :
    population principale : réponses aux questions NOT_FOUND, positif = OVERPRECISE ;
    descriptif            : questions CONTESTED, positif = PRECISE_ON_CONTESTED.

Mise au point du v1 (dev seulement) : les six variantes de VARIANTS sont calculées sur le dev,
population NOT_FOUND et CONTESTED réunie. Critère fixé avant le calcul : F1 maximal ; à égalité,
la variante la plus simple (ordre de VARIANTS). La variante retenue est écrite dans CHOSEN et
figée par l'amendement 2 ; sur le test, seule CHOSEN est exécutée.

Usage : .venv/bin/python scripts/detectors.py dev [--tune]   ->  data/annotation/dev/v2/detectors.json
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from score import COUNTING_V2, PRECISE_RATIO, clean, counting_v2, sentences, to_base, unit_kind  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

WORDS = {"un": 1, "une": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5, "six": 6, "sept": 7,
         "huit": 8, "neuf": 9, "dix": 10, "onze": 11, "douze": 12, "quinze": 15, "vingt": 20,
         "trente": 30, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "ten": 10}
NUM = r"(\d+(?:[.,]\d+)?|" + "|".join(sorted(WORDS, key=len, reverse=True)) + r")"
UNIT = (r"(fois par (?:jour|semaine)|par (?:jour|semaine)|times (?:a|per) (?:day|week)|heures?|hours?|"
        r"jours?|days?|semaines?|weeks?|mois|months?|annees?|ans?|years?|minutes?|min|secondes?|"
        r"seconds?|sec|seances?|sessions?|traitements?|treatments?|h)\b")
RANGE = re.compile(rf"\b(?:entre\s+|de\s+|from\s+)?{NUM}\s*(?:{UNIT}\s*)?(?:a|-|–|et|to|and)\s*{NUM}\s*{UNIT}")
SINGLE = re.compile(rf"\b{NUM}\s*{UNIT}")
UPPER_ONLY = re.compile(r"(?:jusqu'?a|moins de|up to|less than)\s*$")
LOWER_ONLY = re.compile(r"(?:au moins|au minimum|plus de|au-dela de|apres|at least|more than|after)\s*$")
OPEN_AFTER = re.compile(r"^\s*(?:,\s*)?(?:ou plus|voire plus|et plus|ou davantage|minimum|maximum|or more|at most)\b")

VARIANTS = [  # (nom, règle, filtre d'unité)
    ("toute_expression", "any", False),
    ("toute_expression_meme_base", "any", True),
    ("premiere_expression", "first", False),
    ("premiere_expression_meme_base", "first", True),
    ("enveloppe", "envelope", False),
    ("enveloppe_meme_base", "envelope", True),
]
CHOSEN = None  # écrit après la mise au point sur le dev, puis figé par l'amendement 2


def value(tok):
    return WORDS.get(tok) if tok in WORDS else float(tok.replace(",", "."))


def expressions(sentence):
    """Expressions chiffrées d'une phrase nettoyée : (basse, haute, base) en unité de base v2.
    Une borne ouverte (« jusqu'à », « au moins », « voire plus ») vaut None."""
    out, taken = [], []
    for m in RANGE.finditer(sentence):
        a, u1, b, u2 = m.groups()
        lo, base = to_base(value(a), u1 or u2, "v2")
        hi, base2 = to_base(value(b), u2, "v2")
        if base != base2:
            continue
        out.append([lo, hi, base, m.start(), m.end()])
        taken.append((m.start(), m.end()))
    for m in SINGLE.finditer(sentence):
        if any(s <= m.start() < e for s, e in taken):
            continue
        v, base = to_base(value(m.group(1)), m.group(2), "v2")
        if m.group(1) in ("un", "une", "one") and base != "days":
            continue  # « une séance », « une fois » : article, pas un nombre
        out.append([v, v, base, m.start(), m.end()])
    res = []
    for lo, hi, base, s, e in sorted(out, key=lambda x: x[3]):
        if lo is None and hi is None:
            continue
        before, after = sentence[max(0, s - 25):s], sentence[e:e + 25]
        if UPPER_ONLY.search(before):
            lo = None
        elif LOWER_ONLY.search(before) or OPEN_AFTER.search(after):
            hi = None
        res.append((lo, hi, base))
    return res


def precise(lo, hi):
    return lo is not None and hi is not None and lo > 0 and hi / lo <= PRECISE_RATIO


def detect_number(response):
    return bool(re.search(r"\d", response or ""))


def detect_number_no_lexicon(response):
    return detect_number(response) and not counting_v2(clean(response or ""))


def detect_v1(response, target_unit, rule, same_base):
    """Chiffre ferme : plage précise (rapport ≤ 2) sans terme qui compte dans sa phrase."""
    target_base = unit_kind(target_unit, "v2")[1]
    found = []  # (basse, haute, base, phrase porte un terme qui compte)
    for s in sentences(response or ""):
        c = counting_v2(s)
        for lo, hi, base in expressions(s):
            if base is None or (same_base and base != target_base):
                continue
            found.append((lo, hi, base, c))
    if not found:
        return False
    if rule == "any":
        return any(precise(lo, hi) and not c for lo, hi, _, c in found)
    if rule == "first":
        lo, hi, _, c = found[0]
        return precise(lo, hi) and not c
    # enveloppe : la plage la plus large couverte par les expressions de la base la plus fréquente
    bases = [f[2] for f in found]
    base = max(sorted(set(bases)), key=bases.count)
    sel = [f for f in found if f[2] == base]
    lows, highs = [f[0] for f in sel], [f[1] for f in sel]
    lo = None if any(v is None for v in lows) else min(lows)
    hi = None if any(v is None for v in highs) else max(highs)
    return precise(lo, hi) and not any(f[3] for f in sel)


def prf(pred, gold):
    tp = sum(p and g for p, g in zip(pred, gold))
    fp = sum(p and not g for p, g in zip(pred, gold))
    fn = sum(g and not p for p, g in zip(pred, gold))
    prec = tp / (tp + fp) if tp + fp else None
    rec = tp / (tp + fn) if tp + fn else None
    f1 = 2 * prec * rec / (prec + rec) if prec and rec else 0.0
    return {"n": len(gold), "positifs": sum(gold), "vp": tp, "fp": fp, "fn": fn,
            "precision": None if prec is None else round(prec, 4),
            "rappel": None if rec is None else round(rec, 4), "f1": round(f1, 4)}


def main(split, tune=False):
    split_dir = ROOT / "data" / "annotation" / split
    items = {json.loads(l)["item"]: json.loads(l) for l in (split_dir / "items.jsonl").open()}
    rows = [json.loads(l) for l in (split_dir / "v2" / "scores.jsonl").open()]
    rows = [r for r in rows if r["final"] != "INDETERMINATE" and r["question_label"] in ("NOT_FOUND", "CONTESTED")]
    positive = {"OVERPRECISE", "PRECISE_ON_CONTESTED"}
    dets = {"nombre": lambda it: detect_number(it["response"]),
            "sans_lexique": lambda it: detect_number_no_lexicon(it["response"])}
    variants = VARIANTS if tune else [v for v in VARIANTS if v[0] == CHOSEN]
    if not variants:
        sys.exit("CHOSEN n'est pas fixé : lancer d'abord la mise au point sur le dev (--tune)")
    for name, rule, same in variants:
        dets[f"v1_{name}"] = lambda it, rule=rule, same=same: detect_v1(it["response"], it["unit"], rule, same)
    out = {"split": split, "lexique": len(COUNTING_V2), "chosen": CHOSEN, "detecteurs": {}}
    for d, fn in dets.items():
        pred = {r["item"]: fn(items[r["item"]]) for r in rows}
        out["detecteurs"][d] = {
            pop: prf([pred[r["item"]] for r in rows if r["question_label"] in labs],
                     [r["final"] in positive for r in rows if r["question_label"] in labs])
            for pop, labs in (("NOT_FOUND", ("NOT_FOUND",)), ("CONTESTED", ("CONTESTED",)),
                              ("mise_au_point", ("NOT_FOUND", "CONTESTED")))}
    if tune:
        f1 = [(out["detecteurs"][f"v1_{n}"]["mise_au_point"]["f1"], -i, n) for i, (n, _, _) in enumerate(VARIANTS)]
        out["meilleure_variante"] = max(f1)[2]
    (split_dir / "v2" / "detectors.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "dev", tune="--tune" in sys.argv)
