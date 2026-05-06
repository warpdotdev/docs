# AFDocs Known Exceptions

This file lists checks from the afdocs-audit skill that may flag as warnings or failures but are expected and intentional. When reporting audit results, classify these as "Allowlisted" rather than "Remaining."

## content-start-position

**Expected status**: fail or warn
**Reason**: Sampled pages may have content starting past 50% of the HTML output. This is inherent to Starlight's layout — sidebar navigation, header markup, and JavaScript/CSS precede the `<main>` content area.
**Mitigation**: The llms.txt directive, `<link rel="alternate" type="text/markdown">` in `<head>`, and `Accept: text/markdown` content negotiation middleware all steer agents to the clean markdown version, bypassing the HTML boilerplate entirely.
**Action**: No fix needed. This is a structural property of Starlight sites.

## markdown-content-parity

**Expected status**: warn (several pages, ~2% average difference)
**Reason**: False positive. The "missing" segments are numbered heading text like "2. Tabbed File Viewer" where Turndown correctly escapes the period (`### 2\. Tabbed File Viewer`) to prevent markdown parsers from interpreting it as a list item. The content IS present in the markdown — the AFDocs checker's text comparison doesn't account for markdown escaping.
**Affected pages** (as of 2026-05-05):
- `/agent-platform/cloud-agents/triggers/scheduled-agents-quickstart/` — step headings
- `/agent-platform/cloud-agents/integrations/github-actions/` — numbered use case headings
- `/support-and-community/troubleshooting-and-support/troubleshooting-login-issues/` — URLs with special chars
- `/reference/cli/quickstart/` — optional step headings
- `/guides/getting-started/welcome-to-warp/` — numbered section headings
- `/terminal/editor/vim/` — "See Vim docs:" link text
- `/guides/getting-started/10-coding-features-you-should-know/` — numbered feature headings
**Action**: No fix needed. Content is intact.

## page-size-markdown / page-size-html

**Expected status**: pass (after changelog split)
**Reason**: The changelog was split into yearly pages in May 2026, resolving the page-size issue. No pages should flag this check now.
**Action**: If any page is flagged, treat it as a genuine issue that may need splitting.

## section-header-quality

**Expected status**: skip
**Reason**: Only evaluated when tab panels contain section headers. Most sampled pages with tabs don't have headers inside the tab panels, so the check is skipped.
**Action**: None needed.

## auth-alternative-access

**Expected status**: skip
**Reason**: All docs pages are publicly accessible, so no alternative access path is needed.
**Action**: None needed.
