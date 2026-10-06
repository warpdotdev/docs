---
title: [Sentence case, task-oriented, reading like a search query. Capture the non-branded query a developer would actually type: "How to set up Claude Code", not "How to set up Claude Code in Warp". Do not put "tutorial" or "guide" in the title. This renders as the page H1 — do not add an H1 in the body.]
description: >-
  [One to two sentences, 50-160 characters: what the reader will build or accomplish, in the
  non-branded phrasing they would search for. Example: "Set up Claude Code and run your
  first agentic coding session from the terminal."]
---
[BEFORE PUBLISHING: Delete every bracketed instruction in this file, including this one. They are guidance for the author, not page content.]
[VARS: If this page names a product from src/data/vars.ts, add `import { VARS } from '@data/vars';` below, then use {VARS.KEY} in prose and {{TOKEN}} in frontmatter. See AGENTS.md → Content variables.]
[AEO: If this page is driven by Peec, search-query, or answer-engine data, run `.agents/skills/aeo_brief/SKILL.md` first.]

[SCOPE: This is a tutorial — a full workflow, start to finish, with context at the decision points. If the task fits in about five minutes and 600 words of essential steps, it is a quickstart instead; use `.agents/templates/quickstart.md`. A tutorial also requires that a quickstart already exists for this product area. If none does, write that first.]

[Introduction: who this is for, what prior knowledge it assumes, and what the reader will build. Do NOT state an expected completion time — it varies too much by experience level. (Quickstarts do state one; tutorials do not.)]

[BREVITY: Delete any section below you don't need — a short page is a finished page. See AGENTS.md → Voice & tone → Cut again.]

import VideoEmbed from '@components/VideoEmbed.astro';

[VIDEO: The `title` prop must name the workflow or feature shown, never "video" or "demo". Delete this block entirely if there is no video. The written content must stand alone either way — a reader should never need to watch to follow along.]
<VideoEmbed url="[YouTube or Loom URL]" title="[Specific workflow, integration, or task shown]" />

## Prerequisites

[Each item: what it is, where to get it, and a link. Name the application before any menu path.]

* **[Prerequisite]** — [What it is and where to get it]. See [link](path) for details.

## [1. First step — action-oriented title]

[STEP HEADINGS: Number each H2. Do not add a "## Steps" wrapper heading — go straight into the numbered steps after Prerequisites.]

[One sentence of motivation: why the reader is doing this.]

[Give the real prompt or command, not a placeholder. Use ALL_CAPS for values the reader substitutes, like YOUR_API_KEY.]

```
[prompt or command]
```

[Expected outcome: what should happen after this step.]

## [2. Next step]

[Same pattern: motivation, instruction, expected outcome.]

## Troubleshooting

[Required for tutorials — this is the clearest line between a tutorial and a quickstart, which only links out. Name what commonly goes wrong in this specific workflow and how to recover.]

**[What the reader sees when it breaks]**\
Why it happens, and how to recover.

## Productivity tips

[OPTIONAL. Warp features that extend the workflow the reader just completed — not a sales pitch. Delete this section if nothing fits naturally.]

* **[Feature]** — [How it improves the workflow they just learned.] See [link](path).

## Next steps

[Recap what the reader built, referring back to the example from the introduction. Then 2-3 actionable next steps.]

[CROSS-LINKING: Link at least one other page in the Guides section and one feature page in the main docs. Verify every internal link resolves to a real file under `src/content/docs/` before publishing — do not invent plausible-looking paths.]

* [Related tutorial in the Guides section](path/to/page.md)
* [Feature documentation in the main docs](path/to/page.md)
