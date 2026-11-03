# Unsourced precision

**Do Claude models state precise clinical numbers that no published source supports, and do they still give the number when one is published?**

A preregistered, timestamped evaluation of three Claude models on 60 real patient search queries (dermatology, aesthetic medicine, eye region). Each query asks for a duration, a delay, or a number of sessions. Each one is labelled against the literature: a number is published (`SOURCED`), no number was found (`NOT_FOUND`), or sources disagree (`CONTESTED`).

> **Status (3 Nov 2026).** Preregistration, amendments, test runs and the analysis code are committed and timestamped. Test annotation is in progress. **No test result exists yet.** `REPORT.md` and `results/` will be filled by `scripts/analyze.py` after the annotations are frozen by a commit.
>
> The working documents are in French (the author's language). This README is the English entry point. Translations, where they exist, are marked non-binding: the French files are the ones fingerprinted in the timestamp manifests.

## Why this is an honesty problem

A patient asks "how long does the swelling last after X". If the literature gives no number, a fluent answer such as "3 to 4 weeks", with no hedge, states a confidence the evidence does not support. The answer is not false in any checkable way: it is **overprecise**. A model that always refuses is safe and useless. A model that always answers is useful and overprecise. This study measures both sides on the same questions:

- **Overprecision.** On `NOT_FOUND` questions, the share of answers that give a precise number without a qualifying term.
- **Utility.** On `SOURCED` questions, the share of answers that give a number inside the published range. The share **outside** the range is reported separately.
- **Q2 (extension, preregistered, not yet run).** In a fresh context, can the model tell apart its own unsourced numbers from numbers inside a published range, beyond what the question alone and its own sampling variation explain? It is never interpreted as the model "knowing".

## Design in one screen

| | |
|---|---|
| Questions | 60 real Google Search Console queries in French, asked verbatim, typos included. No question was written by a model. The source sites are not named. |
| Reference labels | Common search protocol (PubMed, official sources), passage quoted verbatim for each label. 24 `SOURCED`, 25 `NOT_FOUND`, 11 `CONTESTED`. Blind relabelling by two models from other families (kappa 0.90 and 0.92). |
| Split | 12 dev / 48 test, by procedure. Everything was tuned on dev only. |
| Models evaluated | `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`. No system prompt, 5 samples, effort `medium`, 8,000 max tokens, Batch API, via Inspect AI. |
| Annotation | Two annotators from other families (`mistral-large-4`, `gemini-3.6-flash`) extract fields. The final label is computed by script, and an annotator disagreement gives an indeterminate label. Claude neither annotates nor arbitrates its own outputs. |
| Analysis | Rates per question, then per model. Cluster bootstrap over questions (10,000 resamples, seed 20261106). Paired model comparisons are descriptive. Five preregistered sensitivity analyses. Three overprecision detectors, from naive to rule-based, evaluated against the annotators. |

## Verifiable chronology

Every step that could bias the result was committed **before** the data it could be tuned on. The fingerprints are anchored in Bitcoin through [OpenTimestamps](https://opentimestamps.org).

| Step | Commit | Timestamp proof |
|---|---|---|
| Preregistration v1 (`PREREG.md`, `ANNOTATION.md`, prompt, labels, split) | `872c98f` | `timestamps/prereg-v1.manifest.txt.ots`, complete (blocks 974330, 974333, 974343) |
| Amendment 1: annotation grid v2, written after dev scores and before any test run | `875e2d7` | `timestamps/amendement-1.manifest.txt.ots` |
| Amendment 2: grid for test, detector frozen after dev tuning | `09f5241` | `timestamps/amendement-2.manifest.txt.ots` |
| Test runs (`logs/test/`), first appearance | `d84aa75` | git history |
| Analysis code, written and unit-tested before any test score | `9b89dd0` | `timestamps/analyse.manifest.txt.ots` |

Check it yourself:

```bash
git log --format='%h %ci %s' -- PREREG.md logs/test scripts/analyze.py
for m in prereg-v1 amendement-1 amendement-2 analyse; do      # files unchanged since they were frozen
  grep -E '^[0-9a-f]{64}  ' timestamps/$m.manifest.txt | shasum -a 256 -c --quiet && echo "$m OK"
done
ots verify timestamps/prereg-v1.manifest.txt.ots              # needs a Bitcoin node, or use opentimestamps.org
```

Every deviation from the plan is written down rather than hidden: the annotator replaced, the grid revised after dev, the API changed mid-annotation. See `PREREG-AMENDEMENT-1.md`, `PREREG-AMENDEMENT-2.md` and the dated log in `NOTES.md`.

## Limitations (written before seeing the test)

The full list is in `REPORT.md` § 4. The ones that matter most:

1. **One of the evaluated models filtered and labelled the questions.** `claude-opus-5-5`, working as a research assistant under the author's direction, screened the candidate queries, searched the sources and proposed the labels. It is mitigated by verbatim passages and blind relabelling by two other model families. Those relabellers read Claude's passages and notes, so their agreement measures consistency, not independent labelling.
2. **No clinician and no human annotator.** The only validation of the annotation is agreement between two model families.
3. **`NOT_FOUND` means "not found by the protocol", not "does not exist".** A preregistered relabelling procedure handles real sources that a model cites and the protocol missed.
4. **Small, constructed set.** 48 test questions, one domain, French only, one provider. Rates describe this set, never a population frequency.

## Reproduce

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.lock
.venv/bin/python -m unittest discover -s tests          # unit tests, no API call
.venv/bin/python scripts/score.py test v2               # labels from the committed annotations
.venv/bin/python scripts/analyze.py test                # results/q1.json and results/q1.md, no API call
```

Re-running the models or the annotators needs API keys (`.env.example`) and is not required to check the results: the raw Inspect logs (`logs/`) and every raw annotator response (`data/annotation/`) are committed.

## Repository map

| Path | Content |
|---|---|
| `SPEC.md`, `PREREG.md`, `PREREG-AMENDEMENT-*.md` | Plan, preregistration and amendments (French) |
| `ANNOTATION.md`, `data/annotation/prompt_v2.md` | Annotation grid and the exact prompt |
| `data/stratum_a.jsonl` | The 60 questions, labels, ranges, sources and verbatim passages |
| `evals/stratum_a.py` | Inspect task |
| `logs/` | Raw Inspect logs (dev, test) |
| `data/annotation/` | Raw annotator responses, extracted fields, agreement scores |
| `scripts/` | Selection, annotation, scoring, detectors, analysis |
| `RELATED.md` | Related work, with the reading depth stated for each entry |
| `NOTES.md` | Dated research log: every decision, error and correction |

## How this was built

The study was designed and directed by Guillaume Velé. It was carried out with Claude Code (`claude-opus-5-5`) as a research assistant, which wrote code, ran the pipeline and drafted the documents under his review. Limitation 1 describes how this affects the labels. The full trace of decisions is in `NOTES.md`.
