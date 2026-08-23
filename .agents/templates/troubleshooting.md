---
description: >-
  [One sentence, 50-160 characters: name the symptoms covered, not the act of troubleshooting.
  Example: "Fix sign-in failures, failed conversation resumes, and update problems in the {{WARP_AGENT_CLI}}."
  See AGENTS.md > Frontmatter > Descriptions by content type for the full rules.
  Use {{TOKEN}} syntax for any product names in src/data/vars.ts.]
---
[VARS: Add this line immediately after the closing --- above if this page references any product names from src/data/vars.ts. Then use {VARS.KEY} for those names in the prose below.
`import { VARS } from '@data/vars';`
See AGENTS.md → Content variables for the full variable list and usage rules.]

# [Title — sentence case. Title convention: "Troubleshooting [feature]" or "Known issues with [feature]"]

[BREVITY: Delete any section below you don't need — a short page is a finished page. See AGENTS.md → Voice & tone → Cut again.]

:::note
[Optional: link to GitHub issues page, support channels, or related resources.]
For a complete list of issues and feature requests, visit our [GitHub issues page](https://github.com/warpdotdev/Warp/issues).
:::

## [Category header — sentence case. e.g., "Environments", "Authentication", "CLI"]

[Group related issues under broad category headers.
Each issue gets its own H3 with the symptom or error message as the header.]

### [Symptom or error message — use the exact text the user sees]

[Cause: 1-2 sentences explaining why this happens.]

[Solution: numbered steps following procedural rules.]

1. Step to fix the issue.
2. Next step.

[Workaround (if no full fix is available):
Describe an alternative approach the user can take.]

### [Another symptom or error message]

[Repeat the pattern: cause → solution → workaround.
The reader arrived because something broke — lead with the fix,
not background context.]
