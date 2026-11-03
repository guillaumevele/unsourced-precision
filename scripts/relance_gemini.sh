#!/usr/bin/env bash
# Relance de l'annotation Gemini sur l'offre gratuite (20 requêtes par jour, amendement 2 § 2).
# Les lots déjà reçus sont relus depuis le disque ; chaque passage reprend au premier lot manquant.
# S'arrête quand <split>/v2/gemini.jsonl compte autant de lignes que items.jsonl.
# Usage : nohup scripts/relance_gemini.sh test >> logs/annotate_test_v2_gemini.last.txt 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/.."
split="${1:-test}"
out="data/annotation/$split/v2/gemini.jsonl"
while true; do
  echo "== $(date '+%d/%m %H:%M') passage"
  .venv/bin/python scripts/annotate.py "$split" --version v2 --only gemini
  if [ -f "$out" ] && [ "$(wc -l < "$out")" -eq "$(wc -l < "data/annotation/$split/items.jsonl")" ]; then
    echo "== $(date '+%d/%m %H:%M') terminé : $(wc -l < "$out") éléments"; exit 0
  fi
  sleep 7200
done
