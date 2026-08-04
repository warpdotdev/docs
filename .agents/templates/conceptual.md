---
title: [Feature or concept name — sentence case. Title convention: noun or "About [subject]". The title field renders as the page H1; do not add a separate H1 in the body.
  Use {{TOKEN}} syntax for any product names in src/data/vars.ts.]
description: >-
  [1-2 sentences: what the concept/feature is + why it matters.
  Write as a standalone summary for search results (benefit + keywords).
  Do NOT write "This page describes..." or only restate the title.
  Use {{TOKEN}} syntax for any product names in src/data/vars.ts.]
---
[VARS: Add this line immediately after the closing --- above if this page references any product names from src/data/vars.ts. Then use {VARS.KEY} for those names in the prose below.
`import { VARS } from '@data/vars';`
See AGENTS.md → Content variables for the full variable list and usage rules.]

[Opening paragraph: What this feature/concept is and its primary benefit.
1-3 sentences. Lead with what the user gains from understanding this.]

## [Key concepts or components — sentence case, specific to the subject. Not "Overview" or "More details"]

[Explain the main ideas, components, or building blocks the reader needs
to understand. Use `*` bulleted lists with bold term + hyphen + description.]

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

[Required on new conceptual pages. Cross-references to related features,
procedural guides, and deeper references.
Use descriptive link text that names the destination — not "here" or "this page".]

* [Related feature](path/to/page.md)
* [How to configure X](path/to/procedural-page.md)
