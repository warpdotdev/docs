# AFDocs audit run log

## 2026-10-30 — partial
- **Spec**: v0.6.0 — native afdocs CLI score
- **Score**: 83/100 (B) — partial-sample observation only; excluded from regression comparisons and future baselines.
- **Reliability**: partial operational assessment. The wrapper reports scan_reliability=complete and no bot-protection interference across 532 requests, but llms-txt-directive-html and markdown-content-parity each disclose one failed fetch.
- **Checks**: 28 total — 19 pass, 2 fail, 5 warn, 2 skip
- **Failing check ids**: llms-txt-links-markdown, content-negotiation
- **Allowlisted**: 2 (llms-txt-links-markdown, content-negotiation)
- **Oz run**: https://staging.warp.dev/conversation/9fbf36f3-2de6-4bde-bff6-94f64c87f0a6
- **Notes**: Audit command exited 0; afdocs-report.json retained as a run artifact. Most recent comparable complete baseline is the first 2026-10-23 entry on this standing branch (native v0.6.0); this partial run is not compared against it. Partial, blocked, legacy, and compatibility results cannot establish a native-score regression baseline. Both failures match known exceptions: intentional OpenAPI YAML/JSON links and Vercel static content negotiation. Five remaining warning observations: llms-txt-directive-md (49/50 directives); page-size-markdown (1/50, max 60K characters); page-size-html (2/50, max 258K HTML converting to 66K markdown); markdown-link-portability (1/50 with a root-relative link); embedded-data-serialization (1/50, a 634-row table occupying 84% of 66K converted characters). Affected URLs and fetch error details are absent from the wrapper report, so long-page exceptions cannot be confirmed and these warnings remain observations pending reliable diagnosis. Diagnostic interaction dynamic-content-rendered-statically groups the size and serialization warnings; it is not an additional scored failure. Owner action: identify the failed HTML fetch and affected warning pages, then obtain a complete scan before remediation. No afdocs-fix invocation, automatic fixes, page splitting, CDN/WAF changes, or standalone schedule changes. Node.js 24, npm 11, GitHub access, and connected Slack MCP channel access verified. Existing log history preserved in an isolated worktree. Public-doc validation suite not run because this is a log-only change; Trunk is not installed.

## 2026-10-23 — valid
- **Spec**: v0.6.0 — native afdocs CLI score
- **Score**: 90/100 (A-)
- **Reliability**: complete; no bot-protection interference across 531 requests.
- **Checks**: 28 total — 23 pass, 2 fail, 1 warn, 2 skip
- **Failing check ids**: llms-txt-links-markdown, content-negotiation
- **Allowlisted**: 3 (llms-txt-links-markdown, content-negotiation, markdown-content-parity)
- **Oz run**: https://staging.warp.dev/conversation/2e199e33-8236-4eeb-8f4e-1f9db5b02cbc
- **Notes**: Audit command exited 0; report retained as a run artifact (afdocs-report.json). Comparable baseline is the earlier complete 2026-10-23 entry on this standing branch, 92/100 with the same spec and native score method. Score decreased by 2 points, meeting the score-drop regression rule; no newly failing check IDs. The additional warning is minor markdown/HTML parity differences on 1/50 sampled pages, matching the documented escaping/sampling exception; the wrapper does not retain the affected page details. Both failures match known exceptions: intentional OpenAPI YAML/JSON links and Vercel static content negotiation. No remaining repo-fixable findings; afdocs-fix not invoked. No diagnostic interaction effects. Partial, blocked, legacy, and compatibility entries excluded from this native-score comparison. Node.js 24, npm, GitHub access, and connected Slack MCP channel access verified. Earlier unmerged entry preserved; no CDN/WAF changes, public-doc edits, or standalone schedule changes.

## 2026-10-23 — valid
- **Spec**: v0.6.0 — native afdocs CLI score
- **Score**: 92/100 (A-)
- **Checks**: 28 total — 24 pass, 2 fail, 0 warn
- **Failing check ids**: llms-txt-links-markdown, content-negotiation
- **Allowlisted**: 2
- **Oz run**: https://platform.warp.dev/runs/01a167c6-317a-74b9-a39f-efdd414f1efa
- **Notes**: Complete scan. Both failures allowlisted (OpenAPI YAML/JSON links in llms.txt; Vercel static hosting cannot honor Accept: text/markdown). No remaining fixable issues; afdocs-fix skipped. Score up from 83/100 on 2026-10-09 (page-size-html no longer failing). No regression.

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

## 2026-10-09 — valid
- **Spec**: v0.6.0 — native afdocs CLI score
- **Score**: 83/100 (B)
- **Checks**: 28 total — 20 pass, 3 fail, 3 warn, 2 skip
- **Failing check ids**: llms-txt-links-markdown, content-negotiation, page-size-html
- **Allowlisted**: 3 (llms-txt-links-markdown, content-negotiation, page-size-html)
- **Oz run**: https://platform.warp.dev/runs/01a11fad-29bf-7edf-9f65-8dd3b4aa4c6e
- **Notes**: Complete scan (scan_reliability=complete; bot-protection-interference passed across 530 requests). Score unchanged vs 2026-10-02 baseline (83/100). Failing set is a subset of the prior baseline (embedded-data-serialization no longer failing this sample). All three failures match known-exceptions.md. Warnings: llms-txt-directive-html/md 48/49 sampling noise; markdown-link-portability 1/49 root-relative. No fixable remaining issues; skipped afdocs-fix.

## 2026-10-02 — valid
- **Spec**: v0.6.0 — native afdocs CLI score
- **Score**: 83/100 (B)
- **Checks**: 28 total — 21 pass, 4 fail, 1 warn, 2 skip
- **Failing check ids**: llms-txt-links-markdown, content-negotiation, page-size-html, embedded-data-serialization
- **Allowlisted**: 3 (llms-txt-links-markdown, content-negotiation, page-size-html)
- **Oz run**: https://platform.warp.dev/runs/01a0fba0-a688-70c6-9eaf-4e5e172c1da1
- **Notes**: First complete v0.6 scan with native CLI score method; establishes new regression baseline (prior 2026-09-18/09-25 were partial/unweighted). scan_reliability=complete; bot-protection-interference passed (534 requests). Remaining non-auto-fixable: embedded-data-serialization (1/50 sample; ~139K JSON blob dominating converted content — design/IA, not docs-repo fix). page-size-html matches known intentionally-long pages. Warning llms-txt-directive-html 49/50 sampling noise. Interaction effect: dynamic-content-rendered-statically (diagnostic). No fixable remaining issues; skipped afdocs-fix.

## 2026-09-25 — partial
- **Spec**: v0.6.0 — unweighted compatibility estimate; warnings count as half-passes
- **Score**: 86/100 (B)
- **Checks**: 28 total — 21 pass, 3 fail, 1 warn, 3 skip
- **Failing check ids**: llms-txt-links-markdown, content-negotiation, bot-protection-interference
- **Allowlisted**: 3 (llms-txt-links-markdown, content-negotiation, markdown-content-parity)
- **Oz run**: https://platform.warp.dev/runs/01a0d794-224a-7de1-ad20-3fdf3c3ae441
- **Notes**: bot-protection-interference 8/16 sustained fetches hit challenge pages (scan_reliability=partial); legacy_cli_score=88/100; no remaining fixable docs-repo issues; interaction effect bot-protection-degrading-scan-reliability observed. Score omitted from regression comparison because scan was partial.

## 2026-09-18 — partial
- **Spec**: v0.6.0 — unweighted compatibility estimate; warnings count as half-passes
- **Score**: 76/100 (C) — partial sample; do not use for regression baseline
- **Checks**: 28 total — 18 pass, 5 fail, 2 warn, 3 skip
- **Failing check ids**: llms-txt-links-markdown, content-negotiation, page-size-html, markdown-content-parity, bot-protection-interference
- **Allowlisted**: 4 (llms-txt-links-markdown, content-negotiation, page-size-html, markdown-content-parity)
- **Oz run**: https://platform.warp.dev/runs/01a0b387-9dec-7160-9308-7c2e24e86df5
- **Notes**: scan_reliability=partial (bot-protection-interference 8/16 sustained fetches hit challenge pages). legacy_cli_score=79/100. Prior valid baseline 2026-09-11 was legacy 23-check (86/100); this is first v0.6 compatibility log entry and establishes a new baseline once a complete scan succeeds. Remaining genuine: bot-protection (WAF, out of repo). Fixable warn markdown-link-portability addressed in PR #763 (afdocs-fixes). llms-txt-directive-html 49/50 sampling noise. Interaction effects: bot-protection-degrading-scan-reliability, dynamic-content-rendered-statically.

## 2026-09-11 — valid
- **Score**: 86/100 (B)
- **Checks**: 23 total — 18 pass, 3 fail, 0 warn
- **Failing check ids**: llms-txt-links-markdown, content-negotiation, markdown-content-parity
- **Allowlisted**: 3
- **Oz run**: https://oz.warp.dev/runs/01a08f7b-1b0e-73ce-8962-f1327cd1c71b
- **Notes**: Score up from 83/100 (2026-09-04). All three failures match known-exceptions.md (OpenAPI links in llms.txt; Vercel static Accept negotiation; Turndown escaping parity on 1/50 sampled pages). markdown-content-parity moved warn→fail due to sampling; not a genuine regression. No remaining fixable issues; skipped afdocs-fix.

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
