---
title: [Sentence case, naming the feature. Use "Quickstart for [product]" or "[Feature] quickstart". Never a bare "Quickstart". This renders as the page H1 — do not add an H1 in the body.]
description: >-
  [One to two sentences, 50-160 characters: what the reader ends up with. Include a supported
  time estimate when available; omit it when unverified.
  Start with an imperative verb, not "Learn how to" or "Get started with". Example:
  "Install the {{WARP_AGENT_CLI}}, log in, and run your first agent conversation in about
  five minutes." Use {{TOKEN}} syntax for product names in src/data/vars.ts.]
---
[BEFORE PUBLISHING: Delete every bracketed instruction in this file, including this one. They are guidance for the author, not page content.]
[VARS: If this page names a product from src/data/vars.ts, add `import { VARS } from '@data/vars';` on the line directly below the frontmatter, then use {VARS.KEY} in prose. See AGENTS.md → Content variables.]

[SCOPE: One bounded task, aiming for about five minutes and roughly 600 words. Cut padding first and justify necessary exceptions. Use a supported time estimate, not an invented promise. Apply AGENTS.md → Procedural → Reader-understanding test; keep first-use choices, consequences, and success signals beside the step.]

[Opening paragraph: who this is for, what prior knowledge it assumes, and what the reader will end up with. Include a supported time estimate when available. 2-3 sentences.]

## Prerequisites

[Minimal. Link to full setup docs rather than inlining them — interrupting the flow defeats the purpose.]

* **Prerequisite** - Brief description with a [link to details](path).

## [Primary workflow — sentence case, e.g. "Run your first cloud agent"]

### 1. [Step title]

[Keep steps explicit enough for first use. Use code blocks and screenshots where they clarify an action or expected result. Stay on the critical path and link edge cases and broader background.]

### 2. [Step title]

### 3. [Step title]

## Troubleshooting

[Optional, and link-only. Point at existing troubleshooting content. Do not write new troubleshooting here — that is tutorial territory and it will blow the word budget.]

## Next steps

[One-line recap of what the reader just accomplished, then 2-3 actionable next steps. Always include a link to the conceptual page for the feature. This section goes last.]

* [Conceptual page for this feature](path/to/page.md)
* [Deeper guide](path/to/page.md)
