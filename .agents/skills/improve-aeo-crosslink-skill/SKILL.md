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

- Docs repo checked out at `main`
- `gh` CLI authenticated with write access to `warpdotdev/docs`
- `SLACK_BOT_TOKEN` — for posting summary to `#growth-docs`
- `GROWTH_DOCS_SLACK_CHANNEL_ID` — channel ID for `#growth-docs`

## Signal

Read `.agents/logs/aeo_crosslink_audit_runs.md`. The run log captures per-run: date, outcome (PR opened / no change), Peec signal availability, GSC signal availability, PR URL, links proposed and added, pages touched, themes observed, and no-change reason.

Do not act if fewer than 8 entries exist. Write a "too early to analyze" notice to run output and skip the PR.

## Workflow

### 0. Merge the standing log PR

Before reading the run log, ensure all accumulated entries are on `main` by merging the standing log PR. This is the PR from `chore/aeo-crosslink-audit-log` that the `aeo_crosslink_audit` agent continuously appends to.

```bash
# Find the open log PR (there should be at most one)
OPEN_LOG_PR=$(gh pr list --repo warpdotdev/docs \
  --head chore/aeo-crosslink-audit-log \
  --state open \
  --json number \
  --jq '.[0].number' 2>/dev/null)

if [[ -n "$OPEN_LOG_PR" ]]; then
  # Safety check: only merge if the PR touches exactly the expected log file.
  CHANGED_FILES=$(gh pr view "$OPEN_LOG_PR" --repo warpdotdev/docs --json files --jq '[.files[].path]')
  ONLY_LOG=$(echo "$CHANGED_FILES" | python3 -c "
import json, sys
files = json.load(sys.stdin)
print('yes' if all(f == '.agents/logs/aeo_crosslink_audit_runs.md' for f in files) else 'no')
")
  if [[ "$ONLY_LOG" == 'yes' ]]; then
    gh pr merge "$OPEN_LOG_PR" --repo warpdotdev/docs --merge
    # Non-destructive fast-forward: fails loudly if worktree is dirty or not fast-forwardable.
    git fetch origin main
    git merge --ff-only origin/main
  else
    echo "Log PR contains unexpected files — skipping merge, reading log from branch instead."
    git fetch origin chore/aeo-crosslink-audit-log
    git checkout origin/chore/aeo-crosslink-audit-log -- .agents/logs/aeo_crosslink_audit_runs.md
  fi
fi
```

If the merge fails (conflict, permissions, or the branch is ahead of main in an unexpected way), log the failure to run output and read the log from the `chore/aeo-crosslink-audit-log` branch instead:

```bash
git fetch origin chore/aeo-crosslink-audit-log
git checkout origin/chore/aeo-crosslink-audit-log -- .agents/logs/aeo_crosslink_audit_runs.md
```

Do not abort the skill run because the log PR could not be merged. Proceed with whatever log entries are available.

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
In both messages, build the `Oz run` link at runtime — never hard-code the Oz host (for example `app.warp.dev` or `oz.warp.dev`). This agent may run on staging or production, and a hard-coded host resolves to the wrong environment (or a generic Runs page). Resolve the environment-correct link from your current run, substituting the run ID this agent is executing as:
```bash
oz run get "<your run ID>" --output-format json | jq -r '.session_link'
```
If the command fails or returns an empty value, omit the `Oz run` line rather than posting a hard-coded or broken URL.

## Deployment

This skill is designed for a monthly Oz scheduled agent. Start it on month 3 after `aeo_crosslink_audit` has been running regularly.

To deploy:
1. Push this skill to `main` in the docs repo.
2. Verify the Oz environment has `SLACK_BOT_TOKEN` and `GROWTH_DOCS_SLACK_CHANNEL_ID` set.
3. In the Oz web app, create a new scheduled agent:
   - **Skill**: `improve-aeo-crosslink-skill` from `warpdotdev/docs`
   - **Schedule**: `0 17 1-7 * 1` (UTC) = first Monday of each month at 9am PT
   - **Environment**: the same environment used for `aeo_crosslink_audit` (has `warpdotdev/docs` and buzz workspace checked out)
   - **Branch**: `main`
