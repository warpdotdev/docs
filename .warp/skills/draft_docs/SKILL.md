---
name: draft_docs
description: Draft new Warp documentation pages or update existing ones using established style conventions, with optional source code context from warp-internal and warp-server.
---

# Draft Docs

This skill guides the process of drafting new documentation pages or updating existing ones for Warp's documentation (referred to as "docs"), which lives at https://docs.warp.dev. All style rules, content type structures, formatting standards, and terminology live in `AGENTS.md` at the gitbook repo root. That file is the single source of truth and must be read before drafting new docs.

## How to use

Invoke this skill with any context that describes what you want to document:
- PRDs or feature specs
- Slack threads or meeting notes
- Existing documentation that needs updating
- A description of a feature or concept

Example: "Use the draft_docs skill to write docs for [feature name] based on this PRD: [context]"

## Workflow

When this skill is invoked, follow these steps in order:

### 1. Gather context
Review all provided context (PRD, spec, existing doc, etc.). Identify:
- What feature or topic is being documented
- Key user benefits and capabilities
- Technical details that need explaining

### 2. Clarify placement
Ask the user where the doc should live. The docs are organized into sections, each with its own `SUMMARY.md`:
- `docs/warp/` - Warp Terminal and IDE → `docs.warp.dev/warp/`
- `docs/agent-platform/` - Agent Platform → `docs.warp.dev/agent-platform/`
- `docs/reference/` - Technical reference (CLI, API & SDK) → `docs.warp.dev/reference/`
- `docs/support-and-community/` - Support → `docs.warp.dev/support-and-community/`
- `docs/enterprise/` - Enterprise → `docs.warp.dev/enterprise/`
- `docs/changelog/` - Changelog → `docs.warp.dev/changelog/`

Also clarify: Is this a new page or an update to an existing page?

### 3. Read the style guide
Read `AGENTS.md` in the gitbook repo root. This is required — it contains all voice/tone rules, formatting standards, content type structures, terminology, and the quality checklist. Do not draft without reading it first.

### 4. Identify the content type
Using the "Drafting by content type" section in `AGENTS.md`, determine which content type the page is:
- **Conceptual** — explains what/why, no procedures
- **Procedural** — step-by-step task instructions
- **Quickstart** — fast path to a working result
- **Reference** — structured information for lookup
- **Troubleshooting** — problem → cause → solution
- **FAQ** — question-and-answer format
- **Feature documentation** — combined conceptual + procedural (the most common type)

Follow the structure and rules for the identified type.

### 5. Research existing patterns
Read 1-2 similar pages in the target section to match existing patterns and conventions.

### 6. Research source code (if needed)
For technical accuracy, optionally look in Warp's source repositories:
- **warp-internal** - Client-side code (Rust, Swift, etc.)
- **warp-server** - Server-side code (Go)

To find these repos, search for directories named `warp-internal` and `warp-server` on the user's machine. If not found, ask the user where the repos are located.

Use source code to verify technical behavior, understand feature implementation, and find accurate terminology.

### 7. Draft the doc
Create the documentation following the structure for its content type and all rules in `AGENTS.md`.

### 8. Review
Before presenting the draft, run through the Quality Checklist in `AGENTS.md`. Verify every item passes.

### 9. Update navigation
If this is a new page, remind the user to add it to the relevant section's `SUMMARY.md`.

## Output

Present the drafted documentation as a complete markdown file that can be saved directly to the appropriate location in `docs/`.
