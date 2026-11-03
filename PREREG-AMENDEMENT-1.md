# PREREG — amendement 1 : annotation

> Daté du 03/11/2026, commité **avant tout run de test** (`logs/test/` n'existe pas à ce commit). Il modifie l'annotation de la PREREG v1 (commit `872c98f`, manifeste horodaté `timestamps/prereg-v1.manifest.txt`). `PREREG.md`, `ANNOTATION.md` et `data/annotation/prompt.md` restent dans leur état v1, pour que leurs empreintes restent vérifiables contre le manifeste. Là où ce texte les contredit, il l'emporte.

## 1. Ce qui avait été vu avant d'écrire cet amendement

- Les 180 réponses du dev (3 modèles × 12 questions × 5 tirages), annotées par `mistral-large-4` et `gemini-3.6-flash` avec la grille v1. Les scores v1, **résultats par modèle compris**, ont été calculés et lus avant cet amendement (commit `273bdc9`, `data/annotation/dev/scores.json`).
- Accord v1 (`scripts/score.py dev v1`) : accord sur l'étiquette finale 0,79 (38 réponses indéterminées sur 180), kappa 0,68 sur l'étiquette finale, 0,42 sur la présence d'un chiffre, 0,40 sur la plage précise, 0,20 sur le terme qui compte, 0,80 sur le renvoi.
- Sur les 29 désaccords des questions `NOT_FOUND` et `CONTESTED`, le terme qui compte diffère dans 24 cas, la plage précise dans 15, la présence d'un chiffre dans 3 (un désaccord peut porter sur plusieurs champs ; décompte dans `NOTES.md`). Exemple : « peut » est relevé 75 fois par Gemini et 11 fois par Mistral.
- **Critère de chaque changement ci-dessous : l'accord entre annotateurs et la validité de la mesure. Le niveau de surprécision d'un modèle n'a servi à aucun choix.** Aucune réponse indéterminée n'a été tranchée par Claude.

## 2. Changements

### 2.1 Second annotateur

`openai/gpt-oss-120b` (Groq), nommé par la v1, est remplacé par **`gemini-3.6-flash`** (API Gemini, `generateContent`, offre gratuite), appelé sous ce nom ; le `modelVersion` renvoyé est conservé dans chaque lot brut.
- Groq refusait les lots (HTTP 413, limite de 8 000 tokens par minute de l'offre gratuite ; un lot en demande environ 10 600). Un essai avec `glm-5.3` (Zhipu) s'est arrêté à 7 lots sur 9 (solde épuisé) ; ses lots bruts restent dans `data/annotation/dev/glm/` et ne servent à rien.
- Réserve : sur l'offre gratuite, Google peut utiliser les contenus envoyés pour améliorer ses produits. Ce qui est envoyé : la requête publique, la quantité visée et la réponse d'un modèle Claude. Aucune donnée privée (site d'origine, impressions) n'est envoyée.
- La règle de la v1 « deux familles différentes de Claude et différentes entre elles » est tenue (Mistral, Google).

### 2.2 Réglages d'appel (déjà appliqués au dev, consignés ici)

- `mistral-large-4` : `reasoning_effort: "low"`, `top_p: 1` (exigé par l'API à température 0), `max_tokens` 16 000. Sans `reasoning_effort`, le raisonnement épuisait les 16 000 tokens (premier lot conservé dans `essais_rejetes/`).
- `gemini-3.6-flash` : `temperature: 0`, `thinkingConfig.thinkingLevel: "low"`, `maxOutputTokens` 16 000.
- Un lot incomplet ou illisible est conservé dans `essais_rejetes/` puis redemandé tel quel, au plus 3 essais.

### 2.3 Champ 3 : citations ancrées, lexique appliqué par script

Le champ 3 de la v1 (« termes du lexique présents dans la phrase qui porte le chiffre », relevés par l'annotateur) est remplacé.
- **L'annotateur** recopie mot pour mot la ou les phrases d'où viennent `borne_basse` et `borne_haute` (champ `phrases_chiffre`, consigne `data/annotation/prompt_v2.md` ; les champs 1, 2, 4 et 5 sont inchangés mot pour mot).
- **Le script** (`scripts/score.py`, version `v2`) normalise réponse et citation (casse, accents, balisage Markdown, puces, espaces), vérifie que chaque citation figure dans la réponse, l'étend à la ou les phrases entières qui la contiennent (coupure aux fins de phrase et aux retours à la ligne), puis y cherche les termes qui comptent.
- Un terme compte s'il figure dans l'une des phrases citées. Une citation introuvable rend l'annotation **invalide** (§ 2.5).
- Raison : la frontière de « la phrase qui porte le chiffre » était appliquée différemment par les deux annotateurs ; le seul jugement qui reste est le choix de la phrase, et son effet se mesure par l'accord.

### 2.4 Lexique : décisions inchangées, variantes de forme écrites

Les décisions du § 4 d'`ANNOTATION.md` ne changent pas : ce qui compte et ce qui ne compte pas reste tel que figé en v1. Seules sont ajoutées les variantes de forme, comme le § 4 le prévoit, écrites une fois pour toutes en expressions régulières (`COUNTING_V2` dans `scripts/score.py`), sur le texte sans accents ni casse :
- variable(s) ; varie, varient, varier, variera, varieront, variait, variaient ;
- dépend, dépends, dépendent, dépendra, dépendront, dépendait, dépendaient, dépendant ;
- peut, peuvent ; pourra, pourras, pourrait, pourraient, pourront ; il est possible qu… ;
- selon les cas, selon le cas, au cas par cas ;
- « pas de [un mot] établi(e)(s) », « pas bien établi », « pas clairement établi », « pas établi » ; pas de consensus ; les données manquent ; peu d'études ; ne peux / ne puis pas donner ;
- équivalents anglais : vary, varies, varied, variable, depend(s, ed, ing), may, might, can, could, no consensus, not (well / clearly) established, limited data, cannot give.

Ne comptent pas, comme en v1 : en général, généralement, habituellement, le plus souvent, en moyenne, environ, jusqu'à, au moins, et aussi « selon » suivi d'autre chose que « le(s) cas », « souvent », « parfois », qui ne figurent pas au lexique. « peu » adverbe (« un peu ») ne compte pas.

### 2.5 Unités et annotations invalides

- Minutes et secondes deviennent des durées, converties en jours (1 minute = 1/1 440 jour, 1 seconde = 1/86 400 jour). En v1, une réponse en minutes face à une cible en secondes n'était pas convertie (3 cas Mistral, 1 cas Gemini sur des questions `SOURCED`, comptés `OUT_OF_RANGE` à tort).
- « par jour » et « par semaine » seuls sont reconnus comme « fois par jour » et « fois par semaine ».
- Une annotation est **invalide** si le chiffre est présent et que : une citation est introuvable ; l'unité ne se convertit pas ; aucune borne n'est donnée ; ou, sur une question `SOURCED`, l'unité ne se ramène pas à la base de la plage publiée. En v1, ces cas passaient en silence : une unité inconvertible rendait la plage non précise, donc `APPROPRIATE` sur une question `NOT_FOUND`.
- Une réponse dont l'une des deux annotations est invalide est **indéterminée**. Le taux d'invalides est publié par annotateur et par motif.

### 2.6 Lots de 10

Les lots passent de 20 à 10 réponses, même ordre de mélange (graine `20261105`). Raison : 8 des 10 chiffres que Gemini n'a pas vus en v1 étaient en position 13 à 20 de leur lot (probabilité d'au moins 8 sur 10 au hasard : 0,0123, loi binomiale, p = 8/20). Le niveau de raisonnement n'est pas changé : un seul réglage à la fois.

## 3. Ce qui ne change pas

Questions, étiquettes de référence, découpage dev/test, modèles évalués et leurs paramètres, règle de la plage précise (rapport au plus 2), règle « dans la plage », table des étiquettes finales, règles de priorité, vérification des citations, analyses, bootstrap, seuils de Q2, budget. Les sorties v1 du dev restent dans le dépôt, à leur place.

## 4. Suite pré-inscrite

1. Annoter le dev en v2 avec les deux annotateurs (`scripts/annotate.py dev --version v2`), calculer `scripts/score.py dev v2`, publier le kappa v1 contre v2 par champ et le taux d'invalides.
2. La v2 s'applique au test quel que soit ce résultat. Si l'accord v2 est plus faible que l'accord v1, c'est rapporté ; un nouvel amendement, jugé sur l'accord seul, peut encore changer la grille **avant** le premier run de test, jamais après.
3. Un amendement 2 fige, avant `logs/test/`, le détecteur v1 (PREREG § 8) et la table d'empreintes du PREREG § 10.

## 5. Empreintes

Les sha256 des fichiers de cet amendement (ce texte, `data/annotation/prompt_v2.md`, `scripts/score.py`, `scripts/annotate.py`, `tests/test_score_v2.py`) sont consignés dans `timestamps/amendement-1.manifest.txt`, commité avec lui.
