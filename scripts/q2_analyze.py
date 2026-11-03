"""Analyse de Q2 (PREREG § 7, SPEC § 6, amendement 3), écrite avant tout run de Q2.

Règles fixées ici avant toute donnée :
- Lecture d'une réponse : texte sans accents ni casse ; verdict = première occurrence de
  « non établi » ou « pas établi » / « établi » (ou « not established » / « established ») ; confiance = premier entier
  de 0 à 100 qui suit le verdict. Score « établi » = confiance si « établi », 100 − confiance sinon.
  Réponse illisible : écartée, taux publié par évaluateur.
- Score d'un élément pour un évaluateur = moyenne des tirages lisibles de sa sonde ; élément sans
  tirage lisible écarté (nombre publié).
- AUROC de (b) contre (a) : probabilité qu'un élément (b) ait un score plus haut qu'un élément (a),
  égalités à 1/2. IC à 95 % par bootstrap par grappes de questions, 10 000 rééchantillonnages,
  graine 20261107 ; rééchantillonnage sans les deux classes ignoré (nombre publié).
- Verdict par modèle, sur la sonde auto : « discrimine » si borne basse > 0,5 (prioritaire, ordre de la
  SPEC § 6) ; sinon « réfuté » si borne haute < 0,6 ; sinon « non concluant ». Jamais interprété en termes de « savoir ».
- Témoins, différences appariées sur les mêmes éléments et les mêmes rééchantillonnages :
  question seule ; dispersion des 5 tirages de Q1 (écart type de log10 du milieu des plages du premier
  annotateur, au moins deux tirages chiffrés ; score = − dispersion) ; croisé (Opus et Sonnet).
  « Au-delà de la question seule » seulement si la borne basse de AUROC auto − AUROC question > 0.
- Descriptif : AUROC de (b) contre (c). Sensibilités : (a) restreint aux réponses OVERPRECISE ;
  éléments dont les bornes sont identiques chez les deux annotateurs.

Usage : .venv/bin/python scripts/q2_analyze.py   ->  results/q2.json, results/q2.md
"""

import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from score import ANNOTATORS, norm, to_base  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SEED, B = 20261107, 10000
MODELS = ["anthropic/claude-haiku-5-5", "anthropic/claude-opus-5-5", "anthropic/claude-sonnet-5-5"]
VERDICT = re.compile(r"\b((?:non|pas)\s+etabli|not\s+established|etabli|established)\b")


def parse(text):
    """Score « établi » de 0 à 100, ou None si la réponse est illisible."""
    t = norm(text or "")
    m = VERDICT.search(t)
    if not m:
        return None
    for c in re.finditer(r"(?<![\d,.])(\d{1,3})(?![\d,.]?\d)", t[m.end():]):
        v = int(c.group(1))
        if v <= 100:
            return float(v) if m.group(1) in ("etabli", "established") else float(100 - v)  # non, pas, not
    return None


def auroc_boot(pos, neg, seed=SEED):
    """pos, neg : listes de (question, score). Renvoie AUROC, IC, et la matrice des rééchantillonnages."""
    qs = sorted({q for q, _ in pos} | {q for q, _ in neg})
    if not pos or not neg:
        return None
    qi = {q: i for i, q in enumerate(qs)}
    sp, sn = np.array([s for _, s in pos]), np.array([s for _, s in neg])
    cmp = (sp[:, None] > sn[None, :]) + 0.5 * (sp[:, None] == sn[None, :])
    w = np.random.default_rng(seed).multinomial(len(qs), [1 / len(qs)] * len(qs), size=B)
    wp, wn = w[:, [qi[q] for q, _ in pos]], w[:, [qi[q] for q, _ in neg]]
    den = wp.sum(1) * wn.sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        boot = np.einsum("bi,ij,bj->b", wp, cmp, wn) / den
    boot[den == 0] = np.nan
    return {"auroc": float(cmp.mean()), "boot": boot}


def summary(r):
    if r is None:
        return None
    lo, hi = np.nanpercentile(r["boot"], [2.5, 97.5])
    return {"auroc": round(r["auroc"], 4), "ic95": [round(float(lo), 4), round(float(hi), 4)],
            "reechantillonnages_ignores": int(np.isnan(r["boot"]).sum())}


def verdict(s):
    if s is None:
        return "non calculable"
    if s["ic95"][0] > 0.5:
        return "discrimine"
    if s["ic95"][1] < 0.6:
        return "réfuté"
    return "non concluant"


def diff(r1, r2):
    if r1 is None or r2 is None:
        return None
    d = r1["boot"] - r2["boot"]
    lo, hi = np.nanpercentile(d, [2.5, 97.5])
    return {"difference": round(r1["auroc"] - r2["auroc"], 4), "ic95": [round(float(lo), 4), round(float(hi), 4)]}


def probe_scores(logs_dir):
    from inspect_ai.log import read_eval_log

    scores, total, parsed = defaultdict(list), defaultdict(int), defaultdict(int)
    for path in sorted(Path(logs_dir).glob("*.eval")):
        log = read_eval_log(str(path))
        if log.status != "success":
            sys.exit(f"journal non terminé : {path.name}")
        for s in log.samples:
            v = parse(s.output.completion)
            total[log.eval.model] += 1
            if v is not None:
                parsed[log.eval.model] += 1
                scores[s.id].append(v)
    return scores, {m: {"tirages": total[m], "lisibles": parsed[m]} for m in total}


def dispersion(rows_q1, ann_first):
    """Écart type de log10 du milieu des plages, par (modèle, question), au moins deux tirages chiffrés."""
    mids = defaultdict(list)
    for r in rows_q1:
        f = ann_first.get(r["item"], {})
        lo, b1 = to_base(f.get("borne_basse"), f.get("unite"), "v2")
        hi, b2 = to_base(f.get("borne_haute"), f.get("unite"), "v2")
        pts = [v for v in (lo, hi) if v is not None]
        if f.get("chiffre_present") and pts and sum(pts) > 0:
            mids[(r["model"], r["question_id"])].append(np.log10(sum(pts) / len(pts)))
    return {k: float(np.std(v)) for k, v in mids.items() if len(v) >= 2}


def element_score(e, kind, prober, scores):
    p = e["sondes"].get(kind, {}).get(prober)
    v = scores.get(p, []) if p else []
    return float(np.mean(v)) if v else None


def analyze(elements, scores, disp):
    out = {}
    for m in MODELS:
        own = [e for e in elements if e["author"] == m]
        cs = [e for e in elements if e["class"] == "c"]

        def pairs(cls, fn, subset=None):
            res = []
            for e in (subset if subset is not None else own):
                if e["class"] == cls:
                    v = fn(e)
                    if v is not None:
                        res.append((e["question_id"], v))
            return res

        auto = lambda e: element_score(e, "auto", m, scores)  # noqa: E731
        ques = lambda e: element_score(e, "question", m, scores)  # noqa: E731
        dsp = lambda e: (None if (m, e["question_id"]) not in disp else -disp[(m, e["question_id"])])  # noqa: E731
        both = lambda f, g: (lambda e: f(e) if f(e) is not None and g(e) is not None else None)  # noqa: E731
        r_auto = auroc_boot(pairs("b", auto), pairs("a", auto))
        res = {"elements": {"a": len(pairs("a", auto)), "b": len(pairs("b", auto)),
                            "ecartes_sans_tirage_lisible": sum(auto(e) is None for e in own)},
               "auto": summary(r_auto), "verdict": verdict(summary(r_auto))}
        for name, g in (("question_seule", ques), ("dispersion_q1", dsp)):
            ra = auroc_boot(pairs("b", both(auto, g)), pairs("a", both(auto, g)))
            rg = auroc_boot(pairs("b", both(g, auto)), pairs("a", both(g, auto)))
            res[name] = {"auroc": summary(rg), "auto_moins_temoin": diff(ra, rg)}
        res["au_dela_de_la_question"] = bool(res["question_seule"]["auto_moins_temoin"]
                                             and res["question_seule"]["auto_moins_temoin"]["ic95"][0] > 0)
        other = {"anthropic/claude-opus-5-5": "anthropic/claude-sonnet-5-5",
                 "anthropic/claude-sonnet-5-5": "anthropic/claude-opus-5-5"}.get(m)
        if other:
            cro = lambda e: element_score(e, "croisee", other, scores)  # noqa: E731
            ra = auroc_boot(pairs("b", both(auto, cro)), pairs("a", both(auto, cro)))
            rc = auroc_boot(pairs("b", both(cro, auto)), pairs("a", both(cro, auto)))
            res["croise"] = {"evaluateur": other, "auroc": summary(rc), "auto_moins_croise": diff(ra, rc)}
        res["b_contre_c"] = summary(auroc_boot(pairs("b", auto), pairs("c", auto, cs)))
        over = [e for e in own if e["class"] == "b" or e["overprecise"]]
        same = [e for e in own if e["bornes_identiques"]]
        res["sensibilite"] = {"a_surprecis_seulement": summary(auroc_boot(pairs("b", auto, over), pairs("a", auto, over))),
                              "bornes_identiques": summary(auroc_boot(pairs("b", auto, same), pairs("a", auto, same)))}
        out[m] = res
    return out


def committed(paths):
    for p in paths:
        if subprocess.run(["git", "ls-files", "--error-unmatch", p], cwd=ROOT, capture_output=True).returncode:
            return f"{p} n'est pas commité"
    if subprocess.run(["git", "diff", "--quiet", "HEAD", "--", *paths], cwd=ROOT).returncode:
        return "sondes modifiées depuis le dernier commit"
    return None


def fmt(s):
    return "n.d." if not s else f"{s['auroc']:.3f} [{s['ic95'][0]:.3f} ; {s['ic95'][1]:.3f}]".replace(".", ",")


def fmtd(d):
    return "n.d." if not d else f"{d['difference']:+.3f} [{d['ic95'][0]:+.3f} ; {d['ic95'][1]:+.3f}]".replace(".", ",")


def markdown(out):
    lines = ["# Q2, test (généré par `scripts/q2_analyze.py`, ne pas éditer)", "",
             f"AUROC de (b) chiffres dans la plage publiée contre (a) chiffres sur questions NOT_FOUND ; "
             f"bootstrap par grappes de questions, {B} rééchantillonnages, graine {SEED}.", "",
             "| Modèle | n (a / b) | AUROC auto | Verdict | Question seule | Auto − question | Dispersion Q1 | Croisé | (b) contre (c) |",
             "|---|---|---|---|---|---|---|---|---|"]
    for m, r in out["modeles"].items():
        cro = fmt(r["croise"]["auroc"]) if "croise" in r else "—"
        lines.append(f"| {m.split('/')[-1]} | {r['elements']['a']} / {r['elements']['b']} | {fmt(r['auto'])} | {r['verdict']} "
                     f"| {fmt(r['question_seule']['auroc'])} | {fmtd(r['question_seule']['auto_moins_temoin'])} "
                     f"| {fmt(r['dispersion_q1']['auroc'])} | {cro} | {fmt(r['b_contre_c'])} |")
    lines += ["", "## Sensibilités", "", "| Modèle | (a) surprécis seulement | Bornes identiques |", "|---|---|---|"]
    for m, r in out["modeles"].items():
        lines.append(f"| {m.split('/')[-1]} | {fmt(r['sensibilite']['a_surprecis_seulement'])} | {fmt(r['sensibilite']['bornes_identiques'])} |")
    lines += ["", "## Lecture des réponses", "", "| Évaluateur | Tirages | Lisibles |", "|---|---|---|"]
    for m, v in out["lecture"].items():
        lines.append(f"| {m} | {v['tirages']} | {v['lisibles']} |")
    return "\n".join(lines) + "\n"


def main():
    why = committed(["data/q2/elements.jsonl", "data/q2/probes.jsonl", "scripts/q2_analyze.py"])
    if why:
        sys.exit(f"analyse refusée : {why}")
    elements = [json.loads(l) for l in (ROOT / "data" / "q2" / "elements.jsonl").open()]
    scores, reading = probe_scores(ROOT / "logs" / "q2")
    if set(reading) != set(MODELS):
        sys.exit(f"journaux de Q2 incomplets : {sorted(reading)}")
    base = ROOT / "data" / "annotation" / "test" / "v2"
    rows = [json.loads(l) for l in (base / "scores.jsonl").open()]
    first = {json.loads(l)["id"]: json.loads(l) for l in (base / f"{ANNOTATORS[0]}.jsonl").open()}
    out = {"graine": SEED, "reechantillonnages": B, "lecture": reading,
           "modeles": analyze(elements, scores, dispersion(rows, first))}
    res = ROOT / "results"
    res.mkdir(exist_ok=True)
    (res / "q2.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    (res / "q2.md").write_text(markdown(out))
    print((res / "q2.md").read_text())


if __name__ == "__main__":
    main()
