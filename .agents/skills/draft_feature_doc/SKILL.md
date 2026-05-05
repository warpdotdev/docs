---
name: draft_feature_doc
description: Draft a new feature documentation page or update an existing one. This is the most common page type in Warp's docs (~75+ pages). Feature docs combine conceptual content (what a feature is and how it works) with procedural content (step-by-step usage instructions) in one page.
---

# Draft feature documentation page

Draft a feature documentation page that combines conceptual and procedural content — explaining what a feature is, then showing how to use it.

## Workflow

Follow the workflow in `.warp/skills/draft_docs/SKILL.md`, using the **feature-doc template** at `.warp/templates/feature-doc.md`.

## Content type rules

These rules are specific to feature documentation pages (from the "Drafting by content type" section of `AGENTS.md`):

- Apply the **conceptual** rules to the explanatory sections (explain what and why, define terms, no procedures in the overview).
- Apply the **procedural** rules to the step-by-step sections (motivate steps, expected outcomes, focused steps).
- **Keep the conceptual and procedural sections clearly separated with distinct headers.** Don't let explanation creep into procedures or vice versa.
- Title convention: feature name as noun

## Heading case

All headings (H1–H4) must use **sentence case**: capitalize only the first word and proper feature names.

- ✅ `## How it works`
- ✅ `## Configuring your environment`
- ✅ `## Agent Mode settings` ("Agent Mode" is a proper feature name)
- ❌ `## How It Works`
- ❌ `## Configuring Your Environment`
- ❌ `## Agent Mode Settings`

## Existing examples

Read 2-3 of these strong examples to match the existing pattern:
- `src/content/docs/agent-platform/capabilities/skills.md`
- `src/content/docs/agent-platform/cloud-agents/environments.md`
