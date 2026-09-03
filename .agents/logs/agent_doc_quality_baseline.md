# Agent-doc quality v1 baseline log (GROW-6092)

Durable record of the pre-rollout baseline window and the post-rollout
comparison window used by `improve-drafting-skills`'s
`scripts/compute_metrics.py` (see that skill's "v1 baseline and outcome
metrics" section). Each entry names the window, the record source, and where
the resulting report was persisted (the standing signal-log branch/PR, per
`.agents/references/skill-authoring-guidelines.md`).

Entries are appended, never rewritten — the baseline entry is captured once,
immediately before v1 checks/labels/review go live, and is never recomputed.

## Entries

### 2026-08-01 to 2026-08-30 — pre-rollout baseline

Captured from the existing `.agents/logs/human_review_feedback.jsonl` signal
log (real per-comment data already collected by `improve-drafting-skills`,
covering 2026-06-29 through 2026-08-31) plus live `gh pr view` line-count
lookups against `warpdotdev/docs`, using
`scripts/build_baseline_records.py` to convert the comment-level log into
per-PR records and `scripts/compute_metrics.py` to compute the report. This
is the last full 30-day window available in the existing log before this v1
rollout PR, so it is used as the frozen pre-rollout baseline rather than
waiting for a window that starts exactly at rollout.

- **Records**: `.agents/logs/baseline/pre-rollout-2026-08-01-to-2026-08-30.jsonl` (62 PRs)
- **Report**: `.agents/logs/baseline/pre-rollout-2026-08-01-to-2026-08-30-report.json`
- **In-scope PRs**: 62
- **Human review comments/PR**: mean 5.19, median 1.0
- **Human edit churn ratio**: mean 0.0021, median 0.0
- **Gate coverage**: 0/62 (expected — the v1 checks did not exist during this window; `risk`/`check_outcome`/`review_outcome` are recorded as `"unknown"` per the documented pre-rollout degradation, not fabricated as passing)

The post-rollout 30-day comparison report must be computed the same way
(`compute_metrics.py --baseline .agents/logs/baseline/pre-rollout-2026-08-01-to-2026-08-30-report.json`)
and appended below as a new dated entry once 30 days of post-rollout data
(or 10 in-scope PRs, whichever comes first per the small-sample rule) exist.
