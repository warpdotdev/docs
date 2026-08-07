---
name: improve-aeo-crosslink-skill
description: Monthly outer loop agent that reads the aeo_crosslink_audit run log and proposes targeted improvements to the aeo_crosslink_audit skill itself. Part of the docs self-improvement loop architecture. Deploy after at least 8 entries exist in the run log (roughly month 3 of aeo_crosslink_audit operation).
---

# Improve AEO crosslink audit skill

Monthly outer loop agent. Reads `.agents/logs/aeo_crosslink_audit_runs.md` to identify systematic patterns in how the `aeo_crosslink_audit` skill performs over time, and opens a draft PR with targeted edits to `aeo_crosslink_audit/SKILL.md`.

This skill is part of the self-improvement loop architecture. The `aeo_crosslink_audit` skill already writes structured run log entries after every run — this skill reads those entries and acts on patterns.

## Schedule

Monthly, first Monday of each month, 9am PT. Start this agent on month 3 after `aeo_crosslink_audit` is running regularly (requires at least 8 run log entries for meaningful pattern analysis).

Cron: `0 17 * * 1` (UTC) — every Monday — combined with the first-week guard in step 0 below.

:::caution
Do **not** use `0 17 1-7 * 1`. That expression looks like "first Monday" but is not: when a cron expression restricts **both** day-of-month and day-of-week, the two fields are **ORed**, so it fires on every day of the 1st through 7th **and** every Monday — roughly 11 times a month. The `improve-drafting-skills` agent shipped with this exact expression and opened four conflicting PRs in six days before it was caught. Standard cron cannot express "first Monday," so the day-of-month guard is required.
:::

## Step 0: First-week guard

Run this before anything else. The schedule fires every Monday, so a run outside the first week of the month must exit immediately without reading logs, editing files, opening a PR, or posting to Slack.

```bash
DAY_OF_MONTH=$(date -u +%d)
if [ "$DAY_OF_MONTH" -gt 7 ]; then
  echo "Skipping: today is day $DAY_OF_MONTH, not the first Monday of the month. This agent runs monthly."
  exit 0
fi
```

A skipped run is a no-op, not a failure. Write the skip line to the run output and post nothing.

## Prerequisites

- Docs repo checked out at `main`
- `gh` CLI authenticated with write access to `warpdotdev/docs`
- `BUZZ_SLACK_TOKEN` — for posting a summary to `#growth-docs`. This token posts as `buzz`, the bot account that is a member of that channel. Do not substitute another Slack token: several exist in the Oz secret store, and one that authenticates successfully can still fail with `channel_not_found` if its bot is not in the channel.
- `GROWTH_DOCS_SLACK_CHANNEL_ID` — channel ID for `#growth-docs`

## Signal

Read `.agents/logs/aeo_crosslink_audit_runs.md`. The run log captures per-run: date, outcome (PR opened / no change), Peec signal availability, GSC signal availability, PR URL, links proposed and added, pages touched, themes observed, and no-change reason.

Do not act if fewer than 8 entries exist. Write a "too early to analyze" notice to run output and skip the PR.

## Workflow

### 0. Read the run log from its branch

Read the log directly from `chore/aeo-crosslink-audit-log`, the branch the `aeo_crosslink_audit` agent appends to after every run:

```bash
git fetch origin chore/aeo-crosslink-audit-log
git checkout origin/chore/aeo-crosslink-audit-log -- .agents/logs/aeo_crosslink_audit_runs.md
```

The branch always holds the complete history. `main` only has entries up to the last time a human merged the standing log PR, so reading `main` would silently analyze a truncated set and skew every pattern threshold below.

**Do not merge the standing log PR.** An earlier version of this skill attempted the merge as its first step. That coupled the analysis to a repo write the agent may not have permission to perform, and turned an unmerged PR into a hard failure rather than a non-event. Merging is human housekeeping; see "Log availability" in `.agents/references/skill-authoring-guidelines.md`.

**If the branch does not exist or the fetch fails, stop before step 1.** Do not fall back to the copy in the current checkout. That copy comes from `main`, which is exactly the truncated history this step exists to avoid — and a truncated log does not fail loudly, it silently changes the answer. With fewer entries the run either drops below the 8-entry minimum and reports "too early to analyze," or clears it with stale entries and proposes skill edits from an incomplete picture. Both look like normal outcomes.

A fetch failure is a blocked run, not a no-op: post the "run blocked" message (see step 6) naming the branch that could not be fetched, and end the run without analyzing or opening a PR.

### 1. Parse the run log

Read all entries from `.agents/logs/aeo_crosslink_audit_runs.md`. For each entry, extract:
- Outcome: PR opened or no change
- Peec available: yes/no
- GSC available: yes/no
- Links proposed and links added (0 if no change)
- No-change reason (if applicable)
- Themes field

### 2. Identify patterns across the last 12 entries

Look for these patterns:

**Consistently no-change runs (6+ of the last 12 entries are "No change")**
Possible causes:
- Confidence threshold is too conservative
- Scope (agents, cloud agents, orchestration) is too narrow and has been saturated
- Peec or GSC data is consistently unavailable, reducing signal

**Peec consistently unavailable (5+ entries where `Source signals` shows `Peec unavailable`)**
Cause: the `PEEC_PAT` secret in the Oz environment is expired, revoked, or missing; or the Peec MCP config is incorrect.
Fix: verify the `PEEC_PAT` secret is valid at app.peec.ai → Company → API Keys → Personal Access Tokens. Renew or recreate it and update the Oz environment secret. Also confirm the scheduled agent config includes the Peec MCP server entry.

**Links proposed but not added pattern (proposed > 0, added = 0 consistently)**
Cause: the self-review step is rejecting candidates that have already passed the initial selection. Confidence rules may be miscalibrated.
Fix: review the "Self-review before opening a PR" section and loosen overly strict criteria.

**Same theme recurring in every run's "Themes" field**
Cause: the same content gap or topic keeps appearing but isn't being acted on. The scope or confidence threshold may need to expand.
Fix: move the recurring theme from `## Future expansion boundaries` to the active scope, or add it to the pilot topic area.

**PR acceptance rate** (compare "PR opened" entries to PRs that were merged without human corrections vs. PRs that were corrected or closed)
Note: this requires checking GitHub PR history. Use `gh pr list --repo warpdotdev/docs --search "AEO cross-links" --state all` to find both merged and closed-without-merge PRs. Check each closed PR's reason and comments to classify it as "accepted", "corrected before merge", or "closed without merge".
- If mostly accepted without corrections: confidence scoring is well-calibrated; no change needed.
- If frequently corrected or closed: tighten the confidence scoring or add more specific exclusion rules.

### 3. Draft targeted edits to aeo_crosslink_audit/SKILL.md

For each confirmed pattern, draft the smallest edit that addresses it:

- **No-change too frequent**: Lower the "at least 2 high-confidence link additions" threshold to 1, or add new topic areas to the pilot scope under `## Scope`.
- **Peec unavailable**: This is usually a credential or config problem rather than a skill problem. Confirm the `PEEC_PAT` secret is valid and that the schedule still passes the `peec-ai` MCP server, and flag it for a human instead of editing the skill. Only change `## Source data` if the call contract itself has drifted.
- **Links proposed not added**: Loosen the specific gate in `## Self-review before opening a PR` that is rejecting otherwise valid candidates (identify which gate by reading the no-change reports in run output).
- **Recurring theme**: Move the theme from `## Future expansion boundaries` to `## Scope` with a clear instruction.
- **PR acceptance problems**: Strengthen the specific heuristic that led to incorrect link proposals.

Cap the diff at the `aeo_crosslink_audit/SKILL.md` file only. Do not rewrite unrelated sections.

### 4. Self-review before opening a PR

Before opening a PR, verify:
- Each edit is grounded in a specific pattern from the run log (cite the entry count and dates)
- No edit changes the fundamental goal or scope of the skill without clear justification from the data
- The proposed changes would not cause the skill to produce lower-quality outputs
- Run `git diff --check` to catch whitespace or encoding issues in the changed files
- Verify the YAML frontmatter of any changed `.md` file is parseable: `python3 -c "import sys; content = open(sys.argv[1]).read(); parts = content.split('---', 2); assert len(parts) >= 3" .agents/skills/aeo_crosslink_audit/SKILL.md`
- Note: `style_lint.py --changed` only scans `src/content/docs/` and does not cover `.agents/skills/`; do not rely on it to validate skill file edits

### 5. Create or update the standing improvement PR

This agent maintains **one** long-lived improvement PR, never one per run — see "One standing PR per automation" in `.agents/references/skill-authoring-guidelines.md`.

Stable branch: `docs/improve-aeo-crosslink-skill`
Stable title (no date — the date goes in the body):
```text
docs(skills): improve aeo_crosslink_audit skill from run log analysis
```

Look for an existing open PR first:
```bash
gh pr list --repo warpdotdev/docs --state open \
  --search 'improve aeo_crosslink_audit skill from run log analysis in:title' \
  --json number,headRefName
```
If one exists, check out its branch, rebase on the latest `origin/main`, apply this run's edits, push, and append dated bullets under the existing headings. If none exists, create the branch from the latest `origin/main` and open a draft PR.

PR body carries these headings, each appearing exactly once (`check_pr_body.py` rejects duplicates, so do not add a per-run copy):
- **Entries analyzed**: N run log entries, date range
- **Patterns identified**: each pattern, evidence (entry count and dates), and proposed fix
- **Patterns reviewed but not acted on**: patterns observed but below threshold or already addressed
- **Open questions for human review**: anything that requires editorial judgment before the change is applied

Prefix each appended bullet with its run date so the reviewer can tell runs apart.

### 6. Notify only if there is something to act on

Post to `#growth-docs` **only** when the standing PR was created or received new commits, or when the run was blocked by a failure. Follow the actionable-only rule in `.agents/references/skill-authoring-guidelines.md`. A run that finds no actionable patterns — or that skips via the step 0 guard, or exits because fewer than 8 entries exist — posts nothing and is recorded in the run output only.

**PR opened or updated:**
```
✅ AEO crosslink audit skill improvement · YYYY-MM-DD
PR [created | updated]: [PR URL]
Patterns addressed: N
Evidence base: N run log entries (last N weeks)
Oz run: [run URL]
```

**Run blocked by a failure:**
```
⚠️ AEO crosslink audit skill review · YYYY-MM-DD — run blocked
What failed: [brief reason — e.g., "could not fetch the log branch"]
Oz run: [run URL]
```
In both messages, build the `Oz run` link at runtime — never hard-code the Oz host (for example `app.warp.dev` or `oz.warp.dev`). This agent may run on staging or production, and a hard-coded host resolves to the wrong environment (or a generic Runs page). Resolve the environment-correct link from your current run, substituting the run ID this agent is executing as:
```bash
oz run get "<your run ID>" --output-format json | jq -r '.session_link'
```
If the command fails or returns an empty value, omit the `Oz run` line rather than posting a hard-coded or broken URL.

## Deployment

This skill is designed for a monthly Oz scheduled agent. Start it on month 3 after `aeo_crosslink_audit` has been running regularly.

To deploy:
1. Push this skill to `main` in the docs repo.
2. Verify the Oz environment has `BUZZ_SLACK_TOKEN` and `GROWTH_DOCS_SLACK_CHANNEL_ID` set.
3. In the Oz web app, create a new scheduled agent:
   - **Skill**: `improve-aeo-crosslink-skill` from `warpdotdev/docs`
   - **Schedule**: `0 17 * * 1` (UTC) = every Monday at 9am PT. The step 0 first-week guard narrows this to the first Monday only. See the caution in `## Schedule` for why the day-of-month field must stay `*`.
   - **Environment**: the same environment used for `aeo_crosslink_audit` (has `warpdotdev/docs` and buzz workspace checked out)
   - **Branch**: `main`
