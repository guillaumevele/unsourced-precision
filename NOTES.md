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
