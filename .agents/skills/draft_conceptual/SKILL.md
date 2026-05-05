---
name: draft_conceptual
description: Draft a new conceptual documentation page or update an existing one. Use for pages that explain what something is, why it exists, and how it works — without step-by-step procedures. Examples include product overviews, architecture explanations, and design philosophy pages.
---

# Draft conceptual page

Draft a conceptual documentation page that explains what a feature or concept is, why it matters, and how it works at a high level.

## Workflow

Follow the workflow in `.warp/skills/draft_docs/SKILL.md`, using the **conceptual template** at `.warp/templates/conceptual.md`.

## Content type rules

These rules are specific to conceptual pages (from the "Drafting by content type" section of `AGENTS.md`):

- Explain "what" and "why" before "how"
- Define new terms when they first appear
- Use diagrams or architecture descriptions where they clarify relationships
- **Do NOT include step-by-step procedures** — link to a procedural or quickstart page instead
- Show real-world scenarios, not just abstract descriptions
- Title convention: noun or "About [subject]"

## Heading case

All headings (H1–H4) must use **sentence case**: capitalize only the first word and proper feature names.

- ✅ `## How it works`
- ✅ `## When to use Codebase Context`
- ❌ `## How It Works`
- ❌ `## When To Use Codebase Context`

## Existing examples

Read 2-3 of these strong examples to match the existing pattern:
- `src/content/docs/agent-platform/cloud-agents/deployment-patterns.md`
- `src/content/docs/agent-platform/cloud-agents/overview.md`
