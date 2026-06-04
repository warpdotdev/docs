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

## Source data

Use the smallest reliable set of source data needed to justify link changes:
- **Peec MCP** - Review recent prompts, recommendations, source URLs, and query vocabulary related to agents, cloud agents, and orchestration.
- **Google Search Console** - When available, use the environment's `GSC_SERVICE_ACCOUNT_CREDENTIALS_JSON` secret to inspect recent queries and pages related to agents, cloud agents, and orchestration.
- **Docs repo** - Search existing pages under `src/content/docs/` for relevant source pages, link targets, and related terminology.

If Peec or Google Search Console data is unavailable, say what could not be verified and proceed only with repo-grounded recommendations. Do not invent source signals.

## Workflow

1. **Gather source signals.** Use Peec MCP and Google Search Console data, when available, to identify relevant user language, prompts, recommendations, or pages.
2. **Search existing docs.** Look for pages under `src/content/docs/` that already mention or imply related concepts in agents, cloud agents, or orchestration.
3. **Identify link opportunities.** Find up to 5 internal cross-link opportunities where:
   - The source page already mentions or implies the related concept.
   - The target page exists.
   - The link helps a reader continue a real workflow.
   - The edit can be made with a small, natural copy change.
4. **Make only safe edits.** Add links with minimal surrounding copy changes. Preserve the existing page structure and voice.
5. **Run self-review.** Apply the quality gates in this skill before opening a PR or writing a no-change report.
6. **Open a PR or report no changes.** Open a PR only when there are at least 2 high-confidence link additions. Otherwise, write a no-change report in the Oz run output.

## Self-review before opening a PR

Before opening a PR, verify every proposed change:
- **Real signal** - Each link is backed by a Peec, Google Search Console, or existing-docs signal, not generic SEO advice.
- **Reader value** - Each link helps a developer understand or complete a real workflow.
- **Natural language** - The added link text reads naturally in context and is not keyword-stuffed.
- **Existing target** - Every internal link points to an existing file under `src/content/docs/`.
- **Navigation awareness** - Check `src/sidebar.ts` when a linked page is expected to appear in navigation.
- **Small scope** - The diff is limited to cross-linking and small copy changes needed to make links natural.
- **No broad rewrites** - Remove any edit that becomes a rewrite, strategy recommendation, or new content proposal.
- **No duplication** - Do not add links that create repetitive related-links lists or duplicate nearby links.

Run:

```bash
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

For the pilot, no-change reports stay in the Oz run output. If team input is needed, share the Oz run link manually in `#growth-docs`.

## Human review expectations

The human reviewer should be able to understand the PR or no-change report without replaying the full run. Optimize the output for quick review:
- Keep PRs small and focused.
- Explain the source signal behind each link.
- Flag any uncertainty directly.
- Avoid hiding product or terminology questions in the diff.

## Future expansion boundaries

Do not implement future expansion ideas in this pilot skill. If the audit finds opportunities outside internal cross-linking, mention them only as follow-up recommendations in the PR body or no-change report.

Possible future phases include:
- Existing-doc improvements such as terminology additions, clearer headings, or better descriptions.
- New-guide recommendations using AEO briefs before drafting.
- Cross-linking across docs and marketing pages.
- Broader Peec content-gap integration with Buzz's `peec-content-gap` workflow.
- Lightweight trend reporting across scheduled runs.
