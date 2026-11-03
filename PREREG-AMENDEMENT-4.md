# PREREG — amendement 4 : pilote sur un modèle ouvert

> Daté du 03/11/2026. Commité et horodaté **avant toute extraction d'activations sur les questions** (`pilot/activations.npz` n'existe pas à ce commit). Ce pilote est une extension exploratoire, hors de Q1 et Q2 : il ne change rien aux amendements 1 à 3 ni à leurs résultats.

## 1. Ce qui avait été vu avant

- Tous les résultats de Q1 et Q2 sur Claude (`results/`). Les étiquettes des 60 questions sont publiques depuis la v1.
- Le modèle ouvert n'a reçu aucune des questions. Il n'a tourné que sur deux phrases synthétiques sans rapport (essai de la chaîne, `pilot/extract.py --smoke`).

## 2. Question et portée

Question : la représentation interne d'une question, au moment où le modèle va répondre, permet-elle de prédire linéairement si la littérature publie un chiffre (`SOURCED`) ou non (`NOT_FOUND`), au-delà de ce que donnent les mots de la question ?

- Les étiquettes portent sur la **question**, pas sur un chiffre produit. Ce pilote est donc l'analogue interne du témoin « question seule » de Q2. Ce n'est pas la question de recherche de la candidature, qui porte sur le chiffre que le modèle s'apprête à dire. C'en est le premier pas.
- Facteur de confusion attendu : un acte très étudié a plus souvent un chiffre publié. Une sonde réussie pourrait n'encoder que la notoriété du sujet. Les témoins (§ 4) servent à le départager.
- Formulation permise : « décodable linéairement », « au-delà d'une ligne de base textuelle ». Jamais « le modèle sait ».
- Avec 49 questions, **un résultat non concluant est probable**. Il sera publié tel quel.

## 3. Modèle et extraction (`pilot/extract.py`)

- `Qwen/Qwen2.5-1.5B-Instruct`, révision Hugging Face `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`, licence Apache-2.0. 28 couches, dimension 1 536.
- Gabarit de chat du modèle, un seul message utilisateur contenant la requête telle quelle. Le prompt système par défaut que le gabarit insère est gardé, comme en usage normal. `add_generation_prompt=True`.
- Position : le dernier token du prompt, après le marqueur de génération de l'assistant. Les 29 états cachés sont relevés : sortie des plongements, puis 28 couches.
- CPU, float32, aucune génération. Sauvegarde en float16 dans `pilot/activations.npz`, commitée, ce qui permet de refaire l'analyse sans le modèle.
- Entrées : les 49 questions `SOURCED` (24) et `NOT_FOUND` (25), dev et test confondus. `CONTESTED` est exclu.

## 4. Analyse (`pilot/probe.py`, numpy seul)

- Sonde : régression logistique L2, C = 0,1, sans réglage, en forme duale. Standardisation apprise sur les seules questions d'entraînement.
- Validation croisée : un pli par `procedure_id` (38 plis). AUROC sur les scores hors pli, positif = `SOURCED`. Score hors pli = X·w, sans l'intercept : celui-ci dépend du taux de positifs de chaque pli et fausserait l'AUROC calculée sur tous les plis réunis (défaut trouvé par un audit avant toute donnée ; sans signal, l'AUROC tombait à 0,05).
- Bootstrap et permutation portent sur les questions, pas sur les procédures : seules 12 questions sur 49 partagent une procédure. C'est une limite déclarée.
- **Couche principale : 14**, le milieu du réseau, fixée ici. Les autres couches sont descriptives.
- Témoins, avec les mêmes plis et la même sonde :
  1. texte : unigrammes et bigrammes de mots de la question, vocabulaire appris sur chaque pli ;
  2. plongements lexicaux : moyenne de la couche 0 sur les tokens de la requête. Au dernier token, la couche 0 est la même pour toutes les questions et ne peut pas servir de témoin ;
  3. permutation des étiquettes entre questions, 1 000 permutations, couche principale.
- IC à 95 % par bootstrap sur les questions : 10 000 tirages, graine `20261108`, mêmes tirages pour les différences appariées.
- **Verdict** :
  - « décodable » si la borne basse de l'AUROC de la couche 14 est > 0,5 et le p de permutation < 0,05 ;
  - « au-delà du texte » seulement si, en plus, les bornes basses de (couche 14 − texte) et de (couche 14 − plongements) sont > 0 ;
  - sinon « non concluant ».
- Ce qui n'est pas fait : aucun jugement verbal lu dans du texte libre (leçon du défaut de lecture de Q2), aucune autre couche ni valeur de C essayée pour choisir.

## 5. Coût et emplacement

Aucun appel payant. Le modèle (3,09 Go), l'environnement Python et les caches sont sur le SSD externe, pas sur le disque du Mac.

## 6. Empreintes

Les sha256 de ce texte, de `pilot/extract.py`, `pilot/probe.py` et `tests/test_pilot.py` sont consignés dans `timestamps/amendement-4.manifest.txt`, commité avec lui.
