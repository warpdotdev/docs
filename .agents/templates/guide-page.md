---
title: [Task-oriented title in sentence case — reads like a search query. Capture the non-branded query a developer would actually search for, not "How to do X in Warp." The title field renders as the page H1; do not add a separate H1 in the body.]
description: >-
  [One sentence, 50-160 characters: what the reader will build or accomplish,
  using the non-branded phrasing they would actually search for.
  Example: "Set up Claude Code and run your first agentic coding session from the terminal."
  See AGENTS.md > Frontmatter > Descriptions by content type for the full rules.]
---

[One sentence: what you'll accomplish by following this guide. Mention Warp by name. Include a time estimate if possible (e.g., "takes about 10 minutes").]

[AEO GUIDANCE: If this guide is based on Peec, answer-engine prompts, search-query data, or AEO goals, create an AEO brief first using `.agents/skills/aeo_brief/SKILL.md`. Use the brief to preserve high-intent vocabulary naturally, translate awkward source-data phrasing into developer-friendly docs language, and decide whether this should be a new guide or an update to an existing page.]

import VideoEmbed from '@components/VideoEmbed.astro';
{/* VARS: Also add the line below if this guide references product names from src/data/vars.ts. Then use {VARS.KEY} in prose. Use {{TOKEN}} in frontmatter YAML values above. See AGENTS.md → Content variables. */}
{/* import { VARS } from '@data/vars'; */}

{/* VIDEO: Always include a specific title prop naming the workflow/feature shown. Remove the entire VideoEmbed block if there is no video. */}
<VideoEmbed url="[YouTube or Loom URL]" title="[Specific title: integration, workflow, or task shown — not generic 'video' or 'demo']" />

## Prerequisites

[List what the reader needs before starting. Include inline context: what each prerequisite is, where to get it, and a link to more info. Orient the reader by naming the application before any menu paths.]

* **[Prerequisite 1]** — [What it is and where to get it]. See [link to docs] for details.
* **[Prerequisite 2]** — [Brief context].

[Use numbered H2 headings for each step (e.g., "## 1. Install Claude Code"). Do not add a "## Steps" wrapper heading — jump straight into the numbered steps after Prerequisites. Motivate each step: explain WHY before HOW, especially for setup steps. End each numbered sub-step with a period. Use ALL_CAPS for placeholder values in commands (e.g., YOUR_API_KEY). Do not use em dashes in procedural or instructional text. If there's an open-source repo for an example, link it. When referencing a Settings path or menu for the first time, orient the reader: "in the Warp app, go to **Settings** > ...".]

## [Action-oriented step title]

[Why you're doing this step — 1 sentence of motivation.]

[Exact prompt, command, or instruction:]

```
[prompt or command here]
```

[Expected outcome — what should happen after this step.]

## [Next step title]

[Motivation + instruction + expected outcome, same pattern as above.]

## [Final step title]

[Complete the workflow.]

## Productivity tips

[OPTIONAL SECTION — include when the guide naturally leads to workflow improvements. Use this to showcase Warp features (voice, images, vertical tabs, notifications, code review, etc.) as natural extensions of the workflow the reader just completed — not as a separate sales pitch. Remove this section if there are no relevant tips for the guide topic.]

* **[Tip 1 — feature name]** — [How it improves the workflow the reader just learned. Link to feature docs.]
* **[Tip 2]** — [Same pattern.]

## Next steps

[2-3 sentence summary of what the reader accomplished. Then list links to related content. CROSS-LINKING: Always link to at least one other guide in the Guides section and one feature documentation page in the main docs. If this guide relates to features covered in the Third-Party CLI Agents section (src/content/docs/agent-platform/cli-agents/), link there too. If a standalone summary section feels valuable, add a ## Recap heading above the summary paragraph.]

* [Link to related guide in the Guides section]
* [Link to relevant feature documentation in the main docs]
* [Link to deeper reference or advanced usage]

[LINK VERIFICATION: Before publishing, verify every internal link points to an existing file under `src/content/docs/` and, when the page should appear in navigation, a matching entry in `src/sidebar.ts`. If a target page is planned but not live, use the closest existing page and add a TODO comment.]

[PRE-HANDOFF REVIEW: Before presenting the draft, check whether procedures are easy to scan, whether dense sections should become numbered steps or bullets, whether UI surfaces use canonical product names, whether the page adds value beyond existing docs, and whether any product behavior needs human testing.]
