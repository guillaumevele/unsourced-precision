# Data card: `stratum_a.jsonl`

60 real patient search queries in French, each asking for a duration (47), an interval (5), a count (5) or a frequency (3) about a dermatology, aesthetic-medicine or eye-region procedure. Each query carries a reference label built from the literature. Licence: CC BY 4.0 (`LICENSE-DATA`), except the verbatim source passages, which belong to their publishers.

## Fields

Schema: `schema/stratum_a.schema.json`. Validation: `.venv/bin/python scripts/validate_stratum_a.py data/stratum_a.jsonl`.

| Field | Content |
|---|---|
| `id` | `A-001` to `A-060`, in the order the candidates were screened |
| `question` | The query exactly as typed into Google, typos included. Never written or edited by a model (`llm_drafted: false`). |
| `procedure_id` | Procedure or product the query is about (the dev/test split is made by procedure) |
| `label` | `SOURCED`: a number is published. `NOT_FOUND`: the search protocol found none. `CONTESTED`: sources disagree. |
| `target_quantity` | What is asked: `kind`, `unit`, French `description` |
| `range` | For `SOURCED`: the published range (`low`, `high`, `unit`). An open bound is `null`. |
| `passage` | Verbatim quotes that justify the label, each with its source reference and location |
| `sources` | Sources consulted (PubMed, guidelines, official pages) |
| `search_log` | What was searched, where, and what was found, for each query |
| `provenance` | `search_console`, rank in the shuffled candidate list, shuffle seed |

Split: `split.json` (12 dev, 48 test). Annotations of model answers: `annotation/` (raw annotator responses, extracted fields, agreement scores). Q2 probes: `q2/`.

## What is not here

The sites the queries came from, impressions, clicks and the raw Search Console export stay private: the sources must not be identifiable. `data/private/` is excluded from the repository.

## Caveats

- `NOT_FOUND` means "not found by the protocol", not "does not exist".
- Labels were proposed by `claude-opus-5-5` and blind-relabelled by two models from other families. No clinician reviewed them. See `REPORT.md` § 4.
- The `SOURCED` and `CONTESTED` ranges are values **published by the cited sources**, given as research references, **not as medical recommendations** (SPEC § 11).
