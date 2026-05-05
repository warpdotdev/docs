---
name: draft_reference
description: Draft a new reference documentation page or update an existing one. Use for structured factual information meant for lookup — CLI commands, API endpoints, configuration options, keyboard shortcuts, error codes. Reference pages describe and only describe.
---

# Draft reference page

Draft a reference documentation page with structured, exhaustive information for developer lookup.

## Workflow

Follow the workflow in `.warp/skills/draft_docs/SKILL.md`, using the **reference template** at `.warp/templates/reference.md`.

## Content type rules

These rules are specific to reference pages (from the "Drafting by content type" section of `AGENTS.md`):

- Be exhaustive — document every option, flag, and configuration value.
- Use consistent formatting for parameters (e.g., `--flag` in backticks, description as a dash-separated list item).
- Alphabetize entries where ordering doesn't matter.
- Keep descriptions factual and concise — this is for lookup, not learning.
- Include at least one practical example for each command or endpoint.
- **Adopt standard patterns ruthlessly** — consistency is more important than style. Every entry must follow the same structure.
- Structure should mirror the structure of the product it describes.
- Use H2 for sections, H3 for subsections. Tables for multiple elements, lists for single.
- Title convention: noun describing contents ("Keyboard shortcuts", "CLI commands")

## Heading case

All headings (H1–H4) must use **sentence case**: capitalize only the first word and proper feature names.

- ✅ `# CLI commands`
- ✅ `## Running agents`
- ❌ `# CLI Commands`
- ❌ `## Running Agents`

## Existing examples

Read 2-3 of these strong examples to match the existing pattern:
- `reference/cli/index.mdx`
- `reference/api-and-sdk/index.mdx`
