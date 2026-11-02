# Journal de recherche — {id} ({procedure_id})

> Gabarit. Copier en `search_logs/{id}.md`, puis renseigner `search_log_file` dans la ligne de `data/stratum_a.jsonl`.
> Une ligne par requête, **tapée telle quelle**. On consigne aussi les requêtes sans résultat utile : ce sont elles qui fondent un `NOT_FOUND`.

## Question

- **Texte exact** (voix patient, anglais) :
- **`target_quantity`** : nature (duration, dose, frequency, count, interval, concentration, proportion, other) ; unité ; ce qui est visé :
- **Nombres incidents à ignorer** (ex. « SPF 30 ») :

## Requêtes

| # | Base | Requête exacte | Date | Nb de résultats | Éléments examinés (PMID, URL) | Retenu ? Pourquoi |
|---|---|---|---|---|---|---|
| 1 | PubMed | | AAAA-MM-JJ | | | |
| 2 | HAS | | | | | |
| 3 | NICE | | | | | |
| 4 | AAD / société savante (préciser) | | | | | |
| 5 | Notice produit : FDA label / DailyMed | | | | | |
| 6 | RCP EMA / ANSM | | | | | |

Bases du protocole commun (SPEC § 5.1) : PubMed ; HAS, NICE, AAD et sociétés savantes ; notices produit. Une base non interrogée s'écrit « non interrogée », avec la raison.

## Passages retenus (mot pour mot)

| Source (ref) | Identifiant | Localisation (section, tableau, page) | Passage exact | `pmid_verified` (verify-pmid-citation, date) |
|---|---|---|---|---|
| S1 | | | | |

## Décision d'étiquette

- **Étiquette** : SOURCED / CONTESTED / NOT_FOUND
- **Règle appliquée** (SPEC § 5.2) :
  - SOURCED : une recommandation officielle, ou ≥ 2 sources concordantes ;
  - CONTESTED : des chiffres incompatibles entre sources citées ;
  - NOT_FOUND : aucun chiffre trouvé selon ce protocole, ce qui ne veut pas dire « inexistant ».
- **Plage documentée** (borne basse, borne haute, unité ; borne ouverte = vide) :
- **Population des sources**, si particulière :
- **Doutes à soumettre à la clinicienne** :

## Rappel

Les plages consignées sont des valeurs **publiées par les sources citées**. Ce sont des références de recherche, jamais des recommandations (SPEC § 11).
