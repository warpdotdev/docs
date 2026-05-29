---
name: aeo_brief
description: Build a source-grounded AEO brief for Warp docs using Peec data, existing docs, and product terminology. Use whenever a docs request mentions AEO, answer-engine optimization, SEO visibility, Peec recommendations, AI search prompts, content gaps, search-query vocabulary, or deciding whether to create new docs versus update existing docs.
---

# AEO brief

Create a concise, source-grounded brief before drafting or revising AEO-driven Warp documentation. The brief should help the human reviewer decide what content is worth creating and help the drafting agent use the right vocabulary without turning the doc into a keyword dump.

## When to use

Use this skill when the user asks for docs work based on:
- AEO, answer-engine optimization, AI search visibility, or SEO goals
- Peec recommendations, prompts, topics, search queries, or source URLs
- A content gap, competitive/source-data comparison, or ranking opportunity
- A question about whether to create a new page, update an existing page, or avoid duplicative content

If the task is not AEO-driven, use the normal docs drafting workflow instead.

## Inputs to gather

Start with the smallest set of inputs that can support a useful brief:
- **Goal** - What decision or draft should this brief support?
- **Target topic** - The feature, workflow, product area, or user problem.
- **Known source data** - Peec project, prompts, topics, recommendations, source URLs, or notes supplied by the user.
- **Target docs area** - Existing page, section, or proposed new page if known.
- **Open questions** - Anything that affects scope, placement, or product accuracy.

Ask the user only when a missing input blocks the brief. Otherwise, use the available context and flag assumptions as open questions.

## Peec research workflow

Use the Peec MCP when available. Prefer source data over invented SEO advice.

1. **Resolve the project.** Use `list_projects` if the project ID is not already known.
2. **Find relevant prompts.** Use `list_prompts` to identify prompts tied to the topic, tag, or project. Capture the exact prompt text when it informs the brief.
3. **Extract search-query vocabulary.** Use `list_search_queries` for the relevant prompts, topic, or date range. Group repeated phrasing and note user-language variants, not every raw query.
4. **Inspect recommendations.** Use `get_actions` with `scope=overview` first, then drill into the highest-opportunity slices that matter for docs content. Use the returned recommendation text as the source of truth.
5. **Review source URLs when useful.** Use `get_url_content` for specific source URLs when the brief needs to compare content coverage, language, or examples.

Keep Peec output compact. The brief should explain what the data suggests, not reproduce a full report.

## Repo research workflow

Ground every recommendation in the current docs:
- Read `AGENTS.md` and `.agents/references/terminology.md` when drafting language or naming product surfaces.
- Search existing docs for the target topic before recommending a new page.
- Identify the best existing pages to update, link from, or avoid duplicating.
- Note when a proposed topic risks becoming a thin page or junk-drawer doc.

## Vocabulary translation

Translate AEO/source-data language into user-facing docs language:
- Preserve high-intent search terms when they are accurate and useful.
- Replace vague or internal shorthand with precise product names and UI surfaces.
- Explain the feature or workflow in plain developer language before using branded terms.
- Avoid keyword stuffing. AEO vocabulary should appear where it helps readers understand the page.

Example pattern:
- **Source-data language** - “Track or observe AI agents in real time.”
- **Docs translation** - “Track and review cloud agent runs in the Agent Management Panel in the Warp app or the Runs page in the Oz web app.”

## Brief format

Return the brief in this structure:

## AEO brief

**Goal:** [What this brief supports.]

**Recommendation:** [Create a new page, update an existing page, merge into another page, or do not pursue yet.]

**Source signals:**
- [Peec prompt, search-query cluster, action recommendation, or source URL.]
- [Existing docs signal, gap, or duplication risk.]

**Vocabulary map:**
- **Users/answer engines say:** [Raw or clustered phrase.]
  **Docs should say:** [Natural, accurate Warp docs phrasing.]

**Content scope:**
- **Include** - [High-value topics, procedures, examples, or links.]
- **Avoid** - [Junk-drawer coverage, duplicate explanations, unsupported claims, or outdated terms.]

**Existing docs to touch or link:**
- `[path]` - [Why it matters.]

**Open questions for human review:**
- [Question that affects accuracy, positioning, or scope.]

## Handoff rules

- If the user asked for a plan, use the brief as research context before creating the plan.
- If the user asked for a draft, use the brief before drafting and include only the decisions that matter in the final summary.
- If the brief shows the content should not be created, recommend the smaller update instead of forcing a new page.
- If Peec or Notion data is unavailable, say what could not be verified and proceed with repo-grounded recommendations.
