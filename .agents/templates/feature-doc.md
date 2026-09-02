---
title: [Sentence case, task-based gerund when the page contains a procedure. Keep it general enough to cover the range of tasks on the page and agnostic about which option the reader picks: "Setting repository visibility", not "Making a private repository public". This renders as the page H1 — do not add an H1 in the body.]
description: >-
  [One to two sentences, 50-160 characters: what the feature does and its primary benefit. Example:
  "Control what the agent can do with permission cards, auto-approve, and execution profiles."
  Use {{TOKEN}} syntax for product names in src/data/vars.ts.]
---
[BEFORE PUBLISHING: Delete every bracketed instruction in this file, including this one. They are guidance for the author, not page content.]
[VARS: If this page names a product from src/data/vars.ts, add `import { VARS } from '@data/vars';` on the line directly below the frontmatter, then use {VARS.KEY} in prose. See AGENTS.md → Content variables.]

[This is the most common page type in Warp's docs (~75+ pages) and the one most prone to sprawl, because it accepts the most kinds of content. Two limits:

1. Never fold quickstart or tutorial content in here. Both are defined by a scope budget and a single continuous path, and both lose their purpose once embedded in a longer page. Link to them instead. Conceptual, procedural, reference, and troubleshooting sections can coexist here; those two cannot.
2. Past roughly 1500 words, split the procedures onto their own pages rather than adding another section.]

[Opening paragraph: what the feature does and its primary benefit. 1-3 sentences. Lead with what the reader can accomplish, not the implementation.]

[BREVITY: Delete any section below you don't need — a short page is a finished page. See AGENTS.md → Voice & tone → Cut again.]

:::note
[Optional. Key context the reader needs upfront — a prerequisite, a limitation, or when NOT to use this. Delete if nothing applies.]
:::

## Key features

[2-4 capabilities. Bold term + hyphen + what it means for the reader. Collapse this into the opening paragraph if the feature is simple enough that a list is padding.]

* **Feature A** - What it does and why it matters to the user.
* **Feature B** - What it does and why it matters to the user.

## How it works

[CONCEPTUAL section. System behavior, architecture, or flow. Answer "what" and "why" before "how". Define new terms on first use. No step-by-step procedures here — keep the conceptual and procedural halves clearly separated.]

## [Usage or configuration — sentence case, renamed to match the feature, e.g. "Creating environments"]

[PROCEDURAL section. Motivate before instructing, include expected outcomes after key steps, and group related actions that share a UI context. Bold clickable controls and selected options; put non-clickable field labels in quotation marks ("Harness" dropdown, not **Harness** dropdown). Keep steps short — cut internal implementation detail and move reference lists into a :::note or a linked page.]

### Prerequisites

[Inline context for each: what it is, where to get it, and a link to the full reference.]

### [Task name — sentence case, e.g. "Create an environment with the CLI"]

1. Step description.
2. Step description.

## [Additional sections as needed]

[ORDER: broad to specific. Conceptual, then reference, then procedures in lifecycle order — enable, use, manage, disable, destructive actions — then troubleshooting.]

## Related pages

[Cross-links. Use descriptive link text that names the destination. If a quickstart or tutorial exists for this feature, link it here rather than inlining it above.]

* [Related feature](path/to/page.md)
* [Quickstart for this feature](path/to/page.md)
