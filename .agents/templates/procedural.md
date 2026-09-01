---
title: [Sentence case, beginning with a gerund that names the task. Example: "Configuring a self-hosted GitLab integration". Not "Self-hosted GitLab integration setup". This renders as the page H1 — do not add an H1 in the body.]
description: >-
  [One to two sentences, 50-160 characters: the task the reader will complete. Start with an
  imperative verb, not "This page explains". Example: "Connect Slack to the Automation
  Platform so mentions and channel messages can trigger cloud agent runs."
  Use {{TOKEN}} syntax for product names in src/data/vars.ts.]
---
[BEFORE PUBLISHING: Delete every bracketed instruction in this file, including this one. They are guidance for the author, not page content.]
[VARS: If this page names a product from src/data/vars.ts, add `import { VARS } from '@data/vars';` on the line directly below the frontmatter, then use {VARS.KEY} in prose. See AGENTS.md → Content variables.]
[AEO: If this page is driven by Peec, search-query, or answer-engine data, run `.agents/skills/aeo_brief/SKILL.md` first.]

[Opening paragraph: what the reader will accomplish and why. 1-2 sentences. Focus on the goal, not the tool.]

[BREVITY: Delete any section below you don't need for this task — a short page is a finished page. See AGENTS.md → Voice & tone → Cut again.]

## Prerequisites

[Only if needed. Each item needs inline context: what it is in one clause, where to get it, and a link to the full reference. Assume the reader arrived here directly.]

* **A Warp API key** - Authenticate API requests with a key from **Settings** > **Cloud platform** > **API keys** in the Warp app. See [API keys](path) for details.

## [Primary task — sentence case, e.g. "Creating an API key"]

[One sentence of motivation before the steps. Explain why the reader is doing this, so they are not left wondering. Then the numbered steps.]

1. Step description. [Include the expected outcome where it is not obvious, so the reader can confirm they are on track.]
2. Step description.
3. Step description.

[STEP SIZING: Aim for one primary action per step, but group tightly related actions that share the same UI context — up to about three. A simple task should not need 10+ steps, and a single step should not be a mini-procedure.]

:::note
[Optional. One or two callouts per page at most; prefer body prose. Delete if nothing applies.]
:::

## [Secondary task — sentence case, e.g. "Rotating an API key"]

[Same pattern: motivation, then steps. Order sections by reader chronology — requirements, setup, usage, management, then destructive actions.]

## Troubleshooting

[Recommended. Keep error messages here rather than woven through the steps above. Format each as the symptom in bold, then cause, then fix.]

**Exact error message the user sees**\
Why it happens, and how to fix it.

## Related pages

[Cross-links. Use descriptive link text that names the destination.]

* [Conceptual page for this feature](path/to/page.md)
* [Related task](path/to/page.md)
