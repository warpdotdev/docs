# PR review run log

New entries are written by the `improve-drafting-skills` outer loop during its monthly feedback collector step. Most recent entry first.

This is a human-readable audit trail of `review-docs-pr` runs on agent-authored PRs. It is **not** written directly by `review-docs-pr` — that skill emits `[SIGNAL:pr-review]` markers to stdout. The outer loop reads those markers from Oz run artifacts and appends entries here as part of its Step A collection.

**Format**:
```markdown
## YYYY-MM-DD — PR #NNN [Approve | Approve with nits | Request changes]
- **Branch**: docs/branch-name
- **Skill used**: draft_feature_doc
- **Critical**: 0 · **Important**: 2 · **Suggestions**: 4 · **Nits**: 1
- **Top issue categories**: header_case (2), list_format (1), missing_frontmatter_description (1)
- **Oz run**: [run URL]
```

---
