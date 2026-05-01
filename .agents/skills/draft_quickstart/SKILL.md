---
name: draft_quickstart
description: Draft a new quickstart documentation page or update an existing one. Use for first-time experiences that get the reader to a working result fast (~10 minutes). Quickstarts focus on the critical path with minimal prerequisites and link to deeper guides for edge cases.
---

# Draft quickstart page

Draft a quickstart that gets the reader from zero to a working result in about 10 minutes.

## Workflow

Follow the workflow in `.warp/skills/draft_docs/SKILL.md`, using the **quickstart template** at `.warp/templates/quickstart.md`.

## Content type rules

These rules are specific to quickstart pages (from the "Drafting by content type" section of `AGENTS.md`):

- **Give every quickstart a descriptive H1 title.** Don't use a bare "Quickstart" — include the feature or topic name.
- Minimize prerequisites — the reader should be able to start quickly.
- Target ~10 minutes or less.
- Keep steps focused on the critical path — defer edge cases and advanced options to other pages.
- Steps can be less formal than full procedural content. Use heavy visual cues (code blocks, screenshots).
- All procedural rules apply (focused steps, motivate steps, expected outcomes).
- End with 2-3 actionable next steps linking to deeper content.
- Title convention: "[Feature] quickstart" or "Quickstart for [product]"

## Heading case

All headings (H1–H4) must use **sentence case**: capitalize only the first word and proper feature names.

- ✅ `# Cloud Agents quickstart`
- ✅ `## Running your first cloud agent`
- ❌ `# Cloud Agents Quickstart`
- ❌ `## Running Your First Cloud Agent`

## Existing examples

Read 2-3 of these strong examples to match the existing pattern:
- `src/content/docs/agent-platform/cloud-agents/quickstart.md`
- `src/content/docs/getting-started/quickstart/installation-and-setup.md`
