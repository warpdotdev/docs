---
title: [Sentence case, beginning with a gerund that names the task. Example: "Configuring a self-hosted GitLab integration". Not "Self-hosted GitLab integration setup". This renders as the page H1 — do not add an H1 in the body.]
description: >-
  [One to two sentences, 50-160 characters: the task the reader will complete. Start with an
  imperative verb, not "This page explains". Example: "Connect Slack to the Automation
  Platform so mentions and channel messages can trigger cloud agent runs."
  Use {{TOKEN}} syntax for product names in src/data/vars.ts.]
---
[BEFORE PUBLISHING: Delete every bracketed instruction in this file, including this one. They are guidance for the author, not page content.]
[VARS: If this page names a product from src/data/vars.ts, add `import { VARS } from '@data/vars';` on the line directly below the frontmatter, then use {VARS.KEY} in prose. See AGENTS.md → Content variables.]
[AEO: If this page is driven by Peec, search-query, or answer-engine data, run `.agents/skills/aeo_brief/SKILL.md` first.]

[Opening paragraph: what the reader will accomplish and why. 1-2 sentences. Focus on the goal, not the tool.]

[BREVITY: Delete any section below you don't need for this task — a short page is a finished page. See AGENTS.md → Voice & tone → Cut again.]

## Prerequisites

[Only if needed. Use short, unbolded bullets. Name each requirement, say what it is needed for, and link to its setup instructions. State required permissions and technical limits. If credentials are needed only for one test, explain that condition beside the access setup or test that needs them; do not require them for every reader.]

* A Warp API key to authenticate API requests. See [API keys](path) to create one.

## [Primary task — sentence case, e.g. "Creating an API key"]

[One sentence of motivation before the steps. Explain why the reader is doing this, so they are not left wondering. Then the numbered steps.]

1. Step description. [Include the expected outcome where it is not obvious, so the reader can confirm they are on track.]
2. Step description.
3. Step description.

[STEP SIZING: Aim for one primary action per step, but group tightly related actions that share the same UI context — up to about three. A simple task should not need 10+ steps, and a single step should not be a mini-procedure.]
[State what the reader is configuring before listing fields or example names. Explain what each selected agent, environment, or credential is used for, then give the field, command, or file to change and its value.]
[If readers can reuse an agent or resource, show how to find and edit or select it as well as how to create a new one. For file-based setup, identify the existing file or agent directory.]
[Give configuration choices, tool and credential access, skill or prompt instructions, and testing their own steps or groups of related steps. Do not imply that writing instructions installs tools or grants access.]
[Use sample data the reader understands. If a prepared test file or record is required, explain what it contains and where to get or create it. Apply configuration changes before testing. State the behavior and evidence to check, not only that a run finishes.]
[Put safety limits beside the action they restrict and inside prompts that can be copied separately. After changing a sentence, reread the paragraph and surrounding steps for unclear references, missing actions, or incorrect ordering.]
[UI LABELS: Bold clickable controls and the option the reader selects. Put non-clickable field labels in quotation marks. Example: In the "Harness" dropdown, select **Claude Code**. Not: In the **Harness** dropdown...]
[BREVITY IN STEPS: Apply AGENTS.md → Procedural → Reader-understanding test. Keep necessary choices, consequences, and success signals beside the action. Link long lookup lists to their owning reference; a short callout must fit the page's budget.]
[If this procedure connects to another, read their examples together. Identify the event that starts each task, the agent that receives it, what information passes to the next stage, where work stops, and which decisions require a person.]
[Check whether the same input matches several rules. Say whether that is intended; if not, give conditions that prevent unwanted matches. Preserve existing filters and exclusions when adding new ones. Explain what happens when none of the specialized rules match.]
[Verify whether configuration changes affect new tasks, existing conversations, or both. Do not promise that a rule change transfers work to another agent unless verified. Include tests and expected results for matching, overlapping, and unmatched inputs, plus continued conversations when supported. See AGENTS.md → Check connected procedures for the full checks.]

:::note
[Optional. One or two callouts per page at most; prefer body prose. Delete if nothing applies.]
:::

## [Secondary task — sentence case, e.g. "Rotating an API key"]

[Same pattern: motivation, then steps. Order sections by reader chronology — requirements, setup, usage, management, then destructive actions.]

## Troubleshooting

[Recommended. Keep error messages here rather than woven through the steps above. Format each as the symptom in bold, then cause, then fix.]

**Exact error message the user sees**\
Why it happens, and how to fix it.

## Related pages

[Cross-links. Use descriptive link text that names the destination.]
[LINK FORMAT: Follow AGENTS.md → Closing section. Start with an unbolded link. Add a description only when it clarifies why to open the page: spaced hyphen, capitalized first word, proper-name casing, no terminal punctuation. Keep this section last.]

* [Conceptual page for this feature](path/to/page.md)
* [Related task](path/to/page.md) - Extend this setup to a related workflow
