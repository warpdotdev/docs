---
description: >-
  [1-2 sentences: what the feature does + primary user benefit.
  Lead with the benefit, include key terms for SEO.
  Use {{TOKEN}} syntax here for any product names that have a var in src/data/vars.ts.
  Example: "Use the {{WARP_AGENT_CLI}} to run agents."]
---
[VARS: Add this line immediately after the closing --- above if this page references any product names from src/data/vars.ts. Then use {VARS.KEY} for those names in the prose below.
`import { VARS } from '@data/vars';`
See AGENTS.md → Content variables for the full variable list and usage rules.]

# [Feature name — sentence case, capitalize only the first word and proper feature names]

[Opening paragraph: What this feature does and its primary benefit.
1-3 sentences. Lead with what the user can accomplish.]

:::note
[Optional: Key context the reader needs upfront, e.g., when they
DON'T need this feature, or a prerequisite they should know about.
Remove this callout if not needed.]
:::

## Key features

[Bulleted list. Bold term + dash + description for each.
Focus on what each capability means for the user.]

* **Feature A** - What it does and why it matters to the user.
* **Feature B** - What it does and why it matters to the user.

## How it works

[CONCEPTUAL section: explain the system behavior, architecture, or flow.
Explain "what" and "why" before "how."
Define new terms when they first appear.
IMPORTANT: Do NOT include step-by-step procedures in this section.
Keep the conceptual and procedural sections clearly separated.
State platform, plan, preview, or interactive-only limits next to the behavior they constrain.
Do not invent internal tool names or implementation details the reader cannot act on.]

## [Usage/configuration section — sentence case. Rename to match the feature, e.g., "Creating environments", "Configuring integrations"]

[PROCEDURAL section: step-by-step instructions.
Apply all procedural rules from AGENTS.md:
- Motivate steps before giving instructions
- Include expected outcomes after key steps
- Group related actions when they share the same UI context
- Verify every UI label, Settings path, and CLI flag against source or the live product before publishing. If you cannot verify one, omit it or mark it with an inline `{/* VERIFY: ... */}` comment and report it per step 9.5 of the draft_docs skill
- Prefer durable actions and outcomes over ephemeral chrome (glyph colors, pure layout narration)]

### Prerequisites

[Bulleted list with inline context for each prerequisite.
Include: what the thing is, where to get it, link to full reference.
For integrations and team features, include admin requirements, who gains access after install, and any per-user auth steps.]

### [Task name — sentence case. e.g., "Create an environment with the CLI"]

1. Step description.
2. Step description.
3. Step description.

## [Additional sections as needed — sentence case. e.g., "Managing X", "Advanced usage"]

[Repeat the conceptual or procedural pattern as appropriate.
Keep sections clearly delineated by type.]

## Related pages

[Required on new feature and integration pages so the page does not dead-end.
Cross-reference related features, sibling integrations, next steps, and deeper references.
Use descriptive link text. Include at least one sibling or overview link and one next-step workflow link.]

* [Related feature](path/to/page.md)
* [Deeper guide](path/to/page.md)
