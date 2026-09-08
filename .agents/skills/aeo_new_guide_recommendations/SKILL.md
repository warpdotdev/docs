---
name: aeo_new_guide_recommendations
description: Run a recurring AEO new-guide recommendations brief for Warp docs using Peec data and existing docs. Use for scheduled agents that run monthly and identify missing or underserved topics in agents, cloud agents, orchestration, and Oz — and recommend whether to create a new page, update an existing page, or avoid a topic. Does not draft content.
---

# AEO new-guide recommendations

Produce 3–5 source-grounded AEO briefs that recommend whether to create a new guide, update an existing page, or avoid a topic — without drafting content. This skill is designed for an Oz scheduled agent that runs monthly. The goal is to give the Docs team a repeatable upstream input to content planning without generating more noise than the team can act on.

## Agent-doc quality contract

This skill does not draft content or open content PRs (see "Do not" below), so
it does not stamp the `warpy-factory` marker itself. See
`.agents/references/doc-quality-policy.md` for the contract that applies once
a recommendation here becomes a real drafting task in `draft_docs` or a
type-specific drafting skill.

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

- `PEEC_PAT` — Peec Personal Access Token for MCP authentication. Create one at **app.peec.ai → Company → API Keys → Personal Access Tokens**. If unavailable or expired, the run proceeds with docs-only signals and logs "Peec: unavailable" in the run output.
- `BUZZ_SLACK_TOKEN` — Slack bot token for posting to `#growth-docs`, authenticating as the `buzz` bot. This is the account that posts to that channel; do not substitute another Slack token without confirming the bot is a member of the channel. If unavailable, write the notification body to the run output instead and skip Slack posting.
- `GROWTH_DOCS_SLACK_CHANNEL_ID` — Slack channel ID for `#growth-docs`. Find it in Slack by right-clicking the channel → Copy link (the ID begins with `C`). If unavailable, skip Slack posting.

The scheduled cloud agent must also include the Peec MCP server in its agent config (pass via `--mcp` flag or the agent config file `mcp_servers` key):

```json
{
  "peec-ai": {
    "url": "https://api.peec.ai/mcp",
    "headers": {
      "Authorization": "Bearer ${PEEC_PAT}"
    }
  }
}
```

Do NOT print, log, commit, or include secret values in reports or Slack messages.

## Source data

Use the smallest reliable set of source data needed to justify recommendations.

- **Peec** - Call the Peec MCP (authenticated with the `PEEC_PAT` secret) to collect prompts, search queries, actions/recommendations, and source URLs for agents, cloud agents, orchestration, and Oz (last 30 days). See "Calling Peec" below for the call contract — the MCP may not appear as a native tool in a cloud run, in which case call the HTTP endpoint directly. Filter prompts and queries for relevance to the topic areas. Because Oz is the agent platform underlying cloud agents and orchestration, substantial Oz-relevant signal appears within the agents and orchestration data — look for Oz-related prompts and queries there. Dedicated Oz-surface signals (Oz web app, Oz CLI, Oz scheduling) may still be thin; when Oz-specific coverage is sparse, flag the brief as lower-confidence and note what additional signal would strengthen the recommendation. If the Peec MCP returns an error or is unavailable (missing `PEEC_PAT`, expired token, or connection failure), log "Peec: unavailable" in the run output and follow the "Peec unavailable" section below.
- **Docs repo** - Search existing pages under `src/content/docs/` for relevant coverage of each candidate topic. Read `AGENTS.md` and `.agents/references/terminology.md` for product naming guidance.
- **Prior run log** - Read `.agents/logs/aeo_new_guide_recommendation_runs.md` to identify topics that were recommended in previous runs. If a candidate topic from this run matches a topic from a prior run, note it explicitly in the brief (see "Repeat topic flag" below).

Do not invent Peec signals. If Peec has no usable data for a candidate topic, say so in the brief and flag it as low-confidence.

### Calling Peec

Even when `peec-ai` is configured in the agent config, a cloud run may not expose it as a native tool. In that case, call the MCP endpoint directly over HTTP with the `PEEC_PAT` secret — do not conclude that Peec is unavailable just because no `peec-ai` tool appears in your tool list.

The endpoint speaks JSON-RPC over HTTP at `https://api.peec.ai/mcp`:

1. `POST` an `initialize` request with `Authorization: Bearer $PEEC_PAT`, `Content-Type: application/json`, and `Accept: application/json, text/event-stream`. Capture the `Mcp-Session-Id` response header.
2. Send the `notifications/initialized` notification with that session header.
3. Call tools with `method: "tools/call"` and `params: {"name": "<tool>", "arguments": {...}}`, passing the session header on every request.

Resolve the project first with `list_projects` — every other tool requires a `project_id`. Select the Warp project from the result rather than hard-coding an ID.

Tool contract details that are easy to get wrong:

- **`get_actions` requires `url_classification` for drill-downs.** Call `scope=overview` first; those rows are navigation metadata and carry no recommendation text. Drilling into `scope=owned` or `scope=editorial` fails validation unless you pass the `url_classification` from the overview row (for example `HOW_TO_GUIDE` or `ARTICLE`). `scope=reference` and `scope=ugc` require `domain` instead.
- **`list_search_queries` returns `query_text`**, not `query`. Parsing for a generic `query` field yields empty clusters.
- **Editorial actions are often outreach, not docs work.** Many `EDITORIAL` rows read like "pitch this publication" or "contact this author." Use `OWNED` rows with a `HOW_TO_GUIDE` or `ARTICLE` classification as the primary docs signal, and only treat an editorial row as a docs signal when its text describes a genuine content gap.
- Responses are columnar JSON (`{columns, rows, rowCount}`), so map values by column index rather than assuming objects.

## Workflow

1. **Collect Peec signals.** Use the Peec MCP to collect prompts, search queries, actions/recommendations, and source URLs for agents, cloud agents, orchestration, and Oz (last 30 days). If the Peec MCP is unavailable, log "Peec: unavailable" and follow the "Peec unavailable" section.

2. **Read the prior run log.** Open `.agents/logs/aeo_new_guide_recommendation_runs.md` and extract the `Topics` field from each previous entry. Build a list of previously recommended topic slugs so you can detect repeats in step 4.

3. **Extract and cluster the signals.** From the Peec results, pull out:
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
   3. Verify the entry was written: `head -10 .agents/logs/aeo_new_guide_recommendation_runs.md` and confirm the new heading appears at the top. If the file is unchanged, the prepend failed — write the entry to run output and skip to step 8.
   4. Stage only that file and commit with this message:

      ```text
      chore: log aeo new-guide rec run YYYY-MM-DD
      ```

   5. Push the branch. Verify the push succeeded by checking the exit code or running `git log --oneline -1 origin/chore/aeo-new-guide-rec-log` after the push.
   6. Ensure exactly one open PR exists from `chore/aeo-new-guide-rec-log` into `main`, titled `chore: aeo new-guide recommendation run log`. Create it if missing; otherwise the push updates the existing PR. Keep this log PR separate from any other PR.

   This produces one perpetual, low-noise PR that accumulates every run's entry regardless of outcome. Reviewers merge it periodically so the log data reaches `main` and can inform the skill-improvement loop. If any git step fails, write the log entry to the run output instead and continue to step 8 — do not silently skip the log.

8. **Post Slack notification.** After writing the log entry, post the formatted message to `#growth-docs` using the Python snippet below. Python is preferred over curl because it reads `BUZZ_SLACK_TOKEN` from the environment (keeping the token out of process argv) and JSON-encodes the payload correctly regardless of newlines or special characters. If either secret is unavailable, write the notification body to the run output instead.

   ```bash
   python3 - <<'SLACK_EOF'
   import os, json, urllib.request, sys

   token = os.environ.get("BUZZ_SLACK_TOKEN", "")
   channel = os.environ.get("GROWTH_DOCS_SLACK_CHANNEL_ID", "")
   if not token or not channel:
       print("BUZZ_SLACK_TOKEN or GROWTH_DOCS_SLACK_CHANNEL_ID not set — skipping Slack notification", file=sys.stderr)
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

   Replace `<message text here>` with the message from the appropriate format in the "Slack notification format" section. Do not print `BUZZ_SLACK_TOKEN` or `GROWTH_DOCS_SLACK_CHANNEL_ID` values in the run output or in any file.

   **If `chat.postMessage` returns `channel_not_found`**, the secrets being set is not sufficient — either the channel ID is stale or the bot is not a member of the channel. Do not treat this as a successful post. Instead:
   1. Try resolving the channel by name: call `conversations.list` (types `public_channel,private_channel`) and look for `growth-docs`. If found, retry the post with that ID and report that the stored `GROWTH_DOCS_SLACK_CHANNEL_ID` is wrong so a human can correct the secret.
   2. If the lookup also fails or returns `missing_scope`, the bot is not in the channel or lacks scope. Write the notification body to the run output, and state explicitly in the run output that the Slack post failed with `channel_not_found` — never imply it was delivered.

## Brief quality rules

Before finalizing each brief:

- **Real signal** — Each recommendation is backed by a Peec signal, not generic SEO advice.
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
**Source signals:** Peec [available | unavailable]
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

If the run cannot produce at least 3 actionable briefs — because Peec has insufficient signal for the topic areas, existing docs already cover all candidates well, or fewer than 3 topics pass the brief quality rules — write a no-run report in the Oz run output instead of the full brief set.

```text
## AEO new-guide recommendations — no briefs produced — YYYY-MM-DD

**Topic area:** Agents, cloud agents, orchestration, and Oz.

**Source signals reviewed:**
- [Peec signal summary, or "Peec: unavailable".]
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

## Peec unavailable

Peec is the primary signal for this skill. When the Peec MCP is unavailable — missing or expired `PEEC_PAT`, the MCP server is not configured in the agent, or the connection fails — do not invent signals and do not silently continue as though the data existed.

Instead:

1. Log `Peec: unavailable` in the run output, along with the specific failure (for example, "MCP server not configured" or "401 from api.peec.ai"). Never include the token value.
2. Continue with docs-only analysis. A docs-only run can still identify obvious coverage gaps, but every brief it produces must be flagged as low-confidence with a note that Peec signal was unavailable.
3. Apply a higher bar: only produce a brief when the gap is clearly evident from existing docs structure alone. If fewer than 3 topics clear that bar, write the no-run report with `peec unavailable` as the `No-run reason`.
4. Post the Slack notification as usual, using the "No briefs" format when no briefs were produced.

If `PEEC_PAT` is present but Peec still fails, note in the run output that the token may need rotating at **app.peec.ai → Company → API Keys → Personal Access Tokens** so a human can fix it before the next run.

## Run log format

Prepend each new entry at the top of `.agents/logs/aeo_new_guide_recommendation_runs.md`, immediately after the `---` separator line. Use this format:

```markdown
## YYYY-MM-DD — [Briefs produced | No briefs]

- **Run**: [Oz run URL if available, otherwise the run ID]
- **Source signals**: Peec [available | unavailable]
- **Briefs produced**: [N | 0]
- **Topics**: [comma-separated topic slugs, e.g. "oz-scheduling, cloud-agent-setup, ambient-agents" | N/A]
- **Repeat topics**: [comma-separated slugs that appeared in a prior run, or "none"]
- **No-run reason**: [low signal | well-covered | peec unavailable | N/A]
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
No briefs: [brief reason — e.g., "fewer than 3 topics with usable signal" or "Peec unavailable"]
Oz run: [run URL]
```

Rules:
- Post on every run, including no-brief runs.
- Never include raw secret values, personal access tokens, or credential file paths in the Slack message.
- Build the `Oz run` link at runtime — never hard-code the Oz host (for example `app.warp.dev` or `oz.warp.dev`). This agent may run on staging or production, and a hard-coded host resolves to the wrong environment (or a generic Runs page). Resolve the environment-correct link from your current run with `oz run get "<your run ID>" --output-format json | jq -r '.session_link'`, substituting the run ID this agent is executing as. Cloud sandboxes ship the `oz` CLI; `oz-dev` is a local development build and is not present, so do not call it.
- If the Oz run URL is unavailable, omit that line rather than posting a broken link.

## Human review expectations

The Docs team reviewer should be able to read the full brief set in 15–30 minutes before a content planning sync and make decisions without re-doing the Peec research. Optimize output for quick review:

- Keep each brief to the seven required sections. No additional prose.
- Explain the source signal behind each recommendation.
- Flag uncertainty and repeat topics clearly.
- Do not hide product or terminology questions in the recommendation.

## Relationship to other AEO skills

- **`aeo_brief`** — The brief format this skill uses for each recommendation. Read `.agents/skills/aeo_brief/SKILL.md` for format guidance and vocabulary translation rules.
- **`aeo_crosslink_audit`** — Handles internal cross-linking between existing pages. If the main gap is a missing link, refer to that skill instead of creating a brief here. It reads Peec through the same MCP and `PEEC_PAT` setup.
- **`refresh-peec-aeo-snapshot`** — Legacy. This skill previously read a Peec snapshot committed to the `buzz` repo because cloud agents could not authenticate with Peec. That is no longer the case, and the snapshot is not part of this pipeline. See `buzz/.agents/skills/refresh-peec-aeo-snapshot/SKILL.md` only if you need a local snapshot for another purpose.

## Future expansion

Do not implement future expansion ideas in this pilot skill. If the audit finds opportunities outside the four topic areas, mention them only as follow-up notes in the run output.

Possible future phases include:
- **Outer self-improvement loop** — After the run log has accumulated several entries (roughly 3–4 runs, equivalent to 3–4 months at a monthly cadence), an `improve-aeo-new-guide-rec-skill` skill should read the log and the run outputs to identify systematic weaknesses: topics that keep repeating without being addressed, briefs that reviewers consistently ignore, vocabulary the agent gets wrong, or signal gaps that suggest the Peec query scope needs expanding. This mirrors the `improve-aeo-crosslink-skill` pattern used for the crosslink audit. The improvement skill should run manually (not on a schedule) and propose diffs to this SKILL.md for human review before being applied.
- **Expanding topic areas** beyond agents, cloud agents, orchestration, and Oz once the pilot cadence is stable.
- **Comparison against open Notion content-planning items** to detect when a recommended topic is already tracked or in progress.
- **Lightweight trend reporting** across scheduled runs (e.g., topics that recur three or more times without a logged action become high-priority backlog items).
- **Integration with the `missing_docs` skill's output** as an additional signal source.
- **Oz-specific Peec coverage** — Add tracked Peec prompts for dedicated Oz surfaces (Oz web app, Oz CLI, Oz scheduling) so the pilot scope is covered with equal confidence.
