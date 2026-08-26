---
name: weekly-404-monitor
description: Weekly recurring agent that surfaces broken docs.warp.dev URLs by querying the docs_404 Rudderstack track event, diffing against existing vercel.json redirects, and posting a summary to Slack. Use for the Monday 9am PT scheduled Oz agent that monitors 404 gaps and supports the ongoing redirect-fix workflow.
---

# Weekly 404 monitor

Runs every Monday at 9am PT. Leads with the overall 404 volume trend, surfaces the uncovered paths that get enough traffic to be worth a redirect, and posts a concise Slack summary so the docs team can prioritize redirect additions without being distracted by long-tail bot/old-link noise.

## Prerequisites

The following environment secrets must be set in the Oz cloud agent environment:

- `METABASE_API_KEY` — Metabase API key for BigQuery queries. If unavailable, the run must fail fast with a clear error.
- `BUZZ_SLACK_TOKEN` — Slack bot token for posting to the docs channel. If unavailable, write a no-post report to the run output instead.

The `#growth-docs` Slack channel ID is `C09BVK0PL3Y`. Use this value directly when posting — it does not need to be an environment variable.

Do NOT print, log, or include secret values in reports, commits, or Slack messages.

## Workflow

### 1. Query docs_404 events

Run `python3 .agents/skills/weekly-404-monitor/run_404_report.py` in the docs repo.

The script:
- Queries `warp-data-357114.prod.stg_website_events` via the Metabase API
- Extracts `broken_url` from `event_properties` for all `event_name = 'docs_404'` events in the past 7 days
- Normalises and groups by path **in SQL** (lowercase, no trailing slash, no scheme/host, no query/fragment) so trailing-slash, case, and host variants of the same page are summed into one row *before* the top-500 cap is applied — a page whose hits are split across variants can't be dropped by the cap and undercounted
- Returns a ranked list of broken pages and their hit counts for the current week, sorted by hit count descending
- Re-applies the same normalisation in Python as an idempotent safety net
- Computes the same for the prior week (days 8–14) for trend comparison
- Total weekly 404 count (current + prior) for the trend line

### 2. Fetch current vercel.json redirect sources

Fetch `vercel.json` from the docs repo (already checked out locally in the cloud environment, or via GitHub raw URL `https://raw.githubusercontent.com/warpdotdev/docs/main/vercel.json`).

Extract all `source` values from the `redirects` array. Normalise: lowercase, strip trailing slashes and anchor fragments.

### 3. Find uncovered URLs

Broken URLs are first aggregated by their normalised form, so `/foo`, `/foo/`, and `/Foo` collapse into one page with summed hits (this prevents the same page being reported as several separate gaps). For each aggregated page:
- Normalise (lowercase, strip trailing slash, strip query params and fragments)
- Check if it exists as a `source` in `vercel.json` redirects
- If not covered, it is a **gap**

### 4. Compute delta vs prior week

Compare this week's uncovered gaps against last week's uncovered gaps (from step 1 prior-week query).

**New gaps** = uncovered this week AND not seen as uncovered last week.
**Resolved** = uncovered last week AND now either covered (has redirect) or no longer generating 404s.

**Significant vs long-tail.** Split uncovered URLs by the reporting threshold (`REPORT_MIN_HITS`, default 5; must be a positive integer — invalid or non-positive values fall back to 5):
- **Significant gaps** = uncovered URLs with `hits_this_week >= REPORT_MIN_HITS`. These are worth a redirect and belong in the headline.
- **Long-tail noise** = uncovered URLs below the threshold. Because the monitor is only weeks old (low sample), most broken URLs are hit once by bots, crawlers, or stale bookmarks, so the raw uncovered and "new gap" counts churn heavily week-over-week and overstate the problem. Roll these up into a single count — never list them individually or put them in the headline.

### 5. Determine whether the run is actionable

This agent posts **at most one message per run**, and only when the run is actionable. Follow the actionable-only rule in `.agents/references/skill-authoring-guidelines.md`.

Decide here; send later. The order for the rest of the run is: write the CSV (step 6), run Phase 2, then send one combined message if this step marked the run actionable **or** Phase 2 produced redirect results.

The run is actionable when any of these is true:
- `significant_uncovered_count` is 1 or more (at least one gap at or above `REPORT_MIN_HITS`).
- Phase 2 found at least one HIGH-confidence redirect, or produced MEDIUM-confidence suggestions needing human review.
- The run was blocked by a failure (Metabase error, missing `docs_404` data, truncated `vercel.json`).

Stay silent when the only findings are long-tail URLs below the threshold. That is the normal steady state once redirect coverage is healthy, and posting it weekly is what trains the channel to ignore this report. The run log entry and the CSV artifact remain the record of every run.

**Do not send the message from this step.** Because Phase 2 can add HIGH-confidence redirects and MEDIUM-confidence suggestions to the same report, defer the send until Phase 2 completes, then send one combined message. Two messages per run for a single report is exactly the noise this removes.

If `BUZZ_SLACK_TOKEN` is unavailable, write the full message body to the run output instead and note that Slack posting was skipped.

### 6. Write CSV artifact

Write `404-report-YYYY-MM-DD.csv` to `data/404-reports/` in the docs repo working directory. Each row is one normalised page (hits summed across trailing-slash/case/host variants). Format:

```
broken_url,hits_this_week,hits_last_week,is_covered_by_redirect,is_new_gap
/old/path,42,0,false,true
/another/path,18,22,false,false
```

Do NOT commit this file to the repo. It is an Oz run artifact only — readable from the Oz web app Runs page.

## Slack message format

Use Slack Block Kit. The message should be scannable in under 30 seconds.

```
📊 *docs.warp.dev 404 Report* — week of {YYYY-MM-DD}

*404 volume:* {trend_summary}
{one-line read, e.g. "Down — redirect coverage is holding." or "Up — check the gaps below."}

*Gaps worth fixing (≥{report_min_hits} hits):* {significant_uncovered_count} ({significant_new_gaps_count} new)
{hit_count}  `/path` {🆕 if new this week}
...

_+{long_tail_count} other uncovered URLs under {report_min_hits} hits each (mostly bots/old links) — see CSV._
*{resolved_count} resolved since last week* (redirect added or traffic stopped)

🔀 *Redirect drafter:* {N} HIGH-confidence redirects → {PR URL, or "none found this week"}
{MEDIUM-confidence suggestions needing review, if any:}
{path} → {suggested destination} [{reason}]

→ Add redirects for the gaps above: `vercel.json` › `redirects` array (PR against `main`)
→ Full breakdown: {oz_run_url}
```

The redirect-drafter line is part of this single message, not a separate post. Omit the line entirely when Phase 2 found nothing and the message is being sent because of significant gaps alone.

Build `{oz_run_url}` at runtime — never hard-code the Oz host (for example `app.warp.dev` or `oz.warp.dev`). This agent may run on staging or production, and a hard-coded host resolves to the wrong environment (or a generic Runs page). Resolve the environment-correct link from your current run, substituting the run ID this agent is executing as:
```bash
oz run get "<your run ID>" --output-format json | jq -r '.session_link'
```
If the command fails or returns an empty value, omit the `→ Full breakdown` line rather than posting a hard-coded or broken URL.

Rules:
- **Lead with volume trend, not distinct-URL counts.** The first line is always `trend_summary` — the pre-formatted total-404 trend, which reflects real user impact. It already includes the direction arrow (▼ fewer 404s, ▲ more, → no change) and falls back to a "no prior-week baseline yet" message when last week had no data, so the percentage is never rendered as null.
- **Only list significant gaps.** List `top_significant_uncovered` (URLs with `hits_this_week >= report_min_hits`), capped at 10. If there are more, note "and N more — see full CSV in the run." If `significant_uncovered_count` is 0, write "None this week — remaining 404s are all low-hit long-tail traffic." and omit the list.
- **Roll up the long tail.** Never list sub-threshold URLs individually; collapse them into the single `long_tail_count` line so noise doesn't dominate the report.
- Mark new gaps with 🆕.
- If `total_404s_this_week` is less than 50, add a brief positive note: "404 volume is low — good signal that redirect coverage is working."
- Never include raw user data (e.g. query strings with user IDs, tokens) in the Slack message. Strip query params from broken_url before displaying.

## Phase 2: Redirect drafter

After the CSV artifact is written, continue with Phase 2. Phase 2 proposes redirect entries for high-confidence uncovered 404 gaps, reducing the manual work required from the docs team.

Phase 2 runs **before** the Slack message is sent, so its results can be folded into that single message (see step 5).

### Threshold and confidence scoring

Only process gaps where `hits_this_week >= 5`. This is the **automation** threshold for opening redirect PRs — aligned with the **reporting** threshold (`REPORT_MIN_HITS`, default 5) used for the Phase 1 Slack summary. Review and adjust based on run log data (see `## Run log`).

For each qualifying uncovered URL, attempt to find a redirect target using these heuristics in order:

1. **Exact path match** (HIGH confidence) — strip legacy prefixes (`/docs/`, `/warp-docs/`, `/warp/`) and check if the remainder matches a current file path under `src/content/docs/` (convert `.mdx`/`.md` to URL slug).
2. **GitBook-to-Starlight migration** (HIGH confidence) — check a known path mapping for common patterns from the GitBook-era URL structure (e.g., `/getting-started/` → `/getting-started/quickstart/`, `/features/warp-drive/` → `/knowledge-and-collaboration/warp-drive/`). Infer from patterns already in `vercel.json`.
3. **Fuzzy slug match** (MEDIUM confidence) — tokenize the broken URL path and find the closest matching file path in `src/content/docs/` by segment similarity.
4. **No match** (LOW confidence) — cannot propose a redirect target.

### Actions by confidence level

- **HIGH**: Include in draft PR against `vercel.json`.
- **MEDIUM**: List in the Slack message as "Suggested redirects needing human review" with the proposed target and confidence reason. Do not include in the PR.
- **LOW**: Log to run output only. Do not include in Slack or PR.

### PR requirements

Open a **draft** PR only when at least 1 HIGH-confidence redirect is found. Always pass `--draft` to `gh pr create`.

This skill follows the "One standing PR per automation" contract in `.agents/references/skill-authoring-guidelines.md`. Every redirect PR edits the same `redirects` array in `vercel.json`, so a dated PR per week would guarantee conflicts.

Use the stable branch `docs/404-redirects` and a title with no date:
```text
docs: add redirects for top uncovered 404 paths
```

Look for an existing open PR before creating one:
```bash
gh pr list --repo warpdotdev/docs --state open \
  --search 'add redirects for top uncovered 404 paths in:title' \
  --json number,headRefName
```
If one exists, check out `docs/404-redirects`, rebase on the latest `origin/main`, add this week's redirects, push, and append them to the existing PR body under its existing headings. Do not add a duplicate heading per week — `check_pr_body.py` rejects those. If none exists, create the branch from the latest `origin/main`.

For each proposed redirect, add an entry to the `redirects` array in `vercel.json`:
```json
{"source": "/old/path", "destination": "/new/path", "statusCode": 308}
```

PR body must include:
- The broken URL, hit count, proposed destination, and confidence reason for each redirect
- The hit threshold used (`hits_this_week >= N`)
- A note that MEDIUM-confidence suggestions are in the Slack message and require human review before adding

Run `python3 .agents/skills/check_for_broken_links/check_links.py --internal-only` after editing `vercel.json` to catch any malformed destinations.

### Handing results to the Slack message

Do not post a separate redirect-drafter message. Pass these values into the single Phase 1 message described in "Slack message format":
- The count of HIGH-confidence redirects and the PR URL, if a PR was opened or updated.
- Any MEDIUM-confidence suggestions, each with its proposed target and confidence reason, for human review.

If no gaps meet the threshold and no HIGH-confidence matches are found, contribute nothing to the message and omit the redirect-drafter line. If that leaves the run with no significant gaps either, the run is a no-op: post nothing at all and let the run log record it.

### Threshold calibration note

After the first 4 weeks, review: if HIGH-confidence PRs contain redirects that are merged without changes, the threshold or confidence scoring is working. If PRs are frequently corrected or closed, raise the `hits_this_week` threshold or tighten the match heuristics.

## Run log

After every run — whether or not a PR is opened — prepend a structured entry to `.agents/logs/weekly_404_monitor_runs.md`. This log is the signal source for the `improve-404-monitor-skill` outer loop.

**Never commit the run log directly to `main`.** Use the standing log branch pattern:

1. Fetch and check out `chore/404-monitor-log`. If it does not exist, create it from the latest `origin/main`.
2. Prepend the log entry to `.agents/logs/weekly_404_monitor_runs.md`.
3. Commit with the message:
   ```text
   chore: update 404 monitor run log YYYY-MM-DD
   ```
4. Push the branch.
5. Ensure exactly one open PR exists from `chore/404-monitor-log` into `main`, titled `chore: 404 monitor run log`. Create it if missing; otherwise the push updates the existing PR.

If any git step fails, continue with the rest of the run and note the failure in the Slack summary.

### Run log format

```markdown
## YYYY-MM-DD — [PR opened | No PR | No data]
- **Total 404s this week**: N
- **Total 404s last week**: N
- **Trend**: ▼▲→ N%
- **Significant gaps (≥{report_min_hits} hits)**: N ({new_gaps_count} new)
- **Redirect candidates processed**: N  (hits ≥ {automation_threshold})
- **HIGH-confidence redirects**: N
- **PR**: [URL] | none
- **Oz run**: [URL]
- **Notes**: [any anomalies, threshold exceptions, Metabase errors, skipped URLs, etc.]
```

## Self-review before posting

Before posting to Slack, verify:
- The `docs_404` event exists in `stg_website_events` for the query window. If the table has no rows for `event_name = 'docs_404'`, it means PR #191 has not been live long enough to collect data. Post a clear "no data yet" message to Slack and end the run.
- The Metabase query completed successfully (HTTP 200, no `error` field in the response body).
- The `broken_url` field was present in the event properties for at least some rows. If it is consistently null, the `docs_404` tracking implementation has a bug — report it in the Slack message and tag the docs team.
- The vercel.json redirect list was loaded successfully and contains more than 500 entries (sanity check that the file is not truncated).
- The CSV artifact was written before posting to Slack.
- The Slack summary leads with the volume trend and lists only significant gaps (`hits_this_week >= report_min_hits`); long-tail URLs are rolled up into the `long_tail_count` line, never listed individually.

## No-data report

If `stg_website_events` returns 0 rows for `event_name = 'docs_404'` in the past 7 days, post this Slack message:

```
⏳ *docs.warp.dev 404 Report* — week of {YYYY-MM-DD}

No `docs_404` events recorded yet. This is expected if PR #191 (404 instrumentation) has been live for less than a week, or if the Rudderstack write key is not set in the Vercel environment.

Check: Vercel project env vars include `PUBLIC_RUDDERSTACK_WRITE_KEY` and `PUBLIC_RUDDERSTACK_DATA_PLANE_URL`.
```

## Failure handling

- If the Metabase query fails (non-200, timeout, or query error), post a brief failure notice to Slack, include the error message, and end the run with a non-zero exit code.
- Do NOT silently swallow errors or post incomplete data as if it were complete.
- Log all HTTP requests and responses to stdout for debugging via the Oz run log viewer.

## Scheduling

This skill is designed for an Oz scheduled agent with a weekly cron trigger: every Monday at 9am PT (`0 17 * * 1` in UTC).

To deploy (one-time setup):
1. Push this skill to `main` in the docs repo.
2. Verify the **Docs Agent** Oz environment (`K5KStCm5aYvhfBJb8cHol6`) has these secrets set:
   - `METABASE_API_KEY` — Metabase API key for BigQuery
   - `BUZZ_SLACK_TOKEN` — Slack bot token (already provisioned; used by other doc agents in this environment)
3. Register the schedule via the Oz CLI:
   ```sh
   oz schedule create \
     --name "weekly-404-monitor" \
     --cron "0 17 * * 1" \
     --environment K5KStCm5aYvhfBJb8cHol6 \
     --prompt "You are running in the warpdotdev/docs repo. Read and follow the instructions in .agents/skills/weekly-404-monitor/SKILL.md."
   ```
   This will make the schedule visible in oz.warp.dev under Schedules and ensure runs open PRs under the @oz-by-warp bot account.
