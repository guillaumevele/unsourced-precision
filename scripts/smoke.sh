#!/usr/bin/env bash
# Test de fumée : inspect eval sur le fournisseur factice, sans appel réseau à un modèle.
# --model est figé à mockllm/model ; les journaux vont dans smoke_logs/ (ignoré par git),
# jamais dans logs/, réservé aux vrais runs après le PREREG.
set -euo pipefail
cd "$(dirname "$0")/.."
exec .venv/bin/inspect eval evals/smoke.py \
  --model mockllm/model \
  --log-dir smoke_logs \
  --display plain \
  "$@"
