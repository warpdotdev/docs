---
name: afdocs-audit
description: >-
  Audit docs.warp.dev for agent-friendly documentation issues using the AFDocs
  scorecard. Checks llms.txt, markdown availability, content negotiation, page
  size, URL stability, and content structure. Use when asked to check agent
  readiness, run an AFDocs audit, improve the docs score, or verify llms.txt
  and markdown support.
---

# AFDocs Audit

Run the [AFDocs scorecard](https://agentdocsspec.com/spec/) against docs.warp.dev and report results.

## Running the audit

From the docs repo root:

```bash
node .agents/skills/afdocs-audit/scripts/afdocs_audit.mjs \
  --output /tmp/afdocs-report.json
```

The script runs `npx afdocs check https://docs.warp.dev --format json`, parses the output, and writes a structured report.

### Options

- `--output FILE` — Write the JSON report to a file (otherwise prints to stdout).
- `--url URL` — Override the site URL (default: `https://docs.warp.dev`).

## Reading the report

The JSON report contains:
- `score` — Overall score out of 100
- `grade` — Letter grade (A+ through F)
- `total_checks` — Number of checks run
- `summary` — Counts by status (`pass`, `fail`, `warn`, `skip`)
- `categories` — Per-category scores and grades
- `issues` — Array of failing and warning checks with details and fix guidance

Each issue includes:
- `id` — Check identifier (e.g., `llms-txt-directive-html`)
- `category` — Check category (e.g., `content-discoverability`)
- `status` — `fail` or `warn`
- `message` — Human-readable description
- `fix` — Suggested fix from the AFDocs spec

### Known exceptions

Before reporting, cross-reference every issue against the known exceptions in `references/known-exceptions.md`. Classify each issue into exactly one bucket:
- **Allowlisted** — known exceptions that are intentional (not problems)
- **Remaining** — genuine issues that need attention

Only include a section if its count is > 0. Never list allowlisted issues under "Remaining."

## Reporting results

After running the audit, ALWAYS report the results to the user before taking any action. Include:

1. **Score**: Overall score and grade
2. **Failures first**: List every fail-severity check with its message and fix guidance. These are the most impactful.
3. **Warnings**: List warning-severity checks with context.
4. **Allowlisted**: Briefly note any known exceptions that were flagged.
5. **If all checks pass**: Explicitly tell the user everything looks clean.

Example report format:
```
AFDocs audit complete: 23 checks run, score 82/100 (B).

**Failures (5):**
- llms-txt-directive-html: No llms.txt directive in HTML pages
  Fix: Add a visually-hidden element near the top of each page with a link to /llms.txt
- content-negotiation: Server ignores Accept: text/markdown
  Fix: Add middleware to serve .md variants when Accept: text/markdown is requested

**Warnings (1):**
- llms-txt-coverage: 80% of sitemap pages covered (247/308)

**Allowlisted (2):**
- page-size-markdown: 1 page over 50K (changelog — intentionally long)
- markdown-content-parity: 7 pages with minor diffs (Turndown escaping, not real content gaps)
```

After reporting, ask the user which issues they want to address.

## Slack notification (optional)

If instructed to send a report to Slack, post a summary after the audit completes.

1. Check if `BUZZ_SLACK_TOKEN` environment variable exists.
2. If the token exists, send a summary to the channel the user specified (or the channel configured in the agent's instructions).

**Format:**

```
*AFDocs Audit — <date>*
Score: <score>/100 (<grade>) | <total_checks> checks | <pass> pass, <fail> fail, <warn> warn

*Failures (<count>):*
• <check_id>: <message>

*Warnings (<count>):*
• <check_id>: <message>

*Allowlisted (<count>):*
• <check_id>: <reason>
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

Node.js 18+ with npm (for `npx afdocs`). No additional install required — `afdocs` is fetched on demand by npx.

## Checks performed

The AFDocs scorecard evaluates these categories:

**Content Discoverability** — llms.txt existence, validity, size, link resolution, markdown links, and in-page directives
**Markdown Availability** — .md URL support and Accept: text/markdown content negotiation
**Page Size and Truncation Risk** — rendering strategy, page sizes (markdown and HTML), and content start position
**Content Structure** — tabbed content serialization, section header quality, code fence validity
**URL Stability and Redirects** — HTTP status codes and redirect behavior
**Observability and Content Health** — llms.txt coverage, markdown/HTML parity, cache headers
**Authentication and Access** — auth gate detection and alternative access paths

Full spec: https://agentdocsspec.com/spec/
