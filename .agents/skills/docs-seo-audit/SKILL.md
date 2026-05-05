---
name: docs-seo-audit
description: >-
  Audit docs.warp.dev for SEO issues like duplicate titles, missing meta
  descriptions, title length problems, and H1 tag issues. Crawls the live
  sitemap, generates a report, and fixes issues in the source markdown. Use
  when asked to check SEO, fix duplicate titles, audit meta tags, improve
  search rankings, or run an SEO check on the docs site.
---

# SEO Audit

Crawl the live docs.warp.dev sitemap to find SEO issues and fix them in the source markdown files.

## Running the audit

From the docs repo root:

```bash
python3 .warp/skills/docs-seo-audit/scripts/seo_audit.py \
  --repo-root . \
  --output /tmp/seo-report.json
```

The script fetches all pages listed in `https://docs.warp.dev/sitemap.xml` (a sitemap index including sub-sitemaps), extracts SEO metadata from each page's HTML, and checks for issues.

### Options

- `--repo-root PATH` — Path to the docs repo root. Enables mapping live URLs to local source files in the report.
- `--output FILE` — Write the JSON report to a file (otherwise prints to stdout).
- `--max-pages N` — Limit to the first N pages (useful for quick testing).
- `--workers N` — Number of concurrent fetch workers (default: 6).

### Quick test with a small sample

```bash
python3 .warp/skills/docs-seo-audit/scripts/seo_audit.py --repo-root . --max-pages 20 --output /tmp/seo-sample.json
```

## Reading the report

The JSON report contains:
- `total_pages` — Number of pages scanned
- `total_issues` — Total issues found
- `by_severity` — Counts by severity (`error`, `warning`, `info`)
- `by_type` — Counts by issue type
- `issues` — Array of individual issues, sorted by severity

Each issue includes:
- `url` — The live page URL
- `source_file` — The local markdown file (if `--repo-root` was provided)
- `severity` — `error` (must fix), `warning` (should fix), or `info` (nice to fix)
- `type` — Issue category (see below)
- `message` — Human-readable description

### Issue types

**Errors (must fix)**:
- `duplicate_title` — Multiple pages share the same `<title>` tag. Hurts search rankings and confuses users.
- `missing_title` — Page has no `<title>` tag.
- `fetch_error` — Page could not be fetched.

**Warnings (should fix)**:
- `duplicate_description` — Multiple pages share the same meta description.
- `missing_description` — Page has no meta description. Search engines may generate a snippet from page content instead.
- `title_too_short` — Title under 20 chars; may not be descriptive enough for search results.
- `title_too_long` — Title over 70 chars; Google will truncate it in search results.
- `missing_h1` — No H1 heading found on the page.
- `multiple_h1` — More than one H1 heading on the page.

**Info (nice to fix)**:
- `description_too_short` — Description under 50 chars.
- `description_too_long` — Description over 160 chars; will be truncated in search results.
- `og_title_mismatch` — OG title differs from the title tag (usually auto-matched by Astro Starlight).
- `og_description_mismatch` — OG description differs from the meta description.

## Reporting results

After running the audit, ALWAYS report the results to the user before taking any action. Include:

1. **Summary**: Total pages scanned, total issues, breakdown by severity (errors / warnings / info)
2. **Errors first**: List every error-severity issue with the URL, source file, and what's wrong. These are the most impactful and should be fixed.
3. **Warnings**: Summarize warning-severity issues grouped by type (e.g., "58 pages missing meta descriptions"). List specific pages only for the most impactful ones (duplicate titles, duplicate descriptions).
4. **Info**: Briefly note info-level issues with counts. No need to list every page.
5. **If no issues found**: Explicitly tell the user everything looks clean — don't just silently finish.

Example report format:
```
SEO audit complete: 276 pages scanned, 183 issues found.

**Errors (8):**
- Duplicate title "Overview | Agents | Warp" on 4 pages:
  - /agent-platform (source: src/content/docs/agent-platform/index.mdx)
  - /agent-platform/local-agents/overview (source: src/content/docs/agent-platform/local-agents/overview.mdx)
  ...

**Warnings (108):**
- 58 pages missing meta descriptions (top offenders: ...)
- 33 titles too short (<20 chars)
- 15 titles too long (>70 chars)

**Info (67):**
- 55 descriptions over 160 chars
- 12 descriptions under 50 chars
```

After reporting, ask the user which issues they want to fix before making changes.

## Fixing issues

Before making any changes, read these references:
1. `references/gitbook-seo.md` in this skill directory — explains the non-obvious way Astro Starlight generates title tags from astro.config.mjs (sidebar config) link text (not the H1 heading).
2. `AGENTS.md` at the docs repo root — the single source of truth for documentation style, voice, terminology, and formatting. All titles and descriptions you write must follow these conventions (terminology, sentence case, active voice, frontmatter description format).

### Key principles

1. **Title tags come from astro.config.mjs (sidebar config) link text**, not the H1 heading. To fix a title, change the link text in the relevant space's `astro.config.mjs (sidebar config)`.
2. **Meta descriptions come from frontmatter**. To fix a description, edit the `description:` field in the page's YAML frontmatter.
3. **OG and Twitter tags mirror title and description** automatically. No separate fix needed.
4. **Changing astro.config.mjs (sidebar config) link text has side effects**: it also changes the sidebar label, breadcrumbs, and prev/next pagination. URLs are NOT affected.
5. **When changing a title, also update the H1** in the markdown file for consistency.

### Title exceptions

Some page titles are intentionally short or specific and must **not** be changed, even if they trigger a `title_too_short` warning. Skip these pages and note them as intentional exceptions in your report:

- **`src/content/docs/changelog/README.md`** (`Changelog`) — "Changelog" is a clear, universally understood industry term. Branding prefixes like "Warp changelog" or "Release changelog" add no descriptive value and this title should remain as-is.
- **`src/content/docs/terminal/appearance/app-icons.md`** (`App icons`) — The article explicitly explains that *custom* app icons are not available to users. Renaming to "Custom app icons" directly contradicts the page content and must be avoided.
- **`src/content/docs/university/README.md`** (`Guides`) — "Guides" is the landing page for the Guides space. The title is clear and matches the space name; prefixing it (e.g., "Developer Guides") adds no value and creates a mismatch with the space title shown in breadcrumbs.

When the audit flags these pages for `title_too_short`, exclude them from your fix list and include a note in your report explaining they are intentional exceptions.

If you believe a new title should be added to this exceptions list, flag it for human review before proceeding.

### Fixing duplicate titles

This is the most impactful issue. Common causes:
- Multiple pages named `[Overview](...)` under different sections of the same space
- Generic names like `[Getting Started](...)` or `[FAQs](...)` repeated across sections

Fix by making each astro.config.mjs (sidebar config) link text unique and descriptive. The link text should identify the specific topic, not just the page type. Use sentence case and correct terminology per `AGENTS.md` (e.g., capitalize product feature names like "Agent Mode", "Warp Drive", "Codebase Context"). Example:
- Before: `[Overview](local-agents/overview.mdx)` + `[Overview](cloud-agents/overview.md)`
- After: `[Local Agents Overview](local-agents/overview.mdx)` + `[Cloud Agents Overview](cloud-agents/overview.md)`

### Fixing missing descriptions

Add a `description` field to the page's frontmatter:

```yaml
---
description: >-
  A concise 1-2 sentence summary of what this page covers and what
  value it provides to the reader.
---
```

Write descriptions that:
- Summarize the page's content in 50-160 characters
- Include the primary keyword/topic naturally
- Describe user benefit, not just feature existence
- Follow the voice and terminology conventions in `AGENTS.md` (e.g., use "Warp" not "Warp Terminal", "Oz" for the orchestration platform, active voice, user-focused phrasing)

### Review loop

After making fixes, review every change before presenting to the user. Run through this checklist, and if anything fails, fix it and re-run the checklist from the top. Only present changes when everything passes.

- **Does this still mean the same thing?** Titles and descriptions must accurately represent the page content. Read the actual page before writing or rewriting anything. Never invent features, capabilities, or details that aren't on the page. If unsure what the page covers, read it first.
- **Did I introduce a new duplicate?** Scan the full astro.config.mjs (sidebar config) for the space you edited. Verify every link text is unique. This is the most common mistake — fixing one duplicate by picking a name that collides with an existing entry.
- **Does the H1 match?** Every astro.config.mjs (sidebar config) title change needs a corresponding H1 update in the markdown file. Mismatches between sidebar label and page heading confuse readers.
- **Is the terminology right?** Cross-check against `AGENTS.md` and how the feature is actually referred to in the existing docs. Don't rename things to terms that aren't used elsewhere in the docs.
- **Does this read naturally in context?** Consider how the title appears (a) as a sidebar label under its section header, and (b) as a search result: `{Title} | {Space} | Warp`. If it sounds awkward or uses internal jargon that users wouldn't recognize, rephrase.
- **Are descriptions grounded in page content?** Don't write descriptions based on the title alone. Read the page, then summarize what's actually there.
- **Any other improvements nearby?** Look at adjacent entries in the astro.config.mjs (sidebar config). Are there other generic titles ("Overview", "Getting Started", "FAQ") that could become duplicates in the future? Flag them proactively.

### Delivering changes

**Interactive (user in the loop):** Present the full list of changes with old → new values so the user can review at a glance. Wait for approval before committing.

**Autonomous (scheduled agent, CI):** The review loop above is your quality gate. Commit directly and include the old → new summary in the PR description.

**PR conventions:**
- Title must be prefixed with `Automated SEO fixes:` (e.g., `Automated SEO fixes: resolve duplicate titles in agent-platform and reference spaces`)
- Add the `seo` label to the PR (e.g., `gh pr create --label seo`)

## Slack notification (optional)

If instructed to send a report to Slack, post a summary after the audit completes. This works regardless of whether fixes were made.

1. Check if `BUZZ_SLACK_TOKEN` environment variable exists.
2. If the token exists, send a summary to the channel the user specified (or the channel configured in the agent's instructions).

**Categorizing issues in the summary:** Before composing the message, cross-reference every issue against the title exceptions list above and check whether the issue has a local source file. Classify each issue into exactly one bucket:
- **Fixed** — issues you resolved in this run
- **Unfixable** — issues with no local source file (e.g., auto-generated API pages)
- **Allowlisted** — issues that match a title exception entry (these are intentional, not problems)
- **Remaining** — everything else (genuine issues that still need attention)

Only include a section in the Slack message if its count is > 0. Never list allowlisted pages under "Remaining".

**If a PR was opened**, include the PR link and a summary of what was fixed:

```
*SEO Audit — <date>*
<total_pages> pages scanned | <total_issues> issues found

*Fixed (<count>):*
• Duplicate title "Overview | Agents | Warp" → split into 4 unique titles
• Trimmed 3 overly long descriptions to ≤160 chars

*Unfixable (<count>):*
• <N> pages missing meta descriptions (auto-generated, no local source)

*Allowlisted (<count>):*
• <page1>, <page2>, <page3> (intentionally short titles)

*Remaining (<count>):*
• <N> pages missing meta descriptions
• <N> titles too short/long

PR: <pr_url>
```

**If no issues were found:**

```
*SEO Audit — <date>*
<total_pages> pages scanned | ✅ No issues found
```

**If issues were found but no fixes made** (report-only run):

```
*SEO Audit — <date>*
<total_pages> pages scanned | <total_issues> issues found (<errors> errors, <warnings> warnings, <info> info)

*Unfixable (<count>):*
• <N> pages missing meta descriptions (auto-generated, no local source)

*Allowlisted (<count>):*
• <page1>, <page2> (intentionally short titles)

*Remaining (<count>):*
• <N> duplicate titles
• <N> pages missing meta descriptions
• <N> titles too short/long
```

Send using:

```bash
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $BUZZ_SLACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "<CHANNEL_ID>",
    "text": "<formatted_summary>",
    "unfurl_links": false,
    "unfurl_media": false
  }'
```

If `BUZZ_SLACK_TOKEN` is not set, skip the notification and note that the token is required.

## Dependencies

Python 3.7+ with only standard library modules (no pip install required).

## Checks performed

- Duplicate `<title>` tags across all pages
- Duplicate `<meta name="description">` across all pages
- Missing title or description
- Title length outside 20-70 char range
- Description length outside 50-160 char range
- Missing or multiple `<h1>` headings
- Mismatches between title/OG title and description/OG description
- URL-to-source-file mapping for actionable fixes
