"""Strate A : pose chaque requête telle quelle au modèle (PREREG § 4).

Aucun prompt système, aucun scorer : les réponses sont annotées ensuite (ANNOTATION.md).
Les paramètres (modèle, --epochs 5, --effort medium, --max-tokens 8000, --batch) sont
passés en ligne de commande par scripts/run_stratum_a.sh, jamais ici.

Usage : inspect eval evals/stratum_a.py -T split=dev ...
"""

import json
from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset, Sample
from inspect_ai.solver import generate

ROOT = Path(__file__).resolve().parent.parent


@task
def stratum_a(split: str = "dev") -> Task:
    if split not in ("dev", "test"):
        raise ValueError("split doit valoir dev ou test")
    ids = set(json.loads((ROOT / "data" / "split.json").read_text())[split])
    rows = [json.loads(line) for line in (ROOT / "data" / "stratum_a.jsonl").open()]
    samples = [
        Sample(id=r["id"], input=r["question"],
               metadata={"label": r["label"], "procedure_id": r["procedure_id"]})
        for r in rows if r["id"] in ids
    ]
    return Task(dataset=MemoryDataset(samples, name=f"stratum_a_{split}"), solver=generate())
