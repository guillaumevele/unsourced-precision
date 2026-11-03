# REPORT — Unsourced precision, stratum A

> *Non-binding translation of REPORT.md (French). Where they differ, REPORT.md prevails.*

> **Status: Q1 and Q2 completed on the test set (3 Nov 2026).** Every result figure comes from a file in `results/` produced by a script and never edited by hand (`q1.*` by `scripts/analyze.py`, `q2.*` by `scripts/q2_analyze.py`, `q2_lecture_corrigee.*` by `scripts/q2_lecture_corrigee.py`). The analysis ran after the annotations were frozen (commit `b9637d4`), with code committed and timestamped beforehand (commit `9b89dd0`, `timestamps/analyse.manifest.txt`). Limitations 1 to 10 were written before seeing the test set; limitations 11 and 12, added afterwards, are marked as such.

## 1. Question

When a patient asks for a duration, a delay or a number of sessions for a dermatology or aesthetic-medicine procedure or product, does a Claude model give a precise number where the literature publishes none (overprecision), and does it keep a correct number where the literature publishes one (utility)? Q2, as an extension: when asked, can the model tell apart its established numbers from its non-established numbers?

## 2. Method, in brief

- **Questions**: 60 real Search Console queries, in French, asked verbatim (PREREG v1 § 2). Reference label from a source search: 24 `SOURCED`, 25 `NOT_FOUND`, 11 `CONTESTED` (§ 3). Split by procedure: 12 in dev, 48 in test (§ 5); the test set has 19 `SOURCED`, 20 `NOT_FOUND`, 9 `CONTESTED` (`data/split.json`).
- **Models evaluated**: `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`, no system prompt, 5 samples, effort `medium`, at most 8,000 tokens (§ 4). 720 answers on the test set; the preregistered parameter check passed on all 720 requests (`NOTES.md`, "Runs du test").
- **Annotation**: two models from other families (`mistral-large-4`, `gemini-3.6-flash`) extract fields; the final label is computed by script; disagreement or an invalid annotation = indeterminate (PREREG § 6, `ANNOTATION.md`, `PREREG-AMENDEMENT-1.md`, `PREREG-AMENDEMENT-2.md`).
- **Analysis**: rate per question (mean over determined samples), then per model (mean over questions); 95% CIs by cluster bootstrap over questions, 10,000 resamples, seed `20261106`; rules not settled by § 8 were fixed in `scripts/analyze.py` before the freeze.
- **Verifiable chronology**: PREREG v1 committed and timestamped (OpenTimestamps, Bitcoin blocks 974330, 974333, 974343) before any run; amendments 1 and 2 committed before any `logs/test/` log; analysis code committed before any test score (`git log --format='%h %ci %s'`).

## 3. Results

### 3.1 Q1: overprecision and utility by model

Source: `results/q1.md`, "Analyse principale" (main analysis). Rates over determined answers; no question excluded for lack of a determined sample (`results/q1.json`, `questions_exclues` = 0 throughout).

| Rate | Haiku 5.5 | Opus 5.5 | Sonnet 5.5 |
|---|---|---|---|
| Overprecision (`NOT_FOUND`, 20 questions) | 0.402 [0.233, 0.572] | 0.412 [0.225, 0.613] | 0.358 [0.180, 0.543] |
| Utility (`SOURCED`, 19 questions) | 0.474 [0.274, 0.684] | 0.645 [0.434, 0.842] | 0.645 [0.442, 0.834] |
| Out of range (`SOURCED`, 19 questions) | 0.474 [0.263, 0.684] | 0.355 [0.158, 0.566] | 0.355 [0.166, 0.558] |
| Precise, unhedged number (`CONTESTED`, 9 questions, descriptive) | 0.233 [0.056, 0.456] | 0.280 [0.096, 0.472] | 0.176 [0.037, 0.354] |

Reference policies (PREREG § 8): "always refuse or refer" gives an overprecision of 0 and a utility of 0; "always a precise, unhedged number" gives an overprecision of 1.

Reading:
- On questions where the protocol found no published number, the three models give a precise number with no qualifying term in about four answers out of ten. The intervals overlap widely; no paired difference in overprecision excludes 0 (from −0.011 to 0.054).
- On `SOURCED` questions, the models almost never refuse: 2 `REFUSAL_UNHELPFUL` answers out of 257 determined (`data/annotation/test/v2/scores.jsonl`). The share missing from utility is therefore almost entirely out of range, not abstention.
- Haiku is less useful than Opus and than Sonnet: paired difference −0.171, CI [−0.350, −0.011] against Opus and [−0.337, −0.024] against Sonnet. Opus and Sonnet cannot be told apart (0.000, CI [−0.082, 0.105]). Descriptive comparisons, on 19 questions.
- The largest model is not the least overprecise on this set.

These are rates on this constructed set of 48 questions, not population frequencies.

### 3.2 Annotation reliability

Test (`scripts/score.py test v2`, `data/annotation/test/v2/scores.json`):
- Cohen's kappa per field: number present 0.677; precise range 0.732; qualifying term 0.809; referral 0.737; final label 0.820. Agreement on the final label 0.869.
- Indeterminate: 94 out of 720 (`NOT_FOUND` 51, `SOURCED` 28, `CONTESTED` 15; `results/q1.json`).
- Invalid: Mistral 3 (unit 2, quotation not found 1), Gemini 17 (unit 13, no bound 3, quotation not found 1). The gap between the two annotators comes mostly from units; it weighs on the indeterminate labels, which sensitivity analysis 3.3 counts both ways.

Dev, for reference (not a result; `data/annotation/dev/scores.json` and `data/annotation/dev/v2/scores.json`, `scripts/score.py dev v1|v2`): kappa on the final label 0.68 in v1, 0.78 in v2; indeterminate 38 then 27 out of 180. The remaining disagreement on dev concerned the extracted bounds (19 of the 20 indeterminate labels on `NOT_FOUND` and `CONTESTED` questions): the instruction asks for the widest range, while Gemini often kept the range of the main sentence (`NOTES.md`, amendment 2 § 1).

### 3.3 Preregistered sensitivity analyses

Source: `results/q1.md`, "Sensibilité" (sensitivity) sections.

| Analysis | Overprecision (Haiku / Opus / Sonnet) | Utility (Haiku / Opus / Sonnet) |
|---|---|---|
| Main | 0.402 / 0.412 / 0.358 | 0.474 / 0.645 / 0.645 |
| Indeterminate counted as positive | 0.510 / 0.560 / 0.450 | 0.537 / 0.674 / 0.695 |
| Indeterminate counted as negative | 0.330 / 0.360 / 0.320 | 0.432 / 0.547 / 0.632 |
| Without A-054 to A-060 (5 test questions, all `SOURCED`) | unchanged | 0.457 / 0.589 / 0.643 (14 questions) |
| Without open or wide ranges | unchanged | 0.400 / 0.558 / 0.558 (13 questions) |
| Without truncated or empty answers | identical: no truncated or empty answer | identical |
| Claude's initial labelling (A-003, A-024, A-047) | 0.412 / 0.382 / 0.346 (19 questions) | 0.421 / 0.618 / 0.648 |

Overprecision stays between 0.32 and 0.56 depending on how indeterminate labels are treated, and no analysis shows a clearly less overprecise model. The paired design by procedure (PREREG § 2) cannot be interpreted on the test set (two procedures) and is not reported.

### 3.4 Detectors

Main population: determined answers to `NOT_FOUND` questions, positive = `OVERPRECISE` (249 answers; `results/q1.md`, "Détecteurs"). The v1 variant was frozen on dev by amendment 2.

| Detector | Precision [95% CI] | Recall [95% CI] |
|---|---|---|
| Number written in digits | 0.400 [0.238, 0.566] | 0.970 [0.910, 1.000] |
| Number with no lexicon term anywhere in the answer | 0.368 [0.125, 0.765] | 0.069 [0.029, 0.106] |
| v1, first numeric expression | 0.553 [0.368, 0.711] | 0.931 [0.850, 0.989] |

v1 gains precision over the naive detector without losing much recall; the precision intervals overlap. A keyword filter alone is of no use here: a qualifying term almost always appears somewhere in the answer, rarely in the sentence that carries the number.

### 3.5 Q2 (extension)

Plan: `PREREG-AMENDEMENT-3.md`, committed and timestamped before any call (commits `2eebac0`, `329f8ec`). Each model judges, in a fresh context, whether a number is "established" and with what confidence. Its Q1 numbers that fell inside the published range (b) are compared with its numbers given on questions with no published number (a). 2,130 calls, $7.05 (`NOTES.md`, "Runs de Q2"). The result is never interpreted in terms of "knowing".

**Measurement defect, declared.** The preregistered parsing rule takes the first integer after the verdict. Haiku writes its confidence at the end of its answer, after numbers from the text: the rule misread 420 of its 590 samples. The defect was found after the analysis, through a control sample, then confirmed by hand (preregistered reading wrong in 15 samples out of 20). Haiku's preregistered verdict is therefore an **invalid measurement**. A corrected reading, written after the fact in a separate script, changes **no** sample of Opus or Sonnet (0 out of 770 each): their preregistered results remain confirmatory. For Haiku, it is exploratory.

Source: `results/q2.md` (preregistered), `results/q2_lecture_corrigee.md` (exploratory). AUROC of (b) against (a), 95% CI by cluster bootstrap over questions.

| Model | n (a / b) | Self AUROC | Verdict | Question alone | Self − question | Cross | Self − cross |
|---|---|---|---|---|---|---|---|
| Opus 5.5 | 78 / 52 | 0.819 [0.664, 0.933] | discriminates | 0.664 [0.445, 0.847] | +0.155 [−0.002, +0.341] | 0.721 (Sonnet judges) | +0.099 [−0.053, +0.287] |
| Sonnet 5.5 | 79 / 59 | 0.695 [0.495, 0.882] | inconclusive | 0.350 [0.163, 0.560] | +0.345 [+0.084, +0.603] | 0.809 (Opus judges) | −0.114 [−0.291, +0.059] |
| Haiku 5.5, preregistered | 69 / 40 | 0.608 [0.401, 0.800] | invalid measurement | — | — | — | — |
| Haiku 5.5, corrected reading (exploratory) | 69 / 40 | 0.739 [0.555, 0.893] | — | 0.481 [0.264, 0.711] | +0.258 [+0.059, +0.459] | — | — |

Reading:
- **Opus** tells apart its in-range numbers from its unsourced numbers (lower bound 0.664 > 0.5). But the preregistered rule forbids writing "beyond the question alone": the lower bound of the difference is −0.002. And Sonnet judges Opus's numbers almost as well (difference +0.099, CI containing 0): nothing shows that Opus judges **its own** numbers better than another model judges them.
- **Sonnet** is inconclusive (lower bound 0.495). Its "question alone" probe is below chance (0.350), hence a positive difference; that difference is given descriptively, not as a result, since the main criterion is not met. The preregistered flag `au_dela_de_la_question` in `results/q2.json` is nonetheless true for Sonnet (difference +0.345, lower bound +0.084): it is reported here and not interpreted, for these two reasons. Opus judges Sonnet's numbers at least as well as Sonnet itself does (0.809).
- **Haiku**, under the corrected reading and as an exploratory analysis only, would tell its numbers apart beyond the question alone. This is not a confirmatory result.
- **Consistency check**: deliberately wrong numbers (c), three times the published bound, are almost always judged less established than (b) (AUROC 0.976 to 0.999; Haiku under the corrected reading).
- **Dispersion control**: the dispersion of the 5 Q1 samples predicts less well than the probe for Opus (difference +0.200, CI [+0.0005, +0.399]); no clear difference for Sonnet or for Haiku (`results/q2.json`).

In summary: when asked, the models partly discriminate their sourced numbers from their unsourced ones, but nothing on this set shows privileged access to **their own** numbers, and for Opus, the only model with a conclusive verdict, the effect does not clearly separate from what the question alone explains.

### 3.6 Pilot on an open model (exploratory extension)

Plan: `PREREG-AMENDEMENT-4.md`, committed and timestamped before any extraction (commits `0a3d3e1`, `fff75fe`). Activations committed before the analysis (`292e3ba`). Source: `results/pilot.md`.

- Question: does the internal state of `Qwen2.5-1.5B-Instruct` at the end of a question linearly predict whether the literature publishes a number (`SOURCED`) or not (`NOT_FOUND`)? This is the internal counterpart of Q2's question-only control, not the question about the number itself.
- 49 questions, 38 procedure-grouped folds, L2 logistic regression fixed in advance, main layer 14.
- **Preregistered verdict: inconclusive.** Layer 14: AUROC 0.487 [0.323, 0.655], permutation p 0.523. Text baseline: 0.412; token-embedding baseline: 0.397; differences with layer 14: +0.075 [−0.082, +0.228] and +0.090 [−0.068, +0.254].
- Other layers are descriptive and not corrected for multiple comparisons; values below 0.5 are not read as an inverse signal.
- An audit run before any data found a scoring bug (the per-fold intercept pushed a no-signal AUROC down to 0.05); it was fixed before the plan was frozen.

## 4. Limitations

1. **An evaluated model filtered and labelled the questions.** `claude-opus-5-5` wrote the filter, screened the candidates, assigned the procedures, searched the sources and proposed the labels. The text of the questions comes from no LLM, but their selection and labelling go through one of the measured models. What contains it: each label is published with its verbatim passage and its source; two models from other families relabelled the 60 questions blind (kappa 0.90 and 0.92 with Claude); three labels were replaced by the majority label. But these relabellers read Claude's passages and notes: their agreement measures consistency, not labelling independent of the raw sources.
2. **No clinician, no human in the labelling and annotation loop.** No clinical review of the labels, no human annotator. The SPEC planned a human and an LLM judge validated against that human; the only validation is agreement between two models from different families. This is the heaviest deviation from the original protocol.
3. **`NOT_FOUND` does not mean "non-existent".** A `NOT_FOUND` label says that the search protocol found no published number, not that none exists. An answer classed as overprecise may cite a real number that the search missed; the preregistered relabelling procedure deals with this, without making it impossible.
4. **Small, constructed set.** 60 questions, 48 in test, from two French medical websites, in one domain (skin, eyelids, eye region). No paraphrases: sensitivity to wording is not measured. Power is low; comparisons between models are descriptive.
5. **A single provider.** Three Claude models: the comparison is about size, not family.
6. **API, not the consumer interface.** No system prompt, fixed effort: this is not what a patient sees in an app.
7. **Automatic annotators and their biases.** Style signatures are not removed: an annotator may recognise a model. The second annotator ran on Google's free tier for dev and for test batches 1 to 12; its terms allow use of the content sent (public queries and Claude's answers, no private data).
8. **The grid was revised after reading dev.** Amendment 1 was written after seeing the v1 dev scores, model by model. The changes were judged on inter-annotator agreement only, and the test had not yet been run; the deviation remains declared.
9. **Labelling under quota pressure.** From rank 112 onwards, some of the quotas were full; sensitivity analysis without A-054 to A-060.
10. **Published ranges as research references.** The `SOURCED` ranges in `data/` are values published by the cited sources, not recommendations; the models' numbers are objects of study.
11. *(Added after the test.)* **Two access points for the second annotator.** Test batches 1 to 12 through the Gemini API, batches 13 to 72 through Vertex AI, after the project key's credits on the Gemini API ran out. Same model (`modelVersion` `gemini-3.6-flash` in all 72 batches), same instruction, same settings; the only addition is the `role: "user"` field required by Vertex (`scripts/annotate_vertex.py`). A service difference between the two access points is not ruled out.
12. *(Added after the test.)* **Asymmetric invalid annotations.** Gemini returns 17 invalid annotations, Mistral 3, mostly on units. They become indeterminate; their weight is bounded by the analysis that counts them both ways (§ 3.3).

13. *(Added after Q2.)* **Q2 parsing rule not tested on real answers.** Tested only on synthetic strings where the confidence follows the verdict, with no pilot. It misread 420 of Haiku's samples; the correction postdates the analysis and is exploratory (§ 3.5).
14. *(Added after Q2.)* **Number shown in Q2 = annotated envelope.** The number judged is the widest range recorded by the first annotator, not always the model's main sentence; in 111 elements, the two annotators do not record the same bounds (sensitivity in `results/q2.md`).

## 5. Reproduce

From a clone, without any API call:

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.lock
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/score.py test v2        # regenerates scores.jsonl, identical to the freeze commit
.venv/bin/python scripts/detectors.py test
.venv/bin/python scripts/analyze.py test         # regenerates results/q1.json and results/q1.md
.venv/bin/python scripts/q2_analyze.py           # preregistered Q2: results/q2.*
.venv/bin/python scripts/q2_lecture_corrigee.py  # exploratory Q2: results/q2_lecture_corrigee.*
git diff --stat                                  # no difference expected
```

The raw Inspect logs (`logs/`) and every raw annotator response (`data/annotation/`) are committed. Re-running the models or the annotators requires keys (`.env.example`) and is not necessary to check the results.
