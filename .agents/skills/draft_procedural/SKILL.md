---
name: draft_procedural
description: Draft a new procedural documentation page or update an existing one. Use for task-oriented, step-by-step instructions that help a reader accomplish a specific goal. Examples include configuring an integration, creating an API key, or setting up an environment.
---

# Draft procedural page

Draft a procedural documentation page with step-by-step instructions to accomplish a specific goal.

## Workflow

Follow the workflow in `.warp/skills/draft_docs/SKILL.md`, using the **procedural template** at `.warp/templates/procedural.md`.

## Content type rules

These rules are specific to procedural pages (from the "Drafting by content type" section of `AGENTS.md`):

- **Keep steps focused, not artificially atomic.** Aim for one primary action per step, but group tightly related actions together when they share the same UI context. Up to ~3 related actions per step is acceptable.
- **Motivate steps before giving instructions.** Briefly explain WHY before HOW, especially for setup steps.
- Include expected outcomes after key steps so the reader can confirm they're on track.
- Test all instructions for accuracy.
- Provide troubleshooting for common failure points.
- Don't over-explain — link to conceptual pages for the "why."
- Title convention: gerund ("Configuring X", "Managing X")

## Heading case

All headings (H1–H4) must use **sentence case**: capitalize only the first word and proper feature names.

- ✅ `# Configuring environments`
- ✅ `## Creating an API key`
- ❌ `# Configuring Environments`
- ❌ `## Creating An API Key`

## Existing examples

Read 2-3 of these strong examples to match the existing pattern:
- `src/content/docs/reference/cli/api-keys.md`
- `src/content/docs/agent-platform/cloud-agents/integrations/slack.md`
