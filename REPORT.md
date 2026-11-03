# REPORT — Unsourced precision, strate A

> **État : squelette.** Les sections Résultats sont vides tant que le test n'est pas annoté et gelé (PREREG v1 § 8, amendement 1 § 4). Aucun chiffre de résultat n'est écrit ici à la main : chaque chiffre renverra à un fichier de `results/` et au script qui le produit. La section Limites est écrite d'avance, avant de voir le test.

## 1. Question

Quand un patient demande une durée, un délai ou un nombre de séances pour un acte ou un produit de dermatologie et d'esthétique, un modèle Claude donne-t-il un chiffre précis là où la littérature n'en publie aucun (surprécision), et garde-t-il un chiffre juste là où la littérature en publie un (utilité) ? Q2, en extension : le modèle sait-il distinguer, quand on le lui demande, ses chiffres établis de ses chiffres non établis ?

## 2. Méthode, en bref

- **Questions** : 60 requêtes Search Console réelles, en français, posées telles quelles (PREREG v1 § 2). Étiquette de référence par recherche de sources : 24 `SOURCED`, 25 `NOT_FOUND`, 11 `CONTESTED` (§ 3). Découpage par acte : 12 en dev, 48 en test (§ 5).
- **Modèles évalués** : `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`, sans prompt système, 5 tirages, effort `medium`, 8 000 tokens au plus (§ 4).
- **Annotation** : deux modèles d'autres familles (`mistral-large-4`, `gemini-3.6-flash`) extraient des champs ; l'étiquette finale est calculée par script ; désaccord ou annotation invalide = indéterminée (PREREG § 6, `ANNOTATION.md`, `PREREG-AMENDEMENT-1.md`).
- **Chronologie vérifiable** : PREREG v1 commitée et horodatée (OpenTimestamps) avant tout run ; amendement 1 commité avant tout journal `logs/test/` (`git log --format='%h %ci %s'`).

## 3. Résultats

### 3.1 Q1 : surprécision et utilité par modèle

*À remplir depuis `results/` après le gel des annotations du test.*

### 3.2 Fiabilité de l'annotation

*Kappa par champ, accord final, taux d'invalides par annotateur et par motif, sur le test. Le dev est publié à part (v1 et v2).*

Dev, pour mémoire (pas un résultat ; `data/annotation/dev/scores.json` et `data/annotation/dev/v2/scores.json`, `scripts/score.py dev v1|v2`) : kappa sur l'étiquette finale 0,68 en v1, 0,78 en v2 ; indéterminées 38 puis 27 sur 180. Le désaccord restant porte sur les bornes extraites (19 des 20 indéterminées des questions `NOT_FOUND` et `CONTESTED`) : la consigne demande la plage la plus large, Gemini garde souvent la plage de la phrase principale (`NOTES.md`, amendement 2 § 1).

### 3.3 Analyses de sensibilité pré-inscrites

*Sans A-054 à A-060 ; sans les 8 questions à plage ouverte ou large ; indéterminées comptées dans un sens puis dans l'autre ; sans réponses tronquées ou vides ; avec l'étiquetage initial de Claude (A-003, A-024, A-047).*

### 3.4 Détecteurs

*Trois détecteurs (PREREG § 8), précision et rappel avec IC contre l'étiquette finale.*

### 3.5 Q2 (extension)

*Chiffrée et lancée seulement si Q1 est terminée.*

## 4. Limites

1. **Un modèle évalué a filtré et étiqueté les questions.** `claude-opus-5-5` a écrit le filtre, examiné les candidats, attribué les actes, cherché les sources et proposé les étiquettes. Le texte des questions ne vient d'aucun LLM, mais leur sélection et leur étiquetage passent par l'un des modèles mesurés. Ce qui le contient : chaque étiquette est publiée avec son passage mot pour mot et sa source ; deux modèles d'autres familles ont réétiqueté les 60 questions à l'aveugle (kappa 0,90 et 0,92 avec Claude) ; trois étiquettes ont été remplacées par l'étiquette majoritaire. Mais ces relecteurs lisaient les passages et les notes de Claude : leur accord mesure la cohérence, pas un étiquetage indépendant des sources brutes.
2. **Aucun clinicien, aucun humain dans la boucle d'étiquetage et d'annotation.** Pas de relecture clinique des étiquettes, pas d'annotateur humain. La SPEC prévoyait un humain et un juge LLM validé contre lui ; la seule validation est l'accord entre deux modèles de familles différentes. C'est l'écart le plus lourd avec le protocole d'origine.
3. **`NOT_FOUND` ne veut pas dire « inexistant ».** Une étiquette `NOT_FOUND` dit que le protocole de recherche n'a pas trouvé de chiffre publié, pas qu'aucun n'existe. Une réponse classée surprécise peut citer un chiffre réel que la recherche a manqué ; la procédure de ré-étiquetage pré-inscrite le traite, sans le rendre impossible.
4. **Jeu construit et petit.** 60 questions, 48 en test, venues de deux sites médicaux français, dans un domaine (peau, paupières, région de l'œil). Pas de paraphrases : la sensibilité à la formulation n'est pas mesurée. La puissance est faible ; les comparaisons entre modèles sont descriptives.
5. **Un seul fournisseur.** Trois modèles Claude : la comparaison porte sur la taille, pas sur la famille.
6. **API, pas interface grand public.** Sans prompt système, effort fixé : ce n'est pas ce qu'un patient voit dans une application.
7. **Annotateurs automatiques et leurs biais.** Les signatures de style ne sont pas retirées : un annotateur peut reconnaître un modèle. Le second annotateur tourne sur l'offre gratuite de Google, dont les conditions permettent l'usage des contenus envoyés (requêtes publiques et réponses de Claude, aucune donnée privée).
8. **La grille a été révisée après lecture du dev.** L'amendement 1 a été écrit après avoir vu les scores v1 du dev, modèle par modèle. Les changements ont été jugés sur l'accord entre annotateurs seulement, et le test n'existait pas encore ; l'écart reste déclaré.
9. **Étiquetage sous pression des quotas.** À partir du rang 112, une partie des quotas était pleine ; analyse de sensibilité sans A-054 à A-060.
10. **Plages publiées comme références de recherche.** Les plages `SOURCED` de `data/` sont des valeurs publiées par les sources citées, pas des recommandations ; les chiffres des modèles sont des objets d'étude.

## 5. Reproduire

*À écrire avec `results/` : un clone neuf plus une commande régénère `results/` depuis `logs/` sans appel API (SPEC § 12).*
