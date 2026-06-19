---
name: improve-drafting-skills
description: Monthly outer loop agent that reads accumulated signal logs from agent-authored PRs and proposes targeted improvements to the drafting skills and templates. Part of the docs self-improvement loop architecture. Use when asked to run the drafting improvement loop, or as a scheduled monthly cloud agent.
---

# Improve drafting skills

Monthly outer loop agent. Reads three signal logs accumulated from agent-authored PRs, identifies the top recurring patterns in drafting errors, and opens a draft PR with targeted edits to the skills or templates that caused them.

This skill is part of the self-improvement loop architecture. See the architecture plan for context on the inner loops that populate the signal logs.

## Schedule

Monthly, first Monday of each month, 9am PT (`0 17 1-7 * 1` in UTC).

## Prerequisites

The following must be available in the cloud agent environment:

- Docs repo checked out at `main`
- `gh` CLI authenticated with write access to `warpdotdev/docs`
- `SLACK_BOT_TOKEN` — for posting a summary to `#growth-docs`
- `SLACK_CHANNEL_ID` — channel ID for `#growth-docs`

## Signal logs

Three input files, all in `.agents/logs/`:

- `human_review_feedback.jsonl` — human corrections and preferences collected after agent-authored PRs are merged. **Primary signal.** Fields: `date`, `pr`, `skill_used`, `file`, `feedback_type`, `severity`, `comment`, `tag`, `resolved_by`.
- `pr_review_runs.md` — markdown log of every `review-docs-pr` run on an agent-authored PR. **Secondary signal.** Fields: date, PR number, verdict, severity counts, top issue categories.
- `style_lint_runs.jsonl` — aggregated violation counts per check name from every style lint run on an agent-authored branch. **Tertiary signal.** Fields: `date`, `pr`, `branch`, `authored_by`, `skill_used`, `files_scanned`, `violations`.

## Feedback collector step

Before reading the logs, run the feedback collector to capture any merged agent-authored PRs from the past 30 days that have not yet been logged to `human_review_feedback.jsonl`:

1. Use `gh pr list --repo warpdotdev/docs --state merged --label oz-agent` or search for PRs with `oz-agent@warp.dev` as a commit author in the past 30 days.
2. For each such PR, use `gh pr view NNN --json reviews,comments` to extract human review comments and verdicts.
3. Also run `git diff MERGE_BASE..PR_HEAD -- src/content/docs/` to capture human follow-up edits made to the branch after the agent's last commit.
4. For each human comment or edit, append a record to `.agents/logs/human_review_feedback.jsonl`:
   ```json
   {"date":"YYYY-MM-DD","pr":"NNN","skill_used":"draft_feature_doc","file":"src/content/docs/path.mdx","feedback_type":"review_comment","severity":"important","comment":"Comment text here","tag":"[skill-feedback]","resolved_by":"human_edit"}
   ```
   - Set `tag` to the prefix found in the comment (`[skill-feedback]`, `[template-feedback]`, `[style-rule-gap]`) or `""` if none.
   - Set `feedback_type` to `"review_comment"`, `"human_edit"`, or `"review_verdict"`.
   - Skip comments from `oz-agent@warp.dev` or other bot actors.
5. Commit the updated `human_review_feedback.jsonl` directly to `main`:
   ```text
   chore: collect human review feedback for improve-drafting-skills run YYYY-MM-DD
   ```

## Workflow

### 1. Read the last 30 days of signal data

Parse all three log files and filter to entries from the past 30 days.

### 2. Aggregate patterns by signal strength

Group findings by pattern type. Use these thresholds before acting on a pattern:

| Signal type | Threshold to act |
|---|---|
| Human comment with `[skill-feedback]`, `[template-feedback]`, or `[style-rule-gap]` tag | 1 occurrence |
| Repeated human review comment or human edit across multiple PRs | 2+ PRs |
| `review-docs-pr` agent finding (from `pr_review_runs.md`) | 3+ occurrences |
| Style lint violation (from `style_lint_runs.jsonl`) | 3+ occurrences |

Weight human feedback above automated checks. A pattern meeting its threshold from the human feedback log overrides a contradicting pattern from style lint.

### 3. Rank top-5 actionable patterns

Identify up to 5 patterns that:
- Meet the threshold for their signal type
- Are not already explicitly addressed in the relevant skill or template (check before proposing any edit)
- Have a clear, targeted fix (not a vague recommendation)

For each pattern, identify the best improvement target:
1. `.agents/templates/*.md` — bracket instruction update; affects all 9 drafting skills automatically
2. `draft_docs/SKILL.md` step 6.5 (Critical formatting rules) — add or sharpen an example
3. Type-specific skill (e.g., `draft_feature_doc/SKILL.md`) — for violations that appear only in one content type

### 4. Check existing coverage

For each top pattern, read the relevant skill and template files to verify the issue is not already documented. If the rule exists but is vague or lacks a concrete example, that still qualifies for improvement.

### 5. Draft targeted edits

For each pattern selected for improvement:
- Make the smallest edit that would prevent the pattern from recurring
- Prefer adding a concrete ✅/❌ example over restating a rule in prose
- Do not restructure sections or rewrite prose not related to the pattern
- Cap the diff at 3 files total across all patterns

### 6. Self-review before opening a PR

Before opening a PR, verify:
- Each edit targets a real, recurring pattern backed by signal data
- Each edit is additive — nothing is removed from the existing skill or template
- The diff is limited to `.agents/skills/` and `.agents/templates/` files
- Run `python3 .agents/skills/style_lint/style_lint.py --changed` to confirm the edits themselves are clean

### 7. Open a draft PR

Open a draft PR with title:
```text
docs(skills): improve drafting skills from signal log patterns YYYY-MM-DD
```

PR body must include:
- **Patterns addressed** — list each pattern, its signal source (which log, which check/tag), and the occurrence count
- **Improvement targets** — which files were edited and why
- **Patterns reviewed but not acted on** — any patterns that met the threshold but were already covered or had insufficient signal
- **Open questions for human review** — any judgment calls about whether a proposed rule change is correct

Post a Slack summary to `#growth-docs`:
```
✅ Drafting skills improvement · YYYY-MM-DD
PR: [PR URL]
Patterns addressed: N (human feedback: N, agent review: N, style lint: N)
Top patterns: [pattern 1], [pattern 2], [pattern 3]
Oz run: [run URL]
```

If fewer than 2 actionable patterns are found, do not open a PR. Write a no-change report to the run output instead:

```text
## Drafting skills improvement — no-change report

**Date**: YYYY-MM-DD
**Signal window**: last 30 days
**Patterns reviewed**: N total, N below threshold, N already covered
**Why no PR was opened**: [reason]
**Suggested adjustment**: [one specific suggestion for the next run, e.g., lower a threshold or check a different log]
```

Post the no-change report link to Slack.

## Run log

After completing the run (PR opened or no-change report written), update `.agents/logs/style_lint_runs.jsonl` with a summary entry — no; this skill does not have its own run log. Its outputs are the PR itself and the Slack message, which are durable artifacts.

## Deployment

This skill is designed for a monthly Oz scheduled agent.

To deploy:
1. Push this skill to `main` in the docs repo.
2. Verify the Oz environment has `SLACK_BOT_TOKEN` and `SLACK_CHANNEL_ID` set.
3. In the Oz web app (oz.warp.dev), create a new scheduled agent:
   - **Skill**: `improve-drafting-skills` from `warpdotdev/docs`
   - **Schedule**: `0 17 1-7 * 1` (UTC) = first Monday of each month at 9am PT
   - **Environment**: the same environment used for `weekly-404-monitor` (already has `warpdotdev/docs` checked out)
   - **Branch**: `main`
