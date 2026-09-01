---
title: [Sentence case. Use "Troubleshooting [feature]" or "Known issues with [feature]". This renders as the page H1 — do not add an H1 in the body.]
description: >-
  [One to two sentences, 50-160 characters: name the symptoms covered, not the act of
  troubleshooting. Example: "Fix sign-in failures, failed conversation resumes, and update
  problems in the {{WARP_AGENT_CLI}}."
  Use {{TOKEN}} syntax for product names in src/data/vars.ts.]
---
[BEFORE PUBLISHING: Delete every bracketed instruction in this file, including this one. They are guidance for the author, not page content.]
[VARS: If this page names a product from src/data/vars.ts, add `import { VARS } from '@data/vars';` on the line directly below the frontmatter, then use {VARS.KEY} in prose. See AGENTS.md → Content variables.]

[The reader arrived because something broke. Lead with the fix, not background. Skip a general introduction unless it genuinely helps them find their symptom faster.]

[BREVITY: Delete any section below you don't need — a short page is a finished page. See AGENTS.md → Voice & tone → Cut again.]

:::note
[Optional. Link to the GitHub issues page or support channels. Delete if not useful.]
For a complete list of issues and feature requests, visit our [GitHub issues page](https://github.com/warpdotdev/Warp/issues).
:::

## [Category — sentence case, e.g. "Authentication", "Environments"]

[Group related issues under broad categories so the reader can scan to their area.]

### [The exact error message or symptom the user sees]

[HEADER: Use the literal error text where there is one. This is what the reader pastes into search, and matching it exactly is the single highest-value thing on the page.]

[Cause: 1-2 sentences on why this happens.]

1. Step to fix it.
2. Next step.

[Workaround: if no full fix exists, describe the alternative and say plainly that it is a workaround.]

### [Another symptom or error message]

[Same pattern every time: symptom as the header, then cause, then fix, then workaround.]

## Related pages

[Cross-links. Use descriptive link text that names the destination.]

* [Feature documentation](path/to/page.md)
* [Related troubleshooting](path/to/page.md)
