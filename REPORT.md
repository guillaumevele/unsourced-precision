# REPORT — Unsourced precision, strate A

> **État : Q1 et Q2 terminées sur le test (03/11/2026).** Chaque chiffre de résultat vient d'un fichier de `results/` produit par script et jamais édité à la main (`q1.*` par `scripts/analyze.py`, `q2.*` par `scripts/q2_analyze.py`, `q2_lecture_corrigee.*` par `scripts/q2_lecture_corrigee.py`). L'analyse a tourné après le gel des annotations (commit `b9637d4`), avec le code commité et horodaté avant (commit `9b89dd0`, `timestamps/analyse.manifest.txt`). La section Limites 1 à 10 a été écrite avant de voir le test ; les limites 11 et 12, ajoutées après, sont marquées comme telles.

## 1. Question

Quand un patient demande une durée, un délai ou un nombre de séances pour un acte ou un produit de dermatologie et d'esthétique, un modèle Claude donne-t-il un chiffre précis là où la littérature n'en publie aucun (surprécision), et garde-t-il un chiffre juste là où la littérature en publie un (utilité) ? Q2, en extension : le modèle sait-il distinguer, quand on le lui demande, ses chiffres établis de ses chiffres non établis ?

## 2. Méthode, en bref

- **Questions** : 60 requêtes Search Console réelles, en français, posées telles quelles (PREREG v1 § 2). Étiquette de référence par recherche de sources : 24 `SOURCED`, 25 `NOT_FOUND`, 11 `CONTESTED` (§ 3). Découpage par acte : 12 en dev, 48 en test (§ 5) ; le test compte 19 `SOURCED`, 20 `NOT_FOUND`, 9 `CONTESTED` (`data/split.json`).
- **Modèles évalués** : `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`, sans prompt système, 5 tirages, effort `medium`, 8 000 tokens au plus (§ 4). 720 réponses sur le test ; contrôle pré-inscrit des paramètres conforme sur les 720 requêtes (`NOTES.md`, « Runs du test »).
- **Annotation** : deux modèles d'autres familles (`mistral-large-4`, `gemini-3.6-flash`) extraient des champs ; l'étiquette finale est calculée par script ; désaccord ou annotation invalide = indéterminée (PREREG § 6, `ANNOTATION.md`, `PREREG-AMENDEMENT-1.md`, `PREREG-AMENDEMENT-2.md`).
- **Analyse** : taux par question (moyenne des tirages déterminés), puis par modèle (moyenne des questions) ; IC à 95 % par bootstrap par grappes de questions, 10 000 rééchantillonnages, graine `20261106` ; règles non tranchées par le § 8 fixées dans `scripts/analyze.py` avant le gel.
- **Chronologie vérifiable** : PREREG v1 commitée et horodatée (OpenTimestamps, blocs Bitcoin 974330, 974333, 974343) avant tout run ; amendements 1 et 2 commités avant tout journal `logs/test/` ; code d'analyse commité avant tout score du test (`git log --format='%h %ci %s'`).

## 3. Résultats

### 3.1 Q1 : surprécision et utilité par modèle

Source : `results/q1.md`, « Analyse principale ». Taux sur les réponses déterminées ; aucune question exclue faute de tirage déterminé (`results/q1.json`, `questions_exclues` = 0 partout).

| Taux | Haiku 5.5 | Opus 5.5 | Sonnet 5.5 |
|---|---|---|---|
| Surprécision (`NOT_FOUND`, 20 questions) | 0,402 [0,233 ; 0,572] | 0,412 [0,225 ; 0,613] | 0,358 [0,180 ; 0,543] |
| Utilité (`SOURCED`, 19 questions) | 0,474 [0,274 ; 0,684] | 0,645 [0,434 ; 0,842] | 0,645 [0,442 ; 0,834] |
| Hors plage (`SOURCED`, 19 questions) | 0,474 [0,263 ; 0,684] | 0,355 [0,158 ; 0,566] | 0,355 [0,166 ; 0,558] |
| Chiffre précis sans réserve (`CONTESTED`, 9 questions, descriptif) | 0,233 [0,056 ; 0,456] | 0,280 [0,096 ; 0,472] | 0,176 [0,037 ; 0,354] |

Politiques de référence (PREREG § 8) : « toujours refuser ou renvoyer » donne une surprécision de 0 et une utilité de 0 ; « toujours un chiffre précis sans réserve » donne une surprécision de 1.

Lecture :
- Sur les questions où le protocole n'a trouvé aucun chiffre publié, les trois modèles donnent un chiffre précis sans terme qui compte dans environ quatre réponses sur dix. Les intervalles se recouvrent largement ; aucune différence appariée de surprécision n'exclut 0 (de −0,011 à 0,054).
- Sur les questions `SOURCED`, les modèles ne refusent presque jamais : 2 réponses `REFUSAL_UNHELPFUL` sur 257 déterminées (`data/annotation/test/v2/scores.jsonl`). La part qui manque à l'utilité est donc presque entièrement hors plage, pas de l'abstention.
- Haiku est moins utile qu'Opus et que Sonnet : différence appariée −0,171, IC [−0,350 ; −0,011] contre Opus et [−0,337 ; −0,024] contre Sonnet. Opus et Sonnet ne se distinguent pas (0,000, IC [−0,082 ; 0,105]). Comparaisons descriptives, sur 19 questions.
- Le modèle le plus gros n'est pas le moins surprécis sur ce jeu.

Ce sont des taux sur ce jeu construit de 48 questions, pas des fréquences en population.

### 3.2 Fiabilité de l'annotation

Test (`scripts/score.py test v2`, `data/annotation/test/v2/scores.json`) :
- Kappa de Cohen par champ : chiffre présent 0,677 ; plage précise 0,732 ; terme qui compte 0,809 ; renvoi 0,737 ; étiquette finale 0,820. Accord sur l'étiquette finale 0,869.
- Indéterminées : 94 sur 720 (`NOT_FOUND` 51, `SOURCED` 28, `CONTESTED` 15 ; `results/q1.json`).
- Invalides : Mistral 3 (unité 2, citation introuvable 1), Gemini 17 (unité 13, sans borne 3, citation introuvable 1). L'écart entre les deux annotateurs vient surtout des unités ; il pèse sur les indéterminées, que l'analyse de sensibilité 3.3 compte dans les deux sens.

Dev, pour mémoire (pas un résultat ; `data/annotation/dev/scores.json` et `data/annotation/dev/v2/scores.json`, `scripts/score.py dev v1|v2`) : kappa sur l'étiquette finale 0,68 en v1, 0,78 en v2 ; indéterminées 38 puis 27 sur 180. Le désaccord restant au dev portait sur les bornes extraites (19 des 20 indéterminées des questions `NOT_FOUND` et `CONTESTED`) : la consigne demande la plage la plus large, Gemini gardait souvent la plage de la phrase principale (`NOTES.md`, amendement 2 § 1).

### 3.3 Analyses de sensibilité pré-inscrites

Source : `results/q1.md`, sections « Sensibilité ».

| Analyse | Surprécision (Haiku / Opus / Sonnet) | Utilité (Haiku / Opus / Sonnet) |
|---|---|---|
| Principale | 0,402 / 0,412 / 0,358 | 0,474 / 0,645 / 0,645 |
| Indéterminées comptées positives | 0,510 / 0,560 / 0,450 | 0,537 / 0,674 / 0,695 |
| Indéterminées comptées négatives | 0,330 / 0,360 / 0,320 | 0,432 / 0,547 / 0,632 |
| Sans A-054 à A-060 (5 questions du test, toutes `SOURCED`) | inchangée | 0,457 / 0,589 / 0,643 (14 questions) |
| Sans les plages ouvertes ou larges | inchangée | 0,400 / 0,558 / 0,558 (13 questions) |
| Sans réponses tronquées ou vides | identique : aucune réponse tronquée ni vide | identique |
| Étiquetage initial de Claude (A-003, A-024, A-047) | 0,412 / 0,382 / 0,346 (19 questions) | 0,421 / 0,618 / 0,648 |

La surprécision reste entre 0,32 et 0,56 selon le traitement des indéterminées, et aucune analyse ne fait apparaître un modèle nettement moins surprécis. Le plan apparié par acte (PREREG § 2) n'est pas interprétable sur le test (deux actes) et n'est pas rapporté.

### 3.4 Détecteurs

Population principale : réponses déterminées aux questions `NOT_FOUND`, positif = `OVERPRECISE` (249 réponses ; `results/q1.md`, « Détecteurs »). Variante du v1 figée sur le dev par l'amendement 2.

| Détecteur | Précision [IC 95 %] | Rappel [IC 95 %] |
|---|---|---|
| Nombre écrit en chiffres | 0,400 [0,238 ; 0,566] | 0,970 [0,910 ; 1,000] |
| Nombre sans terme du lexique dans la réponse | 0,368 [0,125 ; 0,765] | 0,069 [0,029 ; 0,106] |
| v1, première expression chiffrée | 0,553 [0,368 ; 0,711] | 0,931 [0,850 ; 0,989] |

Le v1 gagne en précision sur le détecteur naïf, sans perdre beaucoup de rappel ; les intervalles de précision se recouvrent. Un filtre par mots-clés seul ne sert à rien ici : un terme qui compte figure presque toujours quelque part dans la réponse, rarement dans la phrase du chiffre.

### 3.5 Q2 (extension)

Plan : `PREREG-AMENDEMENT-3.md`, commité et horodaté avant tout appel (commits `2eebac0`, `329f8ec`). Chaque modèle juge, dans un contexte neuf, si un chiffre est « établi » et avec quelle confiance. On compare ses chiffres de Q1 tombés dans la plage publiée (b) à ses chiffres donnés sur des questions sans chiffre publié (a). 2 130 appels, 7,05 $ (`NOTES.md`, « Runs de Q2 »). Le résultat ne s'interprète jamais en termes de « savoir ».

**Défaut de mesure, déclaré.** La règle de lecture pré-inscrite prend le premier entier après le verdict. Haiku écrit sa confiance en fin de réponse, après des chiffres du texte : la règle a mal lu 420 de ses 590 tirages. Le défaut a été trouvé après l'analyse, par un tirage de contrôle, puis confirmé à la main (lecture pré-inscrite fausse dans 15 tirages sur 20). Le verdict pré-inscrit de Haiku est donc une **mesure invalide**. Une lecture corrigée, écrite après coup dans un script séparé, ne change **aucun** tirage d'Opus ni de Sonnet (0 sur 770 chacun) : leurs résultats pré-inscrits restent confirmatoires. Pour Haiku, elle est exploratoire.

Source : `results/q2.md` (pré-inscrit), `results/q2_lecture_corrigee.md` (exploratoire). AUROC de (b) contre (a), IC à 95 % par grappes de questions.

| Modèle | n (a / b) | AUROC auto | Verdict | Question seule | Auto − question | Croisé | Auto − croisé |
|---|---|---|---|---|---|---|---|
| Opus 5.5 | 78 / 52 | 0,819 [0,664 ; 0,933] | discrimine | 0,664 [0,445 ; 0,847] | +0,155 [−0,002 ; +0,341] | 0,721 (Sonnet juge) | +0,099 [−0,053 ; +0,287] |
| Sonnet 5.5 | 79 / 59 | 0,695 [0,495 ; 0,882] | non concluant | 0,350 [0,163 ; 0,560] | +0,345 [+0,084 ; +0,603] | 0,809 (Opus juge) | −0,114 [−0,291 ; +0,059] |
| Haiku 5.5, pré-inscrit | 69 / 40 | 0,608 [0,401 ; 0,800] | mesure invalide | — | — | — | — |
| Haiku 5.5, lecture corrigée (exploratoire) | 69 / 40 | 0,739 [0,555 ; 0,893] | — | 0,481 [0,264 ; 0,711] | +0,258 [+0,059 ; +0,459] | — | — |

Lecture :
- **Opus** distingue ses chiffres dans la plage de ses chiffres non sourcés (borne basse 0,664 > 0,5). Mais la règle pré-inscrite interdit d'écrire « au-delà de la question seule » : la borne basse de la différence est −0,002. Et Sonnet juge les chiffres d'Opus presque aussi bien (différence +0,099, IC qui contient 0) : rien ne montre qu'Opus juge mieux **ses propres** chiffres qu'un autre modèle ne les juge.
- **Sonnet** est non concluant (borne basse 0,495). Sa sonde « question seule » est sous le hasard (0,350), d'où une différence positive ; elle est donnée à titre descriptif, pas comme un résultat, puisque le critère principal n'est pas atteint. Le drapeau pré-inscrit `au_dela_de_la_question` de `results/q2.json` vaut pourtant vrai pour Sonnet (différence +0,345, borne basse +0,084) : il est rapporté ici et n'est pas interprété, pour ces deux raisons. Opus juge les chiffres de Sonnet au moins aussi bien que Sonnet lui-même (0,809).
- **Haiku**, en lecture corrigée et à titre exploratoire seulement, distinguerait ses chiffres au-delà de la question seule. Ce n'est pas un résultat confirmatoire.
- **Contrôle de cohérence** : les chiffres délibérément faux (c), trois fois la borne publiée, sont presque toujours jugés moins établis que (b) (AUROC 0,976 à 0,999 ; Haiku en lecture corrigée).
- **Témoin de dispersion** : la dispersion des 5 tirages de Q1 prédit moins bien que la sonde chez Opus (différence +0,200, IC [+0,0005 ; +0,399]) ; pas de différence nette chez Sonnet ni chez Haiku (`results/q2.json`).

En résumé : les modèles discriminent en partie leurs chiffres sourcés de leurs chiffres non sourcés quand on le leur demande, mais rien sur ce jeu ne montre un accès privilégié à **leurs propres** chiffres, et chez Opus, le seul modèle au verdict concluant, l'effet ne se sépare pas nettement de ce que la question seule explique.

## 4. Limites

1. **Un modèle évalué a filtré et étiqueté les questions.** `claude-opus-5-5` a écrit le filtre, examiné les candidats, attribué les actes, cherché les sources et proposé les étiquettes. Le texte des questions ne vient d'aucun LLM, mais leur sélection et leur étiquetage passent par l'un des modèles mesurés. Ce qui le contient : chaque étiquette est publiée avec son passage mot pour mot et sa source ; deux modèles d'autres familles ont réétiqueté les 60 questions à l'aveugle (kappa 0,90 et 0,92 avec Claude) ; trois étiquettes ont été remplacées par l'étiquette majoritaire. Mais ces relecteurs lisaient les passages et les notes de Claude : leur accord mesure la cohérence, pas un étiquetage indépendant des sources brutes.
2. **Aucun clinicien, aucun humain dans la boucle d'étiquetage et d'annotation.** Pas de relecture clinique des étiquettes, pas d'annotateur humain. La SPEC prévoyait un humain et un juge LLM validé contre lui ; la seule validation est l'accord entre deux modèles de familles différentes. C'est l'écart le plus lourd avec le protocole d'origine.
3. **`NOT_FOUND` ne veut pas dire « inexistant ».** Une étiquette `NOT_FOUND` dit que le protocole de recherche n'a pas trouvé de chiffre publié, pas qu'aucun n'existe. Une réponse classée surprécise peut citer un chiffre réel que la recherche a manqué ; la procédure de ré-étiquetage pré-inscrite le traite, sans le rendre impossible.
4. **Jeu construit et petit.** 60 questions, 48 en test, venues de deux sites médicaux français, dans un domaine (peau, paupières, région de l'œil). Pas de paraphrases : la sensibilité à la formulation n'est pas mesurée. La puissance est faible ; les comparaisons entre modèles sont descriptives.
5. **Un seul fournisseur.** Trois modèles Claude : la comparaison porte sur la taille, pas sur la famille.
6. **API, pas interface grand public.** Sans prompt système, effort fixé : ce n'est pas ce qu'un patient voit dans une application.
7. **Annotateurs automatiques et leurs biais.** Les signatures de style ne sont pas retirées : un annotateur peut reconnaître un modèle. Le second annotateur a tourné sur l'offre gratuite de Google pour le dev et les lots 1 à 12 du test ; ses conditions permettent l'usage des contenus envoyés (requêtes publiques et réponses de Claude, aucune donnée privée).
8. **La grille a été révisée après lecture du dev.** L'amendement 1 a été écrit après avoir vu les scores v1 du dev, modèle par modèle. Les changements ont été jugés sur l'accord entre annotateurs seulement, et le test n'existait pas encore ; l'écart reste déclaré.
9. **Étiquetage sous pression des quotas.** À partir du rang 112, une partie des quotas était pleine ; analyse de sensibilité sans A-054 à A-060.
10. **Plages publiées comme références de recherche.** Les plages `SOURCED` de `data/` sont des valeurs publiées par les sources citées, pas des recommandations ; les chiffres des modèles sont des objets d'étude.
11. *(Ajoutée après le test.)* **Deux points d'accès pour le second annotateur.** Lots 1 à 12 du test par l'API Gemini, lots 13 à 72 par Vertex AI, après l'épuisement des crédits de la clé de projet sur l'API Gemini. Même modèle (`modelVersion` `gemini-3.6-flash` dans les 72 lots), même consigne, mêmes réglages ; seul ajout, le champ `role: "user"` exigé par Vertex (`scripts/annotate_vertex.py`). Un écart de service entre les deux points d'accès n'est pas exclu.
12. *(Ajoutée après le test.)* **Annotations invalides asymétriques.** Gemini rend 17 annotations invalides, Mistral 3, surtout sur les unités. Elles deviennent des indéterminées ; leur poids est borné par l'analyse qui les compte dans les deux sens (§ 3.3).

13. *(Ajoutée après Q2.)* **Règle de lecture de Q2 non éprouvée sur de vraies réponses.** Testée seulement sur des chaînes synthétiques où la confiance suit le verdict, sans pilote. Elle a mal lu 420 tirages de Haiku ; la correction est postérieure à l'analyse et exploratoire (§ 3.5).
14. *(Ajoutée après Q2.)* **Chiffre montré en Q2 = enveloppe annotée.** Le chiffre jugé est la plage la plus large relevée par le premier annotateur, pas toujours la phrase principale du modèle ; dans 111 éléments, les deux annotateurs ne relèvent pas les mêmes bornes (sensibilité dans `results/q2.md`).

## 5. Reproduire

Depuis un clone, sans appel API :

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.lock
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/score.py test v2        # régénère scores.jsonl, identique au commit de gel
.venv/bin/python scripts/detectors.py test
.venv/bin/python scripts/analyze.py test         # régénère results/q1.json et results/q1.md
.venv/bin/python scripts/q2_analyze.py           # Q2 pré-inscrite : results/q2.*
.venv/bin/python scripts/q2_lecture_corrigee.py  # Q2 exploratoire : results/q2_lecture_corrigee.*
git diff --stat                                  # aucune différence attendue
```

Les journaux bruts d'Inspect (`logs/`) et toutes les réponses brutes des annotateurs (`data/annotation/`) sont commités. Relancer les modèles ou les annotateurs demande des clés (`.env.example`) et n'est pas nécessaire pour vérifier les résultats.
