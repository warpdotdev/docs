---
description: >-
  [One sentence, 50-160 characters: the task the reader will complete.
  Start with an imperative verb, not "This page explains."
  Example: "Connect Slack to Oz so mentions and channel messages can trigger cloud agent runs."
  See AGENTS.md > Frontmatter > Descriptions by content type for the full rules.
  Use {{TOKEN}} syntax here for any product names that have a var in src/data/vars.ts.]
---
[VARS: Add this line immediately after the closing --- above if this page references any product names from src/data/vars.ts. Then use {VARS.KEY} for those names in the prose below.
`import { VARS } from '@data/vars';`
See AGENTS.md → Content variables for the full variable list and usage rules.]

# [Task-oriented title — sentence case. Title convention: gerund, e.g., "Configuring X" or "Managing X"]

[Opening paragraph: What the reader will accomplish and why.
1-2 sentences. Focus on the goal, not the tool.]

[BREVITY: Delete any section below you don't need for this task — a short page is a finished page. See AGENTS.md → Voice & tone → Cut again.]

[AEO GUIDANCE: If this procedure is based on Peec, answer-engine prompts, search-query data, or AEO goals, create an AEO brief first using `.agents/skills/aeo_brief/SKILL.md`. Use the brief to translate source-data vocabulary into precise, natural docs language and confirm whether this belongs in a new page or an existing page.]

## Prerequisites

[Only if needed. Bulleted list with inline context for each prerequisite.
Each item should include: what it is (1 short clause), where to get or
create it, and a link to the full reference.
Example:
* **A Warp API key** - Authenticate API requests with a key from
  **Settings** > **Cloud platform** > **Oz Cloud API Keys** in the Warp app. See [API Keys](path) for details.]

## [Primary task name — sentence case. e.g., "Creating API keys"]

[Brief motivation: why the reader would do this (1 sentence).
Then numbered steps.]

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
while following these steps.
Format: symptom/error as bold text, then cause and fix.]

## Best practices

[Optional. Bulleted list of actionable recommendations.
Bold the key action at the start of each item.]

* **Use environment variables** - Avoid passing secrets directly in commands.

[PRE-HANDOFF REVIEW: Before presenting the draft, check whether steps are easy to scan, whether each important step has an expected outcome, whether UI names and Settings paths are current, whether AEO vocabulary is natural rather than stuffed, and whether any step needs human product testing.]
