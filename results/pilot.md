# Pilote : représentation interne de « chiffre publié » (généré par `pilot/probe.py`, ne pas éditer)

Modèle `Qwen/Qwen2.5-1.5B-Instruct` (révision `989aa7980e4c`), 49 questions (24 SOURCED), 38 plis par procédure, régression logistique L2 (C = 0.1).

| Mesure | AUROC [IC 95 %] |
|---|---|
| Couche 14 (principale) | 0,487 [0,323 ; 0,655], p permutation 0,523 |
| Témoin texte (n-grammes) | 0,412 [0,251 ; 0,582] |
| Témoin plongements lexicaux | 0,397 [0,238 ; 0,566] |
| Couche principale − texte | 0,075 [-0,082 ; 0,228] |
| Couche principale − plongements | 0,090 [-0,068 ; 0,254] |

**Verdict pré-inscrit : non concluant.**

## Par couche (descriptif)

| Couche | AUROC |
|---|---|
| 0 | 0,500 |
| 1 | 0,437 |
| 2 | 0,462 |
| 3 | 0,538 |
| 4 | 0,493 |
| 5 | 0,555 |
| 6 | 0,482 |
| 7 | 0,498 |
| 8 | 0,458 |
| 9 | 0,422 |
| 10 | 0,490 |
| 11 | 0,502 |
| 12 | 0,523 |
| 13 | 0,515 |
| 14 | 0,487 |
| 15 | 0,462 |
| 16 | 0,400 |
| 17 | 0,360 |
| 18 | 0,443 |
| 19 | 0,418 |
| 20 | 0,357 |
| 21 | 0,368 |
| 22 | 0,352 |
| 23 | 0,358 |
| 24 | 0,355 |
| 25 | 0,362 |
| 26 | 0,392 |
| 27 | 0,433 |
| 28 | 0,380 |
