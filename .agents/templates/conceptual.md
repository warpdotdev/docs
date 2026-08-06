---
title: [Feature or concept name — sentence case. Title convention: noun or "About [subject]". The title field renders as the page H1; do not add a separate H1 in the body.
  Use {{TOKEN}} syntax for any product names in src/data/vars.ts.]
description: >-
  [One sentence, 50-160 characters: what the concept is and why it matters.
  Start with the subject, not "Learn about" or "This page covers."
  Example: "Environments give cloud agents the same toolchain and setup on every run, no matter what triggers them."
  See AGENTS.md > Frontmatter > Descriptions by content type for the full rules.
  Use {{TOKEN}} syntax for any product names in src/data/vars.ts.]
---
[VARS: Add this line immediately after the closing --- above if this page references any product names from src/data/vars.ts. Then use {VARS.KEY} for those names in the prose below.
`import { VARS } from '@data/vars';`
See AGENTS.md → Content variables for the full variable list and usage rules.]

[Opening paragraph: What this feature/concept is and its primary benefit.
1-3 sentences. Lead with what the user gains from understanding this.]

## [Key concepts or components — sentence case. Rename to match the subject]

[Explain the main ideas, components, or building blocks the reader needs
to understand. Use bulleted lists with bold term + dash + description.]

* **Concept A** - What it is and why it matters.
* **Concept B** - What it is and why it matters.

## How it works

[Explain the system behavior, architecture, or data flow.
Focus on "what" and "why" before "how."
Define new terms when they first appear.
Use diagrams or architecture descriptions where they clarify relationships.
IMPORTANT: Do NOT include step-by-step procedures here.
Link to a procedural or quickstart page instead.]

## When to use [feature name]

[Decision guidance: when to use this feature and when not to.
Help the reader decide if this is the right tool for their situation.]

## Related pages

[Cross-references to related features, procedural guides, and deeper references.
Use descriptive link text.]

* [Related feature](path/to/page.md)
* [How to configure X](path/to/procedural-page.md)
