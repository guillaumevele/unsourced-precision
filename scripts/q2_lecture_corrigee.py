"""Q2, lecture corrigée des réponses : analyse EXPLORATOIRE, écrite après l'analyse pré-inscrite.

Raison (NOTES.md, « Runs de Q2 ») : la règle pré-inscrite de scripts/q2_analyze.py prend le premier
entier après le verdict ; quand la confiance n'arrive qu'en fin de réponse (420 tirages de Haiku sur
590), elle lit un chiffre du texte. q2_analyze.py reste inchangé (empreinte de l'amendement 3) ;
ce script ne remplace que la lecture, puis réutilise son analyse.

Règle corrigée : verdict comme avant ; confiance = entier suivi de « /100 » s'il y en a un (un « % » seul peut être
un chiffre du texte, « 80 % des patients »),
sinon entier qui suit « confiance » ou « confidence » (« de », « d'environ », « : », gras tolérés) ;
sans l'un ni l'autre, tirage illisible (pas de repli sur le premier entier).

Usage : .venv/bin/python scripts/q2_lecture_corrigee.py   ->  results/q2_lecture_corrigee.json, .md
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import q2_analyze  # noqa: E402
from q2_analyze import ANNOTATORS, ROOT, VERDICT, analyze, dispersion, markdown, norm  # noqa: E402

PREINSCRIT = q2_analyze.parse
SUR_100 = re.compile(r"(?<![\d,.])(\d{1,3})\s*/\s*100")
MOT = re.compile(r"(?:confiance|confidence)[^\d\n]{0,25}?(\d{1,3})(?![\d,.]?\d)")


def parse_corrigee(text):
    t = norm(text or "").replace("*", "")
    m = VERDICT.search(t)
    if not m:
        return None
    c = SUR_100.search(t) or MOT.search(t)
    if not c or int(c.group(1)) > 100:
        return None
    v = int(c.group(1))
    return float(v) if m.group(1) in ("etabli", "established") else float(100 - v)


def changes(logs_dir):
    """Par évaluateur : tirages dont la lecture change, tirages illisibles en lecture corrigée."""
    from inspect_ai.log import read_eval_log

    out = {}
    for path in sorted(Path(logs_dir).glob("*.eval")):
        log = read_eval_log(str(path))
        c = {"tirages": 0, "lecture_changee": 0, "illisibles_corrigee": 0}
        for s in log.samples:
            a, b = PREINSCRIT(s.output.completion), parse_corrigee(s.output.completion)
            c["tirages"] += 1
            c["lecture_changee"] += a != b
            c["illisibles_corrigee"] += b is None
        out[log.eval.model] = c
    return out


def main():
    q2_analyze.parse = parse_corrigee  # probe_scores lit ce nom à l'appel
    elements = [json.loads(l) for l in (ROOT / "data" / "q2" / "elements.jsonl").open()]
    scores, reading = q2_analyze.probe_scores(ROOT / "logs" / "q2")
    base = ROOT / "data" / "annotation" / "test" / "v2"
    rows = [json.loads(l) for l in (base / "scores.jsonl").open()]
    first = {json.loads(l)["id"]: json.loads(l) for l in (base / f"{ANNOTATORS[0]}.jsonl").open()}
    out = {"statut": "exploratoire, lecture corrigée après l'analyse pré-inscrite", "lecture": reading,
           "changements": changes(ROOT / "logs" / "q2"), "modeles": analyze(elements, scores, dispersion(rows, first))}
    res = ROOT / "results"
    (res / "q2_lecture_corrigee.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    md = markdown(out).replace("# Q2, test (généré par `scripts/q2_analyze.py`, ne pas éditer)",
                               "# Q2, test, lecture corrigée : EXPLORATOIRE (généré par `scripts/q2_lecture_corrigee.py`, ne pas éditer)")
    md += "\n## Tirages dont la lecture change\n\n| Évaluateur | Tirages | Lecture changée | Illisibles (lecture corrigée) |\n|---|---|---|---|\n"
    for m, c in out["changements"].items():
        md += f"| {m} | {c['tirages']} | {c['lecture_changee']} | {c['illisibles_corrigee']} |\n"
    (res / "q2_lecture_corrigee.md").write_text(md)
    print(md)


if __name__ == "__main__":
    main()
