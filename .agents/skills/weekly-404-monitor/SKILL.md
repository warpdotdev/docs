---
name: weekly-404-monitor
description: Weekly recurring agent that surfaces broken docs.warp.dev URLs by querying the docs_404 Rudderstack track event, diffing against existing vercel.json redirects, and posting a summary to Slack. Use for the Monday 9am PT scheduled Oz agent that monitors 404 gaps and supports the ongoing redirect-fix workflow.
---

# Weekly 404 monitor

Runs every Monday at 9am PT. Identifies new broken URL patterns on docs.warp.dev, surfaces the top uncovered paths, and posts a concise Slack summary so the docs team can prioritize redirect additions.

## Prerequisites

The following environment secrets must be set in the Oz cloud agent environment:

- `METABASE_API_KEY` — Metabase API key for BigQuery queries. If unavailable, the run must fail fast with a clear error.
- `SLACK_BOT_TOKEN` — Slack bot token for posting to the docs channel. If unavailable, write a no-post report to the run output instead.
- `SLACK_CHANNEL_ID` — Slack channel ID for the docs team (e.g. `#docs` or `#growth-docs`). Fall back to `SLACK_CHANNEL_ID=C0123456789` if not set explicitly.

Do NOT print, log, or include secret values in reports, commits, or Slack messages.

## Workflow

### 1. Query docs_404 events

Run `python3 .agents/skills/weekly-404-monitor/run_404_report.py` in the docs repo.

The script:
- Queries `warp-data-357114.prod.stg_website_events` via the Metabase API
- Extracts `broken_url` from `event_properties` for all `event_name = 'docs_404'` events in the past 7 days
- Groups by `broken_url`, sorted by hit count descending
- Returns a ranked list of broken URLs and their hit counts for the current week
- Computes the same for the prior week (days 8–14) for trend comparison
- Total weekly 404 count (current + prior) for the trend line

### 2. Fetch current vercel.json redirect sources

Fetch `vercel.json` from the docs repo (already checked out locally in the cloud environment, or via GitHub raw URL `https://raw.githubusercontent.com/warpdotdev/docs/main/vercel.json`).

Extract all `source` values from the `redirects` array. Normalise: lowercase, strip trailing slashes and anchor fragments.

### 3. Find uncovered URLs

For each broken URL in the current week's data:
- Normalise (lowercase, strip trailing slash, strip query params and fragments)
- Check if it exists as a `source` in `vercel.json` redirects
- If not covered, it is a **gap**

### 4. Compute delta vs prior week

Compare this week's uncovered gaps against last week's uncovered gaps (from step 1 prior-week query).

**New gaps** = uncovered this week AND not seen as uncovered last week.
**Resolved** = uncovered last week AND now either covered (has redirect) or no longer generating 404s.

### 5. Post Slack summary

Post a Slack message using the Block Kit format defined in the "Slack message format" section below.

If `SLACK_BOT_TOKEN` is unavailable, write the full Slack message body to the run output instead and note that Slack posting was skipped.

### 6. Write CSV artifact

Write `404-report-YYYY-MM-DD.csv` to `data/404-reports/` in the docs repo working directory. Format:

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

*Total 404s this week:* {N} ({+N / -N vs last week})
*Uncovered broken URLs:* {M} ({+N new this week})

*Top 10 uncovered URLs (by hits):*
{hit_count}  `/path` {🆕 if new this week}
...

*{K} resolved since last week* (redirect added or traffic stopped)

→ Add missing redirects: `vercel.json` › `redirects` array (PR against `main`)
→ Full breakdown: {oz_run_url}
```

Rules:
- Cap the list at 10 entries. If there are more, note "and N more — see full CSV in the run."
- Mark new gaps with 🆕.
- If total 404s this week is less than 50, add a brief positive note: "404 volume is low — good signal that redirect coverage is working."
- Never include raw user data (e.g. query strings with user IDs, tokens) in the Slack message. Strip query params from broken_url before displaying.

## Self-review before posting

Before posting to Slack, verify:
- The `docs_404` event exists in `stg_website_events` for the query window. If the table has no rows for `event_name = 'docs_404'`, it means PR #191 has not been live long enough to collect data. Post a clear "no data yet" message to Slack and end the run.
- The Metabase query completed successfully (HTTP 200, no `error` field in the response body).
- The `broken_url` field was present in the event properties for at least some rows. If it is consistently null, the `docs_404` tracking implementation has a bug — report it in the Slack message and tag the docs team.
- The vercel.json redirect list was loaded successfully and contains more than 500 entries (sanity check that the file is not truncated).
- The CSV artifact was written before posting to Slack.

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

To deploy:
1. Push this skill to `main` in the docs repo.
2. In the Oz web app (oz.warp.dev), create a new scheduled agent:
   - **Skill**: `weekly-404-monitor` from `warpdotdev/docs`
   - **Schedule**: `0 17 * * 1` (UTC) = 9am PT
   - **Environment**: docs-monitoring (must include `METABASE_API_KEY`, `SLACK_BOT_TOKEN`, `SLACK_CHANNEL_ID`)
   - **Repo**: `warpdotdev/docs` (main branch)
