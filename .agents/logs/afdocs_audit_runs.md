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

## 2026-09-04 — valid
- **Score**: 83/100 (B)
- **Checks**: 23 total — 16 pass, 2 fail, 3 warn
- **Failing check ids**: llms-txt-links-markdown, content-negotiation
- **Allowlisted**: 5
- **Oz run**: https://oz.warp.dev/runs/01a06b6e-9cba-7348-9467-9a7f8189886c
- **Notes**: Score down from 86/100 (2026-08-28) due to sampling: page-size-markdown, page-size-html, and markdown-content-parity warned this run (all allowlisted). Failing set unchanged (OpenAPI links in llms.txt; Vercel static Accept negotiation). No genuine remaining issues; skipped afdocs-fix.

## 2026-08-28 — valid
- **Score**: 86/100 (B)
- **Checks**: 23 total — 17 pass, 2 fail, 2 warn
- **Failing check ids**: llms-txt-links-markdown, content-negotiation
- **Allowlisted**: 4
- **Oz run**: https://oz.warp.dev/runs/01a04762-139a-7f02-8a22-28c574a00654
- **Notes**: Score up from 76/100 (2026-08-21). Both failures and both warnings match known-exceptions.md (OpenAPI links in llms.txt; Vercel static Accept negotiation; Turndown escaping parity; 1/50 sampled md page missing directive — sampling noise, /api.md has no Starlight md variant by design). No genuine remaining issues; skipped afdocs-fix. markdown-url-support 50/50. page-size checks passed this sample.

## 2026-08-21 — valid
- **Score**: 76/100 (C)
- **Checks**: 23 total — 15 pass, 4 fail, 2 warn
- **Failing check ids**: llms-txt-links-markdown, content-negotiation, page-size-html, markdown-content-parity
- **Allowlisted**: 4
- **Oz run**: https://oz.warp.dev/runs/01a02355-8faa-7396-9e54-e49391c8fb53
- **Notes**: All 4 failures match known-exceptions.md. Warnings: llms-txt-directive-html (48/49; 1 failed to fetch), llms-txt-directive-md (47/48; 2 no markdown). No genuine fixable site issues; first logged baseline on chore/afdocs-audit-log. markdown-url-support 100% (49/49). llms.txt coverage 100% of 377 sitemap pages.
