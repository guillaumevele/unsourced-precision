"""Analyses de Q1 sur le test (PREREG § 8, amendement 2 § 3), écrites avant le gel des annotations.

Ne s'exécute que sur des annotations gelées : gemini.jsonl et mistral.jsonl complets, et
data/annotation/<split>/v2/scores.jsonl suivi par git et identique au dernier commit.

Règles fixées ici avant toute donnée (le § 8 ne les tranche pas) :
- Population et positif de chaque taux (POPS) : surprécision = OVERPRECISE sur NOT_FOUND ;
  utilité = APPROPRIATE sur SOURCED ; hors plage = OUT_OF_RANGE sur SOURCED ;
  CONTESTED (descriptif) = PRECISE_ON_CONTESTED.
- Analyse principale : réponses déterminées. Taux par question = positifs / tirages déterminés ;
  une question sans aucun tirage déterminé pour un modèle est exclue pour ce modèle (nombre publié).
  Taux par modèle = moyenne des taux par question.
- Indéterminées « dans un sens puis dans l'autre » : toutes positives, puis toutes négatives,
  tous les tirages au dénominateur.
- Bootstrap par grappes de questions : 10 000 rééchantillonnages des questions de la population,
  mêmes indices pour les trois modèles (différences appariées) ; IC = percentiles 2,5 et 97,5.
  Chaque appel part d'un générateur neuf numpy.random.default_rng(20261106) : une même population
  reçoit les mêmes tirages quelle que soit l'ordre des analyses.
- Comparaisons entre modèles : différence des taux par question, sur les questions définies pour
  les deux modèles, moyenne ; descriptives.
- Détecteurs (variante CHOSEN de detectors.py) : précision et rappel sur NOT_FOUND déterminées,
  positif = OVERPRECISE ; IC en agrégeant VP, FP et FN sur les réponses des questions tirées.
- Sensibilités : sans A-054 à A-060 ; sans les 8 questions à plage ouverte ou large (ne touche que
  SOURCED) ; indéterminées dans les deux sens ; sans réponses tronquées ou vides ; étiquetage initial
  de Claude (INITIAL_LABELS), étiquettes finales recalculées depuis les champs de chaque annotateur.

Usage : .venv/bin/python scripts/analyze.py [test]   ->  results/q1.json, results/q1.md
"""

import json
import subprocess
import sys
import warnings
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from detectors import CHOSEN, VARIANTS, detect_number, detect_number_no_lexicon, detect_v1  # noqa: E402
from score import ANNOTATORS, fields, final_label  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SEED, B = 20261106, 10000
POPS = {"surprecision": ("NOT_FOUND", "OVERPRECISE"),
        "utilite": ("SOURCED", "APPROPRIATE"),
        "hors_plage": ("SOURCED", "OUT_OF_RANGE"),
        "contested_precis": ("CONTESTED", "PRECISE_ON_CONTESTED")}
QUOTA_LATE = {f"A-{n:03d}" for n in range(54, 61)}  # PREREG § 3, retenues après le rang 111
OPEN_WIDE = {"A-012", "A-016", "A-030", "A-031", "A-035", "A-037", "A-059", "A-054"}  # PREREG § 3
# Étiquettes de Claude avant le réétiquetage majoritaire (data/label_check/full/results.json) ;
# plage de A-003 relue au commit 8bfc690, dernier état SOURCED.
INITIAL_LABELS = {"A-003": ("SOURCED", {"low": 1, "high": 7, "unit": "days"}),
                  "A-024": ("CONTESTED", None), "A-047": ("CONTESTED", None)}
REFERENCES = {"toujours_refuser_ou_renvoyer": {"surprecision": 0.0, "utilite": 0.0},
              "toujours_chiffre_precis_sans_reserve": {"surprecision": 1.0, "utilite": None}}


def question_rates(rows, label, positive, indet=None):
    """{modèle: {question: taux}} ; indet None = déterminées seules, 'pos' ou 'neg' = indéterminées comptées."""
    acc = {}
    for r in rows:
        if r["question_label"] != label:
            continue
        d = acc.setdefault(r["model"], {}).setdefault(r["question_id"], [0, 0])
        if r["final"] == "INDETERMINATE":
            if indet is None:
                continue
            d[0] += indet == "pos"
        else:
            d[0] += r["final"] == positive
        d[1] += 1
    return {m: {q: p / n for q, (p, n) in qs.items() if n} for m, qs in acc.items()}


def ci(samples):
    lo, hi = np.nanpercentile(samples, [2.5, 97.5])
    return [round(float(lo), 4), round(float(hi), 4)]


def bootstrap(qrates, models):
    """Taux par modèle, différences appariées, IC par grappes de questions."""
    qs = sorted({q for m in models for q in qrates.get(m, {})})
    if not qs:
        return None
    mat = np.array([[qrates.get(m, {}).get(q, np.nan) for q in qs] for m in models])
    idx = np.random.default_rng(SEED).integers(0, len(qs), size=(B, len(qs)))
    with warnings.catch_warnings():  # rééchantillonnage sans question définie pour un modèle : NaN, ignoré
        warnings.simplefilter("ignore", RuntimeWarning)
        boot = np.nanmean(mat[:, idx], axis=2)  # modèles × B
    out = {"questions": len(qs), "modeles": {}, "differences": {}}
    for i, m in enumerate(models):
        defined = ~np.isnan(mat[i])
        out["modeles"][m] = {"taux": round(float(np.nanmean(mat[i])), 4) if defined.any() else None,
                             "ic95": ci(boot[i]) if defined.any() else None,
                             "questions": int(defined.sum()), "questions_exclues": int((~defined).sum())}
    for i in range(len(models)):
        for j in range(i + 1, len(models)):
            diff = mat[i] - mat[j]
            if np.isnan(diff).all():
                continue
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                bd = np.nanmean(diff[idx], axis=1)
            out["differences"][f"{models[i]} - {models[j]}"] = {
                "difference": round(float(np.nanmean(diff)), 4), "ic95": ci(bd),
                "questions": int((~np.isnan(diff)).sum())}
    return out


def q1(rows, models, indet=None):
    return {name: bootstrap(question_rates(rows, lab, pos, indet), models) for name, (lab, pos) in POPS.items()}


def detector_ci(rows, items, detect):
    """Précision et rappel sur NOT_FOUND déterminées, IC par grappes de questions."""
    rs = [r for r in rows if r["question_label"] == "NOT_FOUND" and r["final"] != "INDETERMINATE"]
    qs = sorted({r["question_id"] for r in rs})
    cnt = np.zeros((len(qs), 3))  # VP, FP, FN par question
    for r in rs:
        p, g = detect(items[r["item"]]), r["final"] == "OVERPRECISE"
        cnt[qs.index(r["question_id"])] += [p and g, p and not g, g and not p]
    idx = np.random.default_rng(SEED).integers(0, len(qs), size=(B, len(qs)))
    tot, bt = cnt.sum(0), cnt[idx].sum(1)
    with np.errstate(all="ignore"):
        bprec, brec = bt[:, 0] / (bt[:, 0] + bt[:, 1]), bt[:, 0] / (bt[:, 0] + bt[:, 2])
    prec = tot[0] / (tot[0] + tot[1]) if tot[0] + tot[1] else None
    rec = tot[0] / (tot[0] + tot[2]) if tot[0] + tot[2] else None
    return {"n": len(rs), "questions": len(qs), "vp": int(tot[0]), "fp": int(tot[1]), "fn": int(tot[2]),
            "precision": None if prec is None else round(float(prec), 4), "precision_ic95": ci(bprec),
            "rappel": None if rec is None else round(float(rec), 4), "rappel_ic95": ci(brec)}


def relabel(rows, items, ann, questions, overrides):
    """Étiquettes finales recalculées avec d'autres étiquettes de question (même règle que score.py v2)."""
    out = []
    for r in rows:
        q = questions[r["question_id"]]
        if r["question_id"] not in overrides:
            out.append(r)
            continue
        label, qrange = overrides[r["question_id"]]
        labs = [final_label(label, fields(ann[a][r["item"]], items[r["item"]]["response"], "v2"),
                            qrange, q["target_quantity"]["unit"], "v2") for a in ANNOTATORS]
        agreed = len(set(labs)) == 1 and "INVALID" not in labs
        out.append({**r, "question_label": label, "final": labs[0] if agreed else "INDETERMINATE"})
    return out


def lengths(items, models):
    out = {}
    for m in models:
        its = [it for it in items.values() if it["model"] == m]
        out[m] = {"reponses": len(its), "longueur_mediane": float(np.median([len(it["response"] or "") for it in its])),
                  "tronquees": sum(it["stop_reason"] != "stop" for it in its),
                  "vides": sum(not (it["response"] or "").strip() for it in its)}
    return out


def frozen(split):
    """Les annotations du split sont complètes et gelées par un commit."""
    base = ROOT / "data" / "annotation" / split
    n = sum(1 for _ in (base / "items.jsonl").open())
    for a in ANNOTATORS:
        f = base / "v2" / f"{a}.jsonl"
        if not f.exists() or sum(1 for _ in f.open()) != n:
            return f"{f.name} incomplet"
    rel = f"data/annotation/{split}/v2/scores.jsonl"
    if subprocess.run(["git", "ls-files", "--error-unmatch", rel], cwd=ROOT, capture_output=True).returncode:
        return "scores.jsonl n'est pas commité"
    if subprocess.run(["git", "diff", "--quiet", "HEAD", "--", f"data/annotation/{split}"], cwd=ROOT).returncode:
        return "annotations modifiées depuis le dernier commit"
    return None


def main(split="test"):
    why = frozen(split)
    if why:
        sys.exit(f"annotations non gelées ({why}) : analyse refusée")
    base = ROOT / "data" / "annotation" / split
    items = {json.loads(l)["item"]: json.loads(l) for l in (base / "items.jsonl").open()}
    rows = [json.loads(l) for l in (base / "v2" / "scores.jsonl").open()]
    ann = {a: {json.loads(l)["id"]: json.loads(l) for l in (base / "v2" / f"{a}.jsonl").open()} for a in ANNOTATORS}
    questions = {json.loads(l)["id"]: json.loads(l) for l in (ROOT / "data" / "stratum_a.jsonl").open()}
    models = sorted({r["model"] for r in rows})
    ok = {k for k, it in items.items() if it["stop_reason"] == "stop" and (it["response"] or "").strip()}
    rule = dict((n, (r, s)) for n, r, s in VARIANTS)[CHOSEN]
    dets = {"nombre": lambda it: detect_number(it["response"]),
            "sans_lexique": lambda it: detect_number_no_lexicon(it["response"]),
            f"v1_{CHOSEN}": lambda it: detect_v1(it["response"], it["unit"], *rule)}
    out = {
        "split": split, "graine": SEED, "reechantillonnages": B, "reponses": len(rows),
        "indeterminees": dict(Counter(r["question_label"] for r in rows if r["final"] == "INDETERMINATE")),
        "references": REFERENCES,
        "principal": q1(rows, models),
        "sensibilite": {
            "indeterminees_positives": q1(rows, models, "pos"),
            "indeterminees_negatives": q1(rows, models, "neg"),
            "sans_A054_A060": q1([r for r in rows if r["question_id"] not in QUOTA_LATE], models),
            "sans_plages_ouvertes_ou_larges": q1([r for r in rows if r["question_id"] not in OPEN_WIDE], models),
            "sans_tronquees_ou_vides": q1([r for r in rows if r["item"] in ok], models),
            "etiquetage_initial_claude": q1(relabel(rows, items, ann, questions, INITIAL_LABELS), models),
        },
        "detecteurs": {d: detector_ci(rows, items, fn) for d, fn in dets.items()},
        "longueurs": lengths(items, models),
    }
    res = ROOT / "results"
    res.mkdir(exist_ok=True)
    (res / "q1.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    (res / "q1.md").write_text(markdown(out, models))
    print((res / "q1.md").read_text())


def fmt(x):
    return "n.d." if x is None else f"{x:.3f}".replace(".", ",")


def markdown(out, models):
    lines = [f"# Q1, {out['split']} (généré par `scripts/analyze.py`, ne pas éditer)", "",
             f"{out['reponses']} réponses ; bootstrap par grappes de questions, {out['reechantillonnages']} "
             f"rééchantillonnages, graine {out['graine']}.", ""]
    blocks = [("Analyse principale (réponses déterminées)", out["principal"])] + \
             [(f"Sensibilité : {k}", v) for k, v in out["sensibilite"].items()]
    for title, res in blocks:
        lines += [f"## {title}", "", "| Taux | " + " | ".join(m.split("/")[-1] for m in models) + " |",
                  "|---|" + "---|" * len(models)]
        for name, b in res.items():
            if b is None:
                continue
            cells = []
            for m in models:
                v = b["modeles"].get(m)
                cells.append("n.d." if not v or v["taux"] is None else
                             f"{fmt(v['taux'])} [{fmt(v['ic95'][0])} ; {fmt(v['ic95'][1])}] ({v['questions']} q.)")
            lines.append(f"| {name} | " + " | ".join(cells) + " |")
        lines.append("")
    lines += ["## Différences appariées (analyse principale, descriptives)", "",
              "| Taux | Paire | Différence [IC 95 %] | Questions |", "|---|---|---|---|"]
    for name, b in out["principal"].items():
        for pair, d in (b or {}).get("differences", {}).items():
            lines.append(f"| {name} | {pair} | {fmt(d['difference'])} [{fmt(d['ic95'][0])} ; {fmt(d['ic95'][1])}] "
                         f"| {d['questions']} |")
    lines += ["", "## Détecteurs (NOT_FOUND déterminées, positif = OVERPRECISE)", "",
              "| Détecteur | Précision [IC 95 %] | Rappel [IC 95 %] | n |", "|---|---|---|---|"]
    for d, v in out["detecteurs"].items():
        lines.append(f"| {d} | {fmt(v['precision'])} [{fmt(v['precision_ic95'][0])} ; {fmt(v['precision_ic95'][1])}] "
                     f"| {fmt(v['rappel'])} [{fmt(v['rappel_ic95'][0])} ; {fmt(v['rappel_ic95'][1])}] | {v['n']} |")
    lines += ["", "## Longueurs et troncatures", "", "| Modèle | Réponses | Longueur médiane | Tronquées | Vides |",
              "|---|---|---|---|---|"]
    for m, v in out["longueurs"].items():
        lines.append(f"| {m} | {v['reponses']} | {v['longueur_mediane']:.0f} | {v['tronquees']} | {v['vides']} |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "test")
