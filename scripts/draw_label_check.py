"""Tire 15 questions de la strate A, graine fixe, pour la vérification des étiquettes à l'aveugle (PREREG § 3).

Écrit data/label_check_sheet.md : pour chaque question, la requête, la quantité visée et les passages,
sans l'étiquette. Guillaume note SOURCED, CONTESTED ou NOT_FOUND ; le taux d'accord est calculé ensuite.
Usage : .venv/bin/python scripts/draw_label_check.py
"""

import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED, N = 20261103, 15

rows = [json.loads(line) for line in (ROOT / "data" / "stratum_a.jsonl").open()]
sample = random.Random(SEED).sample(sorted(rows, key=lambda r: r["id"]), N)
out = ["# Vérification des étiquettes à l'aveugle", "",
       f"{N} questions tirées avec la graine {SEED}. Pour chacune, lire les passages et écrire SOURCED, CONTESTED ou NOT_FOUND.", ""]
for r in sample:
    out += [f"## {r['id']}", "", f"- Requête : {r['question']}", f"- Quantité visée : {r['target_quantity']['description']}"]
    out += [f"- Passage {p['source_ref']} : « {p['text']} »" for p in r["passage"]]
    for s in r["search_log"]:
        note = re.sub(r"\b(SOURCED|CONTESTED|NOT_FOUND)\b", "[étiquette masquée]", s.get("notes", ""))
        out.append(f"- Recherche ({s['database']}) « {s['query']} », {s['n_results']} résultat(s). {note}".rstrip())
    out += ["- Ton étiquette : ", ""]
(ROOT / "data" / "label_check_sheet.md").write_text("\n".join(out))
print("ids :", " ".join(r["id"] for r in sample))
