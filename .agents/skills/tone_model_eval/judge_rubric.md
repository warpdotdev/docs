Fixed 1-5 rubric `score_outputs.py` uses to score a single copy-pass output against
its fixture's "before" text. Every dimension is scored independently on a 1
(worst) to 5 (best) integer scale.

## Dimensions

1. **Concision** — does the rewrite say the same thing in fewer, tighter words
   without dropping meaning? 1 = as wordy or wordier than the original; 5 =
   consistently tightened with no padding.
2. **Avoids over-explaining** — does the rewrite cut restated cause-and-effect,
   meta-openers, hedging stacks, and rule-of-three padding (AGENTS.md → Voice &
   tone)? 1 = still over-explains; 5 = states facts once, plainly.
3. **Technical fidelity** — does the rewrite preserve every technical claim from
   the original, without dropping or distorting one? 1 = drops or distorts a
   claim; 5 = fully preserves technical accuracy. A concise rewrite that damages
   technical fidelity never qualifies for the "recommend a cheaper model" arm,
   regardless of its concision score (see the spec's Behavior #4).

## Anonymization

The judge is never told which model produced the output it scores.
`build_judge_prompt` includes only the fixture's "before" text and the
candidate output — never a model name or id. Score each fixture/model output in
its own independent judge call so scoring one output never reveals another's
identity by comparison.

## Judge response format

Return a single JSON object with an integer 1-5 for each dimension:

```json
{"concision": 4, "avoids_over_explaining": 5, "technical_fidelity": 5}
```

`score_outputs.py score` reads this from a file via `--judge-response-file` and
parses it with `parse_judge_response`.

## Composite-score formula

- **Per-model, per-fixture composite** — simple average of the three dimension
  scores for that one output.
- **Per-model composite (report-level)** — average of the per-fixture
  composites across every fixture that model was scored on.
- **Per-model, per-dimension composite** (used for the Behavior #4
  concision-margin threshold) — average of that one dimension's score across
  every fixture, kept separate from the 3-dimension composite above.

## Judge-bias mitigation

Record which model, if any, served as judge in the eval report — a same-family
match between the judge and a candidate model is a reason for a reviewer to
discount that candidate's score. See `out_of_repo_handoff.md` for how to find
the model powering a given schedule or Agent Profile.
