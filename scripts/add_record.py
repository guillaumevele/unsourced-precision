"""Ajoute une décision au parcours de la strate A (PREREG § 2).

Lit un objet JSON sur l'entrée standard :
    {"rank": 2, "decision": "RETENU" | "EXCLU-E1".."EXCLU-E4" | "QUOTA_PLEIN",
     "motif": "...", "record": {...ligne du schéma, sans id ni provenance...}}
Le rang donne la requête, le site et la provenance ; l'identifiant A-NNN est attribué
dans l'ordre. Écrit data/review_log.jsonl et, si RETENU, data/stratum_a.jsonl.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANDIDATES = ROOT / "data" / "private" / "candidates_ordered.jsonl"
STRATUM = ROOT / "data" / "stratum_a.jsonl"
LOG = ROOT / "data" / "review_log.jsonl"
SEED = 20261103


def main() -> None:
    entry = json.load(sys.stdin)
    rank = entry["rank"]
    cand = next(c for c in map(json.loads, CANDIDATES.open()) if c["rank"] == rank)
    logged = [json.loads(line) for line in LOG.open()] if LOG.exists() else []
    if any(e["rank"] == rank for e in logged):
        sys.exit(f"rang {rank} déjà consigné")
    expected = max((e["rank"] for e in logged), default=0) + 1
    if rank != expected:
        sys.exit(f"rang {rank} hors ordre : le prochain rang à examiner est {expected}")

    log = {"rank": rank, "query": cand["query"],
           "decision": entry["decision"], "motif": entry.get("motif", "")}
    if entry["decision"] in ("RETENU", "QUOTA_PLEIN"):
        rec = entry["record"]
        log["label"] = rec["label"]
        log["procedure_id"] = rec["procedure_id"]
    if entry["decision"] == "RETENU":
        n = sum(1 for _ in STRATUM.open()) if STRATUM.exists() else 0
        rec = {"id": f"A-{n + 1:03d}", "procedure_id": rec["procedure_id"], "label": rec["label"],
               "question": cand["query"], "lang": "fr", "voice": "patient", "llm_drafted": False,
               "provenance": {"source": "search_console", "rank": rank, "seed": SEED},
               **{k: v for k, v in rec.items() if k not in ("procedure_id", "label")}}
        log["id"] = rec["id"]
        with STRATUM.open("a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    with LOG.open("a") as f:
        f.write(json.dumps(log, ensure_ascii=False) + "\n")
    print(log)


if __name__ == "__main__":
    main()
