---
title: [Sentence case. Use "About [subject]" or a plain noun phrase naming the subject. Not "Understanding how X works". This renders as the page H1 — do not add an H1 in the body.]
description: >-
  [One to two sentences, 50-160 characters: what the thing is and why it matters. Start with the
  subject, not "Learn about". Example: "Environments give cloud agents the same toolchain
  and setup on every run, no matter what triggers them."
  Use {{TOKEN}} syntax for product names in src/data/vars.ts.]
---
[BEFORE PUBLISHING: Delete every bracketed instruction in this file, including this one. They are guidance for the author, not page content.]
[VARS: If this page names a product from src/data/vars.ts, add `import { VARS } from '@data/vars';` on the line directly below the frontmatter, then use {VARS.KEY} in prose. See AGENTS.md → Content variables.]

[Opening paragraph: what this concept is and its primary benefit. 1-3 sentences. Lead with what the reader gains from understanding it. Assume they arrived here directly, not from a parent page.]

[BREVITY: Delete any section below you don't need for this page — a short page is a finished page. See AGENTS.md → Voice & tone → Cut again.]

## [Key concepts — sentence case, renamed to match the subject]

[The main ideas or components the reader needs. Bold term + hyphen + description.]

* **Concept A** - What it is and why it matters.
* **Concept B** - What it is and why it matters.

## How it works

[System behavior, architecture, or data flow. Answer "what" and "why" before "how". Define new terms on first use. Diagrams help where relationships are hard to describe in prose.]

[Do NOT put step-by-step procedures here. Link to a procedural or quickstart page instead.]

## When to use [subject]

[Decision guidance: when this is the right tool, and when it is not. The "when not to" half is the part readers cannot get anywhere else.]

## Related pages

[Cross-links to related features, the procedural page for doing this, and deeper references. Use descriptive link text that names the destination.]

* [Related feature](path/to/page.md)
* [How to configure X](path/to/procedural-page.md)

[STRUCTURE: Every block of content should sit under a header. Content before the first header is not linkable in the table of contents.]
