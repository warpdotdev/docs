---
description: >-
  [One sentence, 50-160 characters: what the reader ends up with, plus the time budget.
  Start with an imperative verb, not "Learn how to" or "Get started with."
  Example: "Install the {{WARP_AGENT_CLI}}, log in, and run your first agent conversation in about five minutes."
  See AGENTS.md > Frontmatter > Descriptions by content type for the full rules.
  Use {{TOKEN}} syntax here for any product names that have a var in src/data/vars.ts.]
---
[VARS: Add this line immediately after the closing --- above if this page references any product names from src/data/vars.ts. Then use {VARS.KEY} for those names in the prose below.
`import { VARS } from '@data/vars';`
See AGENTS.md → Content variables for the full variable list and usage rules.]

# [Descriptive title — sentence case. Title convention: "[Feature] quickstart" or "Quickstart for [product]". Do NOT use a bare "Quickstart" — include the feature name.]

[Opening paragraph: What the reader will accomplish, who it's for,
and approximately how long it takes (~10 minutes).
1-3 sentences. Keep it brief — this is about speed.]

***

## Prerequisites

[Minimal. Link to full setup docs rather than inlining lengthy setup.
The reader should be able to start quickly.]

* **Prerequisite 1** - Brief description with [link to details](path)
* **Prerequisite 2** - Brief description

***

## [Primary workflow — sentence case. e.g., "Running your first cloud agent"]

_~10 minutes_

### 1. Step title

[Steps can be less formal than full procedural content.
Use heavy visual cues: code blocks, screenshots.
Keep on the critical path — defer edge cases to other pages.]

### 2. Step title

### 3. Step title

***

## Next steps

[2-3 actionable next steps. Always link to conceptual content about the
feature and to deeper procedural guides.]

* [Deeper guide](path/to/page.md)
* [Related feature](path/to/page.md)

## Troubleshooting

[Brief. Only the most common issues someone might hit during the quickstart.
For comprehensive troubleshooting, link to the dedicated page.]

**Issue description**\
Cause and fix.
