# PREREG — SQUELETTE, NON PRÉ-INSCRIT

> **Ce fichier n'est pas une pré-inscription.** C'est un plan de sections, commité le 02/11/2026 pour préparer l'étape 5.
> La **v1** ne commencera qu'au commit dont le message contient « PREREG v1 », poussé avant tout fichier de `logs/` (SPEC § 10, étape 5 ; § 12).
> L'**amendement** (étape 7) ajoutera les hashs avant tout fichier de `logs/test/`.
> Tant que ce bandeau est présent, rien de ce qui suit n'engage.

## 1. Questions de recherche

- Q1 : À remplir, depuis SPEC § 1.
- Q2 (extension) : À remplir, depuis SPEC § 1 et § 6.

## 2. Jeu de questions (strate A)

- Taille : 60 questions, avec une coupe pré-inscrite à 45. Règle de déclenchement de la coupe : À remplir.
- Plan apparié par procédure : une question `SOURCED` et une `NOT_FOUND` par procédure. Place des `CONTESTED` dans le plan : **question ouverte**, à trancher ici.
- Quotas par étiquette : À remplir.
- Auteur des questions : Guillaume, sans LLM (§ 4). Entorses : aucune à ce jour. Toute entorse s'écrit ici.

## 3. Vérité de référence

- Protocole commun (§ 5.1) et règles d'étiquette (§ 5.2) : renvoi aux sections de la SPEC, plus les écarts éventuels.
- Ré-étiquetage pré-inscrit (§ 5.2) : À remplir.
- Pas de relecture clinique des étiquettes (décision du 03/11) ; chaque étiquette est publiée avec son passage et sa source.

## 4. Modèles et paramètres

| Champ | Valeur |
|---|---|
| Modèles (chaîne renvoyée par l'API) | À remplir après l'appel minimal autorisé (étape 0) |
| k tirages | 5 |
| Température | défaut du fournisseur, valeur consignée : À remplir |
| `max_tokens` | À remplir (identique pour tous) |
| Réglage du raisonnement | À remplir |
| Prompt système | aucun |
| Version d'Inspect | 0.3.287 (`requirements.txt`) |

## 5. Découpage dev/test

- 20 % des procédures en dev, stratifiées par étiquette, découpage par procédure.
- Graine : À remplir.
- Paraphrases : dev seulement.

## 6. Annotation

Renvoi à `ANNOTATION.md`, figé au commit de la v1.

## 7. Q2 (extension)

- Formulation exacte du gabarit : À remplir.
- Règle chiffrée de déplacement hors plage pour l'entrée (c) : À remplir.
- Seuils : conclure si la borne basse de l'IC à 95 % de l'AUROC est > 0,5 ; réfuter si la borne haute est < 0,6 ; sinon non concluant (§ 6).

## 8. Analyses

- Couple surprécision/utilité par modèle, avec les politiques de référence (§ 8).
- Détecteurs naïfs et détecteur v1 (§ 8).
- Bootstrap par grappes de questions ; graine : À remplir.
- Comparaisons appariées, déclarées descriptives (§ 9).

## 9. Budget

Calculé aux tarifs du jour avant le lancement : À remplir (§ 7).

## 10. Hashs (amendement, étape 7)

| Objet | Fichier | sha256 |
|---|---|---|
| Étiquettes | `data/stratum_a.jsonl` | — |
| Grille | `ANNOTATION.md` | — |
| Lexique | — | — |
| Détecteur v1 | — | — |
| IDs du découpage | — | — |
