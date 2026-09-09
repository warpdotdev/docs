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

### Sampling variance

AFDocs samples ~50 of ~352 sitemap pages per run, so per-page checks can flip between `pass`, `warn`, and `fail` with no site changes. Re-run the audit before reporting a newly flagged per-page check as a regression, and report a check as reproducible only when it fails on both runs. See the "Sampling variance" section in `references/known-exceptions.md` for which checks fail deterministically.

## Invalid audits (Vercel Firewall challenge)

Before trusting any failures, confirm the audit was actually able to reach the
site. If `docs.warp.dev` is behind a **Vercel Firewall bot challenge** (Attack
Challenge Mode or the Bot Protection ruleset in challenge mode), every request
returns HTTP 429 with an `x-vercel-mitigated: challenge` header, the `afdocs`
crawler can't solve the JavaScript challenge, and **every check becomes a false
positive**. The score is meaningless and must not be reported as a regression.

The wrapper script (`scripts/afdocs_audit.mjs`) now runs a preflight check and
exits early with `status: "invalid"` (exit code `2`) when it detects this. If
you see that, do **not** post a score — report that the audit was blocked and
link the fix.

Confirm manually with:

```bash
curl -sS -D - -o /dev/null https://docs.warp.dev/llms.txt
```

A `429` plus `x-vercel-mitigated: challenge` (or an `x-vercel-challenge-token`
header) means the firewall is blocking the crawler. The fix is on the Vercel
side (disable Attack Mode, switch Bot Protection to log mode, or add a WAF
bypass rule for the runner) — the `afdocs` CLI can't send a bypass header. See
`references/vercel-firewall-challenge.md` for the full diagnosis and
remediation steps.

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

## Run log

Write a run log entry on **every** scheduled run — clean, regressed, or blocked. The log is what makes the regression comparison possible and what makes a silent run distinguishable from a broken one.

Use the standing log-branch pattern from `.agents/references/skill-authoring-guidelines.md`:

1. Fetch and check out `chore/afdocs-audit-log`. Create it from the latest `origin/main` if it does not exist.
2. Prepend the entry to `.agents/logs/afdocs_audit_runs.md`.
3. Verify the write with `head -10 .agents/logs/afdocs_audit_runs.md` before committing.
4. Stage only the log file and commit:
   ```text
   chore: log afdocs audit run YYYY-MM-DD
   ```
5. Push and verify with `git log --oneline -1 origin/chore/afdocs-audit-log`.
6. Ensure exactly one open PR exists from `chore/afdocs-audit-log` into `main`, titled `chore: afdocs audit run log`.

If any git step fails, write the entry to the run output and continue.

### Run log format

```markdown
## YYYY-MM-DD — [valid | blocked]
- **Score**: N/100 (grade)
- **Checks**: N total — N pass, N fail, N warn
- **Failing check ids**: comma-separated list, or "none"
- **Allowlisted**: N
- **Oz run**: [URL]
- **Notes**: [anything unusual]
```

For a firewall-blocked run, record `blocked`, omit the score entirely rather than logging the meaningless one, and note the mitigation status.

## Regression detection

Compare this run against the most recent **valid** entry in the run log — never against a `blocked` entry, whose score is an artifact of the firewall challenge rather than a real measurement. If there is no prior valid entry, this run establishes the baseline: log it and post nothing.

A run is a regression when either:
- The score dropped versus the last valid entry.
- A check id appears in this run's failing set that was not in the last valid entry's failing set.

## Slack notification

Post **only** when the run is actionable, per the actionable-only rule in `.agents/references/skill-authoring-guidelines.md`:

- **Regression detected** — post the summary below.
- **Audit blocked** by the Vercel Firewall challenge — post the blocked notice. This is a failure, so it always posts. Never post a score for a blocked run; every check is a false positive.
- **Clean run with no regression** — post nothing. The run log entry is the record.

A first-ever run with no baseline posts nothing.

1. Check if `BUZZ_SLACK_TOKEN` environment variable exists.
2. If the token exists, send the summary to the channel the user specified (or the channel configured in the agent's instructions).

**Format — regression:**

```
*AFDocs Audit — <date>* — regression
Score: <score>/100 (<grade>), down from <previous_score>/100 on <previous_date>
<total_checks> checks | <pass> pass, <fail> fail, <warn> warn

*New failures since last valid run (<count>):*
• <check_id>: <message>

*Pre-existing failures (<count>):*
• <check_id>: <message>

*Allowlisted (<count>):*
• <check_id>: <reason>
```

Lead with what changed. Pre-existing failures are context, not news — keep that list short or omit it when long.

**Format — audit blocked:**

```
*AFDocs Audit — <date>* — audit blocked, no score
The crawler was blocked by the Vercel Firewall bot challenge, so no checks could run.
Fix: disable Attack Mode, switch Bot Protection to log mode, or add a WAF bypass for the runner.
Details: references/vercel-firewall-challenge.md
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
