---
name: draft_procedural
description: Draft a new procedural documentation page or update an existing one. Use for task-oriented, step-by-step instructions that help a reader accomplish a specific goal. Examples include configuring an integration, creating an API key, or setting up an environment.
---

# Draft procedural page

Draft a procedural documentation page with step-by-step instructions to accomplish a specific goal.

## Workflow

Follow the workflow in `.agents/skills/draft_docs/SKILL.md`, using the **procedural template** at `.agents/templates/procedural.md`.

## Frontmatter description

One to two sentences, 50-160 characters, naming the task the reader will complete. Start with an imperative verb.
- ✅ `Connect Slack to Oz so mentions and channel messages can trigger cloud agent runs.`
- ❌ `This page explains the Slack integration setup process.`

See "Descriptions by content type" under Frontmatter in `AGENTS.md` for the full rules.

## Content type rules

These rules are specific to procedural pages (from the "Drafting by content type" section of `AGENTS.md`):

- **Keep steps focused, not artificially atomic.** Aim for one primary action per step, but group tightly related actions together when they share the same UI context. Up to ~3 related actions per step is acceptable.
- **Move reference detail out of the step into a `:::note`.** When a step's supporting detail is a list of facts (accepted credential types, valid formats) rather than an instruction, keep the step to its one action and put the list in a `:::note` immediately after it.
- **Orient within the step, not just on first mention.** Name the field, dropdown, or location the action happens in before naming the action itself ("In the 'Harness' dropdown, select **Claude Code**", not "Choose **Claude Code** in the **Harness** field"). A step should stand on its own for a reader who lands on it directly, not rely on referring back to an earlier section.
- **Motivate steps before giving instructions.** Briefly explain WHY before HOW, especially for setup steps.
- Include expected outcomes after key steps so the reader can confirm they're on track.
- Test all instructions for accuracy.
- Provide troubleshooting for common failure points.
- Don't over-explain — link to conceptual pages for the "why."
- Title convention: gerund ("Configuring X", "Managing X")

## AEO-driven procedures

If the request is driven by AEO, Peec, AI search prompts, answer-engine visibility, or search-query vocabulary, read `.agents/skills/aeo_brief/SKILL.md` before drafting. Use the brief to:
- Translate source-data language into precise procedure titles, headings, and descriptions
- Preserve accurate high-intent phrases without keyword stuffing
- Decide whether the procedure belongs in a new page or as a tighter update to an existing page
- Surface product or UI terminology questions before presenting the draft

## Pre-handoff self-review

Before presenting the draft, check:
- **Scannability** - Long procedure sections should use numbered steps, short bullets, or concise subsections. Do not leave dense paragraphs that hide actions.
- **Expected outcomes** - Readers should know what success looks like after important steps.
- **UI accuracy** - Product surfaces, buttons, settings paths, and command names should match the current product terminology.
- **Value over coverage** - AEO-driven procedures should solve a real task, not collect loosely related keywords.
- **Open questions** - Flag any steps that still need human product testing or UI verification.

## Heading case

All headings (H1–H4) must use **sentence case**: capitalize only the first word and proper feature names.

- ✅ `# Configuring environments`
- ✅ `## Creating an API key`
- ❌ `# Configuring Environments`
- ❌ `## Creating An API Key`

## Existing examples

Read 2-3 of these strong examples to match the existing pattern:
- `src/content/docs/reference/cli/api-keys.md`
- `src/content/docs/platform/integrations/slack.md`
