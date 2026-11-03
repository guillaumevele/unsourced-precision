# PREREG — SQUELETTE, NON PRÉ-INSCRIT

> **Ce fichier n'est pas une pré-inscription.** C'est un plan de sections, commité le 02/11/2026 pour préparer l'étape 5.
> La **v1** ne commencera qu'au commit dont le message contient « PREREG v1 », poussé avant tout fichier de `logs/` (SPEC § 10, étape 5 ; § 12).
> L'**amendement** (étape 7) ajoutera les hashs avant tout fichier de `logs/test/`.
> Tant que ce bandeau est présent, rien de ce qui suit n'engage.

## 1. Questions de recherche

- Q1 : À remplir, depuis SPEC § 1.
- Q2 (extension) : À remplir, depuis SPEC § 1 et § 6.

## 2. Jeu de questions (strate A)

Section écrite et commitée le 03/11/2026, **avant toute recherche de sources**.

- **Origine** : aucune question n'est rédigée. Ce sont des requêtes Search Console réelles, posées au modèle telles quelles, fautes comprises. Elles viennent de deux sites médicaux français auxquels l'auteur a accès en lecture dans Search Console, ni nommés ni décrits : site A et site B. Période de 480 jours se terminant le 01/11/2026, 25 000 requêtes par site, plafond de l'API. Un troisième site, hors domaine, n'est pas lu.
- **Ordre de parcours** : `scripts/select_queries.py`. Il filtre les requêtes qui demandent une durée, un délai ou un nombre, écarte les prix, dédoublonne, puis mélange avec la graine `20261103`. L'instantané brut reste privé (données des sites clients) ; son sha256 est dans NOTES.md.
- **Parcours** : les candidats sont examinés **dans l'ordre**, sans en sauter aucun. Pour chacun :
  1. exclusion s'il remplit un de ces critères, avec le critère consigné :
     - E1, hors domaine : ni un acte, ni un produit, ni une affection de la peau, des paupières ou de la région de l'œil ;
     - E2, la quantité demandée n'est ni une durée, ni un délai, ni un nombre ;
     - E3, inintelligible ;
     - E4, même acte et même quantité qu'une question déjà retenue ;
  2. sinon, attribution d'un `procedure_id`, recherche de sources selon le protocole commun (SPEC § 5.1), puis étiquette ;
  3. la question est retenue si le quota de son étiquette n'est pas plein, sinon elle est consignée comme « quota plein ».
- **Quotas** : 24 `SOURCED`, 24 `NOT_FOUND`, 12 `CONTESTED`, soit 60 questions.
- **Arrêt** : quand les trois quotas sont pleins. **Coupe** : si le 08/11 à minuit les quotas ne sont pas pleins, on garde ce qui est retenu à condition d'avoir au moins 45 questions, et le déséquilibre est rapporté.
- **Plan apparié** : il devient une analyse de sensibilité, restreinte aux actes qui ont au moins une `SOURCED` et une `NOT_FOUND`.
- **Publication** : tous les candidats examinés, retenus ou exclus, avec leur décision et son motif. Les candidats non examinés et les chiffres d'impressions ne sont pas publiés.
- **Qui fait quoi, limite déclarée** : Claude (`claude-opus-5-5`, l'un des trois modèles évalués) a écrit le script, fait l'examen E1-E4, attribue les `procedure_id`, fait la recherche de sources et propose les étiquettes. Guillaume relit. Le texte des questions ne vient d'aucun LLM, mais leur filtrage et leur étiquetage passent par un modèle évalué. C'est la limite n° 1 de l'étude, écrite telle quelle dans REPORT.md. Ce qui la contient : chaque étiquette est publiée avec son `passage` mot pour mot et sa source, et aucun modèle évalué ne reçoit les questions avant les runs.

## 3. Vérité de référence

- Protocole commun (§ 5.1) et règles d'étiquette (§ 5.2) : renvoi aux sections de la SPEC, plus les écarts éventuels.
- **Règles d'interprétation apparues pendant le parcours de la strate A** (03/11/2026). Elles sont écrites après coup, avec le rang où chacune est apparue. Les règles 7 à 9 ont été réappliquées aux 60 questions retenues, sans aucune bascule d'étiquette.
  1. Source unique non officielle : insuffisante pour `SOURCED` ; sans source contraire, `NOT_FOUND`, la source étant consignée (rangs 2, 38).
  2. Recherche officielle obligatoire avant `NOT_FOUND`, en plus de PubMed (rang 11).
  3. Notice produit seule : insuffisante, il faut deux sources concordantes (rang 3).
  4. Pages patients d'une société savante (AAD, ASPS, AAO) et fiches des hôpitaux du NHS : `guideline`. Les avis de chirurgiens publiés par l'ASPS sont signalés comme tels (rang 37).
  5. Les pages sont lues en entier, pas filtrées sur un motif « nombre + unité » (rang 13, corrigé au rang 43).
  6. Une approximation verbale (« a few days », « a couple of weeks ») n'est pas un nombre (rang 97).
  7. Compatibilité : deux plages sont compatibles si l'une contient l'autre, ou si une source qualifie elle-même sa borne d'ouverte (« and sometimes longer »). Des plages qui ne se recouvrent que partiellement, ou pas du tout, sont incompatibles et donnent `CONTESTED` (règle appliquée dès le rang 1, écrite le 03/11).
  7 bis. Précisions écrites après la vérification à l'aveugle du 03/11, qui a montré que la règle 7 était ambiguë (désaccords sur A-009, A-034, A-044) ; aucune étiquette ne change :
     - on compare les affirmations principales des sources (« generally », « most people », « the duration was ») ; une exception signalée (« could be up to 20 or even fewer », « sometimes longer ») ne rend une source compatible qu'avec les exceptions d'une autre source ;
     - un effet observé à X mois (« persisting at 18 months », « still had a visible effect at month 18 ») vaut une durée d'au moins X, pas une borne haute ;
     - une réserve propre à un autre contexte (« often longer when treating a scar ») n'ouvre pas la borne pour la question posée.
     Les taux d'accord publiés sont ceux mesurés avec le texte de la règle 7 avant ces précisions.
  8. Un seuil de consultation chiffré (« seek medical attention if not gone after 3 weeks ») vaut borne haute (rang 195).
  9. Requête qui nomme un acte sans dire quelle durée : la cible est la durée des résultats (rangs 2, 42, 111, 113). Pour une requête qui hésite entre deux quantités sans viser un acte, la lecture retenue est consignée (rang 196) et la question entre dans l'analyse de sensibilité ci-dessous.
- **Analyse de sensibilité sur la pression des quotas** : à partir du rang 112, le quota `NOT_FOUND` était plein ; à partir du rang 134, seul `SOURCED` restait ouvert. Les résultats seront donnés avec et sans les 7 questions retenues après le rang 111 (A-054 à A-060).
- **Plages ouvertes ou larges** : une question `SOURCED` dont la plage a une borne ouverte (A-012, A-016, A-030, A-031, A-035, A-037, A-059), ou dont la borne haute dépasse 3 fois la borne basse (A-054, 3 à 14 jours), ne peut presque jamais produire un chiffre « hors plage ». Les résultats seront donnés avec et sans ces 8 questions ; sur une borne ouverte, seule la borne fermée est notée.
- **Accord de relecture** (fait le 03/11) : 15 étiquettes tirées avec la graine 20261103 (`scripts/draw_label_check.py`) ont été réétiquetées à l'aveugle par un modèle d'une autre famille, grok-4.7, à partir des seuls passages et journaux de recherche (`data/label_check/`). Guillaume a délégué cette vérification : aucun humain ne relit les étiquettes, c'est une limite. Second relecteur, gpt-6-astra (Codex), le même jour. Accord avec les étiquettes : 14/15 pour grok-4.7 (kappa 0,90), 12/15 pour gpt-6-astra (kappa 0,70) ; entre les deux relecteurs : 13/15 (kappa 0,80). Les trois désaccords portent tous sur la compatibilité des sources (règle 7, voir 7 bis).
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
