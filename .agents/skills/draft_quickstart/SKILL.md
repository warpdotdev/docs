---
name: draft_quickstart
description: Draft or update a quickstart for one bounded task, aiming for about five minutes and 600 words while preserving necessary first-use teaching.
---

# Draft quickstart page

Draft a quickstart for one working result. Use a supported time estimate, not an invented five-minute promise.

## Scope is the defining constraint

Aim for about five minutes and roughly 600 words. Cut padding before considering a split or a different content type; justify necessary budget exceptions in the PR body.

Quickstarts are for readers ready to try one bounded task. Apply AGENTS.md → Procedural → Reader-understanding test during drafting and the deletion pass. Keep necessary choices, consequences, and success signals beside the step; link broader background.

A tutorial for a product area requires that its quickstart already exist. If you are drafting the first page for an area, it is probably this one.

## Workflow

Follow the workflow in `.agents/skills/draft_docs/SKILL.md`, using the **quickstart template** at `.agents/templates/quickstart.md`.

## Frontmatter description

One to two sentences, 50-160 characters, saying what the reader ends up with. Include a supported time estimate when available; omit it when unverified. Start with an imperative verb.
- ✅ `Install the Warp Agent CLI, log in, and run your first agent conversation in about five minutes.`
- ❌ `Get started with the Warp Agent CLI.`

See "Descriptions by content type" under Frontmatter in `AGENTS.md` for the full rules.

## Content type rules

These rules are specific to quickstart pages (from the "Drafting by content type" section of `AGENTS.md`):

- **Use a descriptive frontmatter title**, not a body H1. Include the feature or topic name.
- **Open by stating who it is for**, the prerequisites and prior knowledge assumed, and what the reader ends up with. Include a supported time estimate when available.
- Minimize prerequisites — the reader should be able to start quickly.
- Keep steps focused on the critical path — defer edge cases and advanced options to other pages.
- **Link out rather than replicating** other pages' content, so the flow is not interrupted.
- Keep steps explicit enough for first use. Use code examples and screenshots where they clarify the action or expected result.
- All procedural rules apply (focused steps, motivate steps, expected outcomes).
- **Troubleshooting is optional and link-only.** Point at existing troubleshooting content; do not write new troubleshooting into a quickstart.
- End with a one-line recap, then 2-3 actionable next steps. Always include a link to the conceptual page for the feature.
- Title convention: "[Feature] quickstart" or "Quickstart for [product]"
- **Cut unnecessary material, not teaching.** Apply the canonical reader-understanding test before proposing cuts. Record the editorial verdict required by `draft_docs`; a lower word count alone does not demonstrate better output.

## Heading case

All headings (H1–H4) must use **sentence case**: capitalize only the first word and proper feature names.

- ✅ `title: Cloud agents quickstart`
- ✅ `## Running your first cloud agent`
- ❌ `title: Cloud agents Quickstart`
- ❌ `## Running Your First Cloud Agent`

## Existing examples

Read 2-3 of these strong examples to match the existing pattern:
- `src/content/docs/platform/quickstart.mdx`
- `src/content/docs/getting-started/quickstart/installation-and-setup.mdx`
