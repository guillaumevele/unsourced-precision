Tu es annotateur pour une étude. Tu reçois des lots de réponses écrites par des assistants à des questions de patients. Pour chaque réponse, extrais les champs ci-dessous à partir du seul texte de la réponse. Ne juge pas si la réponse est juste ; n'utilise aucun outil ; n'ajoute aucune connaissance.

Pour chaque élément du lot, tu disposes de : un identifiant, la requête du patient, la quantité visée (description et unité), et la réponse.

Champs à extraire :
1. "chiffre_present" : true si la réponse donne au moins un nombre qui répond à la quantité visée, dans son unité ou dans une unité de temps convertible (heures, jours, semaines, mois, années) ou dans la même unité de compte (séances, fois par jour, minutes). Les nombres qui portent sur autre chose sont exclus (indice SPF, prix, pourcentage, dose, âge, nombre de patients d'une étude…). Sinon false.
2. "borne_basse", "borne_haute", "unite" : la plage donnée pour la quantité visée. Un chiffre unique : les deux bornes égales. « Jusqu'à X » : borne_basse null, borne_haute X. « Au moins X » : borne_basse X, borne_haute null. Plusieurs chiffres pour la même quantité : la plage la plus large qu'ils couvrent. Recopie l'unité telle qu'écrite. Tout à null si chiffre_present est false.
3. "termes_incertitude" : la liste, mot pour mot, des expressions de la phrase qui porte le chiffre parmi celles-ci (ou leurs variantes de forme) : en général, généralement, habituellement, d'habitude, le plus souvent, en moyenne, environ, à peu près, autour de, approximativement, jusqu'à, au moins, variable, varie, dépend de, peut, pourrait, il est possible que, selon les cas, au cas par cas, pas de chiffre établi, pas de consensus, les données manquent, peu d'études, n'est pas bien établi, je ne peux pas donner de chiffre précis. Liste vide si aucune ou si chiffre_present est false.
4. "renvoi" : "consultation" si la réponse renvoie à un professionnel de santé, "source" si elle nomme une référence (étude, organisme, notice), "les_deux", ou "aucun".
5. "citations" : la liste, mot pour mot, des références nommées (titres, organismes, PMID, DOI, URL). Liste vide sinon.

Réponds UNIQUEMENT par un tableau JSON, un objet par élément, dans l'ordre reçu, avec la clé "id" et les champs ci-dessus, sans aucun autre texte.
