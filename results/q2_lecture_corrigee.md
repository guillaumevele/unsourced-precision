# Q2, test, lecture corrigée : EXPLORATOIRE (généré par `scripts/q2_lecture_corrigee.py`, ne pas éditer)

AUROC de (b) chiffres dans la plage publiée contre (a) chiffres sur questions NOT_FOUND ; bootstrap par grappes de questions, 10000 rééchantillonnages, graine 20261107.

| Modèle | n (a / b) | AUROC auto | Verdict | Question seule | Auto − question | Dispersion Q1 | Croisé | (b) contre (c) |
|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 69 / 40 | 0,739 [0,555 ; 0,893] | discrimine | 0,481 [0,264 ; 0,711] | +0,258 [+0,059 ; +0,459] | 0,520 [0,268 ; 0,751] | — | 0,999 [0,991 ; 1,000] |
| claude-opus-5-5 | 78 / 52 | 0,819 [0,664 ; 0,933] | discrimine | 0,664 [0,445 ; 0,847] | +0,155 [-0,002 ; +0,341] | 0,619 [0,414 ; 0,808] | 0,721 [0,510 ; 0,891] | 0,999 [0,994 ; 1,000] |
| claude-sonnet-5-5 | 79 / 59 | 0,695 [0,495 ; 0,882] | non concluant | 0,350 [0,163 ; 0,560] | +0,345 [+0,084 ; +0,603] | 0,725 [0,523 ; 0,897] | 0,809 [0,656 ; 0,925] | 0,976 [0,936 ; 0,998] |

## Sensibilités

| Modèle | (a) surprécis seulement | Bornes identiques |
|---|---|---|
| claude-haiku-5-5 | 0,762 [0,507 ; 0,952] | 0,718 [0,508 ; 0,904] |
| claude-opus-5-5 | 0,690 [0,431 ; 0,890] | 0,780 [0,584 ; 0,926] |
| claude-sonnet-5-5 | 0,705 [0,470 ; 0,902] | 0,695 [0,473 ; 0,903] |

## Lecture des réponses

| Évaluateur | Tirages | Lisibles |
|---|---|---|
| anthropic/claude-opus-5-5 | 770 | 770 |
| anthropic/claude-sonnet-5-5 | 770 | 770 |
| anthropic/claude-haiku-5-5 | 590 | 590 |

## Tirages dont la lecture change

| Évaluateur | Tirages | Lecture changée | Illisibles (lecture corrigée) |
|---|---|---|---|
| anthropic/claude-opus-5-5 | 770 | 0 | 0 |
| anthropic/claude-sonnet-5-5 | 770 | 0 | 0 |
| anthropic/claude-haiku-5-5 | 590 | 420 | 0 |
