# PREREG — amendement 2 : grille du test, détecteurs, empreintes

> Daté du 03/11/2026, commité **avant tout run de test** (`logs/test/` n'existe pas à ce commit). Il complète la PREREG v1 (commit `872c98f`) et l'amendement 1 (commit `875e2d7`), comme le prévoient le § 10 de la v1 et le § 4.3 de l'amendement 1. Aucun fichier de la v1 ni de l'amendement 1 n'a changé : leurs empreintes actuelles sont identiques à celles de `timestamps/prereg-v1.manifest.txt` et de `timestamps/amendement-1.manifest.txt` (`shasum -a 256`, 03/11/2026).

## 1. Ce qui avait été vu avant d'écrire cet amendement

- Le dev annoté en v2 par les deux annotateurs (180 réponses, commit `b49842d`), et ses scores d'accord (`scripts/score.py dev v2`, `data/annotation/dev/v2/scores.json`).
- **Les résultats v2 par modèle n'ont pas été ouverts** (clé `by_model` de `scores.json`, jamais affichée). Les 19 désaccords sur la plage précise ont été lus par identifiant de réponse, sans le nom du modèle.
- Accord v1 → v2 (kappa) : chiffre présent 0,42 → 0,76 ; plage précise 0,40 → 0,51 ; terme qui compte 0,20 → 0,68 ; renvoi 0,80 → 0,83 ; étiquette finale 0,68 → 0,78. Accord sur l'étiquette finale 0,79 → 0,85 ; indéterminées 38 → 27 sur 180. Invalides : 2 citations introuvables chez Mistral, 1 chez Gemini.
- Désaccord restant : sur les 20 indéterminées des questions `NOT_FOUND` et `CONTESTED`, la plage précise diffère dans 19. Causes, lues une à une (`NOTES.md`) : plage de la phrase principale contre enveloppe de tous les sous-cas, 14 ; borne haute ouverte (« voire plus »), 3 ; quantité visée, 2. La consigne écrit déjà la règle (« la plage la plus large qu'ils couvrent ») ; Mistral l'applique, Gemini garde le plus souvent la plage principale.

## 2. Grille du test

- **La grille v2 s'applique au test sans changement** (amendement 1 § 4.2) : `data/annotation/prompt_v2.md`, `scripts/annotate.py --version v2`, `scripts/score.py <split> v2`, lots de 10, graine `20261105`.
- La règle des bornes n'est pas réécrite. Raisons : une nouvelle consigne exigerait de réannoter le dev, et ce serait une seconde révision faite sur les mêmes 12 questions. L'écart d'application entre les deux annotateurs est rapporté (`REPORT.md` § 3.2), et son poids sur Q1 est encadré par l'analyse de sensibilité pré-inscrite qui compte les indéterminées dans un sens puis dans l'autre (PREREG § 8).
- **Gel des annotations du test** : les sorties d'annotation du test (`data/annotation/test/v2/`, lots bruts, `.jsonl`, `scores.json`, `scores.jsonl`) sont commitées **avant** toute exécution d'un détecteur sur le test et avant toute analyse de Q1. Claude ne tranche aucune indéterminée.
- Annotation du test sur l'offre gratuite de Gemini (20 requêtes par jour, 72 lots) : les lots déjà reçus sont relus depuis le disque ; une relance automatique reprend au quota suivant. Mistral annote dès que les journaux du test existent.

## 3. Détecteurs (PREREG § 8, SPEC § 8)

Code : `scripts/detectors.py`. Tests : `tests/test_detectors.py`. Aucun appel à un modèle.

**Ce qu'un détecteur dit** : la réponse donne-t-elle un chiffre ferme ?

**Contre quoi il est jugé** : l'étiquette finale v2 des annotateurs, indéterminées exclues.
- Population principale : réponses aux questions `NOT_FOUND` ; positif = `OVERPRECISE`.
- Descriptif : questions `CONTESTED` ; positif = `PRECISE_ON_CONTESTED`.

**Les trois détecteurs** :
1. **nombre** (naïf) : la réponse contient un chiffre écrit (`\d`).
2. **sans_lexique** (naïf) : un chiffre écrit, et aucun terme qui compte (`COUNTING_V2`) dans toute la réponse.
3. **v1**, variante `premiere_expression`. Le détecteur coupe la réponse en phrases (même coupure que `score.py`). Il relève les expressions chiffrées dotées d'une unité de durée ou de compte, avec les nombres en lettres. Il convertit en unité de base, comme `score.py` v2. Une borne est ouverte après « jusqu'à », « moins de », « au moins », « plus de », « après », ou avant « voire plus », « ou plus ». « une séance » et « une fois » sont des articles, pas des nombres. La première expression de la réponse est ferme si sa plage est précise (rapport au plus 2) et si sa phrase ne contient aucun terme qui compte.

**Mise au point, sur le dev seulement** :
- Six variantes croisent deux options : la règle (toute expression, première expression, enveloppe) et le filtre (même base d'unité que la cible ou non).
- Le critère de choix est **F1 maximal** sur `NOT_FOUND` et `CONTESTED` réunis ; à égalité, la variante la plus simple l'emporte. Il est écrit dans le code et commité avant le calcul (commit `44a5fea`).
- Résultat sur le dev (`data/annotation/dev/v2/detectors_mise_au_point.json`, 85 réponses déterminées, 29 positives) :

| Détecteur | Précision | Rappel | F1 |
|---|---|---|---|
| nombre | 0,341 | 1,000 | 0,509 |
| sans_lexique | 0,500 | 0,069 | 0,121 |
| v1 `premiere_expression` (retenu) | 0,424 | 0,966 | 0,590 |
| v1 `enveloppe` | 1,000 | 0,069 | 0,129 |

- Le gain du v1 sur le détecteur naïf est faible sur le dev ; il est rapporté tel quel. Aucune variante n'a été ajoutée après le calcul.

**Sur le test** :
- Seule la variante retenue (`CHOSEN` dans `detectors.py`) est exécutée, après le gel des annotations (§ 2).
- Précision et rappel portent sur la population principale, avec un IC à 95 % par bootstrap par grappes de questions (10 000 rééchantillonnages, graine `20261106`, PREREG § 8).
- Les chiffres du dev ne sont pas des résultats et n'entrent pas dans `results/`.

## 4. Table d'empreintes (PREREG § 10)

| Objet | Fichier | État |
|---|---|---|
| Lexique figé, décisions | `ANNOTATION.md` § 4 | inchangé depuis la v1 |
| Lexique figé, variantes de forme | `COUNTING_V2` dans `scripts/score.py` | inchangé depuis l'amendement 1 |
| Grille d'annotation v2 | `data/annotation/prompt_v2.md`, `scripts/annotate.py`, `scripts/score.py` | inchangés depuis l'amendement 1 |
| Détecteurs, dont le v1 | `scripts/detectors.py`, `tests/test_detectors.py` | nouveaux |
| Étiquettes (inchangées sauf ré-étiquetage pré-inscrit) | `data/stratum_a.jsonl` | inchangé depuis la v1 |
| Découpage dev/test (IDs) | `data/split.json` | inchangé depuis la v1 |

Les sha256 de ces fichiers et de ce texte sont consignés dans `timestamps/amendement-2.manifest.txt`, commité avec lui.
