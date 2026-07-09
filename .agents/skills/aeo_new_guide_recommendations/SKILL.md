---
name: aeo_new_guide_recommendations
description: Run a recurring AEO new-guide recommendations brief for Warp docs using Peec data and existing docs. Use for bi-weekly scheduled agents that identify missing or underserved topics in agents, cloud agents, orchestration, and Oz — and recommend whether to create a new page, update an existing page, or avoid a topic. Does not draft content.
---

# AEO new-guide recommendations

Produce 3–5 source-grounded AEO briefs that recommend whether to create a new guide, update an existing page, or avoid a topic — without drafting content. This skill is designed for a recurring bi-weekly Oz scheduled agent that gives the Docs team a repeatable upstream input to content planning.

## Scope

Use this skill only for the pilot topic areas:
- Agents
- Cloud agents
- Orchestration
- Oz (the agent platform)

Each brief must be clearly distinct from cross-link work. If the main gap is a missing link between existing pages, that belongs to the `aeo_crosslink_audit` skill, not this one.

Do not:
- Draft content.
- Create or edit docs pages.
- Open docs-content PRs for recommended topics; only the scheduled run-log PR in step 7 is allowed.
- Make broad marketing or product recommendations outside the docs surface.
- Reproduce full Peec reports. Keep signal summaries compact.

## Environment requirements

The following environment secrets should be set in the Oz cloud agent environment:

- `SLACK_BOT_TOKEN` — Slack bot token for posting to `#growth-docs`. If unavailable, write the notification body to the run output instead and skip Slack posting.
- `GROWTH_DOCS_SLACK_CHANNEL_ID` — Slack channel ID for `#growth-docs`. Find it in Slack by right-clicking the channel → Copy link (the ID begins with `C`). If unavailable, skip Slack posting.

Do NOT print, log, commit, or include secret values in reports or Slack messages.

## Source data

Use the smallest reliable set of source data needed to justify recommendations:

- **Peec snapshot** - Check freshness before using any data:
  1. Read `generated_at` from `/workspace/buzz/aeo-snapshots/docs/agents-orchestration/latest.json`.
  2. If the file is missing, `generated_at` is absent, or the snapshot is **14 days old or older**: write the stale-snapshot report (see "Stale snapshot report" below), write a run log entry (step 7) with the appropriate `No-run reason` (see "Stale snapshot report" for exact wording), post the stale Slack alert (step 8), and exit. Do not continue or open a PR.
  3. If the snapshot is fewer than 14 days old, read both `latest.json` and `latest.md` as source signals. These contain pre-exported Peec data (prompts, recommendations, source URLs, query vocabulary, and visibility scores) for agents, cloud agents, and orchestration. Because Oz is the agent platform underlying cloud agents and orchestration, substantial Oz-relevant signal is present in this snapshot — look for Oz-related prompts and queries within the agents/orchestration data. However, dedicated Oz-surface signals (Oz web app, Oz CLI, Oz scheduling) may be limited; when Oz-specific coverage is thin, flag the brief as lower-confidence and note what additional signal would strengthen the recommendation. Use the snapshot as the primary Peec source — do not attempt to call Peec MCP directly (cloud agents cannot authenticate).
- **Docs repo** - Search existing pages under `src/content/docs/` for relevant coverage of each candidate topic. Read `AGENTS.md` and `.agents/references/terminology.md` for product naming guidance.
- **Prior run log** - Read `.agents/logs/aeo_new_guide_recommendation_runs.md` to identify topics that were recommended in previous runs. If a candidate topic from this run matches a topic from a prior run, note it explicitly in the brief (see "Repeat topic flag" below).

Do not invent Peec signals. If the snapshot has no usable data for a candidate topic, say so in the brief and flag it as low-confidence.

## Workflow

1. **Check snapshot freshness.** Read `generated_at` from `latest.json`. If the snapshot is missing or 14 days old or older, write the stale-snapshot report, write a run log entry (step 7), post the stale Slack alert (step 8), and exit — do not proceed further.

2. **Read the prior run log.** Open `.agents/logs/aeo_new_guide_recommendation_runs.md` and extract the `Topics` field from each previous entry. Build a list of previously recommended topic slugs so you can detect repeats in step 4.

3. **Gather source signals from the Peec snapshot.** From `latest.json` and `latest.md`, extract:
   - Top prompts and their relevance to agents, cloud agents, orchestration, and Oz.
   - Search-query clusters — group repeated phrasing; do not list every raw query.
   - Action recommendations — use the recommendation text as the source of truth. Focus on owned and editorial opportunities relevant to docs content.
   - Visibility gaps — note topics where Warp has low or absent coverage compared to competitor mentions.

4. **Compare against existing docs.** For each candidate topic:
   - Search `src/content/docs/` for pages that already cover it.
   - Determine whether the topic is missing entirely, underserved (covered too briefly or outdated), or well-covered (no action needed).
   - If the main gap is a missing cross-link between existing pages (not missing topic coverage), skip this topic — it belongs to `aeo_crosslink_audit`, not here.

5. **Select 3–5 candidate topics.** Prioritize topics where:
   - Peec shows user intent (prompts, queries) but docs coverage is weak or absent.
   - The recommendation is actionable for a Docs team reviewer in a 15–30 minute planning session.
   - The topic is distinct from current open cross-link PRs or tracked content work.

   For each selected topic, check the prior-run list from step 2. If the topic slug matches a previous run's entry, flag it as a repeat in the brief.

6. **Produce a brief for each selected topic.** Use the format from `.agents/skills/aeo_brief/SKILL.md`. Every brief must include all seven sections: Goal, Recommendation, Source signals, Vocabulary map, Content scope, Existing docs to touch or link, and Open questions for human review.

   **Repeat topic flag** — When a topic appeared in a prior run log entry, prepend this line to the brief, immediately after the `## AEO brief` heading:

   ```
   ⚠️ Repeat topic: also recommended in [YYYY-MM-DD run]. Check whether this gap has been addressed since then.
   ```

   Fill in the date from the prior log entry.

7. **Write run log entry.** `main` is a protected branch — do not commit the log directly to it. Record the entry through a single, long-lived log PR:
   1. Fetch and check out the remote branch `chore/aeo-new-guide-rec-log`. If it does not exist, create it from the latest `origin/main`.
   2. Prepend the new entry to `.agents/logs/aeo_new_guide_recommendation_runs.md` using the "Run log format" section below.
   3. Stage only that file and commit with this message:

      ```text
      chore: log aeo new-guide rec run YYYY-MM-DD
      ```

   4. Push the branch.
   5. Ensure exactly one open PR exists from `chore/aeo-new-guide-rec-log` into `main`, titled `chore: aeo new-guide recommendation run log`. Create it if missing; otherwise the push updates the existing PR. Keep this log PR separate from any other PR.

   This produces one perpetual, low-noise PR that accumulates every run's entry regardless of outcome. Reviewers merge it periodically. If any git step fails, write the log entry to the run output instead and continue to step 8.

8. **Post Slack notification.** After writing the log entry, post the formatted message to `#growth-docs` using the Python snippet below. Python is preferred over curl because it reads `SLACK_BOT_TOKEN` from the environment (keeping the token out of process argv) and JSON-encodes the payload correctly regardless of newlines or special characters. If either secret is unavailable, write the notification body to the run output instead.

   ```bash
   python3 - <<'SLACK_EOF'
   import os, json, urllib.request, sys

   token = os.environ.get("SLACK_BOT_TOKEN", "")
   channel = os.environ.get("GROWTH_DOCS_SLACK_CHANNEL_ID", "")
   if not token or not channel:
       print("SLACK_BOT_TOKEN or GROWTH_DOCS_SLACK_CHANNEL_ID not set — skipping Slack notification", file=sys.stderr)
       sys.exit(0)

   # Replace the triple-quoted string with the message from the Slack notification format section.
   # Newlines and special characters are handled automatically by json.dumps.
   message = """<message text here>"""

   payload = json.dumps({
       "channel": channel,
       "text": message,
       "unfurl_links": False,
       "unfurl_media": False,
   }).encode()
   req = urllib.request.Request(
       "https://slack.com/api/chat.postMessage",
       data=payload,
       headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
   )
   with urllib.request.urlopen(req) as resp:
       result = json.load(resp)
   if not result.get("ok"):
       print(f"Slack error: {result.get('error')}", file=sys.stderr)
       sys.exit(1)
   SLACK_EOF
   ```

   Replace `<message text here>` with the message from the appropriate format in the "Slack notification format" section. Do not print `SLACK_BOT_TOKEN` or `GROWTH_DOCS_SLACK_CHANNEL_ID` values in the run output or in any file.

## Brief quality rules

Before finalizing each brief:

- **Real signal** — Each recommendation is backed by a Peec snapshot signal, not generic SEO advice.
- **Actionable scope** — A reviewer can act on the recommendation in a 15–30 minute planning session without re-doing the research.
- **No drafting** — The brief recommends what to create or update; it does not draft any docs content.
- **Distinct from crosslinks** — Do not recommend adding a link as a substitute for a new or updated page.
- **Thin-page check** — Flag topics where a new page would likely be too short (fewer than ~300 meaningful words) and suggest consolidating with an existing page instead.
- **Terminology accuracy** — Use product names from `AGENTS.md` and `.agents/references/terminology.md`. Do not use retired terms (e.g., "Warp University" instead of "Guides").

## Run output format

Write the full run output to the Oz run report. Structure it as follows:

```text
# AEO new-guide recommendations — YYYY-MM-DD

**Topic areas:** Agents, cloud agents, orchestration, and Oz.
**Snapshot age:** N days (generated YYYY-MM-DD)
**Briefs produced:** N

---

[Brief 1 — full aeo_brief format]

---

[Brief 2 — full aeo_brief format]

---

[... up to 5 briefs]

---

## Docs pages inspected

- `[path]` — [Why it was inspected.]

## Candidate topics rejected

- `[topic]` — [Why it was not included: insufficient signal, well-covered, crosslink-only gap, etc.]

## Suggested prompt or skill improvement

- [One specific improvement for the next run.]
```

If no briefs can be produced (fewer than 3 topics with usable signal), write a no-run report instead (see "No-run report" below).

## No-run report

If the run cannot produce at least 3 actionable briefs — because the snapshot has insufficient signal for the topic areas, existing docs already cover all candidates well, or fewer than 3 topics pass the brief quality rules — write a no-run report in the Oz run output instead of the full brief set.

```text
## AEO new-guide recommendations — no briefs produced — YYYY-MM-DD

**Topic area:** Agents, cloud agents, orchestration, and Oz.

**Source signals reviewed:**
- [Peec snapshot summary.]
- [Existing-docs signal.]

**Docs pages inspected:**
- `[path]` — [Why it was inspected.]

**Candidate topics considered:**
- `[topic]` — [Why no brief was produced: well-covered, insufficient signal, crosslink-only, etc.]

**Why no briefs were produced:**
- [Reason.]

**Suggested prompt or skill improvement:**
- [One specific improvement for the next run.]
```

## Stale snapshot report

If the Peec snapshot is missing or 14 days old or older, stop immediately. Write this report to the Oz run output:

```text
## AEO new-guide recommendations — snapshot stale

**Date:** YYYY-MM-DD
**Snapshot age:** [N days (generated YYYY-MM-DD) | file not found | generated_at field missing]
**Threshold:** 14 days

The Peec snapshot is too old to support high-confidence recommendations. No briefs were produced.

**Action required:**
Run the `refresh-peec-aeo-snapshot` skill in a local Warp agent session where Peec MCP is authenticated.
Skill: buzz/.agents/skills/refresh-peec-aeo-snapshot/SKILL.md

The agent will run normally on the next scheduled execution once a fresh snapshot is committed to the buzz repo.
```

Fill in the `Snapshot age` field as follows — do not invent values:
- File exists and `generated_at` is present: `N days (generated YYYY-MM-DD)` — compute `N` from today's date minus `generated_at`.
- File does not exist: `file not found`.
- File exists but `generated_at` is absent or unparseable: `generated_at field missing`.

Use the same wording in the `No-run reason` field of the run log entry:
- File stale: `snapshot stale — N days old`
- File missing: `snapshot missing — file not found`
- Field missing: `snapshot missing — generated_at field absent`

Then post the stale Slack alert (step 8). Exit. Do not write a no-run report. Do not open a PR.

## Run log format

Prepend each new entry at the top of `.agents/logs/aeo_new_guide_recommendation_runs.md`, immediately after the `---` separator line. Use this format:

```markdown
## YYYY-MM-DD — [Briefs produced | No briefs | Snapshot stale]

- **Run**: [Oz run URL if available, otherwise the run ID]
- **Source signals**: Peec snapshot [available | stale | missing]
- **Briefs produced**: [N | 0 | N/A]
- **Topics**: [comma-separated topic slugs, e.g. "oz-scheduling, cloud-agent-setup, ambient-agents" | N/A]
- **Repeat topics**: [comma-separated slugs that appeared in a prior run, or "none"]
- **No-run reason**: [low signal | well-covered | snapshot stale — N days old | N/A]
```

Keep each entry to 6 fields and under 8 lines. Do not add narrative prose. The `Topics` field is how future runs detect repeats — be consistent with slug naming (lowercase, hyphenated).

## Slack notification format

Use a simple text message (not Block Kit). The message should be scannable in under 30 seconds.

**Briefs produced:**

```
✅ AEO new-guide recommendations · YYYY-MM-DD
Briefs produced: N topics: [comma-separated topic slugs]
Repeat topics: [slugs that recurred | none]
Oz run: [run URL]
```

**No briefs produced:**

```
ℹ️ AEO new-guide recommendations · YYYY-MM-DD — No briefs
Topics reviewed: agents, cloud agents, orchestration, Oz
No briefs: [brief reason — e.g., "fewer than 3 topics with usable signal"]
Oz run: [run URL]
```

**Snapshot stale:**

```
⚠️ AEO new-guide recommendations · YYYY-MM-DD — Snapshot stale
Snapshot: [N days old (generated YYYY-MM-DD) | file not found | generated_at missing], threshold: 14 days
No recommendations produced. Refresh the snapshot before the next run.
How: run refresh-peec-aeo-snapshot in a local Warp session
Skill: buzz/.agents/skills/refresh-peec-aeo-snapshot/SKILL.md
Oz run: [run URL]
```

Rules:
- Post on every run, including no-brief runs.
- Never include raw secret values, personal access tokens, or credential file paths in the Slack message.
- Build the `Oz run` link at runtime — never hard-code the Oz host (for example `app.warp.dev` or `oz.warp.dev`). This agent may run on staging or production, and a hard-coded host resolves to the wrong environment (or a generic Runs page). Resolve the environment-correct link from your current run with `oz-dev run get "<your run ID>" --output-format json | jq -r '.session_link'`, substituting the run ID this agent is executing as.
- If the Oz run URL is unavailable, omit that line rather than posting a broken link.

## Human review expectations

The Docs team reviewer should be able to read the full brief set in 15–30 minutes before a content planning sync and make decisions without re-doing the Peec research. Optimize output for quick review:

- Keep each brief to the seven required sections. No additional prose.
- Explain the source signal behind each recommendation.
- Flag uncertainty and repeat topics clearly.
- Do not hide product or terminology questions in the recommendation.

## Relationship to other AEO skills

- **`aeo_brief`** — The brief format this skill uses for each recommendation. Read `.agents/skills/aeo_brief/SKILL.md` for format guidance and vocabulary translation rules.
- **`aeo_crosslink_audit`** — Handles internal cross-linking between existing pages. If the main gap is a missing link, refer to that skill instead of creating a brief here.
- **`refresh-peec-aeo-snapshot`** — Run locally to refresh the Peec snapshot when stale. See `buzz/.agents/skills/refresh-peec-aeo-snapshot/SKILL.md`.

## Future expansion

Do not implement future expansion ideas in this pilot skill. If the audit finds opportunities outside the four topic areas, mention them only as follow-up notes in the run output.

Possible future phases include:
- Expanding topic areas beyond agents, cloud agents, orchestration, and Oz.
- Adding a comparison against open Notion content-planning items to detect duplication.
- Lightweight trend reporting across scheduled runs (e.g., topics that recur three or more times become high-priority backlog items).
- Integration with the `missing_docs` skill's output as an additional signal source.
