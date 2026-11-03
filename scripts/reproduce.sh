#!/usr/bin/env bash
# Régénère tous les résultats depuis les journaux et annotations commités, sans aucun appel API,
# puis vérifie que rien ne diffère du dépôt et que les fichiers figés correspondent à leurs manifestes.
# Usage : scripts/reproduce.sh   (PYTHON=... pour choisir l'interpréteur ; .venv/bin/python par défaut)
set -euo pipefail
cd "$(dirname "$0")/.."
PY="${PYTHON:-.venv/bin/python}"
echo "== tests";            "$PY" -m unittest discover -s tests
echo "== Q1";               "$PY" scripts/score.py test v2 >/dev/null
                            "$PY" scripts/detectors.py test >/dev/null
                            "$PY" scripts/analyze.py test >/dev/null
                            "$PY" scripts/figure.py >/dev/null
echo "== Q2";               "$PY" scripts/q2_build.py >/dev/null
                            "$PY" scripts/q2_analyze.py >/dev/null
                            "$PY" scripts/q2_lecture_corrigee.py >/dev/null
echo "== pilote";           "$PY" pilot/probe.py >/dev/null
echo "== empreintes figées"
for m in prereg-v1 amendement-1 amendement-2 analyse amendement-3 amendement-4; do
  # tests/test_q2.py a reçu 20 lignes ajoutées après l'amendement 3 (README) : vérifié à son commit figé.
  grep -E '^[0-9a-f]{64}  ' "timestamps/$m.manifest.txt" | grep -v ' tests/test_q2.py$' | shasum -a 256 -c --quiet
  echo "   $m OK"
done
want=$(grep ' tests/test_q2.py$' timestamps/amendement-3.manifest.txt | cut -d' ' -f1)
got=$(git show 2eebac0:tests/test_q2.py | shasum -a 256 | cut -d' ' -f1)
[ "$want" = "$got" ] && echo "   tests/test_q2.py OK au commit 2eebac0"
echo "== aucune différence avec le dépôt"
git diff --exit-code --stat
test -z "$(git status --porcelain --untracked-files=all -- results pilot)" || { git status --short -- results pilot; exit 1; }
echo "Reproduction identique."
