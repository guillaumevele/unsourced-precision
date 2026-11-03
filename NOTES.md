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
