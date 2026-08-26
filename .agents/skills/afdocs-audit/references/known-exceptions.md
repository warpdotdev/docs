# AFDocs Known Exceptions

This file lists checks from the afdocs-audit skill that may flag as warnings or failures but are expected and intentional. When reporting audit results, classify these as "Allowlisted" rather than "Remaining."

**Last verified**: 2026-07-31 against `afdocs@0.18.7` (two consecutive runs on `https://docs.warp.dev`).

## Sampling variance

AFDocs samples ~50 of ~352 sitemap pages per run, so which pages surface — and whether a check reports `pass`, `warn`, or `fail` — varies between runs. Two consecutive runs on 2026-07-31 produced different results for `llms-txt-directive-html` (warn, then pass) and `page-size-html` (fail, then pass) with no site changes in between.

Before treating a newly flagged check as a regression, re-run the audit. Only `content-negotiation`, `llms-txt-links-markdown`, and `markdown-content-parity` failed on both runs.

## content-negotiation

**Expected status**: fail
**Reason**: Vercel serves static files before evaluating rewrites. Since all doc pages are pre-rendered as static HTML, header-conditional rewrites (`Accept: text/markdown`) never fire — the CDN matches the static file first and returns HTML. Astro's `middlewareMode: 'edge'` also doesn't work because the edge function's `next()` forwards to `/_render`, which doesn't exist for static pages.
**Already attempted**: Both remediations the `afdocs-fix` skill suggests are already committed and still don't fire — `src/middleware.ts` (Astro middleware using `shouldServeMarkdown()`) and the `accept: .*text/markdown.*` header rewrites in `vercel.json`. Verified 2026-07-31: 0 of 48 sampled pages returned markdown. Do not "fix" this again by re-adding middleware.
**Mitigation**: The practical agent experience is already good despite this check failing:
- The llms.txt directive on every page tells agents that `.md` URLs are available
- `<link rel="alternate" type="text/markdown">` in `<head>` provides a machine-readable signal
- Agents that read either of these (Claude Code, Cursor, OpenCode) get clean markdown
- The `.md` URL convention works for every Starlight doc page (48/48 sampled)
**Action**: No fix available on Vercel's static hosting. Would require migrating to a platform where middleware runs before static file serving (e.g., Cloudflare Pages). Accept as a platform limitation.

## llms-txt-links-markdown

**Expected status**: fail
**Reason**: False positive caused by a threshold edge, not by a content gap. The check requires ≥90% of same-origin llms.txt links to serve markdown. Warp's llms.txt has 15 same-origin links: 13 `.txt` documentation sets (which AFDocs content-sniffs and correctly classifies as markdown) plus `openapi.yaml` and `openapi.json`. That yields 13/15 = 87%, just under the threshold. AFDocs also reports "no markdown alternatives detected" because `toMdUrls()` returns no `.md` candidates for non-page file extensions — so the two OpenAPI links can never satisfy the check, no matter what the site does.
**Affected links** (2 of 15 in llms.txt, configured via `optionalLinks` in `astro.config.mjs`):
- `https://docs.warp.dev/openapi.yaml`
- `https://docs.warp.dev/openapi.json`
**Action**: No fix needed. The OpenAPI specs are intentionally YAML/JSON and don't need markdown variants. Do not delete either link or pad llms.txt with extra links to clear the 90% threshold — both would degrade the file to satisfy a scorecard. Every link that represents documentation prose already serves markdown (13/13).

## llms-txt-directive-html / llms-txt-directive-md

**Expected status**: pass, with intermittent `warn` reporting "2 missing" or "2 had no markdown version"
**Reason**: False positive from page discovery, not a missing directive. AFDocs builds its page sample from the sitemap *and* from llms.txt links, and the top-level llms.txt walk in `walkAggregateLinksWithOriginals()` does not filter non-page file extensions. That pulls `openapi.yaml` and `openapi.json` into the sample as if they were pages. Neither is HTML, so the directive check records them as "not found," and neither has a `.md` variant, so the markdown check records them as "no markdown version."
**Verification**: A full crawl of all 352 sitemap pages on 2026-07-31, using AFDocs' exact detection logic (`LINK_PATTERN` / `TEXT_PATTERN` against the body with `<nav>`, `<script>`, and `<style>` stripped), found the directive present on every page, and buried past the 50% threshold on none. The directive is injected for Starlight pages by `src/components/CustomHeader.astro` and for `/api` by `src/pages/api.astro`.
**Related signal**: `llms-txt-coverage` passes but notes "2 llms.txt links not in sitemap" — the same two OpenAPI URLs.
**Action**: No fix needed. If this warn appears, confirm the count is 2 and that the missing entries are the OpenAPI specs before investigating further.

## markdown-content-parity

**Expected status**: warn or fail (varies by sample; a single flagged page can tip the check to fail)
**Reason**: False positive. The "missing" segments are numbered heading text like "2. Tabbed File Viewer" where Turndown correctly escapes the period (`### 2\. Tabbed File Viewer`) to prevent markdown parsers from interpreting it as a list item. The content IS present in the markdown — the AFDocs checker's text comparison doesn't account for markdown escaping. The specific page(s) flagged vary run to run because AFDocs samples a subset of pages.
**Affected pages** (2026-07-31 run: 41 pass, 8 warn, 1 fail, avg 2% missing):
- `/guides/configuration/creating-rules-for-agents/` — numbered walkthrough headings (fail bucket, 24% "missing" across 4 segments)
- `/guides/agent-workflows/run-a-software-factory-in-the-cloud/` — numbered step headings
- `/agent-platform/local-agents/interacting-with-agents/terminal-and-agent-modes/` — numbered setup headings
- `/enterprise/getting-started/getting-started-developers/` — numbered onboarding headings
- `/agent-platform/capabilities/skills/` — file-listing bullets (`check_links.py`, `config.yaml`)
**Earlier samples** (2026-05-05) additionally flagged `/platform/triggers/scheduled-agents-quickstart/`, `/platform/integrations/github-actions/`, `/support-and-community/troubleshooting-and-support/troubleshooting-login-issues/`, `/reference/cli/quickstart/`, `/guides/getting-started/welcome-to-warp/`, `/terminal/editor/vim/`, and `/guides/getting-started/10-coding-features-you-should-know/`.
**Action**: No fix needed. Content is intact. Confirm any newly flagged page shows escaped-period or list-punctuation diffs in `sampleDiffs` before treating it as a real gap.

## page-size-markdown / page-size-html

**Expected status**: `page-size-html` fail or pass depending on sampling; `page-size-markdown` currently pass
**Reason**: A small set of pages are intentionally long and cannot be meaningfully split. They exceed the AFDocs 100K-char hard-fail threshold, so `page-size-html` fails on any run that samples one of them. The `afdocs-fix` skill explicitly treats page-size as a do-not-auto-fix editorial concern.
**Affected pages** (markdown character counts measured 2026-07-31):
- `/support-and-community/community/open-source-licenses/` — auto-generated third-party license text (~1.37M md chars, ~7.8M HTML chars). Regenerated by the `release_updates` skill; any manual split would be overwritten. Excluded from `llms-small.txt` and `llms-full.txt` via `exclude` in `astro.config.mjs` because it overflows `hast-util-to-text`.
- `/changelog/2026/` — current-year changelog (~154K md chars). Already split by year; the current year grows until year-end rollover.
- `/support-and-community/privacy-and-security/privacy/` — comprehensive privacy and legal content (~112K md chars). Kept whole for legal completeness.
These are the only three pages on the site over 100K markdown chars. `/terminal/settings/all-settings/` was previously flagged as borderline but is now ~40K md chars and no longer a concern.
**Action**: No fix. These pages are intentionally long (auto-generated, current-year changelog, or legal). Do not split. Re-evaluate `/changelog/2026/` at year-end when it rolls over to `/changelog/2027/`.

## content-start-position

**Expected status**: pass (previously fail or warn)
**Reason**: Historically flagged because Starlight's sidebar navigation, header markup, and JavaScript and CSS precede the `<main>` content area. Current AFDocs versions measure the content offset within the searchable `<body>` after stripping `<nav>`, `<script>`, and `<style>`, so Warp's pages now report a median start position of 0% (2026-07-31: all 50 sampled pages start within the first 10%).
**Mitigation** (if it regresses): the llms.txt directive, `<link rel="alternate" type="text/markdown">` in `<head>`, and the `.md` URL convention all steer agents to the clean markdown version, bypassing the HTML boilerplate entirely.
**Action**: None needed. Treat a re-appearance as a structural property of Starlight sites rather than a content problem.

## markdown-url-support

**Expected status**: pass (previously fail for `/api`)
**Reason**: `/api` is a custom Astro page (`src/pages/api.astro`), not a Starlight content page. The docs-markdown integration only generates `.md` variants for Starlight doc pages under `src/content/docs/`, so `/api.md` returns 404. Current AFDocs versions exclude `/api` from the eligible page set, so the check reports 48/48 (100%).
**Action**: No fix needed. This page is intentionally outside the Starlight content pipeline. If `/api` is flagged again, allowlist it rather than generating a stub `/api.md`.

## section-header-quality

**Expected status**: skip
**Reason**: Only evaluated when tab panels contain section headers. Most sampled pages with tabs don't have headers inside the tab panels, so the check is skipped (2026-07-31: 6 pages with tabs, no headers inside panels).
**Action**: None needed.

## auth-alternative-access

**Expected status**: skip
**Reason**: All docs pages are publicly accessible, so no alternative access path is needed.
**Action**: None needed.
