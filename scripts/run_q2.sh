#!/usr/bin/env bash
# Run de Q2 avec les paramètres de Q1 (PREREG § 4, amendement 3).
# Usage : scripts/run_q2.sh claude-opus-5-5|claude-sonnet-5-5|claude-haiku-5-5
set -euo pipefail
cd "$(dirname "$0")/.."
model="$1"
case "$model" in claude-opus-5-5|claude-sonnet-5-5|claude-haiku-5-5) ;; *) echo "modèle non pré-inscrit" >&2; exit 2 ;; esac
exec .venv/bin/inspect eval evals/q2.py -T prober="anthropic/$model" \
  --model "anthropic/$model" \
  --epochs 5 \
  --effort medium \
  --max-tokens 8000 \
  --max-retries 5 \
  --batch \
  --log-dir logs/q2 \
  --display plain
