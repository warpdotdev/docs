---
name: draft_quickstart
description: Draft a new quickstart documentation page or update an existing one. Use when the reader already understands the product and wants the fastest path to a working result - about five minutes and 600 words, essential steps only. If the task needs explanation along the way or exceeds that budget, it is a tutorial, not a quickstart.
---

# Draft quickstart page

Draft a quickstart that gets the reader to a working result in about five minutes.

## Scope is the defining constraint

**About five minutes and roughly 600 words.** This is a budget, not a target. A quickstart that outgrows it has become a tutorial and should be reworked as one rather than allowed to sprawl.

Quickstarts are for readers who **already understand the feature or product** and are ready to try it. Deliberately omit how it works and why they would want it — if the reader needs that, they need conceptual content. If the task needs context at its decision points, they need a tutorial.

A tutorial for a product area requires that its quickstart already exist. If you are drafting the first page for an area, it is probably this one.

## Workflow

Follow the workflow in `.agents/skills/draft_docs/SKILL.md`, using the **quickstart template** at `.agents/templates/quickstart.md`.

## Frontmatter description

One sentence, 50-160 characters, saying what the reader ends up with plus the time budget. Start with an imperative verb.
- ✅ `Install the Warp Agent CLI, log in, and run your first agent conversation in about five minutes.`
- ❌ `Get started with the Warp Agent CLI.`

See "Descriptions by content type" under Frontmatter in `AGENTS.md` for the full rules.

## Content type rules

These rules are specific to quickstart pages (from the "Drafting by content type" section of `AGENTS.md`):

- **Give every quickstart a descriptive H1 title.** Don't use a bare "Quickstart" — include the feature or topic name.
- **Open by stating who it is for**, the prerequisites and prior knowledge assumed, what the reader ends up with, and the time budget.
- Minimize prerequisites — the reader should be able to start quickly.
- Keep steps focused on the critical path — defer edge cases and advanced options to other pages.
- **Link out rather than replicating** other pages' content, so the flow is not interrupted.
- Steps can be less formal than full procedural content, because the audience already knows the product. Use heavy visual cues (code blocks, screenshots).
- All procedural rules apply (focused steps, motivate steps, expected outcomes).
- **Troubleshooting is optional and link-only.** Point at existing troubleshooting content; do not write new troubleshooting into a quickstart.
- End with a one-line recap, then 2-3 actionable next steps. Always include a link to the conceptual page for the feature.
- Title convention: "[Feature] quickstart" or "Quickstart for [product]"
- **Length is the constraint, not just the tone.** A quickstart has a hard ~600-word budget — tighter than any other content type, because speed to a working result is the entire point. Cut every section that isn't on the critical path (AGENTS.md → Voice & tone → Cut again) before adding a word of new content. Also apply the general tone rules: no marketing buzzwords, no meta-openers.

## Heading case

All headings (H1–H4) must use **sentence case**: capitalize only the first word and proper feature names.

- ✅ `# Cloud Agents quickstart`
- ✅ `## Running your first cloud agent`
- ❌ `# Cloud Agents Quickstart`
- ❌ `## Running Your First Cloud Agent`

## Existing examples

Read 2-3 of these strong examples to match the existing pattern:
- `src/content/docs/platform/quickstart.md`
- `src/content/docs/getting-started/quickstart/installation-and-setup.md`
