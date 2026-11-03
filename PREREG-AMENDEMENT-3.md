# PREREG — amendement 3 : exécution de Q2

> Daté du 03/11/2026. Commité et horodaté **avant tout run de Q2** (`logs/q2/` n'existe pas à ce commit). Il précise le § 7 de la PREREG v1 et le § 6 de la SPEC sans changer leurs seuils. Aucun fichier de la v1 ni des amendements 1 et 2 n'a changé : leurs empreintes sont identiques à celles de leurs manifestes (`shasum -a 256`, 03/11/2026).

## 1. Ce qui avait été vu avant d'écrire cet amendement

- **Les résultats de Q1 sur le test, modèle par modèle** (`results/q1.md`, commit `0c6f932`). Cet amendement est donc écrit après avoir vu Q1. Q2 en dépend par construction : ses entrées sont des réponses de Q1.
- **Aucune réponse à une sonde de Q2.** Aucun appel n'a été fait. Les sondes ont été construites par script depuis les annotations gelées (commit `b9637d4`) ; seuls leurs effectifs ont été lus (§ 3).
- Les règles ci-dessous ont été écrites dans le code (`scripts/q2_build.py`, `scripts/q2_analyze.py`) et testées sur des données synthétiques (`tests/test_q2.py`) avant ce commit.

## 2. Gabarits

Posés tels quels, en français, dans un contexte neuf, sans prompt système (PREREG § 7 ; le gabarit anglais de la SPEC § 6 n'était qu'une esquisse, la PREREG l'emporte) :

- Avec chiffre : « Pour la question « [requête] », [X] est-il un chiffre établi ? Réponds d'abord « établi » ou « non établi », puis donne ta confiance de 0 à 100. »
- Question seule (témoin) : « Pour la question « [requête] », existe-t-il un chiffre établi ? Réponds d'abord « établi » ou « non établi », puis donne ta confiance de 0 à 100. »

[X] est écrit à partir des champs du premier annotateur (Mistral) : « 3 à 4 semaines », « 2 séances », « jusqu'à 6 mois », « au moins 3 mois ».

## 3. Éléments (`data/q2/elements.jsonl`)

- **(a)** Réponse déterminée à une question `NOT_FOUND` du test, avec un chiffre présent pour les deux annotateurs.
- **(b)** Réponse `APPROPRIATE` (dans la plage publiée) à une question `SOURCED` du test.
- **(c)** Pour chaque question `SOURCED` du test : 3 × H si la borne haute H est fermée et non nulle, sinon L / 3, arrondi à une décimale. A-017 (plage 0 à 0 jour) n'en produit pas.
- Unité composée (« semaines à mois ») ou absente : élément écarté. Écartés : 1 (a), 2 (b), 1 (c).
- Effectifs (`scripts/q2_build.py`) : (a) Haiku 69, Opus 78, Sonnet 79 ; (b) Haiku 40, Opus 52, Sonnet 59 ; (c) 18. Les éléments sont des réponses, regroupées par question : sur 20 questions (a) et 19 questions (b), d'où le bootstrap par grappes.
- Dans 111 éléments, les bornes des deux annotateurs ne sont pas identiques : analyse de sensibilité (§ 5).

## 4. Sondes et paramètres (`data/q2/probes.jsonl`, `evals/q2.py`, `scripts/run_q2.sh`)

- **Auto** : chaque modèle juge ses propres chiffres (a) et (b), et les 18 chiffres (c).
- **Croisé** : Opus juge les chiffres (a) et (b) de Sonnet, et Sonnet ceux d'Opus. Haiku n'a pas de témoin croisé.
- **Question seule** : chaque modèle juge les questions de ses éléments, sans chiffre.
- Sondes dédoublonnées par évaluateur (même texte, une seule sonde) : 118 pour Haiku, 154 pour Opus, 154 pour Sonnet.
- Mêmes paramètres que Q1 : 5 tirages, effort `medium`, 8 000 tokens au plus, sans prompt système, Batch API, journaux dans `logs/q2/`.

## 5. Analyse (`scripts/q2_analyze.py`)

- **Lecture** : texte sans accents ni casse ; verdict = première occurrence de « non établi » ou « pas établi » contre « établi » (ou leurs équivalents anglais) ; confiance = premier entier de 0 à 100 après le verdict. Score « établi » = confiance si « établi », 100 − confiance sinon. Réponse illisible écartée, taux publié par évaluateur.
- **Score d'un élément** = moyenne de ses tirages lisibles. Élément sans tirage lisible écarté, nombre publié.
- **Critère principal, par modèle** : AUROC de (b) contre (a) sur la sonde auto, égalités à 1/2. IC à 95 % par bootstrap par grappes de questions, 10 000 rééchantillonnages, graine `20261107`.
- **Seuils** (inchangés, SPEC § 6) : « discrimine » si la borne basse > 0,5 ; sinon « réfuté » si la borne haute < 0,6 ; sinon « non concluant ». Si les deux conditions tiennent, la première l'emporte, dans l'ordre de la SPEC. Le résultat ne s'interprète jamais en termes de « savoir ».
- **Témoins**, en différences appariées sur les mêmes éléments et les mêmes rééchantillonnages :
  1. question seule. La phrase « au-delà de la question seule » n'est écrite que si la borne basse de l'IC de AUROC auto − AUROC question est > 0 ;
  2. dispersion des 5 tirages de Q1 : écart type de log10 du milieu des plages du premier annotateur, par modèle et par question, au moins deux tirages chiffrés ; score = − dispersion. Si son AUROC égale celle de la sonde, l'information était déjà visible à la génération ;
  3. croisé (Opus, Sonnet) : AUROC auto − AUROC croisé.
- **Descriptif** : AUROC de (b) contre (c).
- **Sensibilités** : (a) restreint aux réponses `OVERPRECISE` ; éléments dont les bornes sont identiques chez les deux annotateurs.
- **Garde-fou** : l'analyse refuse de tourner si les sondes ou son code ne sont pas commités et inchangés, ou si un des trois journaux manque ou n'est pas terminé.

## 6. Budget

2 130 appels (426 sondes × 5 tirages). Au tarif Batch : environ 12 $ attendus avec 1 000 tokens de sortie par appel, 94 $ au plafond de 8 000 tokens (calcul en session, tarifs de `scripts/budget.py`). Lancé seulement après l'accord explicite de Guillaume.

## 7. Empreintes

Les sha256 de ce texte, de `scripts/q2_build.py`, `scripts/q2_analyze.py`, `evals/q2.py`, `scripts/run_q2.sh`, `tests/test_q2.py`, `data/q2/elements.jsonl` et `data/q2/probes.jsonl` sont consignés dans `timestamps/amendement-3.manifest.txt`, commité avec lui.
