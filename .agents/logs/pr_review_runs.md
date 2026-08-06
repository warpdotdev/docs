# PR review run log

New entries are written by the `improve-drafting-skills` outer loop during its monthly feedback collector step. Most recent entry first.

This is a human-readable audit trail of `review-docs-pr` runs on agent-authored PRs. It is **not** written directly by `review-docs-pr` — that skill emits `[SIGNAL:pr-review]` markers to stdout. The outer loop reads those markers from Oz run artifacts and appends entries here as part of its Step A collection.

**Format**:
```markdown

## 2026-08-06 · improve-drafting-skills collector

- **Branch**: chore/drafting-signal-logs
- **Skill used**: improve-drafting-skills
- **Agent-related content PRs scanned**: 55
- **Fresh human feedback records**: 353 (new appended: 22)
- **Tagged skill-feedback**: 3
- **Top issue categories**: general (258), settings_path (17), content_structure (16), missing_media (11), link_quality (9), list_format (9), terminology (8), frontmatter (7)
- **Oz run signals (style-lint/pr-review markers)**: 0 parseable in sampled drafting runs
- **Notes**: Prior open improve PRs #450/#454/#468 and merged #478 already cover structure/callout/settings/media/frontmatter/list/link/ui patterns. New actionable gaps: vague_wording, action_first_instructions.

## 2026-08-04 — collector scan (no [SIGNAL:pr-review] markers)

- **Branch**: n/a
- **Skill used**: improve-drafting-skills feedback collector
- **Critical**: 0 · **Important**: 0 · **Suggestions**: 0 · **Nits**: 0
- **Top issue categories**: none (0 `[SIGNAL:pr-review]` / `[SIGNAL:style-lint]` markers found in title-matched Oz runs from `oz run list -L 100`; inner-loop markers still sparse)
- **Oz run**: collector-only for monthly improve-drafting-skills on 2026-08-04

## YYYY-MM-DD — PR #NNN [Approve | Approve with nits | Request changes]
- **Branch**: docs/branch-name
- **Skill used**: draft_feature_doc
- **Critical**: 0 · **Important**: 2 · **Suggestions**: 4 · **Nits**: 1
- **Top issue categories**: header_case (2), list_format (1), missing_frontmatter_description (1)
- **Oz run**: [run URL]
```

---
## 2026-08-05 — collector scan (no [SIGNAL:pr-review] markers)

- **Branch**: n/a
- **Skill used**: improve-drafting-skills feedback collector
- **Critical**: 0 · **Important**: 0 · **Suggestions**: 0 · **Nits**: 0
- **Top issue categories**: none (0 `[SIGNAL:pr-review]` / `[SIGNAL:style-lint]` markers found in title-matched Oz runs from `oz run list --limit 100`; pagination/cursor not available on this CLI build; inner-loop markers still sparse)
- **Oz run**: collector-only for monthly improve-drafting-skills on 2026-08-05
- **Human feedback collected**: 218 new review_comment/review_verdict records appended to `human_review_feedback.jsonl` from agent-coauthored merged PRs

## 2026-08-03 — collector scan (no [SIGNAL:pr-review] markers)
- **Branch**: n/a
- **Skill used**: improve-drafting-skills feedback collector
- **Critical**: 0 · **Important**: 0 · **Suggestions**: 0 · **Nits**: 0
- **Top issue categories**: none (0 markers across drafting-related Oz runs in the last 30 days)
- **Oz run**: collector-only; style-lint/pr-review inner-loop markers still absent

---
