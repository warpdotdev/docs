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
Do NOT embed full error messages here — put failures in Troubleshooting at the end.]

## [Usage/configuration section — sentence case. Rename to match the feature, e.g., "Creating environments", "Configuring integrations"]

[PROCEDURAL section: step-by-step instructions.
Order sections for the reader: Prerequisites → setup/config → day-to-day usage → advanced options.
Apply all procedural rules from AGENTS.md:
- Motivate steps before giving instructions
- Include expected outcomes after key steps
- Group related actions when they share the same UI context
- Name the app before the first Settings path or CLI command on this page]

### Prerequisites

[Bulleted list with inline context for each prerequisite.
Include: what the thing is, where to get it, link to full reference.]

### [Task name — sentence case. e.g., "Create an environment with the CLI"]

1. Step description.
2. Step description.
3. Step description.

## [Additional sections as needed — sentence case. e.g., "Managing X", "Advanced usage"]

[Repeat the conceptual or procedural pattern as appropriate.
Keep sections clearly delineated by type.
Avoid stacking multiple callouts; prefer short prose unless a caveat is easy to miss.]

## Troubleshooting

[Optional but recommended when the feature has common failures, permission errors, or exact platform error strings.
Place this section near the end of the page, before Related pages.
Format each item as: bold symptom or exact error message, then cause, then fix.
Do not scatter the same error callouts through earlier sections.]

## Related pages

[Cross-references to related features, next steps, deeper references.
Use descriptive link text. Include at least one related feature or next-step link on new feature pages.]

* [Related feature](path/to/page.md)
* [Deeper guide](path/to/page.md)
