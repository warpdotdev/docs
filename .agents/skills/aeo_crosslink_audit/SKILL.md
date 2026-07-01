---
name: aeo_crosslink_audit
description: Run a narrow AEO cross-link audit for Warp docs using Peec, Google Search Console, and existing docs. Use for recurring or scheduled agents that should identify high-confidence internal cross-linking improvements for agents, cloud agents, and orchestration docs.
---

# AEO cross-link audit

Identify small, high-confidence internal cross-linking improvements for the Warp docs. This skill is designed for a recurring Oz scheduled agent that audits one narrow topic area, opens a small PR when there are safe changes, or writes a no-change report when there are not enough high-confidence opportunities.

## Scope

Use this skill only for the pilot topic area:
- Agents
- Cloud agents
- Orchestration

The audit should focus on one improvement type:
- Internal cross-links between existing docs pages

Do not:
- Create new pages.
- Rewrite large sections.
- Make broad SEO or AEO recommendations.
- Add keyword-stuffed text.
- Force Peec or Google Search Console signals into docs when they do not support a useful reader journey.

## Environment requirements

The following environment secrets should be set in the Oz cloud agent environment:

- `SLACK_BOT_TOKEN` — Slack bot token for posting to `#growth-docs`. If unavailable, write the notification body to the run output instead and skip Slack posting.
- `SLACK_CHANNEL_ID` — Slack channel ID for `#growth-docs`. Find it in Slack by right-clicking the channel → Copy link (the ID begins with `C`). If unavailable, skip Slack posting.

Do NOT print, log, commit, or include secret values in reports or Slack messages.

## Source data

Use the smallest reliable set of source data needed to justify link changes:
- **Peec snapshot** - Check freshness before using any data:
  1. Read `generated_at` from `/workspace/buzz/aeo-snapshots/docs/agents-orchestration/latest.json`.
  2. If the file is missing, `generated_at` is absent, or the snapshot is **14 days old or older**: write the stale-snapshot report (see "Stale snapshot report" below), write a run log entry (step 7) with the appropriate `No-change reason` (see "Stale snapshot report" for exact wording), post the stale Slack alert (step 8), and exit. Do not continue the audit or open a PR.
  3. If the snapshot is fewer than 14 days old, read both `latest.json` and `latest.md` as source signals. These contain pre-exported Peec data (prompts, recommendations, source URLs, query vocabulary, and visibility scores) for agents, cloud agents, and orchestration. The snapshots are generated locally (where Peec OAuth works) and committed to the buzz repo so cloud agents can use them.
- **Google Search Console** - When available, use the environment's `GSC_SERVICE_ACCOUNT_CREDENTIALS_JSON` secret to inspect recent queries and pages related to agents, cloud agents, and orchestration. Never print, log, commit, or include the secret value in reports. If a GSC client requires a credentials file path, write the secret to a restricted temporary file, use it for the run, and remove it before finishing.
- **Docs repo** - Search existing pages under `src/content/docs/` for relevant source pages, link targets, and related terminology.

If Google Search Console data is unavailable, say what could not be verified and proceed with Peec and docs-only analysis. If the Peec snapshot is stale or missing, exit via the staleness path above instead of proceeding. Do not invent source signals.

**Low-signal runs.** If neither live signal is usable for a run — the Peec snapshot has no usable prompt or recommendation data for these topics *and* Google Search Console is unavailable (missing credentials or a 403) — prefer a no-change report over a docs-only PR. Only open a PR in this case when there are at least 3 link additions that are each strongly grounded in existing on-page content and a clear reader journey. This prevents shipping weak, docs-only PRs that reviewers close.

## Workflow

1. **Check snapshot freshness, then gather source signals.** Read `generated_at` from `latest.json`. If the snapshot is missing or 14 days old or older, write the stale-snapshot report, write a run log entry (step 7), post the stale Slack alert (step 8), and exit — do not proceed further. If fresh, read both snapshot files and use Google Search Console data, when available, to identify relevant user language, prompts, recommendations, or pages.
2. **Search existing docs.** Look for pages under `src/content/docs/` that already mention or imply related concepts in agents, cloud agents, or orchestration.
3. **Identify link opportunities.** Find up to 5 internal cross-link opportunities where:
   - The source page already mentions or implies the related concept.
   - The target page exists.
   - The link helps a reader continue a real workflow.
   - The edit can be made with a small, natural copy change.
4. **Make only safe edits.** Add links with minimal surrounding copy changes. Preserve the existing page structure and voice. Follow the link quality rules below when choosing anchor text and surrounding context.
5. **Run self-review.** Apply the quality gates in this skill before opening a PR or writing a no-change report.
6. **Deduplicate, re-validate, then open a PR or report no changes.**
   - **Deduplicate first.** Check for an existing open AEO cross-link PR before opening one: `gh pr list --repo warpdotdev/docs --search 'docs: add AEO cross-links in:title' --state open`. Never leave two open AEO cross-link PRs. If one already exists, either skip this run (note it in the run output) or, if the existing PR is stale or superseded, close it with an explanatory comment before opening the new one.
   - **Re-validate against the latest `main`.** Fetch `origin/main` and confirm every edited file still exists at its path and every link target resolves to a current page (see "Self-review before opening a PR"). If a restructure moved your targets, rebase onto the latest `main` and fix paths before opening.
   - **Open a PR** only when there are at least 2 high-confidence link additions (at least 3 for low-signal runs; see "Source data"). Otherwise, write a no-change report in the Oz run output.

7. **Write run log entry (never commit to protected `main`).** `main` is a protected branch, so do not commit the log to it directly — this silently failed in early runs and left the log empty. Instead, record the entry through a single, long-lived log PR:

   1. Fetch and check out the remote branch `chore/aeo-crosslink-audit-log`. If it does not exist, create it from the latest `origin/main`.
   2. Prepend the new entry to `.agents/logs/aeo_crosslink_audit_runs.md` using the "Run log format" section below.
   3. Stage only that file and commit with this message:

      ```text
      chore: log aeo crosslink audit run YYYY-MM-DD
      ```

   4. Push the branch.
   5. Ensure exactly one open PR exists from `chore/aeo-crosslink-audit-log` into `main`, titled `chore: aeo crosslink audit run log`. Create it if missing; otherwise the push updates the existing PR. Keep this log PR separate from any cross-link docs PR.

   This produces one perpetual, low-noise PR that accumulates every run's entry regardless of outcome. Reviewers merge it periodically (at minimum before each monthly `improve-aeo-crosslink-skill` run) so the log reaches `main`. If any git step fails, write the log entry to the run output instead and continue to step 8.

8. **Post Slack notification.** After writing the log entry, post the formatted message to `#growth-docs` using the Python snippet below. Python is preferred over curl because it reads `SLACK_BOT_TOKEN` from the environment (keeping the token out of process argv) and JSON-encodes the payload correctly regardless of newlines or special characters. If either secret is unavailable, write the notification body to the run output instead.

   ```bash
   python3 - <<'SLACK_EOF'
   import os, json, urllib.request, sys

   token = os.environ.get("SLACK_BOT_TOKEN", "")
   channel = os.environ.get("SLACK_CHANNEL_ID", "")
   if not token or not channel:
       print("SLACK_BOT_TOKEN or SLACK_CHANNEL_ID not set — skipping Slack notification", file=sys.stderr)
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

   Replace `<message text here>` with the message from the appropriate format in the "Slack notification format" section. Do not print `SLACK_BOT_TOKEN` or `SLACK_CHANNEL_ID` values in the run output or in any file.

## Link quality rules

When adding links, follow the link style guidance in `AGENTS.md` and validate with `style_lint`.

- **Use descriptive anchors** - Link meaningful destination text, not generic phrases like "here," "this page," "learn more," "read more," or raw URLs.
- **Add context before the link when needed** - If the destination page is not obvious from the sentence, introduce why the reader should follow it. Do not drop a link into a sentence without explaining its relevance.
- **Use natural destination-page phrasing** - Prefer wording like "the Runs page in the Oz web app," "the Scheduled Agents guide," or "the Slack integration guide" when naming a destination.
- **Avoid redundant prefixes** - Do not add a bold term or label immediately before a link if the link text already provides the context.
- **Keep links reader-first** - The link should help a developer continue the task or understand the concept, not exist only for SEO/AEO coverage.
- **Avoid link stuffing** - Do not add multiple links to the same nearby destination or turn a paragraph into a dense cluster of links.
- **Limit link density** - Prefer 1-2 link additions per page. Do not add more than 3 links to a single page unless the page is an overview or hub, or the page currently has very few existing links and each new link supports a distinct reader next step.
- **Avoid related-link lists by default** - Do not add new "Related pages," "See also," or link-list sections unless the page already uses that pattern or the list clearly improves a reader's next step.
- **Justify each link as a reader journey** - In the PR body, explain what the reader is likely trying to do next and why the destination helps. Do not justify links only with AEO or search coverage.
- **Resolve redirects** - Link directly to the final destination page when known. Do not add redirecting URLs or old paths.

## Self-review before opening a PR

Before opening a PR, verify every proposed change:
- **Real signal** - Each link is backed by a Peec, Google Search Console, or existing-docs signal, not generic SEO advice.
- **Reader value** - Each link helps a developer understand or complete a real workflow.
- **Natural language** - The added link text reads naturally in context and is not keyword-stuffed.
- **Anchor quality** - Link text is descriptive and specific; no raw URL anchors or generic anchors like "here," "this page," "learn more," or "read more."
- **Link context** - The surrounding sentence explains why the destination is relevant when the link target is not obvious.
- **Link density** - The page does not feel visually noisy after the edit. Avoid clusters of links in one paragraph or section.
- **Reader journey** - Each link has a clear next-step rationale in the PR body.
- **Existing target** - Every internal link points to an existing file under `src/content/docs/`.
- **Anchor and route validation** - If a link includes a heading anchor or route path, verify that the route and anchor resolve. Do not rely only on the target file existing.
- **Navigation awareness** - Check `src/sidebar.ts` when a linked page is expected to appear in navigation.
- **Fresh-tree validation** - Immediately before opening the PR, fetch the latest `origin/main` and confirm every edited file and every link target still exists there. A docs restructure can move or rename target pages after the run starts.
- **Redirect resolution** - Check `vercel.json`. If a link target path appears as a redirect `source`, link to its final `destination` instead of the redirecting path.
- **Small scope** - The diff is limited to cross-linking and small copy changes needed to make links natural.
- **No broad rewrites** - Remove any edit that becomes a rewrite, strategy recommendation, or new content proposal.
- **No duplication** - Do not add links that create repetitive related-links lists or duplicate nearby links.

Run:

```bash
git fetch origin main
python3 .agents/skills/style_lint/style_lint.py --changed
python3 .agents/skills/check_for_broken_links/check_links.py --internal-only
git diff --check
```

## PR requirements

Open a PR only when there are at least 2 high-confidence link additions.

Use this title format:

```text
docs: add AEO cross-links for agents and orchestration
```

The PR body must include an AEO brief. Use `.agents/skills/aeo_brief/SKILL.md` as the format and include:
- **Goal** - Identify small internal cross-link improvements for agents, cloud agents, and orchestration docs.
- **Source signals** - Peec prompts/recommendations, Google Search Console queries/pages, or existing-docs signals that justified the links.
- **Pages touched** - Files edited and why.
- **Links added** - Source page, target page, and rationale for each link.
- **Reader next step** - What the reader is likely trying to do next and why each destination helps.
- **Open questions for human review** - Anything that affects product accuracy, terminology, or placement.

Request review from docs and growth-docs reviewers where possible, including:
- Rachael
- Petra
- Hong Yi
- Danny
- Other active reviewers in `#growth-docs`

## No-change report

If there are fewer than 2 high-confidence link opportunities, do not open a PR. Write a no-change report in the Oz run output so reviewers can inspect it from the Oz web app Runs page and shared session history.

Use this format:

```text
## AEO cross-link audit no-change report

**Topic area:** Agents, cloud agents, and orchestration.

**Source signals reviewed:**
- [Peec prompt, recommendation, source URL, or query vocabulary.]
- [Google Search Console query, page, or trend.]
- [Existing-docs signal.]

**Docs pages inspected:**
- `[path]` - [Why it was inspected.]

**Candidate links rejected:**
- `[source path]` → `[target path]` - [Why this was not high-confidence.]

**Why no PR was opened:**
- [Reason.]

**Suggested prompt or skill improvement:**
- [One specific improvement for the next run.]
```

No-change reports stay in the Oz run output. The Oz run link is posted automatically to `#growth-docs` as part of step 8.

## Stale snapshot report

If the Peec snapshot is missing or 14 days old or older, stop immediately. Write this report to the Oz run output:

```text
## AEO cross-link audit — snapshot stale

**Date:** YYYY-MM-DD
**Snapshot age:** [N days (generated YYYY-MM-DD) | file not found | generated_at field missing]
**Threshold:** 14 days

The Peec snapshot is too old to support a high-confidence audit. No PR was opened and no docs were changed.

**Action required:**
Run the `refresh-peec-aeo-snapshot` skill in a local Warp agent session where Peec MCP is authenticated.
Skill: buzz/.agents/skills/refresh-peec-aeo-snapshot/SKILL.md

The audit will run normally on the next scheduled execution once a fresh snapshot is committed to the buzz repo.
```

Fill in the `Snapshot age` field as follows — do not invent values:
- File exists and `generated_at` is present: `N days (generated YYYY-MM-DD)` — compute `N` from today's date minus `generated_at`.
- File does not exist: `file not found`.
- File exists but `generated_at` is absent or unparseable: `generated_at field missing`.

Use the same wording in the `No-change reason` field of the run log entry:
- File stale: `snapshot stale — N days old`
- File missing: `snapshot missing — file not found`
- Field missing: `snapshot missing — generated_at field absent`

Then post the stale Slack alert (step 8). Exit. Do not write a no-change report. Do not open a PR.

## Human review expectations

The human reviewer should be able to understand the PR or no-change report without replaying the full run. Optimize the output for quick review:
- Keep PRs small and focused.
- Explain the source signal behind each link.
- Flag any uncertainty directly.
- Avoid hiding product or terminology questions in the diff.

## Run log format

Prepend each new entry at the top of `.agents/logs/aeo_crosslink_audit_runs.md`, immediately after the `---` separator line. Use this format:

```markdown
## YYYY-MM-DD — [PR opened | No change | Snapshot stale]

- **Run**: [Oz run URL if available, otherwise the run ID]
- **Source signals**: Peec [available | unavailable], GSC [available | unavailable]
- **PR**: [PR URL | N/A]
- **Links proposed / added**: [N proposed, N added | N/A]
- **Pages touched**: [comma-separated file paths | N/A]
- **Themes**: [one sentence on recurring content gaps or topics observed, or "none observed"]
- **No-change reason**: [low confidence | lack of signals | snapshot stale — N days old | N/A]
```

Keep each entry to 7 fields and under 10 lines. Do not add narrative prose.

## Slack notification format

Use a simple text message (not Block Kit). The message should be scannable in under 30 seconds.

**PR opened:**

```
✅ AEO crosslink audit · YYYY-MM-DD
PR opened: [PR URL]
Links added: [N links] across [N pages]: [page names]
Signals: [Peec | GSC | Peec + GSC]
Oz run: [run URL]
```

**No change:**

```
ℹ️ AEO crosslink audit · YYYY-MM-DD — No changes
Checked: agents, cloud agents, and orchestration docs
No PR: [brief reason — e.g., "fewer than 2 high-confidence opportunities"]
Oz run: [run URL]
```

**Snapshot stale:**

```
⚠️ AEO crosslink audit · YYYY-MM-DD — Snapshot stale
Snapshot: [N days old (generated YYYY-MM-DD) | file not found | generated_at missing], threshold: 14 days
No audit ran. Refresh the snapshot before the next run.
How: run refresh-peec-aeo-snapshot in a local Warp session
Skill: buzz/.agents/skills/refresh-peec-aeo-snapshot/SKILL.md
Oz run: [run URL]
```

Rules:
- Post on every run, including no-change runs.
- Never include raw secret values, personal access tokens, or credential file paths in the Slack message.
- If the Oz run URL is unavailable, omit that line rather than posting a broken link.

## Future expansion boundaries

Do not implement future expansion ideas in this pilot skill. If the audit finds opportunities outside internal cross-linking, mention them only as follow-up recommendations in the PR body or no-change report.

Possible future phases include:
- Existing-doc improvements such as terminology additions, clearer headings, or better descriptions.
- New-guide recommendations using AEO briefs before drafting.
- Cross-linking across docs and marketing pages.
- Broader Peec content-gap integration with Buzz's `peec-content-gap` workflow.
- Lightweight trend reporting across scheduled runs.
