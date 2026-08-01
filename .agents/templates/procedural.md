---
description: >-
  [1-2 sentences: what the reader will accomplish.
  Task-oriented: "Create and manage X" or "Configure Y for Z."
  Use {{TOKEN}} syntax here for any product names that have a var in src/data/vars.ts.]
---
[VARS: Add this line immediately after the closing --- above if this page references any product names from src/data/vars.ts. Then use {VARS.KEY} for those names in the prose below.
`import { VARS } from '@data/vars';`
See AGENTS.md → Content variables for the full variable list and usage rules.]

# [Task-oriented title — sentence case. Title convention: gerund, e.g., "Configuring X" or "Managing X"]

[Opening paragraph: What the reader will accomplish and why.
1-2 sentences. Focus on the goal, not the tool.]

[AEO GUIDANCE: If this procedure is based on Peec, answer-engine prompts, search-query data, or AEO goals, create an AEO brief first using `.agents/skills/aeo_brief/SKILL.md`. Use the brief to translate source-data vocabulary into precise, natural docs language and confirm whether this belongs in a new page or an existing page.]

## Prerequisites

[Only if needed. Place prerequisites before any setup or usage steps.
Bulleted list with inline context for each prerequisite.
Each item should include: what it is (1 short clause), where to get or
create it, and a link to the full reference.
Name the app before Settings paths and CLI commands.
Example:
* **A Warp API key** - Authenticate API requests with a key from
  **Settings** > **Cloud platform** > **Oz Cloud API Keys** in the Warp app. See [API Keys](path) for details.]

## [Primary task name — sentence case. e.g., "Creating API keys"]

[Brief motivation: why the reader would do this (1 sentence).
Then numbered steps. Keep failure details for the Troubleshooting section below.]

1. Step description.
2. Step description.
3. Step description.

:::note
[Optional: tip, clarification, or "good to know" context
relevant to the steps above.]
:::

## [Secondary task or follow-up — sentence case. e.g., "Managing API keys"]

[Repeat the pattern: brief context, then numbered steps or
descriptive content as appropriate.]

## Troubleshooting

[Optional but recommended. Common issues the reader might encounter
while following these steps. Keep this section near the end of the page.
Put exact error messages here instead of weaving them through the steps above.
Format: symptom or exact error string as bold text, then cause and fix.
Use at most one callout in this section unless multiple unrelated failures need separation.]

## Best practices

[Optional. Bulleted list of actionable recommendations.
Bold the key action at the start of each item.]

* **Use environment variables** - Avoid passing secrets directly in commands.

[PRE-HANDOFF REVIEW: Before presenting the draft, check whether steps are easy to scan, whether each important step has an expected outcome, whether UI names and Settings paths are current, whether AEO vocabulary is natural rather than stuffed, and whether any step needs human product testing.]
