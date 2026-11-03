Tu es relecteur indépendant d'une étude. Pour chacune des 60 questions ci-dessous, attribue une étiquette en appliquant STRICTEMENT ces règles aux seuls éléments fournis (passages cités et journaux de recherche). Ne cherche rien ailleurs, n'utilise aucun outil, n'utilise pas tes propres connaissances médicales.

Règles :
- SOURCED : une recommandation officielle (page d'un organisme : AAD, ASPS, AAO, NHS, FDA, HAS, ANSM, réglementation) donne la valeur ou une plage pour la quantité visée, ou au moins 2 sources concordantes la donnent. Une notice produit seule ne suffit pas (il en faut deux concordantes).
- CONTESTED : des sources citées donnent des chiffres incompatibles pour la quantité visée. Deux plages sont compatibles si l'une contient l'autre, ou si la source qualifie elle-même sa borne d'ouverte (« and sometimes longer ») ; des plages qui ne se recouvrent que partiellement, ou pas du tout, sont incompatibles.
  Précisions : on compare les affirmations principales des sources (« generally », « most people », « the duration was ») ; une exception signalée (« could be up to 20 or even fewer », « sometimes longer ») ne rend une source compatible qu'avec les exceptions d'une autre source. Un effet observé à X mois (« persisting at 18 months », « still had a visible effect at month 18 ») vaut une durée d'au moins X, pas une borne haute. Une réserve propre à un autre contexte (« often longer when treating a scar ») n'ouvre pas la borne pour la question posée.
- NOT_FOUND : aucun chiffre trouvé pour la quantité visée ; ou une seule source chiffrée non officielle ; ou seulement des approximations verbales (« a few days », « a couple of weeks », « several weeks ») ; ou des chiffres qui portent sur une autre quantité ou un autre contexte que la quantité visée.
- Un seuil de consultation chiffré (« consulter si ce n'est pas parti après 3 semaines ») vaut borne haute.
- Les mentions « [étiquette masquée] » sont à ignorer.

Réponds UNIQUEMENT par un objet JSON sur une seule ligne, de la forme {"A-006": "NOT_FOUND", ...}, avec les 60 identifiants, sans aucun autre texte.


# Questions

## A-001
- Requête : combien de temps dure les injections aux levres
- Quantité visée : durée de l'effet d'une injection d'acide hyaluronique dans les lèvres
- Passage S1 : « HYC-24L is safe and effective for aesthetic lip augmentation, with results lasting up to 1 year. »
- Passage S2 : « At Month 6, 90% of the patients were responders; at Month 12, 70%; and at Month 18, >40% still had a visible effect. »
- Recherche (pubmed) « hyaluronic acid filler lip augmentation duration of effect randomized », 0 résultat(s).
- Recherche (pubmed) « hyaluronic acid lip augmentation 12 months randomized controlled trial », 4 résultat(s). 41273141 : produit topique, hors sujet ; 18986859 : comparaison de volumes sans durée.
- Recherche (other) « NHS dermal fillers how long do they last », 10 résultat(s). La page redirige vers une page générale sans durée (HTTP 301) : non utilisable.

## A-002
- Requête : combien de temps dure un lifting cervico-facial
- Quantité visée : durée des résultats d'un lifting cervico-facial (la durée de l'opération est une lecture possible, non ciblée)
- Recherche (pubmed) « facelift longevity long-term results years follow-up », 6 résultat(s). 23190814 (Jones 2012) : correction maintenue à 5,5 ans, une seule cohorte, pas de durée des résultats ; les autres portent sur le front, le tiers moyen ou la technique.
- Recherche (society) « https://www.plasticsurgery.org/cosmetic-procedures/facelift (+ /results, /recovery) », 3 résultat(s). Aucune durée chiffrée dans le texte servi.

## A-003
- Requête : botox effet apres combien de temps
- Quantité visée : délai entre l'injection de toxine botulique et l'apparition de l'effet
- Passage S1 : « Typically, the initial doses of reconstituted BOTOX Cosmetic induce chemical denervation of the injected muscles one to two days after injection, increasing in intensity during the first week. »
- Passage S2 : « CONCLUSION: onabotulinumtoxinA provides rapid onset (one to two days) based on physician and subject assessment. »
- Recherche (fda_label) « https://api.fda.gov/drug/label.json?search=openfda.brand_name:%22BOTOX+COSMETIC%22 », 1 résultat(s). Phrases filtrées sur onset|days|duration|months|weeks|repeat|interval.
- Recherche (pubmed) « onabotulinumtoxinA glabellar lines onset of effect », 7 résultat(s). 24098087 : délai moyen de 5,29 jours pour l'onabotulinumtoxinA chez les femmes, dans la plage de 1 à 7 jours ; 36536093 : médiane de 2,0 jours (abobotulinumtoxinA).

## A-004
- Requête : combien de temps dure une teinture des cils
- Quantité visée : durée de tenue d'une teinture des cils
- Recherche (pubmed) « eyelash tint duration », 0 résultat(s).
- Recherche (pubmed) « eyelash dye tinting », 4 résultat(s). Tous portent sur des réactions (allergie à la PPD, argyrose, chute des cils) ; aucune durée de tenue.
- Recherche (other) « eyelash tint how long does it last weeks », 10 résultat(s). Résultats sur le bimatoprost et des affections des paupières ; aucune durée de tenue d'une teinture.

## A-005
- Requête : baby botox durée
- Quantité visée : durée de l'effet d'une injection de toxine botulique à faibles doses (« baby botox »)
- Recherche (pubmed) « microbotox duration », 2 résultat(s). Revue mécanistique ; bloc nerveux pour la douleur. Aucune durée d'effet.
- Recherche (pubmed) « microdroplet botulinum toxin duration of effect », 3 résultat(s). 40464862 : durées de procédure et de reprise d'activité, pas de durée d'effet.
- Recherche (pubmed) « baby botox », 370 résultat(s). Requête non spécifique (« baby » apparie la pédiatrie) : non examinée au-delà du titre des 10 premiers.
- Recherche (other) « baby botox microbotox how long does it last », 9 résultat(s). Aucune source sur les faibles doses ; seules des durées pour la toxine aux doses standard.

## A-006
- Requête : combien de temps laisser pousser les poils avant épilation
- Quantité visée : délai de repousse à attendre avant une épilation à la cire (une longueur en pouces ou en millimètres est un nombre incident)
- Recherche (pubmed) « waxing hair removal hair length regrowth before waxing », 0 résultat(s).
- Recherche (pubmed) « epilation waxing interval regrowth weeks », 0 résultat(s).
- Recherche (aad) « how long should hair be before waxing (recherche web limitée à aad.org, fda.gov, has-sante.fr, ansm.sante.fr, nice.org.uk, nhs.uk) », 10 résultat(s). « Before waxing, make sure your hair is about one-fourth to three-fourths of an inch long » : une longueur, pas un délai.

## A-007
- Requête : combien de temps dure un candy lips
- Quantité visée : durée de tenue d'un maquillage permanent des lèvres (« candy lips »)
- Recherche (other) « "candy lips" acide hyaluronique technique lèvres », 18 résultat(s). Identifie « candy lips » comme une dermopigmentation des lèvres. Les durées citées viennent de sites non médicaux, non recevables (§ 5.1).
- Recherche (pubmed) « permanent makeup lip duration », 1 résultat(s). Laser péribuccal, hors sujet.
- Recherche (pubmed) « cosmetic tattooing lips fading years », 0 résultat(s).
- Recherche (fda_label) « https://www.fda.gov/consumers/womens-health-topics/tattoos-and-permanent-make », 1 résultat(s). Seule durée : « Permanent tattoos last a lifetime. » Rien sur le maquillage permanent.

## A-008
- Requête : combien de seance cryolipolyse ventre
- Quantité visée : nombre de séances de cryolipolyse nécessaires pour le ventre (le nombre de cycles par séance est incident)
- Passage S1 : « Cryolipolysis: Device uses cold to freeze the fat, which destroys the fat. Usually 2 treatment sessions »
- Recherche (pubmed) « cryolipolysis abdomen number of treatment sessions », 4 résultat(s). 39829238 : pratique observée, médiane 1 séance par patient, pas une recommandation ; 37138191 et 31375459 : protocoles d'étude à 2 et 1 séance ; 25521101 : « mandate multiple sessions » sans chiffre.
- Recherche (pubmed) « cryolipolysis abdomen two treatments randomized », 0 résultat(s).
- Recherche (aad) « cryolipolysis how many treatment sessions abdomen (recherche web limitée à aad.org, fda.gov, has-sante.fr, ansm.sante.fr, nice.org.uk, nhs.uk, plasticsurgery.org) », 10 résultat(s). AAD : « Usually 2 treatment sessions » (texte vérifié dans le HTML servi). ASPS : retraitement possible, sans nombre de séances. Étiquette d'abord posée à [étiquette masquée] sur PubMed seul, corrigée en [étiquette masquée] après la recherche officielle prévue par le protocole.

## A-009
- Requête : acide hyaluronique cernes durée
- Quantité visée : durée de l'effet d'une injection d'acide hyaluronique dans les cernes (vallée des larmes)
- Passage S1 : « Patient satisfaction was high, and duration of effect ranged from 8 to 12 months. »
- Passage S2 : « Mean duration of the effect was 10.1 months for hyaluronic acid and 12.8 months for calcium hydroxylapatite. »
- Passage S3 : « CONCLUSION: This study challenges conventional beliefs by demonstrating the extended efficacy of TT-HA fillers, providing evidence of significant improvement in infraorbital hollowing up to 18 months posttreatment. »
- Passage S3 : « Most patients experienced an improvement in MIHAS grade posttreatment, with significant results persisting at 18 months. »
- Recherche (other) « tear trough under-eye hyaluronic acid filler how long does it last », 9 résultat(s). Durées données pour les fillers à l'acide hyaluronique en général, pas pour les cernes.
- Recherche (pubmed) « tear trough hyaluronic acid filler duration months », 5 résultat(s). 24245880 : durée variable, sans chiffre ; 20440170 : durée de suivi, pas d'effet.

## A-010
- Requête : combien de seance laser aisselle
- Quantité visée : nombre de séances de laser nécessaires pour épiler les aisselles (l'intervalle entre séances est incident)
- Passage S1 : « To remove the hair, most patients need 2 to 6 laser treatments. »
- Recherche (aad) « https://www.aad.org/public/cosmetic/hair-removal/laser-hair-removal-faqs », 1 résultat(s). Première lecture fautive : le filtre exigeait un nombre collé à « treatments » et a manqué « 2 to 6 laser treatments ». Relu en entier le 03/11 au rang 43 : « To remove the hair, most patients need 2 to 6 laser treatments. » Étiquette corrigée de [étiquette masquée] en [étiquette masquée].
- Recherche (pubmed) « laser hair removal axilla number of sessions », 5 résultat(s). Nombres de séances fixés par le protocole de chaque étude (3, 4, 6), pas un besoin établi.
- Recherche (pubmed) « laser hair removal number of treatments guideline », 3 résultat(s). Sécurité oculaire et droit ; aucun nombre de séances.

## A-011
- Requête : botox levre duree
- Quantité visée : durée de l'effet de la toxine botulique injectée dans la lèvre (« lip flip »)
- Recherche (pubmed) « lip flip botulinum toxin duration », 0 résultat(s).
- Recherche (pubmed) « botulinum toxin perioral lip duration of effect », 1 résultat(s). Revue des fillers péribuccaux, aucune durée de la toxine dans la lèvre.
- Recherche (other) « lip flip botox how long does it last », 10 résultat(s). Durées générales de la toxine (rides du front et de la glabelle), rien sur la lèvre.

## A-012
- Requête : botox tous les combien
- Quantité visée : intervalle entre deux injections de toxine botulique esthétique
- Passage S1 : « L’intervalle entre deux traitements ne doit pas être inférieur à trois mois. »
- Passage S2 : « L’intervalle entre deux traitements par Azzalure ne doit pas être inférieur à trois mois. »
- Recherche (ansm) « Vistabel RCP intervalle entre deux traitements trois mois (recherche web limitée à la base publique des médicaments, ansm.sante.fr, ema.europa.eu, has-sante.fr) », 9 résultat(s). Texte vérifié dans les deux pages servies.
- Recherche (ansm) « Azzalure RCP intervalle traitements trois mois », 9 résultat(s). Texte vérifié dans la page servie.
- Recherche (fda_label) « https://api.fda.gov/drug/label.json?search=openfda.brand_name:%22BOTOX+COSMETIC%22 », 1 résultat(s). La notice américaine ne fixe pas d'intervalle chiffré (« longest feasible intervals »).

## A-013
- Requête : acide hyaluronique nez durée
- Quantité visée : durée de l'effet d'une injection d'acide hyaluronique dans le nez (rhinoplastie médicale)
- Passage S1 : « Perceived duration of results was 6-9 months with no significant differences by injector experience (p = 0.117). »
- Passage S2 : « Of the 16 selected studies, according to six authors, the duration of treatment is therefore between 8 and 12 months. »
- Passage S3 : « Duration of HA effectiveness ranged between 8 and 14 months. »
- Recherche (pubmed) « nonsurgical rhinoplasty hyaluronic acid duration months », 4 résultat(s). 39918162 : polycaprolactone, pas d'acide hyaluronique. S2 rapporte aussi un cas extrême à 8 ans, hors de la plage typique retenue.

## A-014
- Requête : combien de temps dure une séance de mésothérapie
- Quantité visée : durée d'une séance de mésothérapie esthétique (la fréquence des séances est incidente)
- Recherche (pubmed) « mesotherapy session duration minutes », 0 résultat(s).
- Recherche (has) « mésothérapie esthétique durée d'une séance minutes (recherche web limitée à has-sante.fr, ansm.sante.fr, aad.org, nhs.uk, nice.org.uk, plasticsurgery.org, fda.gov) », 10 résultat(s). Rapport HAS 2014 : longueur d'aiguille et fréquence des séances, aucune durée de séance.

## A-015
- Requête : combien de temps dure l'effet du botox
- Quantité visée : durée de l'effet d'une injection de toxine botulique esthétique
- Passage S1 : « This temporarily relaxes the targeted muscles, causing fine lines and wrinkles to diminish. The effect lasts about 3 to 4 months — and sometimes longer. »
- Passage S2 : « The duration of effect of BOTOX Cosmetic for glabellar lines is approximately 3-4 months. »
- Recherche (aad) « https://www.aad.org/public/cosmetic/wrinkles/botulinum-toxin-faqs », 1 résultat(s). Texte vérifié dans le HTML servi.
- Recherche (fda_label) « https://api.fda.gov/drug/label.json?search=openfda.brand_name:%22BOTOX+COSMETIC%22 », 1 résultat(s).

## A-016
- Requête : durée tatouage temporaire
- Quantité visée : durée de tenue d'un tatouage temporaire (henné ou décalcomanie)
- Passage S1 : « A henna tattoo lasts for 3 days up to a few weeks. »
- Passage S1 : « Decal tattoos may last for a day or up to a week or more. »
- Recherche (fda_label) « temporary tattoo henna how long does it last (recherche web limitée à fda.gov, aad.org, nhs.uk, has-sante.fr, ansm.sante.fr, nice.org.uk) », 10 résultat(s). Texte vérifié dans le PDF téléchargé. Borne haute ouverte : « a few weeks » n'est pas chiffré.

## A-017
- Requête : acide hyaluronique effet au bout de combien de temps
- Quantité visée : délai avant de voir le résultat d'une injection d'acide hyaluronique (immédiat = 0 jour)
- Passage S1 : « Most fillers fill the skin, so they produce immediate — or close to immediate — results. »
- Passage S1 : « Hyaluronic acid gel Immediate »
- Recherche (aad) « https://www.aad.org/public/cosmetic/wrinkles/fillers-faqs », 1 résultat(s). Texte vérifié dans le HTML servi.

## A-018
- Requête : barrière cutanée endommagée combien de temps
- Quantité visée : délai de réparation d'une barrière cutanée endommagée
- Recherche (pubmed) « skin barrier recovery time after disruption transepidermal water loss days humans », 4 résultat(s). Délais mesurés dans des modèles d'agression contrôlée (acétone, microaiguilles, ruban adhésif), propres à chaque modèle : pas un délai de réparation général.
- Recherche (other) « damaged skin barrier how long to repair », 9 résultat(s). Brevets et petites études ; aucune page des organismes visés.

## A-019
- Requête : cryolipolyse resultat en combien de temps
- Quantité visée : délai avant le résultat complet d'une cryolipolyse (les premiers changements, dès 3 semaines, sont une lecture secondaire)
- Passage S1 : « If you are treated with a device, you may notice some changes as early as 3 weeks. Most people see the full effect between 3 and 6 months after the last treatment. »
- Passage S2 : « The injured fat cells are gradually eliminated by the body over four to six months. »
- Recherche (aad) « https://www.aad.org/public/cosmetic/fat-removal/non-invasive-what-to-expect », 1 résultat(s). Texte vérifié dans le HTML servi.
- Recherche (society) « https://www.plasticsurgery.org/cosmetic-procedures/nonsurgical-fat-reduction/cryolipolysis », 1 résultat(s). Phrase relevée par WebFetch le 03/11, non revérifiée dans le HTML brut (page rendue côté client). Revérifié mot pour mot dans le navigateur intégré (texte rendu) le 03/11/2026.

## A-020
- Requête : combien de temps dure un tatouage des sourcils
- Quantité visée : durée de tenue d'un tatouage des sourcils (maquillage permanent, microblading)
- Recherche (pubmed) « microblading eyebrow duration months », 1 résultat(s). Détatouage des sourcils au laser picoseconde ; pas de durée de tenue.
- Recherche (pubmed) « eyebrow permanent makeup longevity », 0 résultat(s).
- Recherche (fda_label) « https://www.fda.gov/consumers/womens-health-topics/tattoos-and-permanent-make », 1 résultat(s). Aucune durée pour le maquillage permanent (consultée pour A-007).

## A-021
- Requête : abdominoplastie combien de temps apres accouchement
- Quantité visée : délai entre l'accouchement et une abdominoplastie
- Passage S1 : « This typically means waiting a minimum of six months postpartum, and longer if breastfeeding. »
- Passage S2 : « Typically, surgeons suggest waiting six months to one year before undergoing a mommy makeover. »
- Recherche (society) « tummy tuck how long to wait after pregnancy childbirth months », 10 résultat(s). Phrases relevées par WebFetch (pages rendues côté client). Ce sont des avis de chirurgiens publiés par la société, pas une recommandation formelle : à signaler au relecteur. Revérifié mot pour mot dans le navigateur intégré (texte rendu) le 03/11/2026.

## A-022
- Requête : bbl liquide dure combien de temps
- Quantité visée : durée de l'effet d'une augmentation fessière par injection (« BBL liquide »)
- Recherche (pubmed) « hyaluronic acid buttock augmentation duration », 2 résultat(s). 37407710 : « The estimated duration of product effectiveness is 16.16 months. » Source unique. 32440901 : produits retirés du marché pour durée limitée, sans chiffre.
- Recherche (pubmed) « liquid BBL », 51 résultat(s). « BBL » apparie un polymère et d'autres sigles : hors sujet.
- Recherche (pubmed) « gluteal augmentation filler injection longevity », 0 résultat(s).
- Recherche (society) « non-surgical buttock augmentation filler injections how long does it last », 9 résultat(s). Durées des fillers du visage seulement ; rien sur la région fessière.

## A-023
- Requête : abdominoplastie convalescence
- Quantité visée : durée de convalescence après une abdominoplastie (reprise des activités ou du travail)
- Recherche (society) « https://www.plasticsurgery.org/cosmetic-procedures/tummy-tuck/recovery », 1 résultat(s). Aucune durée ; la page renvoie les questions de délai au chirurgien.
- Recherche (pubmed) « abdominoplasty return to work days recovery time », 0 résultat(s).
- Recherche (pubmed) « abdominoplasty return to work », 8 résultat(s). 31942338 : 16 à 23 jours avec cure de hernie ; 33785269 : 4 semaines après trunkoplastie post-bariatrique ; 23833094 : cas isolé à 3 mois. Populations particulières, pas l'abdominoplastie standard.
- Recherche (pubmed) « abdominoplasty convalescence recovery weeks », 0 résultat(s).

## A-024
- Requête : combien de temps dure les injection d acide hyaluronique
- Quantité visée : durée de l'effet d'une injection d'acide hyaluronique (sans zone précisée)
- Passage S1 : « Hyaluronic acid gel 4 to 12 months »
- Passage S2 : « Deep injections may last as long as 12 months, and newer products on the market may last up to two years. »
- Recherche (aad) « https://www.aad.org/public/cosmetic/wrinkles/fillers-faqs », 1 résultat(s). Tableau vérifié dans le HTML servi.
- Recherche (society) « https://www.plasticsurgery.org/news/blog/how-long-do-dermal-fillers-last », 1 résultat(s). Phrases relevées par WebFetch ; l'article parle des fillers « typically hyaluronic acid ». Autre phrase : « will last for 6-12 months ». Revérifié mot pour mot dans le navigateur intégré (texte rendu) le 03/11/2026.

## A-025
- Requête : blepharoplastie combien de temps
- Quantité visée : durée des résultats d'une blépharoplastie (la durée de l'opération et la convalescence sont des lectures possibles, non ciblées)
- Recherche (pubmed) « blepharoplasty long-term results durability years », 2 résultat(s). Ptosis congénital ; suivi à 3 ans d'une technique de pli, sans durée des résultats.
- Recherche (pubmed) « upper blepharoplasty longevity of results », 12 résultat(s). Aucune durée de résultats chiffrée dans les résumés.
- Recherche (society) « eyelid surgery blepharoplasty how long do results last years », 9 résultat(s). Un chirurgien cité par l'ASPS : 10 à 15 ans avant une seconde intervention (source unique). NHS et ASPS : « many years », « long-lasting », sans chiffre.

## A-026
- Requête : combien de fois devrais-je utiliser mon ulike
- Quantité visée : fréquence d'utilisation d'un épilateur à lumière pulsée domestique (Ulike)
- Recherche (fda_label) « Ulike IPL hair removal 510(k) treatment schedule once a week (recherche web limitée à fda.gov, accessdata.fda.gov, aad.org, nhs.uk) », 10 résultat(s). Indications, modes et capteur cutané ; aucune fréquence d'utilisation. La FAQ de l'AAD (4 à 6 semaines) vise le laser en cabinet, pas l'appareil domestique.
- Recherche (pubmed) « home-use intense pulsed light hair removal », 33 résultat(s). Rythmes propres à chaque protocole d'étude (toutes les 2 à 4 semaines, hebdomadaire puis mensuel), pas de fréquence recommandée. Requête plus étroite « … treatment schedule weekly » : 0 résultat.

## A-027
- Requête : acide hyaluronique combien de fois par jour
- Quantité visée : nombre d'applications quotidiennes d'un soin topique à l'acide hyaluronique
- Recherche (pubmed) « topical hyaluronic acid serum application frequency twice daily », 0 résultat(s).
- Recherche (pubmed) « topical hyaluronic acid skin hydration twice daily randomized », 4 résultat(s). Fréquences fixées par le protocole de chaque essai, pas une recommandation.
- Recherche (aad) « hyaluronic acid serum how often to apply once or twice a day dermatologist (recherche web limitée à aad.org, nhs.uk, has-sante.fr, ansm.sante.fr, fda.gov) », 10 résultat(s). Conseils sur les crèmes hydratantes en général et sur le test d'un produit ; rien sur l'acide hyaluronique topique.

## A-028
- Requête : les cils repoussent en combien de temps
- Quantité visée : délai de repousse des cils après leur chute ou leur arrachage
- Passage S1 : « Eyelashes grow, fall out and replace themselves in a natural cycle every six to 10 weeks, just like the hair on top of your head. »
- Passage S2 : « Epilation can be performed, however, patients should be warned that eyelashes will grow back in 6-12 weeks. »
- Passage S3 : « Manual epilation is temporary because eyelashes normally grow back in 2-3 weeks. »
- Recherche (pubmed) « eyelash regrowth time after loss weeks », 3 résultat(s). Pelade sous inhibiteurs de JAK, hors sujet.
- Recherche (pubmed) « eyelash hair cycle anagen duration », 3 résultat(s). 19804590 : cycle complet de 90 ± 5 jours sur 4 volontaires.
- Recherche (society) « how long do eyelashes take to grow back », 10 résultat(s). Textes vérifiés dans le HTML servi. Madarosis : « up to 8-10 weeks to grow ».

## A-029
- Requête : acide salicylique combien de fois par jour
- Quantité visée : nombre d'applications quotidiennes d'un produit à l'acide salicylique
- Passage S1 : « cover the entire affected area with a thin layer one to three times daily [bullet] because excessive drying of the skin may occur, start with one application daily, then gradually increase to two or three times daily if needed or as directed by a doctor »
- Recherche (fda_label) « https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-21.xml?part=333&section=333.350 », 1 résultat(s). Texte lu dans la version du 01/10/2026. Vaut pour l'usage anti-acné, l'usage principal de l'acide salicylique topique.

## A-030
- Requête : au bout de combien de temps une cicatrice devient blanche
- Quantité visée : délai pour qu'une cicatrice s'estompe et blanchisse (maturation)
- Passage S1 : « You cannot get rid of a scar, but most will fade over time. This can take up to 2 years or more, but there are some things you can do to help it heal or improve how it looks. »
- Passage S2 : « Although scars are permanent, they can fade over a period of up to 2 years. »
- Recherche (other) « how long does it take for a scar to fade mature turn white months », 10 résultat(s). Textes vérifiés dans le HTML servi. La même fiche du CUH dit aussi « approximately 6 months until the scar has fully matured » à propos du massage. Les mentions « 12 to 18 months » du résumé de recherche n'ont pas été retrouvées dans une page vérifiée.

## A-031
- Requête : au bout de combien de temps peut on mettre une cicatrice au soleil
- Quantité visée : délai avant d'exposer une cicatrice au soleil sans protection (le SPF 30 est un nombre incident)
- Passage S1 : « try to keep your scar covered when you're in the sun for at least 1 year – wear clothing that covers it, or put a dressing over it »
- Recherche (other) « https://www.nhs.uk/conditions/scars/ », 1 résultat(s). Texte vérifié dans le HTML servi.

## A-032
- Requête : convalescence après opération trou maculaire
- Quantité visée : durée de convalescence (arrêt de travail) après une opération du trou maculaire ; la durée de la bulle de gaz et la récupération visuelle sont des lectures secondaires
- Passage S1 : « How much time off work will I need? Most people will need at least 2 to 4 weeks off work after surgery. »
- Passage S2 : « How much time will I need off work? Most people will need at least two weeks off work after surgery. »
- Recherche (other) « macular hole surgery recovery time how long off work face down weeks », 9 résultat(s). Textes vérifiés dans les PDF téléchargés. Les fiches hey et fhft ne donnent pas d'arrêt de travail chiffré.

## A-033
- Requête : quel délai entre 2 séances de cryolipolyse
- Quantité visée : intervalle entre deux séances de cryolipolyse
- Recherche (pubmed) « cryolipolysis interval between treatments weeks », 2 résultat(s). 28901051 : intervalle de 10 semaines fixé par le protocole.
- Recherche (pubmed) « cryolipolysis second treatment 8 weeks », 4 résultat(s). 28426847 : réévaluation à 6 semaines par protocole. Pas d'intervalle recommandé.
- Recherche (aad) « cryolipolysis how long to wait between sessions weeks (recherche web limitée à aad.org, plasticsurgery.org, has-sante.fr, nhs.uk, fda.gov) », 9 résultat(s). La page AAD donne « spaced 6 to 8 weeks apart » pour les injections sous le menton seulement, pas pour la cryolipolyse.

## A-034
- Requête : combien de seance pour detatouage
- Quantité visée : nombre de séances de laser nécessaires pour retirer un tatouage (l'intervalle entre séances est incident)
- Passage S1 : « For a good result most people need between 4 and 12 treatment sessions, approximately 12 weeks apart. »
- Passage S2 : « Generally, between 12 – 16 sessions are required but this could be up to 20 or even fewer sessions. »
- Recherche (other) « laser tattoo removal how many treatments sessions needed », 10 résultat(s). Textes vérifiés dans les PDF téléchargés. D'autres chiffres (FDA 6-10, Bristol 4-6 ou 10-12) apparaissent dans le résumé de recherche, non revérifiés.

## A-035
- Requête : combien de temps masser une cicatrice après opération
- Quantité visée : pendant combien de temps masser une cicatrice après une opération (la durée de chaque séance de massage, en minutes, est une lecture secondaire)
- Passage S1 : « Later on, you will probably not need to massage so often but it is best to continue twice daily for at least six months while the scar matures. »
- Passage S2 : « You should continue this for approximately 6 months until the scar has fully matured. »
- Recherche (other) « how long does it take for a scar to fade mature turn white months », 10 résultat(s). Textes vérifiés dans le PDF et le HTML servis. La fiche UHS ne donne pas de durée de massage.

## A-036
- Requête : laser fraxel combien de séance
- Quantité visée : nombre de séances de laser Fraxel (fractionné non ablatif)
- Recherche (other) « fractional laser resurfacing Fraxel how many treatments sessions », 10 résultat(s). Chiffres NHS pour le CO2 fractionné (1 à 3 séances pour l'acné, 3 à 6 pour les cicatrices, d'après le résumé de recherche, non revérifiés) ; K080915 : 1 à 3 séances pour des lésions pigmentées. Rien pour Fraxel en resurfaçage.
- Recherche (pubmed) « Fraxel 1550 nm fractional nonablative number of treatments », 1 résultat(s). Deux séances fixées par le protocole (1927 nm, pigmentation) : pas un nombre recommandé.

## A-037
- Requête : combien de temps sans soleil apres epilation laser
- Quantité visée : durée de protection contre le soleil après une épilation laser (le SPF 30 est un nombre incident)
- Passage S1 : « Please apply sunscreen with an SPF of at least 30 to the treatment areas daily while you are having treatment and for at least 6 weeks after your last treatment. »
- Recherche (aad) « https://www.aad.org/public/cosmetic/hair-removal/laser-hair-removal-faqs », 1 résultat(s). « Avoid direct sunlight from hitting your treated skin. » Sans durée.
- Recherche (other) « how long should hair be before waxing », 10 résultat(s). Texte SWBH vérifié dans le PDF. La page de Leeds ne sert pas de texte exploitable.

## A-038
- Requête : laser couperose combien de séance
- Quantité visée : nombre de séances de laser vasculaire pour la couperose (vaisseaux visibles du visage)
- Passage S1 : « When used to treat visible blood vessels, most patients see a 50% to 75% reduction in visible blood vessels after 1 to 3 treatments. Some people see a 100% reduction. »
- Recherche (aad) « laser treatment facial redness broken blood vessels rosacea how many treatments (recherche web limitée à aad.org, nhs.uk, plasticsurgery.org, has-sante.fr, nice.org.uk) », 10 résultat(s). Texte AAD vérifié dans le HTML servi. Le « 2-4 treatments » de Bristol n'apparaît pas dans la page servie.

## A-039
- Requête : chémosis durée
- Quantité visée : durée d'un chémosis (œdème de la conjonctive)
- Recherche (pubmed) « chemosis after blepharoplasty duration weeks », 0 résultat(s).
- Recherche (pubmed) « postoperative chemosis resolution time », 3 résultat(s). Durées propres à chaque contexte : chémosis léger après blépharoplastie inférieure résolu en 2 semaines (2,1 % des cas) ; chémosis sévère après fracture orbitaire, 3,5 à 7,2 jours selon la tarsorraphie.
- Recherche (other) « chemosis how long does it last », 10 résultat(s). Page EyeWiki sans contenu exploitable dans le HTML servi ; résultats web limités à des essais sur l'allergie.

## A-040
- Requête : combien de temps sans sport apres botox
- Quantité visée : délai avant de reprendre le sport après une injection de toxine botulique
- Passage S1 : « Wait two hours before you engage in strenuous physical activity. This includes lifting heavy items, working out, and any other physical activity that raises your heart rate. »
- Recherche (aad) « https://www.aad.org/public/cosmetic/wrinkles/botulinum-toxin-faqs », 1 résultat(s). Texte vérifié dans le HTML servi (lu au rang 17).

## A-041
- Requête : combien de temps après un détatouage peut-on se refaire tatouer sur la même zone
- Quantité visée : délai avant de se refaire tatouer sur une zone détatouée au laser (l'intervalle entre séances de détatouage est incident)
- Recherche (other) « after laser tattoo removal how long wait before getting new tattoo same area », 10 résultat(s). Intervalles entre séances et délais de cicatrisation seulement ; une citation de dermatologue (« wait about six months ») ne vise pas un nouveau tatouage.
- Recherche (pubmed) « re-tattooing after laser tattoo removal », 0 résultat(s).

## A-042
- Requête : combien de temps apres epilation laser les poils tombent
- Quantité visée : délai de chute des poils après une séance d'épilation laser
- Passage S1 : « Do not be tempted to remove these, they will fall out naturally after 5 7 days. »
- Passage S2 : « Some hairs will remain in the follicles but will naturally fall out within 2 – 3 weeks. »
- Recherche (pubmed) « laser hair removal hair shedding after treatment days », 0 résultat(s).
- Recherche (pubmed) « laser hair removal hairs fall out weeks after treatment », 0 résultat(s).
- Recherche (other) « after laser hair removal when do the hairs fall out shed days weeks », 9 résultat(s). Textes vérifiés dans les PDF. La version 2023 de la fiche de Birmingham a retiré le délai (« will naturally fall out with time »).

## A-043
- Requête : bouton sous-cutané durée
- Quantité visée : durée d'un bouton sous-cutané (bouton profond, sans tête) laissé sans traitement
- Recherche (pubmed) « acne nodule inflammatory lesion natural history duration days », 0 résultat(s).
- Recherche (aad) « blind pimple cystic acne lesion how long does it last to go away (recherche web limitée à aad.org, nhs.uk, has-sante.fr, nice.org.uk) », 10 résultat(s). AAD : une injection de cortisone fait disparaître le bouton « in a few hours to days instead of days to weeks » (pas de chiffre pour l'évolution spontanée). West Yorkshire Healthier Together : 1 à 2 semaines pour les boutons d'acné en général, non revérifié dans la page.

## A-044
- Requête : lipofilling visage durée de vie
- Quantité visée : durée des résultats d'un lipofilling du visage (le pourcentage de graisse qui survit est incident)
- Passage S1 : « Fat taken from your body 1 to 3 years (often longer when treating a scar) »
- Passage S2 : « About 50% of the fat injected will survive, and the surviving fat will last forever. »
- Recherche (aad) « https://www.aad.org/public/cosmetic/wrinkles/fillers-faqs », 1 résultat(s). Tableau vérifié dans le HTML servi (lu au rang 12).
- Recherche (society) « https://www.plasticsurgery.org/cosmetic-procedures/dermal-fillers/fat-injections », 1 résultat(s). Phrases relevées par WebFetch (page rendue côté client). Borne haute ouverte : « last forever ». Revérifié mot pour mot dans le navigateur intégré (texte rendu) le 03/11/2026.

## A-045
- Requête : blépharoplastie convalescence
- Quantité visée : durée de convalescence (arrêt de travail) après une blépharoplastie ; la durée des ecchymoses et des cicatrices est incidente
- Passage S1 : « Most people take about 2 weeks off work to recover from eyelid surgery, depending on their job. »
- Recherche (other) « https://www.nhs.uk/conditions/cosmetic-procedures/cosmetic-surgery/eyelid-surgery/ (redirigée vers /tests-and-treatments/…) », 1 résultat(s). Texte vérifié dans le HTML servi. « About 2 weeks » : la plage est réduite à 2 semaines, le « environ » est consigné ici.
- Recherche (other) « https://www.imperial.nhs.uk/-/media/website/patient-information-leaflets/ophthalmology/blepharoplasty.pdf », 1 résultat(s). PDF non extractible (texte vide).

## A-046
- Requête : combien de temps pour se remettre d'un lipofilling
- Quantité visée : délai pour se remettre d'un lipofilling du visage (reprise des activités)
- Recherche (other) « facial fat transfer fat grafting recovery time swelling weeks », 10 résultat(s). NHS (revue le 19/10/2023) : « You may want to take a couple of weeks off work. » CUH (lipomodelage du sein) : « you should be back at work within a few days ». Approximations verbales, contextes différents du visage. Règle appliquée : pas de nombre, pas de [étiquette masquée] ni de [étiquette masquée].
- Recherche (pubmed) « facial fat grafting recovery downtime days », 1 résultat(s). Lifting associé au resurfaçage plasma ; pas de durée de récupération du lipofilling.

## A-047
- Requête : injection menton durée
- Quantité visée : durée de l'effet d'une injection d'acide hyaluronique dans le menton
- Passage S1 : « While individual results may vary, in the chin augmentation clinical study, the results lasted up to 1 year in a majority of subjects (58%) treated with JUVÉDERM® VOLUMA™ XC. »
- Passage S2 : « The GAIS responder rate was 100% through Month 12 and 84.21% at Month 18. »
- Recherche (pubmed) « hyaluronic acid chin augmentation duration months randomized », 0 résultat(s).
- Recherche (pubmed) « chin augmentation hyaluronic acid filler », 67 résultat(s). 10 premiers examinés. 42545491 (revue systématique) : suivi moyen de 12,8 mois, pas de durée d'effet. S2 porte sur le nez et le menton ensemble : à signaler.
- Recherche (fda_label) « FDA approved chin augmentation hyaluronic acid filler lasts up to year (recherche web limitée à fda.gov, accessdata.fda.gov, plasticsurgery.org, aad.org) », 9 résultat(s). Texte du Voluma vérifié dans le PDF téléchargé.

## A-048
- Requête : hyaluronidase gonflement combien de temps
- Quantité visée : durée du gonflement après une injection d'hyaluronidase (dissolution d'acide hyaluronique)
- Recherche (pubmed) « hyaluronidase injection swelling duration after filler dissolution », 0 résultat(s).
- Recherche (pubmed) « hyaluronidase adverse effects swelling resolve days », 4 résultat(s). Cas de cécité, allergie à l'hyaluronidase, traitement de l'œdème palpébral, inflammation orbitaire : aucune durée de gonflement attendu.
- Recherche (society) « hyaluronidase injection swelling after dissolving filler how long », 9 résultat(s). ASPS : mettre de la glace « the first one to two days » ; consigne de soins, pas une durée de gonflement.

## A-049
- Requête : combien de temps les vergetures restent rouges
- Quantité visée : durée pendant laquelle les vergetures restent rouges avant de blanchir
- Recherche (pubmed) « striae rubrae duration months fade », 0 résultat(s).
- Recherche (pubmed) « stretch marks red to white time », 0 résultat(s).
- Recherche (other) « stretch marks red purple fade silvery white how long months », 10 résultat(s). « Fade over time », « as they mature they lighten » : pas de durée chiffrée.

## A-050
- Requête : combien de temps pour se maquiller apres operation cataracte
- Quantité visée : délai avant de se maquiller les yeux après une opération de la cataracte
- Passage S1 : « Answer: Please ask your ophthalmologist, but in general, 1-2 weeks. »
- Passage S2 : « It’s recommended that you avoid wearing eye makeup after cataract surgery for around four weeks. »
- Passage S3 : « You can swim and use eye make-up when you have finished your eye drops, 4 weeks after your surgery. »
- Recherche (other) « cataract surgery how long avoid eye make-up after operation », 10 résultat(s). Textes vérifiés dans le HTML servi. La page NHS nationale (revue le 06/03/2025) ne donne plus de durée ; le « at least 4 weeks » du résumé de recherche n'y figure pas.

## A-051
- Requête : blépharoplastie œdème combien de temps
- Quantité visée : durée de l'œdème des paupières après une blépharoplastie
- Recherche (society) « https://www.plasticsurgery.org/cosmetic-procedures/eyelid-surgery/recovery », 1 résultat(s). Aucune durée.
- Recherche (other) « https://www.nhs.uk/tests-and-treatments/cosmetic-procedures/cosmetic-surgery/eyelid-surgery/ », 1 résultat(s). « Bruises and redness may take several weeks to fade » : approximation verbale (règle 6).
- Recherche (pubmed) « blepharoplasty postoperative edema duration weeks », 3 résultat(s). 24796200 : 5 jours à 3 semaines après pose d'espaceurs palpébraux (chirurgie reconstructrice). 41137243 (vu au rang 84) : gonflement transitoire résolu en 8 semaines après blépharoplastie inférieure transconjonctivale, source unique.

## A-052
- Requête : combien de temps garder la gaine apres abdominoplastie
- Quantité visée : durée de port de la gaine de compression après une abdominoplastie
- Passage S1 : « After surgery, you will be placed in a compression garment, which will be worn for 4-6 weeks after surgery to help with reducing swelling. »
- Passage S2 : « Your compression garment should be worn day and night (with the exception of showering or bathing) for anywhere between one to three weeks. »
- Recherche (society) « tummy tuck compression garment how long to wear weeks », 10 résultat(s). Fragments relevés par WebFetch (pages rendues côté client, citations limitées à 125 caractères). Troisième article : « a minimum of six weeks » (un chirurgien) et « there are no firm guidelines for how long you'll be wearing each garment ». Revérifié mot pour mot dans le navigateur intégré (texte rendu) le 03/11/2026.

## A-053
- Requête : combien de temps dure une hyménoplastie
- Quantité visée : durée du résultat d'une hyménoplastie (la durée de l'intervention est une lecture possible, non ciblée)
- Recherche (pubmed) « hymenoplasty », 73 résultat(s). 10 premiers examinés : éthique, sociologie, chirurgie génitale esthétique en général, un cas pédiatrique. Aucune durée.
- Recherche (pubmed) « hymenoplasty duration recovery », 0 résultat(s).
- Recherche (other) « hyménoplastie durée résultat combien de temps », 9 résultat(s). Aucune durée. Au Royaume-Uni, le Health and Care Act 2022 interdit l'hyménoplastie (selon le résumé de recherche, non revérifié).

## A-054
- Requête : combien de temps pele t on apres un peeling
- Quantité visée : durée de la desquamation après un peeling chimique superficiel ou moyen (profondeur non précisée)
- Passage S1 : « Healing time: 1 to 7 days. Skin will be red. After the redness disappears, scaling may develop, which lasts 3 to 7 days. »
- Passage S1 : « Healing time: 7 to 14 days. Skin will be red and swollen. Swelling worsens for 48 hours. Eyelids may swell. Blisters can form and break open. Skin crusts and peels off in 7 to 14 days. »
- Recherche (aad) « https://www.aad.org/public/cosmetic/younger-looking/chemical-peels-faqs », 1 résultat(s). Tableau revérifié dans le navigateur le 03/11/2026 : lignes « Refreshing or lunchtime peel » (desquamation 3 à 7 jours) et « Medium peel » (7 à 14 jours). Le peeling profond (« Healing time: 14 to 21 days. Area will be bandaged. ») donne une cicatrisation sous pansement, pas une desquamation : retiré de la plage, qui passe de 3-21 à 3-14 jours.

## A-055
- Requête : cicatrice combien de temps sans piscine
- Quantité visée : délai avant de se baigner en piscine avec une cicatrice récente après une opération
- Passage S1 : « Swimming should be avoided for the first 7 days. »
- Passage S2 : « You need to avoid swimming, sports/exercise, heavy lifting and heavy manual labour for a minimum of two weeks, or until the wound is fully healed. »
- Recherche (other) « how long after surgery stitches can I go swimming wound », 10 résultat(s). Textes vérifiés dans le HTML et les PDF servis. Contextes différents (plaie collée chez l'enfant ; points résorbables chez l'adulte) : à signaler. Northern Care Alliance et Royal Berkshire : pas de chiffre.

## A-056
- Requête : combien de temps dure une seance de cryolipolyse
- Quantité visée : durée d'une séance de cryolipolyse (une heure = 60 minutes)
- Passage S1 : « After the hour-long treatment, the vacuum turns off, the applicator is removed and the area is massaged, which may improve the final results. »
- Recherche (society) « https://www.plasticsurgery.org/cosmetic-procedures/nonsurgical-fat-reduction/cryolipolysis », 1 résultat(s). Fragment relevé par WebFetch au rang 11 (page rendue côté client). Une séance peut enchaîner plusieurs cycles d'applicateur : la durée vaut pour un traitement d'une zone. Revérifié mot pour mot dans le navigateur intégré (texte rendu) le 03/11/2026.

## A-057
- Requête : combien de temps laisser un gommage sur le visage
- Quantité visée : durée d'application d'un gommage sur le visage
- Passage S1 : « If you use a scrub or chemical exfoliator, apply the product gently using small, circular motions. Do this for about 30 seconds and then rinse well with lukewarm — not hot — water. »
- Recherche (pubmed) « facial scrub exfoliation contact time minutes », 0 résultat(s).
- Recherche (aad) « https://www.aad.org/public/everyday-care/skin-care-secrets/routine/safely-exfoliate-at-home », 1 résultat(s). Texte vérifié dans le HTML servi. « About 30 seconds » : plage réduite à 30 secondes, le « environ » est consigné ici.

## A-058
- Requête : combien de temps dure un œil au beurre noir
- Quantité visée : durée d'un œil au beurre noir (ecchymose périorbitaire)
- Passage S1 : « A black eye is bruising and swelling around your eye, usually caused by a blow to the area, such as a punch or fall. It should get better within 2 to 3 weeks. »
- Recherche (other) « https://www.nhs.uk/conditions/black-eye/ », 1 résultat(s). Texte vérifié dans le HTML servi.

## A-059
- Requête : combien de temps pour qu'un bleu disparaisse
- Quantité visée : délai de disparition d'un bleu (ecchymose)
- Passage S1 : « Most bruises settle after a couple of weeks. Seek medical attention if the bruise has not gone after 3 weeks. »
- Recherche (other) « how long does a bruise take to fade disappear weeks », 10 résultat(s). Texte NHS vérifié dans le HTML servi. « A couple of weeks » est verbal (règle 6) ; la borne chiffrée retenue est le seuil de 3 semaines. La fiche du centre médical Priory ne sert pas de texte exploitable.

## A-060
- Requête : combien de temps laisser pousser les poils avant épilation laser
- Quantité visée : délai entre le dernier rasage et une séance d'épilation laser (les 8 semaines sans cire ni pince sont une lecture concurrente, non ciblée)
- Passage S1 : « If you choose to shave or trim please do so 24 hours before your treatment. »
- Passage S2 : « Shaving up to 1-2 days before treatment is acceptable. »
- Recherche (other) « after laser hair removal when do the hairs fall out shed days weeks », 9 résultat(s). Textes vérifiés dans les PDF téléchargés. Leeds dit aussi : « Plucking, waxing and bleaching should be avoided in the eight weeks before your treatment course commences. » La lecture retenue est consignée dans le motif du journal de parcours.
