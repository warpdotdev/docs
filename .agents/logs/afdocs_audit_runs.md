# AFDocs audit run log

Written by the `afdocs-audit` skill on every scheduled run — clean, regressed, or blocked.

This log serves two purposes:

1. **Regression baseline.** The skill compares each run's score and failing-check set against the most recent entry marked `valid`. Entries marked `blocked` are skipped for comparison: a Vercel Firewall challenge makes every check a false positive, so its score is an artifact rather than a measurement.
2. **Proof a quiet run happened.** The skill only posts to Slack on a regression or a blocked audit, so a clean run is silent. This log is what distinguishes "ran, nothing to report" from "did not run."

Newest entries first. Prepend, do not append.

Entry format:

```markdown
## YYYY-MM-DD — [valid | blocked]
- **Score**: N/100 (grade)
- **Checks**: N total — N pass, N fail, N warn
- **Failing check ids**: comma-separated list, or "none"
- **Allowlisted**: N
- **Oz run**: [URL]
- **Notes**: [anything unusual]
```

For a `blocked` run, omit the score line rather than recording the meaningless value.

---
