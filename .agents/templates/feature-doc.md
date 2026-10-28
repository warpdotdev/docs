---
title: [Sentence case, task-based gerund when the page contains a procedure. Keep it general enough to cover the range of tasks on the page and agnostic about which option the reader picks: "Setting repository visibility", not "Making a private repository public". This renders as the page H1 — do not add an H1 in the body.]
description: >-
  [One to two sentences, 50-160 characters: what the feature does and its primary benefit. Example:
  "Control what the agent can do with permission cards, auto-approve, and execution profiles."
  Use {{TOKEN}} syntax for product names in src/data/vars.ts.]
---
[BEFORE PUBLISHING: Delete every bracketed instruction in this file, including this one. They are guidance for the author, not page content.]
[VARS: If this page names a product from src/data/vars.ts, add `import { VARS } from '@data/vars';` on the line directly below the frontmatter, then use {VARS.KEY} in prose. See AGENTS.md → Content variables.]

[This is the most common page type in Warp's docs (~75+ pages) and the one most prone to sprawl, because it accepts the most kinds of content. Two limits:

1. Never fold quickstart or tutorial content in here. Both are defined by a scope budget and a single continuous path, and both lose their purpose once embedded in a longer page. Link to them instead. Conceptual, procedural, reference, and troubleshooting sections can coexist here; those two cannot.
2. Past roughly 1500 words, cut padding and duplication first. Split only if the remaining useful content still needs separate pages; link or relocate necessary facts.]

[Opening paragraph: what the feature does and its primary benefit. 1-3 sentences. Lead with what the reader can accomplish, not the implementation.]

[DEFINE → SHOW → LINK: Plain-language definition, then one concrete example, before jargon-heavy configuration. See AGENTS.md → Define, show, link.]
[Name the product in the opening and description so each makes sense without the navigation. Do not repeat the product name in every heading.]
[In the brief or PR rationale, name the search evidence and what it measured. Distinguish data about this specific topic from data about a broader topic and from your editorial recommendations. Do not add unrelated topics or unsupported product promises to include more search terms.]

[MEDIA: If you have an orientation video or wide product screenshot, place it here or just under Key features — not after long conceptual sections. Never stack two VideoEmbeds back to back.]

[BREVITY: Delete any section below you don't need — a short page is a finished page. Feature pages stay at or under ~1500 words unless the PR body justifies an overage. Run check_compression_contract.py --content-type feature-doc before opening the PR. See AGENTS.md → Voice & tone → Cut again.]

:::note
[Optional. Key context the reader needs upfront — a prerequisite, a limitation, or when NOT to use this. Delete if nothing applies.]
:::

## Key features

[2-4 capabilities. Bold term + hyphen + what it means for the reader. Collapse this into the opening paragraph if the feature is simple enough that a list is padding.]

* **Feature A** - What it does and why it matters to the user.
* **Feature B** - What it does and why it matters to the user.

## How it works

[CONCEPTUAL section. System behavior the reader can act on. Answer "what" and "why" before "how". Define new terms on first use with a concrete example. No step-by-step procedures here — keep the conceptual and procedural halves clearly separated. No internal validation or control-plane walkthroughs.]

## [Usage or configuration — sentence case, renamed to match the feature, e.g. "Creating environments"]

[PROCEDURAL section. Motivate before instructing, include expected outcomes after key steps, and group related actions that share a UI context. Bold clickable controls and selected options; put non-clickable field labels in quotation marks ("Harness" dropdown, not **Harness** dropdown). Keep steps short — cut internal implementation detail and move reference lists into a :::note or a linked page.]
[State what the reader is configuring before listing fields or example names. Explain what each selected agent, environment, or credential is used for, then give the field, command, or file to change and its value.]
[If readers can reuse an agent or resource, show how to find and edit or select it as well as how to create a new one. For file-based setup, identify the existing file or agent directory.]
[Give configuration choices, tool and credential access, skill or prompt instructions, and testing their own steps or groups of related steps. Do not imply that writing instructions installs tools or grants access.]
[Use sample data the reader understands. If a prepared test file or record is required, explain what it contains and where to get or create it. Apply configuration changes before testing. State the behavior and evidence to check, not only that a run finishes.]
[Put safety limits beside the action they restrict and inside prompts that can be copied separately.]
[After changing a sentence, reread the paragraph and surrounding steps. Check that the purpose remains clear, references name the right things, and required actions remain in order.]

### Prerequisites

[Use short, unbolded bullets. Name each requirement, say what it is needed for, and link to its setup instructions. State required permissions and technical limits. If credentials are needed only for one test, explain that condition beside the access setup or test that needs them; do not require them for every reader.]

### [Task name — sentence case, e.g. "Create an environment with the CLI"]

1. Step description.
2. Step description.

## [Additional sections as needed]

[ORDER: broad to specific. Conceptual, then reference, then procedures in lifecycle order — enable, use, manage, disable, destructive actions — then troubleshooting.]
[If this procedure connects to another, read their examples together. Identify the event that starts each task, the agent that receives it, what information passes to the next stage, where work stops, and which decisions require a person.]
[Check whether the same input matches several rules. Say whether that is intended; if not, give conditions that prevent unwanted matches. Preserve existing filters and exclusions when adding new ones. Explain what happens when none of the specialized rules match.]
[Verify whether configuration changes affect new tasks, existing conversations, or both. Do not promise that a rule change transfers work to another agent unless verified. Include tests and expected results for matching, overlapping, and unmatched inputs, plus continued conversations when supported. See AGENTS.md → Check connected procedures for the full checks.]

## Related pages

[Cross-links. Use descriptive link text that names the destination. If a quickstart or tutorial exists for this feature, link it here rather than inlining it above.]
[LINK FORMAT: Follow AGENTS.md → Closing section. Start with an unbolded link. Add a description only when it clarifies why to open the page: spaced hyphen, capitalized first word, proper-name casing, no terminal punctuation. Keep this section last.]

* [Related feature](path/to/page.md)
* [Quickstart for this feature](path/to/page.md) - Try the feature in a working example
