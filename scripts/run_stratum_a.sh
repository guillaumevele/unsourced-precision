#!/usr/bin/env bash
# Run de la strate A avec les paramètres pré-inscrits (PREREG § 4).
# Usage : scripts/run_stratum_a.sh dev|test claude-opus-5-5|claude-sonnet-5-5|claude-haiku-5-5
set -euo pipefail
cd "$(dirname "$0")/.."
split="$1"; model="$2"
case "$split" in dev|test) ;; *) echo "split : dev ou test" >&2; exit 2 ;; esac
case "$model" in claude-opus-5-5|claude-sonnet-5-5|claude-haiku-5-5) ;; *) echo "modèle non pré-inscrit" >&2; exit 2 ;; esac
exec .venv/bin/inspect eval evals/stratum_a.py -T split="$split" \
  --model "anthropic/$model" \
  --epochs 5 \
  --effort medium \
  --max-tokens 8000 \
  --max-retries 5 \
  --batch \
  --log-dir "logs/$split" \
  --display plain
