# data/

- `stratum_a.jsonl` : **pas encore créé**. Une question par ligne, au format de `schema/stratum_a.schema.json`. Rédigé par Guillaume seul, sans LLM (SPEC § 4).
- Validation : `.venv/bin/python scripts/validate_stratum_a.py data/stratum_a.jsonl` (ajouter `--require-pairs` une fois le jeu complet).

Les plages `SOURCED` et `CONTESTED` sont des valeurs **publiées par les sources citées**. Elles sont données comme références de recherche, **pas comme recommandations médicales** (SPEC § 11).
