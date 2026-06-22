---
name: improve-aeo-crosslink-skill
description: Monthly outer loop agent that reads the aeo_crosslink_audit run log and proposes targeted improvements to the aeo_crosslink_audit skill itself. Part of the docs self-improvement loop architecture. Deploy after at least 8 entries exist in the run log (roughly month 3 of aeo_crosslink_audit operation).
---

# Improve AEO crosslink audit skill

Monthly outer loop agent. Reads `.agents/logs/aeo_crosslink_audit_runs.md` to identify systematic patterns in how the `aeo_crosslink_audit` skill performs over time, and opens a draft PR with targeted edits to `aeo_crosslink_audit/SKILL.md`.

This skill is part of the self-improvement loop architecture. The `aeo_crosslink_audit` skill already writes structured run log entries after every run — this skill reads those entries and acts on patterns.

## Schedule

Monthly, first Monday of each month, 9am PT. Start this agent on month 3 after `aeo_crosslink_audit` is running regularly (requires at least 8 run log entries for meaningful pattern analysis).

Suggested cron: `0 17 1-7 * 1` (UTC) = first Monday of each month at 9am PT.

## Prerequisites

- Docs repo checked out at `main`, with at least 8 entries in `.agents/logs/aeo_crosslink_audit_runs.md`
- `gh` CLI authenticated with write access to `warpdotdev/docs`
- `SLACK_BOT_TOKEN` — for posting summary to `#growth-docs`
- `SLACK_CHANNEL_ID` — channel ID for `#growth-docs`

## Signal

Read `.agents/logs/aeo_crosslink_audit_runs.md`. The run log captures per-run: date, outcome (PR opened / no change), Peec signal availability, GSC signal availability, PR URL, links proposed and added, pages touched, themes observed, and no-change reason.

Do not act if fewer than 8 entries exist. Write a "too early to analyze" notice to run output and skip the PR.

## Workflow

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

**Peec snapshot consistently unavailable (5+ entries show "Peec: unavailable")**
Cause: snapshot files in `/workspace/buzz/aeo-snapshots/` are stale or the refresh cadence is too infrequent.
Fix: update the snapshot refresh instructions or cadence in `aeo_crosslink_audit/SKILL.md`.

**Links proposed but not added pattern (proposed > 0, added = 0 consistently)**
Cause: the self-review step is rejecting candidates that have already passed the initial selection. Confidence rules may be miscalibrated.
Fix: review the "Self-review before opening a PR" section and loosen overly strict criteria.

**Same theme recurring in every run's "Themes" field**
Cause: the same content gap or topic keeps appearing but isn't being acted on. The scope or confidence threshold may need to expand.
Fix: move the recurring theme from `## Future expansion boundaries` to the active scope, or add it to the pilot topic area.

**PR acceptance rate** (compare "PR opened" entries to PRs that were merged without human corrections vs. PRs that were corrected or closed)
Note: this requires checking GitHub PR history. Use `gh pr list --repo warpdotdev/docs --search "AEO cross-links" --state merged` to find and inspect closed PRs.
- If merged without corrections: confidence scoring is well-calibrated; no change needed.
- If frequently corrected: tighten the confidence scoring or add more specific exclusion rules.

### 3. Draft targeted edits to aeo_crosslink_audit/SKILL.md

For each confirmed pattern, draft the smallest edit that addresses it:

- **No-change too frequent**: Lower the "at least 2 high-confidence link additions" threshold to 1, or add new topic areas to the pilot scope under `## Scope`.
- **Peec unavailable**: Update the snapshot path references or add a fallback instruction in `## Source data`.
- **Links proposed not added**: Loosen the specific gate in `## Self-review before opening a PR` that is rejecting otherwise valid candidates (identify which gate by reading the no-change reports in run output).
- **Recurring theme**: Move the theme from `## Future expansion boundaries` to `## Scope` with a clear instruction.
- **PR acceptance problems**: Strengthen the specific heuristic that led to incorrect link proposals.

Cap the diff at the `aeo_crosslink_audit/SKILL.md` file only. Do not rewrite unrelated sections.

### 4. Self-review before opening a PR

Before opening a PR, verify:
- Each edit is grounded in a specific pattern from the run log (cite the entry count and dates)
- No edit changes the fundamental goal or scope of the skill without clear justification from the data
- The proposed changes would not cause the skill to produce lower-quality outputs
- Run `python3 .agents/skills/style_lint/style_lint.py --changed` to confirm edits are clean

### 5. Open a draft PR

Open a draft PR with title:
```text
docs(skills): improve aeo_crosslink_audit skill from run log analysis YYYY-MM-DD
```

PR body must include:
- **Entries analyzed**: N run log entries, date range
- **Patterns identified**: each pattern, evidence (entry count and dates), and proposed fix
- **Patterns reviewed but not acted on**: patterns observed but below threshold or already addressed
- **Open questions for human review**: anything that requires editorial judgment before the change is applied

### 6. Post Slack notification

Post to `#growth-docs`:

**PR opened:**
```
✅ AEO crosslink audit skill improvement · YYYY-MM-DD
PR: [PR URL]
Patterns addressed: N
Evidence base: N run log entries (last N weeks)
Oz run: [run URL]
```

**No action (too few patterns or too few entries):**
```
ℹ️ AEO crosslink audit skill review · YYYY-MM-DD — No changes
Entries analyzed: N
No actionable patterns found: [brief reason]
Oz run: [run URL]
```

## Deployment

This skill is designed for a monthly Oz scheduled agent. Start it on month 3 after `aeo_crosslink_audit` has been running regularly.

To deploy:
1. Push this skill to `main` in the docs repo.
2. Verify the Oz environment has `SLACK_BOT_TOKEN` and `SLACK_CHANNEL_ID` set.
3. In the Oz web app (oz.warp.dev), create a new scheduled agent:
   - **Skill**: `improve-aeo-crosslink-skill` from `warpdotdev/docs`
   - **Schedule**: `0 17 1-7 * 1` (UTC) = first Monday of each month at 9am PT
   - **Environment**: the same environment used for `aeo_crosslink_audit` (has `warpdotdev/docs` and buzz workspace checked out)
   - **Branch**: `main`
