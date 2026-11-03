"""Q2 : sondes de vérification (PREREG § 7, amendement 3).

Chaque sonde de data/q2/probes.jsonl est posée telle quelle au modèle évaluateur, dans un contexte
neuf, sans prompt système ni scorer. Les réponses sont lues par scripts/q2_analyze.py.
Paramètres (--epochs 5, --effort medium, --max-tokens 8000, --batch) : scripts/run_q2.sh.

Usage : inspect eval evals/q2.py -T prober=anthropic/claude-opus-5-5 --model anthropic/claude-opus-5-5 ...
"""

import json
from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset, Sample
from inspect_ai.solver import generate

ROOT = Path(__file__).resolve().parent.parent


@task
def q2(prober: str) -> Task:
    rows = [json.loads(line) for line in (ROOT / "data" / "q2" / "probes.jsonl").open()]
    samples = [Sample(id=r["probe"], input=r["text"]) for r in rows if r["prober"] == prober]
    if not samples:
        raise ValueError(f"aucune sonde pour {prober}")
    return Task(dataset=MemoryDataset(samples, name=f"q2_{prober.split('/')[-1]}"), solver=generate())
