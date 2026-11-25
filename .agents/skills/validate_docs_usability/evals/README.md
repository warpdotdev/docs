# Blind calibration

Use synthetic journeys to check whether an evaluator applies the [method](../../../references/docs-usability-validation.md). This is agent calibration, not testing with readers or evidence about Warp product behavior.

## Run without the answers

1. Export each case separately from the docs root. Replace `CASE_ID` with an ID in `evals.json`.

   ```bash
   python3 .agents/skills/validate_docs_usability/evals/calibrate.py export --case CASE_ID > /tmp/usability-input.json
   ```

2. Give only the exported JSON to a fresh evaluator with no repository access, prior fixture discussion, or grading feedback. Do not hand it this directory, the worked example, or `rubric.json`. Case names and expected answers live only in the rubric. Use a separate fresh context for each case.
3. Save the evaluator's returned JSON unchanged as `REPORT_PATH`. The payload defines the report contract: question statuses in prompt order, readiness, the full evidence record, and a separate retest when supplied. Freeze all reports before revealing any answers.
4. In a separate grader context, compare each frozen report:

   ```bash
   python3 .agents/skills/validate_docs_usability/evals/calibrate.py compare --report REPORT_PATH
   ```

5. Read the report's actual paths, passages, findings, limitations, and retained retest against the printed criteria and [rubric](rubric.json). Record each disagreement with its evidence. A matching declared status alone does not establish a correct judgment. Retain the raw report, comparison output, evaluator/model identity, input revision, test time, and manual grading notes in a linked run artifact or PR evidence.

The comparison exits 1 for declared-outcome mismatches and 0 when those declarations match. `false_clear_primary` flags a primary answer declared Clear when the rubric requires another status. It does not detect a fabricated evidence record or an unjustified ready decision whose declared fields happen to match. Review those manually. Do not average outcomes into a usability score or make this a required CI gate.

Run the original cases (1–7) and the evidence/readiness boundary cases (8–11). The paired final cases use the same pages with different primary questions. Keep the assigned priorities when judging readiness.

If fresh evaluator execution is unavailable, report it as not run. Unit tests use deterministic reports to test input isolation and comparison plumbing, including false Clear detection; they do not demonstrate blind evaluator performance.
