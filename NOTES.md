# NOTES — journal d'exécution

Chaque affirmation de ce fichier renvoie à la commande qui l'établit. Aucune valeur de clé n'est jamais affichée ni écrite ici.

## Étape 0 — Clés API et conditions (02/11/2026)

### 0.1 Clés API : état réel

**Périmètre de la recherche** : environnement du shell, fichiers de démarrage du shell, trousseau de session, `.env*` sous `~` jusqu'à la profondeur 4 (hors `Library`, `node_modules`, `.venv`, `.Trash`), plus `~/.hermes`, `~/.claude` et `~/.config`. **Hors périmètre** : `/Volumes/Mac-Archive`, où vit tout ce qui n'est pas Acuence, et le VPS. « Absente » se lit donc « aucune clé trouvée dans ce périmètre ».

| Fournisseur | État | Commande qui l'établit |
|---|---|---|
| Anthropic (API) | **Absente** | `printenv ANTHROPIC_API_KEY` vide ; aucun `ANTHROPIC_API_KEY=` dans `~/.zshrc`, `~/.zprofile`, `~/.zshenv`, `~/.bashrc`, `~/.bash_profile`, `~/.profile` (`grep -nE`) ; aucun fichier `.env*` de `~` (profondeur 4, hors `Library`, `node_modules`, `.venv`) ne contient de valeur réelle (`find … \| grep -cE`) |
| OpenAI (API) | **Absente** | `printenv OPENAI_API_KEY` vide ; `~/.codex/auth.json` : champ `OPENAI_API_KEY` vide, Codex est authentifié par `tokens` ChatGPT (lu avec `python3 -I -c 'json.load…'`, clés seules) |
| Google / Gemini (API) | **Absente** | `printenv GEMINI_API_KEY GOOGLE_API_KEY` vides ; l'entrée de trousseau `svce=gemini` a `acct=antigravity`, probablement la connexion de l'outil Antigravity (hypothèse, voir § 0.4) (`security find-generic-password -s gemini`, attributs seuls, sans `-w`) |
| Mistral, xAI, OpenRouter, Together, DeepSeek, MiniMax | **Absentes** de l'environnement | boucle `printenv` sur ces noms |

Faux positifs écartés :
- `~/Projects/jarvis-OS/.env.example` et `~/nuance-paris/api/.env.example` : **gabarits**. Les valeurs ont des longueurs de 10, 11 et 22 caractères, avec des préfixes de gabarit (`sk-ant`, `your_a`). Une vraie clé est bien plus longue. Contrôle de forme seulement, sans affichage.
- `~/.zshrc` l. 65-70 : la fonction `claude-alibaba` exporte `ANTHROPIC_AUTH_TOKEN` vers un point d'accès Alibaba/Qwen. Ce n'est pas une clé Anthropic.
- Trousseau : `Claude Code-credentials*` (12 entrées) = connexions d'abonnement de Claude Code, OAuth. Elles sont **exclues** pour la mesure (§ 4 de la SPEC et conditions ci-dessous). `com.anthropic.operon-cli` : non lu, sans objet ici.
- Variables présentes mais hors sujet : `ALIBABA_QWEN_TOKEN`, `CLAUDE_CODE_MESSAGING_TOKEN` (`env | cut -d= -f1 | grep -Ei 'key|token|secret'`).

**Conséquence.** Aucun appel minimal n'a été fait, et aucun n'était possible. Les crédits ne sont pas vérifiables sans clé ni accès aux consoles. Il faut que Guillaume :
1. crée une clé API Anthropic sur console.anthropic.com et une clé API OpenAI sur platform.openai.com, et approvisionne les crédits ;
2. les place dans `.env` à la racine du dépôt (ignoré par git, voir `.gitignore`), sur le modèle de `.env.example` ;
3. autorise ensuite explicitement **un** appel minimal par fournisseur, qui sera consigné ici (commande, chaîne de modèle renvoyée, nombre de tokens).

La seconde famille de modèles peut aussi être Google : le minimum demande au moins deux familles (§ 3).

### 0.2 Sources primaires relues

**anthropic.com/candidate-ai-guidance** — lue le 02/11/2026 via WebFetch. Page « Last updated Jul 10, 2025 ».
- Formulaire et réponses écrites : premier jet écrit par le candidat, puis Claude peut affiner. Interdit : faire écrire les réponses par Claude, inventer des expériences.
- Épreuves à la maison et « work samples » : **sans Claude, sauf autorisation explicite d'Anthropic pour la tâche**. Interdit : faire écrire son code par Claude sans permission explicite.
- Entretiens en direct : aucune aide d'IA sauf indication contraire.
- Attente générale : être transparent sur son usage de l'IA. « Use AI to refine your ideas, not replace them. »
- La page **ne mentionne ni la Residency, ni les programmes de recherche, ni les projets de portfolio**.

> **Écart avec la SPEC § 11.** La SPEC dit « le code peut être construit avec Claude Code ». La page ne dit pas cela : elle ne traite pas les projets personnels publiés. Elle interdit le code écrit par Claude **pour les épreuves et work samples**, sauf autorisation. Ce dépôt n'est pas une épreuve demandée par Anthropic, mais il sera joint à la candidature comme preuve de travail. À trancher par Guillaume avant le 20/11, dans cet ordre : (1) le README déclare précisément ce que Claude Code a écrit et ce que Guillaume a écrit ; (2) Guillaume peut expliquer chaque ligne ; (3) en cas de doute, poser la question au recrutement plutôt que de supposer.

**Conditions grand public d'Anthropic** (anthropic.com/legal/consumer-terms) — lues le 02/11/2026, en vigueur au 8 octobre 2025. Section 3, point 7 : interdiction d'accéder aux Services « through automated or non-human means, whether through a bot, script, or otherwise », sauf « when you are accessing our Services via an Anthropic API Key ». Donc : pas de mesure scriptée par l'abonnement (ni `claude -p`, ni connexion OAuth de Claude Code). La décision du § 4 de la SPEC est confirmée. L'usage par clé API relève des Commercial Terms, non relues ici.

**Conditions d'OpenAI** (openai.com/policies/row-terms-of-use, version pour hors États-Unis) — lues le 02/11/2026 dans le navigateur intégré (la page renvoie 403 à `curl` et WebFetch). En vigueur au 1er janvier 2026. Section « What you cannot do » :
- interdiction d'« Automatically or programmatically extract data or Output » ;
- interdiction de présenter une sortie comme humaine ;
- interdiction d'utiliser les sorties pour développer des modèles concurrents.

La page renvoie aux **Business Terms** pour les API. Donc : la mesure passe par l'API OpenAI, jamais par ChatGPT ni par la connexion ChatGPT de Codex. Les sorties publiées dans `logs/` sont étiquetées comme sorties de modèle, objets d'étude, ce qui respecte la clause « human-generated ». Les Business Terms ne sont pas relues ici.

### 0.3 Conditions des API (qui gouvernent les runs et la publication des journaux)

**Anthropic Commercial Terms** (anthropic.com/legal/commercial-terms) — lues le 02/11/2026 via WebFetch, en vigueur au 17 juin 2025.
- Section B : le client « owns its Outputs ».
- Section D.4 : interdiction d'utiliser les Services pour construire un produit concurrent, « including to train competing AI models ».
- Aucune clause ne vise expressément la publication de sorties ou de résultats d'évaluation. Le dépôt ne fait qu'évaluer, sans entraîner aucun modèle.

**OpenAI Services Agreement** (openai.com/policies/business-terms, redirigée vers /services-agreement) — lu le 02/11/2026 dans le navigateur intégré, « Updated: December 1, 2025 ».
- § 4.1 : le client « owns all Output ».
- § 3.3 (e) : interdiction d'utiliser les sorties pour développer des modèles concurrents.
- § 3.3 (f) : interdiction d'extraire des données autrement que par les Services.
- Le mot « benchmark » n'apparaît pas dans la page (recherche `indexOf('benchmark')` → absent).

Lecture : publier des journaux d'évaluation obtenus par API n'est interdit par aucune des deux clauses lues. Ce n'est pas un avis juridique.

### 0.4 Hypothèses corrigées par mesure

- Codex : `auth_mode = chatgpt`, `tokens` = `access_token, account_id, id_token, refresh_token` (lu avec `python3 -I`, clés seules). C'est confirmé : connexion ChatGPT, pas de clé API.
- Entrée de trousseau `gemini` / `antigravity` : **hypothèse**. Le nom du compte laisse penser à la connexion de l'outil Antigravity, mais la valeur n'a pas été lue et ne le sera pas. Dans tous les cas, ce n'est pas une variable `GEMINI_API_KEY` utilisable par Inspect.

## Étape 1 — Squelette et fournisseur factice (02/11/2026)

- `git init -b main` : dépôt **local seulement**, aucun remote, aucun push, aucune création GitHub.
- `.venv` créé avec `/opt/homebrew/bin/python3.12` → `Python 3.12.13`. Le `python3` du shell est 3.10, alors qu'inspect-ai demande `>=3.11` (champ `requires_python` de PyPI).
- Dernière release d'inspect-ai :
  - `gh api repos/UKGovernmentBEIS/inspect_ai/releases/latest` → tag `0.3.287`, publié le 2026-10-31T16:33:20Z ;
  - PyPI : `0.3.287`, téléversé le 2026-10-31T16:34:37.
- Figé : `requirements.txt` (`inspect-ai==0.3.287`, `jsonschema==4.26.0`) et `requirements.lock` (`pip freeze`, 80 lignes).
- **Le fournisseur factice existe.** Il est fourni par Inspect, nul besoin d'en écrire un :
  - déclaration : `inspect_ai/model/_providers/providers.py:301`, `@modelapi(name="mockllm")` ;
  - classe `MockLLM` dans `mockllm.py`, qui renvoie toujours `"Default output from mockllm/model"` sauf `custom_outputs`.
- **Piège du `.env`.** Inspect charge le premier `.env` trouvé en remontant depuis le dossier courant (`inspect_ai/_util/dotenv.py`, `find_dotenv(usecwd=True)` puis `load_dotenv`). Aujourd'hui, aucun `.env` n'existe du dépôt jusqu'à `/Users` (boucle `[ -e "$d/.env" ]`). Quand les clés seront dans `.env`, une commande sans `--model` explicite pourrait viser un vrai modèle. D'où `scripts/smoke.sh`, qui fige `--model mockllm/model`, et la consigne dans `.env.example` : pas de `INSPECT_EVAL_MODEL`.
- **Journaux.** `scripts/smoke.sh` écrit dans `smoke_logs/`, ignoré par git, **jamais dans `logs/`**. Contrôle : `ls logs` → « No such file or directory ». Le contrôle du § 12 (PREREG commité avant tout fichier de `logs/`) reste donc intact.

**Critère de l'étape 1 tenu.** Commande : `env -u ANTHROPIC_API_KEY -u OPENAI_API_KEY scripts/smoke.sh`, qui a pris 6 s. Lu ensuite avec `inspect_ai.log.read_eval_log` :
- `status: success` ;
- `eval.model: mockllm/model` ;
- `packages: {'inspect_ai': '0.3.287'}` ;
- 2 échantillons, `placeholder-1` et `placeholder-2`. Pour chacun, `output.model = mockllm`, complétion `Default output from mockllm/model`, score `C` ;
- `model_usage` ne contient que `mockllm/model`, avec 10 tokens en entrée et 66 en sortie, comptés par le fournisseur factice.

Les deux échantillons sont des marqueurs, `PLACEHOLDER 1` et `PLACEHOLDER 2`, sans aucun contenu clinique.

## Étape 3 — Littérature

Voir `RELATED.md` : niveaux de lecture, commandes, et conséquences pour la revendication. Constat principal : Kadavath et al. 2022, § 5.5, contient déjà un témoin croisé entre deux modèles, lu en texte intégral. Le témoin « soi contre autre » de Q2 n'est donc pas nouveau dans son principe.

## Étape 4 — Outils prêts, sans contenu (02/11/2026)

Fichiers :
- `schema/stratum_a.schema.json` (JSON Schema 2020-12) ;
- `scripts/validate_stratum_a.py` ;
- `tests/test_validate_stratum_a.py` et la fixture synthétique `tests/fixtures/stratum_a_valid.jsonl`, sans contenu clinique (unités `placeholder_unit`, PMID `0000000x`) ;
- `templates/search_log.md` ;
- squelettes `ANNOTATION.md` et `PREREG.md`, ce dernier marqué « SQUELETTE, NON PRÉ-INSCRIT » ;
- `data/README.md`.

`data/stratum_a.jsonl` **n'existe pas** : aucune question n'a été rédigée.

Vérification :
- `.venv/bin/python -m unittest discover -s tests -v` → `Ran 19 tests … OK`. Il y a 17 cas de rejet, chacun cassant une seule règle, plus 2 cas sur la fixture valide. Le 17e a été ajouté après relecture : des passages `CONTESTED` qui viennent tous de la même source.
- Le message d'erreur « question en double » ne donne que les ids, jamais le texte de la question. Un modèle évalué ne doit pas voir les questions (§ 4).
- `scripts/validate_stratum_a.py tests/fixtures/stratum_a_valid.jsonl` → 3/3 lignes valides, 0 erreur, 1 avertissement (plan apparié incomplet pour la procédure `CONTESTED` seule), code de sortie 0.

Points que la SPEC ne tranche pas. Le code ne les tranche pas non plus, ils sont listés dans `PREREG.md` et `ANNOTATION.md` :
1. Place des questions `CONTESTED` dans le plan apparié. Le validateur ne signale l'absence de paire `SOURCED`/`NOT_FOUND` qu'en avertissement, sauf avec `--require-pairs`.
2. `passage` pour `NOT_FOUND`. Il est autorisé et donne un avertissement : une phrase qui atteste une absence est-elle un passage ?
3. Choix de modélisation fait ici et révisable : `passage` est une **liste** de `{source_ref, text, location}`. Une question `CONTESTED` exige au moins deux passages de sources distinctes, ce qu'une chaîne unique ne pouvait pas porter.
4. Règle `SOURCED` codée d'après le § 5.2 : une source de type `guideline`, ou au moins 2 sources avec un passage chacune. La **concordance** des valeurs n'est pas vérifiable par script : elle reste au jugement de l'auteur et de la clinicienne.

## Points à signaler avant le premier push

- **Nom de la clinicienne.** `SPEC.md` la nomme, et il est commité. Le § 5.3 n'autorise son nom qu'après accord écrit (étape 2, pas faite). `ANNOTATION.md` a été anonymisé. `SPEC.md` n'a pas été modifié, c'est la source de vérité de Guillaume. Avant tout push : retirer le nom de `SPEC.md` **et de l'historique**, ou obtenir l'accord écrit.
- **candidate-ai-guidance contre SPEC § 11.** Voir § 0.2. À trancher par Guillaume.

## Budget API — estimation du 03/11/2026

Commande : `python3 scripts/budget.py`. Tarifs relevés le jour même sur platform.claude.com/docs/en/about-claude/pricing et developers.openai.com/api/docs/pricing.

| Modèle | $/MTok entrée / sortie | Q1 (test + dev) | Q2 (sondes) | Total |
|---|---|---|---|---|
| claude-opus-5-5 | 4 / 20 | 19,97 $ | 66,96 $ | 86,93 $ |
| claude-sonnet-5-5 | 2 / 10 | 9,98 $ | 33,48 $ | 43,46 $ |
| gpt-6-astra | 10 / 50 | 49,92 $ | 167,40 $ | 217,32 $ |

- Trois modèles, Q1 + Q2, une passe : 348 $. Avec une marge x2 pour les relances : 695 $. En Batch API (-50 % chez les deux fournisseurs) : 174 $, ou 348 $ avec la marge.
- Hypothèses pessimistes : 2 000 tokens de sortie par réponse (raisonnement compris, facturé en sortie), 3 chiffres par réponse et 3 témoins par chiffre pour Q2.
- Le minimum livrable (Q1 seule, trois modèles) coûte environ 80 $.
- Non vérifié : le solde réel de chaque compte API, et si les 250 $ des abonnements Max sont utilisables avec une clé API de la Console.

### Mise à jour du 03/11 : aucun compte API OpenAI ni Google

Guillaume n'a de crédits API que chez Anthropic. Budget avec Claude seul (`python3 scripts/budget.py claude-opus-5-5 claude-sonnet-5-5 claude-haiku-5-5`) : 133 $ en une passe, 265 $ avec la marge x2, 66 $ en Batch API. Conséquence : le § 3.2 de SPEC.md (« au moins deux familles ») ne tient plus tel quel. Décision à prendre par Guillaume.

### Décision du 03/11 : Claude seul

- Périmètre arrêté par Guillaume : Claude seul. SPEC.md § 3, point 2, mis à jour.
- Crédits relevés par Guillaume dans la Console (copie collée, 03/11) : 0 $ achetés, 1 500 $ promotionnels. 500 $ valables jusqu'au 11/11/2026 (API, Batch, Playground, Agent SDK) ; 1 000 $ valables jusqu'au 06/04/2027 (tous produits).
- Les 500 $ expirent le jour des runs de test : on ne compte que sur les 1 000 $, qui couvrent le budget Claude seul (265 $ avec la marge x2).
- Aucun moyen de paiement enregistré : une fois les crédits épuisés, l'API refuse les appels au lieu de facturer. C'est un plafond de fait.

## Étape 0 : premier appel réel (03/11/2026, accord explicite de Guillaume)

- Commande : `.venv/bin/inspect eval evals/smoke.py --model anthropic/claude-haiku-5-5 --limit 1 --max-tokens 16 --log-dir smoke_logs --display plain`
- Entrée : la question factice `PLACEHOLDER 1`, aucune question de l'étude.
- Journal : `smoke_logs/2026-11-02T23-21-43-00-00_smoke_o2mEdfiQH7eUKwjvonLswM.eval` (ignoré par git, hors `logs/`).
- Résultat : clé acceptée. Chaîne de modèle renvoyée : `claude-haiku-5-5`. Usage : 19 tokens en entrée, 16 en sortie, dont 16 de raisonnement. Coût : environ 0,00001 $.
- Dépendance ajoutée : `anthropic==2.4.0` (Inspect 0.3.287 exige au moins 2.0.0), épinglée dans `requirements.txt` et `requirements.lock`.

**Conséquence pour le protocole.** Les 16 tokens sont tous partis en raisonnement : texte visible vide, arrêt sur `max_tokens`. Sur les modèles Claude actuels, le raisonnement ne peut pas être désactivé sur Opus 5.5 et il est facturé en sortie. À fixer dans PREREG v1 :
- `max_tokens` assez grand pour couvrir raisonnement et réponse, identique pour les trois modèles ;
- niveau d'effort explicite et consigné (défaut `medium` sur Opus 5.5 et Haiku 5.5, `high` sur Sonnet 5.5) ;
- taux de troncature rapporté par modèle, comme prévu au § 7 de SPEC.md.

## Rédaction des questions : piste « vraies questions publiques » (03/11)

- Guillaume demande que Claude s'occupe des questions. Une rédaction libre par Claude biaiserait l'étude, puisque les modèles évalués sont des Claude.
- Piste testée : HealthSearchQA (Singhal et al., jeu `katielink/healthsearchqa` sur Hugging Face, licence « unknown » sur la fiche). 4 436 questions, 184 en dermatologie, **4 seulement** demandent une quantité (filtre par mots-clés). Insuffisant pour 60 questions.
- Piste proposée : questions produites par une règle, pas rédigées. Gabarits = tournures réelles attestées dans HealthSearchQA (« How long does X last? », « How many … »), remplis par une liste publiée d'actes esthétiques et dermatologiques (source à vérifier), avec un tirage à graine fixe. En attente de l'accord de Guillaume.

### Génération par gabarits : essai du 03/11 au soir, arrêté avant le code

- Liste d'actes : glossaire du rapport ASPS 2025 (https://www.plasticsurgery.org/documents/news/statistics/2025/plastic-surgery-statistics-report-2025.pdf, sha256 4e33dc69a1769b2787422fa90dd65589fcd6490b7d58ebf7f6fc6881ccc095cc, pages 41-46). 71 entrées ; une fois retirés la reconstruction et les termes qui ne sont pas des actes, il reste environ 25 actes esthétiques (17 chirurgicaux, 8 peu invasifs).
- Tournures de HealthSearchQA (all.csv, sha256 037dd1b3c227ec5ee8385227d6439742653cdb37f0421e9757ca446ff6cada90) : seules deux formes de quantité s'appliquent telles quelles à un acte, « How long does X last? » (ids 804, 817, 836) et « How long does X take to heal? » (ids 810, 814). « How many sessions », « to work » ou « go back to work » n'y figurent pas : les utiliser serait de la rédaction.
- **Blocage.** Deux gabarits génériques sur 25 actes donnent au plus une cinquantaine de questions, et ce sont des questions générales (« How long does a facelift last? »). Les sociétés savantes publient précisément ces chiffres : on attend surtout des `SOURCED`, très peu de `NOT_FOUND`. Le plan apparié (une `SOURCED` et une `NOT_FOUND` par acte) ne tient pas. Les `NOT_FOUND` demandent des questions précises, donc de la rédaction ou de vraies requêtes de longue traîne.
- Décision demandée à Guillaume.

## Source retenue : vraies requêtes Search Console (03/11, choix de Guillaume)

- Extraction : `gsc_client.get_top_queries(site, days=480, limit=25000)` via `~/.hermes/scripts/seo`, lecture seule, pour trois sites médicaux français, ni nommés ni décrits (décisions du 03/11) : sites A, B et C. 25 000 requêtes par site (plafond de l'API).
- Instantané figé dans `data/private/` (ignoré par git, données des sites clients ; la correspondance est dans `data/private/MAPPING.md`) :
  - site_a.json sha256 10907b276a7c67a9ed72eac05942721ad531b20fef90772b62b30df0d4336ba9
  - site_b.json sha256 3e269eb1a059c26e876757b181d436bc680b81a9933f6aeca52dc3466031e51f
  - site_c.json sha256 16bb0f32ca21bd61641c83d92f723505254b5f16e967cdd0985e1978e7a03ed0
- Requêtes demandant une durée, un délai ou un nombre, prix exclus (filtre par expression régulière, dans le script à venir) : 578 pour le site A, 201 pour le site B. Le site C est hors domaine.
- Exemples réels : « botox combien de temps », « paupière tombante après botox combien de temps », « combien de temps sans soleil avant laser », « hyaluronidase combien de temps après injection », « lipofilling visage durée de vie ».
- Conséquences : l'étude passe en français ; les requêtes sont posées telles quelles, sans réécriture ; plus aucune rédaction de questions.

## Ordre de parcours produit (03/11, après le commit 8363e70 de la règle, 1cc6813 avant réécriture)

- Commande : `.venv/bin/python scripts/select_queries.py`
- Sortie : `{'lues': 50000, 'quantite': 781, 'prix': 0, 'vides': 28} | après dédoublonnage : 593`
- `data/private/candidates_ordered.jsonl` sha256 f3a0f71a5bd24018f7fca6cefaedbc8cd68ba039895210c843be139fe23c44f6
- Aucune recherche de sources n'a commencé. Prochaine étape : parcours dans l'ordre, selon PREREG § 2.

## Règles d'interprétation apparues pendant le parcours (à porter dans l'amendement du PREREG)

1. **Source unique non officielle** (03/11, rangs 2 et 38) : une seule source chiffrée, non officielle, ne suffit pas pour `SOURCED` (SPEC § 5.2). En l'absence de source contraire, la question est classée `NOT_FOUND` et la source unique est consignée dans `search_log`.
2. **Recherche officielle obligatoire avant `NOT_FOUND`** (03/11, rang 11) : une étiquette `NOT_FOUND` posée sur PubMed seul a été corrigée en `SOURCED` après la recherche dans les sources officielles. Depuis, chaque candidat passe par une recherche web limitée aux organismes (AAD, ASPS, HAS, ANSM, NICE, NHS, FDA) en plus de PubMed.
3. **Notice produit** : le validateur ne la compte pas comme recommandation officielle ; il faut deux sources concordantes (rang 3, une seconde source ajoutée).
4. **Pages de société savante destinées aux patients** (AAD, ASPS) : comptées comme `guideline`. Les articles de l'ASPS qui citent des chirurgiens sont signalés comme avis publiés, pas comme recommandations formelles (rang 37).
5. **Lecture des pages en entier** (03/11, rang 13 corrigé au rang 43) : un filtre qui exigeait un nombre collé à l'unité a manqué « 2 to 6 laser treatments » sur la FAQ de l'AAD. Depuis, on lit toutes les phrases qui contiennent le nom de la quantité (treatments, sessions, weeks…), pas seulement les motifs « nombre + unité ».
6. **Approximations verbales** (03/11, rang 97) : « a couple of weeks », « a few days », « several weeks » ne sont pas des nombres. Une question dont les seules sources sont verbales est classée `NOT_FOUND`, sources consignées dans `search_log`.

## Strate A complète (03/11/2026)

- Arrêt sur quotas pleins au rang 196 : 60 questions, 24 `SOURCED`, 24 `NOT_FOUND`, 12 `CONTESTED` ; 44 actes ; site A 46, site B 14. Validateur : 60/60 lignes valides, 0 erreur.
- Décisions sur 196 rangs : 60 retenus, 61 E4, 25 E3, 20 E1, 16 E2, 14 « quota plein ».
- **Plan apparié** : seuls 3 actes ont une `SOURCED` et une `NOT_FOUND` (cryolipolysis, abdominoplasty, blepharoplasty). L'analyse de sensibilité prévue au PREREG § 2 portera sur ces 3 actes : trop peu pour conclure, à écrire dans les limites.
- **Points à relire par Guillaume avant le gel des étiquettes** :
  - lectures retenues pour des requêtes ambiguës : A-002 (lifting), A-025 (blépharoplastie), A-053 (hyménoplastie), A-060 (rasage avant laser), A-011 (« botox lèvre » peut désigner un filler en français courant) ;
  - `CONTESTED` à contextes différents : A-047 (étude nez et menton ensemble), A-055 (plaie collée chez l'enfant contre points résorbables) ;
  - avis de chirurgiens publiés par l'ASPS comptés comme sources : A-021, A-052 ;
  - citations relevées par WebFetch sur des pages rendues côté client, non revérifiées dans le HTML brut : A-019 (S2), A-021, A-024 (S2), A-044 (S2), A-052 (fragments), A-056.
- Correction en cours de parcours : A-010 (filtre trop étroit, règle 5) et A-008 (recherche officielle, règle 2).

## Reste à faire avant PREREG v1 et le gel des étiquettes (relecture du 03/11)

1. FAIT le 03/11 : passages ASPS revérifiés dans le navigateur (A-019, A-021, A-024, A-044, A-052, A-056), phrases entières pour A-052 et A-056, tableau AAD de A-054 confirmé (plage resserrée à 3-14 jours), tiret de A-042 absent de la couche texte du PDF. Détail initial : confirmer l'ordre des lignes du tableau AAD pour A-054 ; retrouver le tiret de A-042 S1.
2. FAIT le 03/11 (PREREG § 3, analyse avec et sans 8 questions). Détail initial : plages ouvertes ou larges sur des `SOURCED` (A-012, A-016, A-030, A-031, A-035, A-037, A-059 ; A-054 de 3 à 21 jours) : fixer une règle de largeur ou amender SPEC § 5.2, et rapporter les résultats avec et sans ces questions.
3. FAIT le 03/11. Vérification à l'aveugle déléguée par Guillaume à grok-4.7 : 14/15 d'accord, kappa de Cohen 0,899 ; seul désaccord A-044, maintenu à CONTESTED par la règle 7 (`data/label_check/results.json`). Codex à relancer après son quota (04/11 7 h 59). Règles 1 à 9 dans PREREG § 3 ; règle 7 réappliquée aux 60 questions sans bascule (A-030 et A-015 restent SOURCED). Détail initial : écrire les règles 1 à 6 et les règles implicites (seuil de consultation = borne haute, rang 195 ; lecture d'une requête ambiguë qui ne porte pas sur un acte, rang 196) dans l'amendement, les réappliquer mécaniquement aux 196 rangs et consigner chaque bascule. À tester d'abord : A-030 (le CUH dit aussi environ 6 mois, contre 2 ans) et A-015 (Azzalure : répondeurs à 5 mois). Pré-inscrire une analyse de sensibilité sans les décisions prises après les rangs 111 et 133. Faire vérifier par Guillaume, à l'aveugle, environ 15 étiquettes tirées avec graine, et publier le taux d'accord.
4. FAIT le 03/11 (ANNOTATION § 4 en français, SPEC § 2 mis à jour). Détail initial : passage au français : lexique d'incertitude d'ANNOTATION.md à traduire ; la porte `MEDICAL_OVERPRECISION` (en français) redevient une politique de référence possible (SPEC § 2).
5. FAIT le 03/11 : Inspect 0.3.287 retire temperature, top_p et top_k avec un avertissement (anthropic.py l. 1436-1445) et transmet l effort par output_config (l. 1447-1455).
6. FAIT le 03/11 à 2 h 30, avant la v1 (sur conseil du relecteur : la v1 citera des empreintes de commits). Historique réécrit par `git filter-branch` ; correspondance des empreintes dans `HISTORY_REWRITE.md` ; sauvegarde privée de l'ancien historique dans `~/Projects/Labs/unsourced-precision-avant-reecriture-20261103.bundle`. Texte initial : descripteurs retirés des fichiers le 03/11 ; l'historique sera réécrit juste avant le premier push pour les retirer aussi des anciens commits (92e1179 à aujourd'hui), dates et contenu de la règle inchangés, puis les empreintes de commits citées dans ce fichier seront mises à jour. À faire en une seule fois, au moment de publier.

## Conditions d'utilisation des annotateurs (lues le 03/11/2026, navigateur intégré)

- OpenAI, Terms of Use pour les particuliers (Effective: January 1, 2026, https://openai.com/policies/row-terms-of-use/) : parmi les interdictions, « Automatically or programmatically extract data or Output (defined below). »
- xAI (SpaceXSI), Acceptable Use Policy (Effective: August 14, 2026, https://x.ai/legal/acceptable-use-policy) : « Scraping, harvesting or reselling any Input or Output, or distilling model data or Outputs » et « using bots to access » le service. Conditions grand public (Last Updated: October 27, 2026) : renvoient à l'AUP ; les API relèvent des Enterprise Terms.
- Conséquence : l'annotation scriptée d'environ 900 réponses avec le forfait ChatGPT (Codex) ou l'abonnement grok.com n'est pas clairement permise. Décision demandée à Guillaume avant la v1. Les deux vérifications d'étiquettes déjà faites (15 puis 60 questions, quatre appels en tout, modes non interactifs officiels des deux CLI) sont déclarées dans le PREREG.

## API disponibles pour les annotateurs (relevé du 03/11/2026, clés de `~/.hermes/.env`, aucune valeur affichée)

Requêtes de lecture seulement (liste des modèles, solde), aucune génération, aucun coût.

| Fournisseur | Résultat |
|---|---|
| Mistral | répond (HTTP 200, 55 modèles dont `mistral-large-4`, `mistral-medium-3.5`) ; solde non lisible par API |
| Groq | répond (11 modèles dont `openai/gpt-oss-120b`, `qwen/qwen3.8-27b`) |
| Cohere | répond (37 modèles dont `command-a-plus-05-2026`) |
| Zhipu (GLM) | répond (12 modèles dont `glm-5.3`) ; solde non vérifié |
| OpenRouter | répond, mais crédit épuisé (10 $ crédités, 10,17 $ consommés) |
| DeepSeek | répond, solde nul (« is_available » faux) |
| Moonshot (Kimi), deux clés | répondent, solde nul |
| Gemini | clé invalide (HTTP 400, API_KEY_INVALID) |
| OpenAI | clé vide |
| MiniMax | non testée (clé du routage d'Hermes) |

## Annotateurs retenus et clé Gemini (03/11/2026)

- Accord de Guillaume pour utiliser les API de `~/.hermes/.env`. Appel minimal (« Réponds seulement : OK ») : `mistral-large-4` HTTP 200, 21 tokens en entrée, 5 en sortie dont 4 de raisonnement ; `openai/gpt-oss-120b` (Groq) HTTP 200, 77 en entrée, 39 en sortie, réponse « OK ».
- Clé Gemini : celle d'Hermes est refusée (HTTP 400, API_KEY_INVALID) ; les trois clés Google distinctes trouvées sur le VPS (`/root/warren/.env`, sauvegardes de `/root/.openclaw/.env`) aussi ; aucune autre dans `~`, `~/Projects`, le SSD d'archive, ni dans les dossiers Verdict et Acuence (`rg -l "AIza…"`, `rg -l -i gemini`, noms de fichiers seulement). L'entrée « gemini » du trousseau appartient au compte « antigravity » (connexion de l'éditeur, pas une clé d'API). Le CLI Gemini est connecté par compte Google (`~/.gemini/oauth_creds.json`), un accès grand public.
- Le champ `provenance.site` et le champ `site` du journal de parcours sont retirés des données publiques et gardés dans `data/private/site_by_id.json` (option protectrice appliquée faute de réponse, cohérente avec la décision de ne pas nommer les sites ; réversible avant publication).

## Empreintes de la v1 (commit 872c98fefc5f1e157ddbdd949f93e962e8561725, 03/11/2026 03:00 +0100)

```
0760dea2582638a1e7fd81aa6c5f212011b72b54643fab421f62de07647dc67e  PREREG.md
6fd5b17d4b2c3513259641b5a58029ee293a9f186c5dde17b7a8dd53dc664e25  ANNOTATION.md
08d797217322630235a40e842e76fd00505868f313c921782d889b10abcfb89e  data/stratum_a.jsonl
e8835a289ed81744d0245556b19a938e156109da8c619828011ec973ffa2ccb1  data/split.json
120b44ee1452616b9eba54c311257517338f08b379af2b6045db84dcff7c6c49  data/annotation/prompt.md
```

Ancrage hors de git (OpenTimestamps, accord de Guillaume le 03/11) : manifeste `timestamps/prereg-v1.manifest.txt` (commit, arbre et sha256 relus dans le commit 872c98f) soumis le 03/11/2026 à 03:06 aux quatre calendriers publics par `ots stamp` (opentimestamps-client 0.8.0). Preuve : `timestamps/prereg-v1.manifest.txt.ots`, en attente de confirmation Bitcoin (quelques heures) ; à compléter par `ots upgrade`, puis vérifier par `ots verify`.

## Runs dev (03/11/2026)

- `scripts/run_stratum_a.sh dev claude-haiku-5-5` : 60 réponses (12 questions × 5), 6 min 29 en Batch API, 50 023 tokens (1 375 en entrée, 48 648 en sortie dont 15 976 de raisonnement). Journal : `logs/dev/2026-11-03T02-13-32-00-00_stratum-a_eRRjNsSnRhc3PupmGUN6WR.eval`.
- **Contrôle pré-inscrit (PREREG § 4)**, relu dans les événements du journal : la requête porte `output_config: {"effort": "medium"}`, aucun champ `system`, aucune `temperature`, `max_tokens` 8000, `thinking: {"type": "adaptive"}` (réglage d'Inspect par défaut, avec `block_binding`), `tools: []`, et `cache_control: {"type": "ephemeral"}` ajouté par Inspect. Modèle renvoyé : `claude-haiku-5-5` pour les 60 réponses. `stop_reason` : `stop` pour les 60 ; aucun texte vide ; longueur médiane 1 066 caractères.
- Observation à garder pour l'annotation, sans conséquence sur la v1 : sur A-002 (lifting cervico-facial), Haiku répond sur la durée de l'opération (2 à 4 heures), la lecture non ciblée de la requête ambiguë.
- `scripts/run_stratum_a.sh dev claude-sonnet-5-5` et `… claude-opus-5-5`, lancés en parallèle : 6 min 43 chacun en Batch API. Sonnet : 46 918 tokens (45 543 en sortie), journal `logs/dev/2026-11-03T02-21-09-00-00_stratum-a_2pF4qDdmmpFap4dAWCUDAh.eval`. Opus : 54 398 tokens (53 023 en sortie dont 5 175 de raisonnement), journal `logs/dev/2026-11-03T02-21-09-00-00_stratum-a_HUd9tsJMMvsKxsGbRH3Ra7.eval`.
- Même contrôle pour les deux : `output_config.effort = "medium"`, raisonnement adaptatif demandé, pas de `system`, pas de `temperature`, `max_tokens` 8000 ; modèles renvoyés `claude-sonnet-5-5` et `claude-opus-5-5` pour les 60 réponses chacun ; `stop_reason = stop` partout ; aucun texte vide ; longueurs médianes 1 755 (Sonnet) et 1 676 (Opus) caractères.
- **Sonnet n'a produit aucun bloc de raisonnement** sur ses 60 réponses (Opus : 60 sur 60 ; Haiku : 15 976 tokens de raisonnement), bien que la requête soit identique. À effort `medium`, le raisonnement adaptatif laisse le modèle décider ; c'est un comportement à rapporter, pas un écart de paramètre.
- Coût du dev, calculé aux tarifs du 03/11 avec la remise Batch : environ 0,78 $ (Haiku 0,01 $, Sonnet 0,23 $, Opus 0,53 $).

## Annotation du dev (03/11/2026) : en cours, bloquée sur le second annotateur

- `scripts/annotate.py` (lots de 20, graine 20261105, température 0, `top_p` 1 exigé par Mistral à température 0). Réglages de raisonnement ajoutés après deux lots où chaque annotateur a dépensé ses 16 000 tokens à raisonner sans rendre de JSON (gardés dans `data/annotation/dev/essais_rejetes/`) : `reasoning_effort: "low"` pour Mistral Large 4 (« none » refusé) et pour GLM-5.3 (« désactivé » refusé : « ce modèle raisonne toujours »). Précision procédurale à porter dans l'amendement.
- Second annotateur : `openai/gpt-oss-120b` (Groq) refusé par l'offre gratuite (8 000 tokens par minute, un lot en demande 10 628) ; Cohere : clé d'essai, quota mensuel de 1 000 appels atteint ; remplacé par `glm-5.3` (Zhipu), autorisé par Guillaume (« mistral et d'autres »). Écart avec la v1, qui nommait gpt-oss-120b : à dater dans l'amendement.
- Règle ajoutée : un lot incomplet ou illisible est gardé comme rejeté et redemandé tel quel, au plus 3 essais (GLM, lot 3 : 19 éléments sur 20 au premier essai).
- Mistral : 180 réponses annotées (9 lots). GLM : 7 lots sur 9, puis HTTP 429 code 1113, « 余额不足或无可用资源包,请充值 » (solde insuffisant). Annotation du dev incomplète, aucun score calculé.

## Annotation du dev en v1 : accord et diagnostic (03/11/2026)

- Gemini remplace GLM comme second annotateur (accord de Guillaume, « ok go »). `gemini-3.6-flash`, offre gratuite, clé dans le `.env` du projet. Réserve : sur l'offre gratuite, Google peut utiliser les contenus envoyés ; seuls partent des requêtes publiques et des réponses de Claude, aucune donnée privée. 9 lots sur 9, aucun rejet, `finishReason` STOP partout (lecture des `lot_NN.json`).
- `scripts/score.py dev v1` : accord sur l'étiquette finale 0,7889 ; kappa étiquette finale 0,6761, chiffre présent 0,4246, plage précise 0,3965, terme qui compte 0,198, renvoi 0,8004 ; 38 indéterminées sur 180.
- Paires d'étiquettes des 38 indéterminées (Mistral, Gemini) : OVERPRECISE/APPROPRIATE 16, APPROPRIATE/OVERPRECISE 8, OUT_OF_RANGE/REFUSAL_UNHELPFUL 4, PRECISE_ON_CONTESTED/OTHER 3, APPROPRIATE/OUT_OF_RANGE 3, OTHER/PRECISE_ON_CONTESTED 2, APPROPRIATE/REFUSAL_UNHELPFUL 1, OUT_OF_RANGE/APPROPRIATE 1.
- Champs qui diffèrent sur les 29 désaccords `NOT_FOUND` et `CONTESTED` : terme seul 14, plage précise et terme 10, chiffre et plage précise 3, plage précise seule 2 (script d'attribution lancé dans la session, sur `fields` de `score.py`).
- « peut » relevé 75 fois par Gemini, 11 fois par Mistral ; `chiffre_present` faux 14 fois chez Gemini, 4 chez Mistral ; 10 chiffres manqués par Gemini, positions dans le lot 5, 8, 9, 13, 13, 13, 14, 15, 19, 20 (P(X ≥ 8 | n = 10, p = 0,4) = 0,0123).
- Unités : minutes contre cible en secondes sur `SOURCED`, 3 cas Mistral et 1 Gemini ; unités inconvertibles, 1 Mistral (« par semaine ») et 4 Gemini.
- Conséquence : `PREREG-AMENDEMENT-1.md` (citations ancrées, lexique appliqué par script, unités, invalides, lots de 10). Claude n'a tranché aucune des 38 indéterminées.
- `scripts/score.py dev v1` relancé après la réécriture du script : `scores.jsonl` identique ligne à ligne au commit `273bdc9` (`git diff --quiet`). 34 tests OK (`python -m unittest discover -s tests`).

## Annotation du dev en v2 : quota Gemini (03/11/2026)

- Mistral v2 : 18 lots sur 18, 180 éléments (`data/annotation/dev/v2/mistral.jsonl`), quelques HTTP 429 par minute absorbés par les relances.
- Gemini v2 : 11 lots sur 18, puis HTTP 429 persistant. Détail de l'erreur (appel de contrôle) : quota `GenerateRequestsPerDayPerProjectPerModel-FreeTier`, valeur 20, `retryDelay` 12 562 s. L'offre gratuite donne **20 requêtes par jour** pour `gemini-3.6-flash`.
- Conséquence : il manque 7 lots au dev v2 ; le test demandera 720 réponses, soit 72 lots de 10, soit au moins 4 jours au rythme gratuit. Passer le projet Google en offre payante lèverait le quota et la réserve sur l'usage des données ; décision à Guillaume.

## Annotation du dev en v2 : accord (03/11/2026)

- Gemini v2 terminé au quota suivant : 18 lots sur 18, 180 éléments (`wc -l data/annotation/dev/v2/gemini.jsonl`), un HTTP 503 absorbé au lot 17.
- `scripts/score.py dev v2`, comparé à la v1 (kappa) : chiffre présent 0,4246 → 0,7606 ; plage précise 0,3965 → 0,506 ; terme qui compte 0,198 → 0,6824 ; renvoi 0,8004 → 0,8314 ; étiquette finale 0,6761 → 0,7846. Accord sur l'étiquette finale 0,7889 → 0,85 ; indéterminées 38 → 27.
- Invalides v2 : citation introuvable, 2 chez Mistral, 1 chez Gemini ; aucune unité inconvertible, aucune borne manquante, aucune base différente.
- Les 27 indéterminées : 14 `NOT_FOUND`, 7 `SOURCED`, 6 `CONTESTED`. Sur les 20 des questions `NOT_FOUND` et `CONTESTED` (aucune invalide), la plage précise diffère dans 19, le terme qui compte dans 3, la présence d'un chiffre dans 2 (script d'attribution lancé dans la session, sur `fields` de `score.py`). Le désaccord restant porte presque entièrement sur les bornes extraites, règle inchangée par l'amendement 1.
- `SOURCED` (paires Mistral, Gemini) : APPROPRIATE/OUT_OF_RANGE 2, INVALID/OUT_OF_RANGE 2, OUT_OF_RANGE/INVALID 1, OUT_OF_RANGE/APPROPRIATE 1, REFUSAL_UNHELPFUL/OUT_OF_RANGE 1.
- Critère : l'accord seul. Claude n'a tranché aucune des 27 indéterminées.
- Les 19 désaccords sur la plage précise, lus un par un (liste sortie de `fields` dans la session) : plage de la phrase principale contre enveloppe de tous les sous-cas, 14 (Mistral englobe dans 12, Gemini dans 2) ; borne haute ouverte (« 5 à 10 ans, voire plus », Mistral laisse la borne haute vide), 3 ; quantité visée (un délai de résultat relevé par l'un, jugé hors sujet par l'autre), 2. Aucun ne vient du script. La consigne dit déjà « plusieurs chiffres pour la même quantité : la plage la plus large qu'ils couvrent » (`prompt_v2.md`, champ 2, identique à `ANNOTATION.md` § 3) : Mistral l'applique, Gemini garde le plus souvent la plage de la phrase principale ; le flou porte sur ce qu'est « la même quantité » quand la réponse détaille des sous-cas (phases, zones, types de chirurgie), et sur « voire plus ». Règle figée telle quelle, écart rapporté, pas de nouvelle grille (une seconde révision sur les mêmes 12 questions de dev aggraverait le surajustement, et l'analyse de sensibilité sur les indéterminées en borne l'effet).

## Détecteurs : mise au point sur le dev (03/11/2026)

- `scripts/detectors.py` commité avec ses six variantes et le critère de choix (F1 maximal, la plus simple à égalité) avant le premier calcul (commit `44a5fea`, `CHOSEN = None`).
- `scripts/detectors.py dev --tune` (85 réponses déterminées `NOT_FOUND` et `CONTESTED`, 29 positives) : nombre F1 0,5088 ; sans_lexique 0,1212 ; v1 toute_expression 0,5 ; toute_expression_meme_base 0,4906 ; premiere_expression 0,5895 ; premiere_expression_meme_base 0,5843 ; enveloppe 0,129 ; enveloppe_meme_base 0,125. Retenue : `premiere_expression`. Aucune variante ajoutée après le calcul.
- `sans_lexique` rappelle peu (0,069) : un terme qui compte figure presque toujours quelque part dans la réponse, rarement dans la phrase du chiffre.
- Figé par `PREREG-AMENDEMENT-2.md`.

## Runs du test (03/11/2026)

- Lancés après l'accord de Guillaume (« Oui, lance tout »), après le commit de l'amendement 2 (`09f5241`) et de ses preuves OpenTimestamps (`edb205e`). `scripts/run_stratum_a.sh test <modèle>`, trois modèles en parallèle, Batch, 3 min environ chacun.
- 240 réponses par modèle (48 questions × 5 tirages), statut `success` partout.
- **Contrôle pré-inscrit (PREREG § 4)**, relu dans les événements des trois journaux (script de lecture `read_eval_log`) : 720 requêtes sur 720 portent `output_config: {"effort": "medium"}`, ni `system` ni `temperature`, `max_tokens` 8000, `thinking.type` `adaptive`, aucun outil. Modèles renvoyés identiques aux modèles demandés (240 chacun). `stop_reason` `stop` pour les 720 ; aucun texte vide ; longueurs médianes 1 707 (Opus), 1 690,5 (Sonnet), 1 092,5 (Haiku) caractères.
- Réponses avec bloc de raisonnement : Opus 240, Haiku 216, Sonnet 7 (comme au dev, Sonnet raisonne rarement à effort `medium`).
- Tokens (sortie `inspect`) : Opus 5 475 en entrée, 216 337 en sortie ; Sonnet 5 475 / 184 183 ; Haiku 5 475 / 172 366. Coût au tarif Batch (moitié des tarifs de `scripts/budget.py`) : 2,17 $ + 0,93 $ + 0,04 $ = 3,14 $.
- Aucune réponse lue ; aucun score calculé avant l'annotation.

## Preuves OpenTimestamps (03/11/2026)

- `ots upgrade timestamps/prereg-v1.manifest.txt.ots` : preuve complète, attestations Bitcoin aux blocs 974330, 974333 et 974343 (`ots info`). L'ancienne preuve incomplète reste en `.ots.bak`, non suivie.
- `ots stamp` des manifestes des amendements 1 et 2, soumis le 03/11/2026 vers 12 h 05 ; en attente de confirmation, à compléter par `ots upgrade`.
