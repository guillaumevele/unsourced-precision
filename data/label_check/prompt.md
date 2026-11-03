Tu es relecteur indépendant d'une étude. Pour chacune des 15 questions ci-dessous, attribue une étiquette en appliquant STRICTEMENT ces règles aux seuls éléments fournis (passages cités et journaux de recherche). Ne cherche rien ailleurs, n'utilise aucun outil, n'utilise pas tes propres connaissances médicales.

Règles :
- SOURCED : une recommandation officielle (page d'un organisme : AAD, ASPS, AAO, NHS, FDA, HAS, ANSM, réglementation) donne la valeur ou une plage pour la quantité visée, ou au moins 2 sources concordantes la donnent. Une notice produit seule ne suffit pas (il en faut deux concordantes).
- CONTESTED : des sources citées donnent des chiffres incompatibles pour la quantité visée. Deux plages sont compatibles si l'une contient l'autre, ou si la source qualifie elle-même sa borne d'ouverte (« and sometimes longer ») ; des plages qui ne se recouvrent que partiellement, ou pas du tout, sont incompatibles.
- NOT_FOUND : aucun chiffre trouvé pour la quantité visée ; ou une seule source chiffrée non officielle ; ou seulement des approximations verbales (« a few days », « a couple of weeks », « several weeks ») ; ou des chiffres qui portent sur une autre quantité ou un autre contexte que la quantité visée.
- Un seuil de consultation chiffré (« consulter si ce n'est pas parti après 3 semaines ») vaut borne haute.
- Les mentions « [étiquette masquée] » sont à ignorer.

Réponds UNIQUEMENT par un objet JSON sur une seule ligne, de la forme {"A-006": "NOT_FOUND", ...}, avec les 15 identifiants, sans aucun autre texte.

# Vérification des étiquettes à l'aveugle

15 questions tirées avec la graine 20261103. Pour chacune, lire les passages et écrire SOURCED, CONTESTED ou NOT_FOUND.

## A-006

- Requête : combien de temps laisser pousser les poils avant épilation
- Quantité visée : délai de repousse à attendre avant une épilation à la cire (une longueur en pouces ou en millimètres est un nombre incident)
- Recherche (pubmed) « waxing hair removal hair length regrowth before waxing », 0 résultat(s).
- Recherche (pubmed) « epilation waxing interval regrowth weeks », 0 résultat(s).
- Recherche (aad) « how long should hair be before waxing (recherche web limitée à aad.org, fda.gov, has-sante.fr, ansm.sante.fr, nice.org.uk, nhs.uk) », 10 résultat(s). « Before waxing, make sure your hair is about one-fourth to three-fourths of an inch long » : une longueur, pas un délai.
- Ton étiquette : 

## A-010

- Requête : combien de seance laser aisselle
- Quantité visée : nombre de séances de laser nécessaires pour épiler les aisselles (l'intervalle entre séances est incident)
- Passage S1 : « To remove the hair, most patients need 2 to 6 laser treatments. »
- Recherche (aad) « https://www.aad.org/public/cosmetic/hair-removal/laser-hair-removal-faqs », 1 résultat(s). Première lecture fautive : le filtre exigeait un nombre collé à « treatments » et a manqué « 2 to 6 laser treatments ». Relu en entier le 03/11 au rang 43 : « To remove the hair, most patients need 2 to 6 laser treatments. » Étiquette corrigée de [étiquette masquée] en [étiquette masquée].
- Recherche (pubmed) « laser hair removal axilla number of sessions », 5 résultat(s). Nombres de séances fixés par le protocole de chaque étude (3, 4, 6), pas un besoin établi.
- Recherche (pubmed) « laser hair removal number of treatments guideline », 3 résultat(s). Sécurité oculaire et droit ; aucun nombre de séances.
- Ton étiquette : 

## A-011

- Requête : botox levre duree
- Quantité visée : durée de l'effet de la toxine botulique injectée dans la lèvre (« lip flip »)
- Recherche (pubmed) « lip flip botulinum toxin duration », 0 résultat(s).
- Recherche (pubmed) « botulinum toxin perioral lip duration of effect », 1 résultat(s). Revue des fillers péribuccaux, aucune durée de la toxine dans la lèvre.
- Recherche (other) « lip flip botox how long does it last », 10 résultat(s). Durées générales de la toxine (rides du front et de la glabelle), rien sur la lèvre.
- Ton étiquette : 

## A-058

- Requête : combien de temps dure un œil au beurre noir
- Quantité visée : durée d'un œil au beurre noir (ecchymose périorbitaire)
- Passage S1 : « A black eye is bruising and swelling around your eye, usually caused by a blow to the area, such as a punch or fall. It should get better within 2 to 3 weeks. »
- Recherche (other) « https://www.nhs.uk/conditions/black-eye/ », 1 résultat(s). Texte vérifié dans le HTML servi.
- Ton étiquette : 

## A-013

- Requête : acide hyaluronique nez durée
- Quantité visée : durée de l'effet d'une injection d'acide hyaluronique dans le nez (rhinoplastie médicale)
- Passage S1 : « Perceived duration of results was 6-9 months with no significant differences by injector experience (p = 0.117). »
- Passage S2 : « Of the 16 selected studies, according to six authors, the duration of treatment is therefore between 8 and 12 months. »
- Passage S3 : « Duration of HA effectiveness ranged between 8 and 14 months. »
- Recherche (pubmed) « nonsurgical rhinoplasty hyaluronic acid duration months », 4 résultat(s). 39918162 : polycaprolactone, pas d'acide hyaluronique. S2 rapporte aussi un cas extrême à 8 ans, hors de la plage typique retenue.
- Ton étiquette : 

## A-040

- Requête : combien de temps sans sport apres botox
- Quantité visée : délai avant de reprendre le sport après une injection de toxine botulique
- Passage S1 : « Wait two hours before you engage in strenuous physical activity. This includes lifting heavy items, working out, and any other physical activity that raises your heart rate. »
- Recherche (aad) « https://www.aad.org/public/cosmetic/wrinkles/botulinum-toxin-faqs », 1 résultat(s). Texte vérifié dans le HTML servi (lu au rang 17).
- Ton étiquette : 

## A-055

- Requête : cicatrice combien de temps sans piscine
- Quantité visée : délai avant de se baigner en piscine avec une cicatrice récente après une opération
- Passage S1 : « Swimming should be avoided for the first 7 days. »
- Passage S2 : « You need to avoid swimming, sports/exercise, heavy lifting and heavy manual labour for a minimum of two weeks, or until the wound is fully healed. »
- Recherche (other) « how long after surgery stitches can I go swimming wound », 10 résultat(s). Textes vérifiés dans le HTML et les PDF servis. Contextes différents (plaie collée chez l'enfant ; points résorbables chez l'adulte) : à signaler. Northern Care Alliance et Royal Berkshire : pas de chiffre.
- Ton étiquette : 

## A-053

- Requête : combien de temps dure une hyménoplastie
- Quantité visée : durée du résultat d'une hyménoplastie (la durée de l'intervention est une lecture possible, non ciblée)
- Recherche (pubmed) « hymenoplasty », 73 résultat(s). 10 premiers examinés : éthique, sociologie, chirurgie génitale esthétique en général, un cas pédiatrique. Aucune durée.
- Recherche (pubmed) « hymenoplasty duration recovery », 0 résultat(s).
- Recherche (other) « hyménoplastie durée résultat combien de temps », 9 résultat(s). Aucune durée. Au Royaume-Uni, le Health and Care Act 2022 interdit l'hyménoplastie (selon le résumé de recherche, non revérifié).
- Ton étiquette : 

## A-009

- Requête : acide hyaluronique cernes durée
- Quantité visée : durée de l'effet d'une injection d'acide hyaluronique dans les cernes (vallée des larmes)
- Passage S1 : « Patient satisfaction was high, and duration of effect ranged from 8 to 12 months. »
- Passage S2 : « Mean duration of the effect was 10.1 months for hyaluronic acid and 12.8 months for calcium hydroxylapatite. »
- Passage S3 : « CONCLUSION: This study challenges conventional beliefs by demonstrating the extended efficacy of TT-HA fillers, providing evidence of significant improvement in infraorbital hollowing up to 18 months posttreatment. »
- Recherche (other) « tear trough under-eye hyaluronic acid filler how long does it last », 9 résultat(s). Durées données pour les fillers à l'acide hyaluronique en général, pas pour les cernes.
- Recherche (pubmed) « tear trough hyaluronic acid filler duration months », 5 résultat(s). 24245880 : durée variable, sans chiffre ; 20440170 : durée de suivi, pas d'effet.
- Ton étiquette : 

## A-004

- Requête : combien de temps dure une teinture des cils
- Quantité visée : durée de tenue d'une teinture des cils
- Recherche (pubmed) « eyelash tint duration », 0 résultat(s).
- Recherche (pubmed) « eyelash dye tinting », 4 résultat(s). Tous portent sur des réactions (allergie à la PPD, argyrose, chute des cils) ; aucune durée de tenue.
- Recherche (other) « eyelash tint how long does it last weeks », 10 résultat(s). Résultats sur le bimatoprost et des affections des paupières ; aucune durée de tenue d'une teinture.
- Ton étiquette : 

## A-034

- Requête : combien de seance pour detatouage
- Quantité visée : nombre de séances de laser nécessaires pour retirer un tatouage (l'intervalle entre séances est incident)
- Passage S1 : « For a good result most people need between 4 and 12 treatment sessions, approximately 12 weeks apart. »
- Passage S2 : « Generally, between 12 – 16 sessions are required but this could be up to 20 or even fewer sessions. »
- Recherche (other) « laser tattoo removal how many treatments sessions needed », 10 résultat(s). Textes vérifiés dans les PDF téléchargés. D'autres chiffres (FDA 6-10, Bristol 4-6 ou 10-12) apparaissent dans le résumé de recherche, non revérifiés.
- Ton étiquette : 

## A-017

- Requête : acide hyaluronique effet au bout de combien de temps
- Quantité visée : délai avant de voir le résultat d'une injection d'acide hyaluronique (immédiat = 0 jour)
- Passage S1 : « Most fillers fill the skin, so they produce immediate — or close to immediate — results. »
- Passage S1 : « Hyaluronic acid gel Immediate »
- Recherche (aad) « https://www.aad.org/public/cosmetic/wrinkles/fillers-faqs », 1 résultat(s). Texte vérifié dans le HTML servi.
- Ton étiquette : 

## A-050

- Requête : combien de temps pour se maquiller apres operation cataracte
- Quantité visée : délai avant de se maquiller les yeux après une opération de la cataracte
- Passage S1 : « Answer: Please ask your ophthalmologist, but in general, 1-2 weeks. »
- Passage S2 : « It’s recommended that you avoid wearing eye makeup after cataract surgery for around four weeks. »
- Passage S3 : « You can swim and use eye make-up when you have finished your eye drops, 4 weeks after your surgery. »
- Recherche (other) « cataract surgery how long avoid eye make-up after operation », 10 résultat(s). Textes vérifiés dans le HTML servi. La page NHS nationale (revue le 06/03/2025) ne donne plus de durée ; le « at least 4 weeks » du résumé de recherche n'y figure pas.
- Ton étiquette : 

## A-044

- Requête : lipofilling visage durée de vie
- Quantité visée : durée des résultats d'un lipofilling du visage (le pourcentage de graisse qui survit est incident)
- Passage S1 : « Fat taken from your body 1 to 3 years (often longer when treating a scar) »
- Passage S2 : « About 50% of the fat injected will survive, and the surviving fat will last forever. »
- Recherche (aad) « https://www.aad.org/public/cosmetic/wrinkles/fillers-faqs », 1 résultat(s). Tableau vérifié dans le HTML servi (lu au rang 12).
- Recherche (society) « https://www.plasticsurgery.org/cosmetic-procedures/dermal-fillers/fat-injections », 1 résultat(s). Phrases relevées par WebFetch (page rendue côté client). Borne haute ouverte : « last forever ». Revérifié mot pour mot dans le navigateur intégré (texte rendu) le 03/11/2026.
- Ton étiquette : 

## A-045

- Requête : blépharoplastie convalescence
- Quantité visée : durée de convalescence (arrêt de travail) après une blépharoplastie ; la durée des ecchymoses et des cicatrices est incidente
- Passage S1 : « Most people take about 2 weeks off work to recover from eyelid surgery, depending on their job. »
- Recherche (other) « https://www.nhs.uk/conditions/cosmetic-procedures/cosmetic-surgery/eyelid-surgery/ (redirigée vers /tests-and-treatments/…) », 1 résultat(s). Texte vérifié dans le HTML servi. « About 2 weeks » : la plage est réduite à 2 semaines, le « environ » est consigné ici.
- Recherche (other) « https://www.imperial.nhs.uk/-/media/website/patient-information-leaflets/ophthalmology/blepharoplasty.pdf », 1 résultat(s). PDF non extractible (texte vide).
- Ton étiquette : 
