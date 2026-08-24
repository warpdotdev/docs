---
title: [Sentence case, naming the feature. Use "Quickstart for [product]" or "[Feature] quickstart". Never a bare "Quickstart". This renders as the page H1 — do not add an H1 in the body.]
description: >-
  [One sentence, 50-160 characters: what the reader ends up with, plus the time budget.
  Start with an imperative verb, not "Learn how to" or "Get started with". Example:
  "Install the {{WARP_AGENT_CLI}}, log in, and run your first agent conversation in about
  five minutes." Use {{TOKEN}} syntax for product names in src/data/vars.ts.]
---
[BEFORE PUBLISHING: Delete every bracketed instruction in this file, including this one. They are guidance for the author, not page content.]
[VARS: If this page names a product from src/data/vars.ts, add `import { VARS } from '@data/vars';` on the line directly below the frontmatter, then use {VARS.KEY} in prose. See AGENTS.md → Content variables.]

[SCOPE — the defining constraint: about five minutes and roughly 600 words. This is a budget, not a target. A quickstart that outgrows it has become a tutorial and should be reworked as one. Written for someone who already understands the product and is ready to try it, so leave out how it works and why they would want it. If the task needs context at its decision points, it is a tutorial.]

[Opening paragraph: who this is for, what prior knowledge it assumes, what the reader will end up with, and the time budget. 2-3 sentences.]

## Prerequisites

[Minimal. Link to full setup docs rather than inlining them — interrupting the flow defeats the purpose.]

* **Prerequisite** - Brief description with a [link to details](path).

## [Primary workflow — sentence case, e.g. "Run your first cloud agent"]

### 1. [Step title]

[Steps can be less explicit than full procedural content, because the audience already knows the product. Use code blocks and screenshots generously — visual confirmation reassures the reader they are on track. Stay on the critical path and defer edge cases to other pages.]

### 2. [Step title]

### 3. [Step title]

## Troubleshooting

[Optional, and link-only. Point at existing troubleshooting content. Do not write new troubleshooting here — that is tutorial territory and it will blow the word budget.]

## Next steps

[One-line recap of what the reader just accomplished, then 2-3 actionable next steps. Always include a link to the conceptual page for the feature. This section goes last.]

* [Conceptual page for this feature](path/to/page.md)
* [Deeper guide](path/to/page.md)
