"""Découpage dev/test de la strate A, par procédure, avec une graine fixe (PREREG § 5).

Règle : les procédures sont mélangées avec la graine. On les parcourt dans cet ordre et on
place une procédure en dev si toutes ses questions tiennent dans les cibles restantes par
étiquette : 20 % de chaque quota, arrondi (SOURCED 5, NOT_FOUND 5, CONTESTED 2). On s'arrête
quand les trois cibles sont atteintes ou que la liste est épuisée. Tout le reste va en test.
Une procédure n'est jamais coupée entre dev et test.

Usage : .venv/bin/python scripts/split_dev_test.py  ->  data/split.json
"""

import json
import random
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED = 20261104
TARGET = {"SOURCED": 5, "NOT_FOUND": 5, "CONTESTED": 2}

rows = [json.loads(line) for line in (ROOT / "data" / "stratum_a.jsonl").open()]
by_proc = defaultdict(list)
for r in rows:
    by_proc[r["procedure_id"]].append(r)

procs = sorted(by_proc)
random.Random(SEED).shuffle(procs)
left, dev_procs = dict(TARGET), []
for p in procs:
    need = Counter(r["label"] for r in by_proc[p])
    if all(need[k] <= left[k] for k in need):
        dev_procs.append(p)
        for k in need:
            left[k] -= need[k]
    if not any(left.values()):
        break

dev = sorted(r["id"] for p in dev_procs for r in by_proc[p])
test = sorted(r["id"] for r in rows if r["id"] not in dev)
labels = {r["id"]: r["label"] for r in rows}
out = {"seed": SEED, "target": TARGET, "dev_procedures": sorted(dev_procs), "dev": dev, "test": test,
       "dev_labels": dict(Counter(labels[i] for i in dev)), "test_labels": dict(Counter(labels[i] for i in test))}
(ROOT / "data" / "split.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print(len(dev), "dev", out["dev_labels"], "|", len(test), "test", out["test_labels"])
