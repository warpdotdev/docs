---
name: tone_model_eval
description: Run a fixed-input copy-pass eval comparing Claude Fable 5.1 against the current-default and cheaper candidate models on docs tone/concision quality, scoring each with existing style_lint tone checks plus a fixed anonymized LLM-judge rubric, to decide whether Fable-5.1-derived guidance should become the tone reference and whether a cheaper model can apply it reliably. Use when asked to evaluate model choice for docs copy passes, compare candidate models' tone/concision output, or decide whether to adopt Fable-5.1-derived AGENTS.md guidance. Never opens a content PR and never edits AGENTS.md, style_lint, or any draft_* skill — its only output is the comparison report.
---

# tone_model_eval

Compares candidate models on a fixed-input copy-pass task and reports which
one most closely follows this repo's AGENTS.md → Voice & tone guidance. The
eval never changes production guidance or model selection itself — see
`out_of_repo_handoff.md` for the separate, out-of-repo steps that act on a
positive recommendation.

## Design

Every candidate model edits the **identical** "before" text for a given
fixture — no model sees a different starting draft than any other candidate
for the same fixture. This fixed-input design is load-bearing: it is what
makes the per-model scores on a fixture comparable to each other. It does
**not** make them comparable to the fixture's original, unknown-provenance
author — see the report's "What this eval can and cannot claim" section
(`score_outputs.py`'s `SCOPE_BOUNDARY_SECTION`), which every report emits
verbatim.

Scoring blends two independent axes, recorded separately rather than blended
into one number:
- **Mechanical** — the existing `style_lint.check_tone_buzzwords` and
  `check_meta_openers` checks, plus a word-count delta against the "before"
  text (reusing `doc_quality_policy.check_compression_contract.count_words`).
- **Judge rubric** — a fixed 1-5 score on three dimensions (concision, avoids
  over-explaining, technical fidelity) from an anonymized judge call. See
  `judge_rubric.md`.

## Running the eval

1. **Select or extend fixtures.** `fixtures.json` is the fixed comparison-set
   manifest. Each entry has `id`, `content_type`, `source_path`,
   `before_commit`, `known_feedback`, and `synthetic` (plus
   `synthetic_content` when `synthetic` is `true` — a deliberately
   over-verbose seed draft used when no natural historical example exists for
   that content type). Validate any change to this file:
   ```bash
   python3 .agents/skills/tone_model_eval/score_outputs.py validate-fixtures
   ```
2. **Dispatch one copy-pass run per candidate model.** For every fixture, send
   every candidate model (Fable 5.1, the current default, and any cheaper
   candidates) the exact same prompt from `copy_pass_prompt.md` with that
   fixture's "before" text inserted verbatim. Save each model's output to its
   own file.
3. **Score each output.** For every (fixture, model) pair:
   ```bash
   python3 .agents/skills/tone_model_eval/score_outputs.py judge-prompt \
     --fixture-id <FIXTURE_ID> --output-file <OUTPUT_FILE>
   ```
   Send the printed prompt to the fixed judge model (or a human judge), save
   its JSON response to a file, then score the row:
   ```bash
   python3 .agents/skills/tone_model_eval/score_outputs.py score \
     --fixture-id <FIXTURE_ID> --model-id <MODEL_ID> \
     --output-file <OUTPUT_FILE> --judge-response-file <JUDGE_RESPONSE_FILE> \
     --rows-file rows.jsonl
   ```
4. **Read the report.** Once every fixture/model pair has a row in
   `rows.jsonl`:
   ```bash
   python3 .agents/skills/tone_model_eval/score_outputs.py report \
     --rows-file rows.jsonl --fable-model-id <FABLE_MODEL_ID> \
     --default-model-id <CURRENT_DEFAULT_MODEL_ID> \
     --output-json report.json --output-md report.md
   ```
   The report applies the pinned adoption thresholds (`score_outputs.py`'s
   `ADOPT_CONCISION_MARGIN`, `ADOPT_MECH_REDUCTION_PCT`,
   `CHEAPER_JUDGE_TOLERANCE`, `CHEAPER_MIN_TECHNICAL_FIDELITY`) and states a
   pass/fail verdict by name for each recommendation arm — including an
   explicit "no meaningful difference found" verdict when neither adoption
   threshold is met, which is a valid, reportable outcome, not a blocked eval.

## Scope

This skill never opens a content PR and never edits `AGENTS.md`, `style_lint`,
`doc_quality_policy`, or any `draft_*` skill — those changes are a follow-up
ticket gated on what a run of this eval finds. Its only output is the
comparison report (JSON + Markdown) and, when the report recommends acting,
a pointer to the separate `out_of_repo_handoff.md` checklist.
