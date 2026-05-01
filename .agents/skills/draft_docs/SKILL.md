---
name: draft_docs
description: Draft new Warp documentation pages or update existing ones using established style conventions, with optional source code context from warp-internal and warp-server.
---

# Draft Docs

This skill guides the process of drafting new documentation pages or updating existing ones for Warp's documentation (referred to as "docs"), which lives at https://docs.warp.dev. All style rules, content type structures, formatting standards, and terminology live in `AGENTS.md` at the docs repo root. That file is the single source of truth and must be read before drafting new docs.

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
Ask the user where the doc should live. The docs are organized into sections, each with its own `astro.config.mjs (sidebar config)`:
- `src/content/docs/` - Warp Terminal and IDE → `docs.warp.dev/`
- `src/content/docs/agent-platform/` - Agent Platform → `docs.warp.dev/agent-platform/`
- `src/content/docs/reference/` - Technical reference (CLI, API & SDK) → `docs.warp.dev/reference/`
- `src/content/docs/support-and-community/` - Support → `docs.warp.dev/support-and-community/`
- `src/content/docs/enterprise/` - Enterprise → `docs.warp.dev/enterprise/`
- `src/content/docs/changelog/` - Changelog → `docs.warp.dev/changelog/`

Also clarify: Is this a new page or an update to an existing page?

### 3. Read the style guide
Read `AGENTS.md` in the docs repo root. This is required — it contains all voice/tone rules, formatting standards, content type structures, terminology, and the quality checklist. Do not draft without reading it first.

### 4. Identify the content type and template
Using the "Drafting by content type" section in `AGENTS.md`, determine which content type the page is:

| Content type | Use when | Template | Skill |
|---|---|---|---|
| **Conceptual** | Explains what/why, no procedures | `.warp/templates/conceptual.md` | `draft_conceptual` |
| **Procedural** | Step-by-step task instructions | `.warp/templates/procedural.md` | `draft_procedural` |
| **Quickstart** | Fast path to a working result | `.warp/templates/quickstart.md` | `draft_quickstart` |
| **Reference** | Structured information for lookup | `.warp/templates/reference.md` | `draft_reference` |
| **Troubleshooting** | Problem → cause → solution | `.warp/templates/troubleshooting.md` | `draft_troubleshooting` |
| **FAQ** | Question-and-answer format | `.warp/templates/faq.md` | `draft_faq` |
| **Guide** | Task-oriented walkthrough (Guides section) | `.warp/templates/guide-page.md` | `draft_guide` |
| **Feature documentation** | Combined conceptual + procedural (most common) | `.warp/templates/feature-doc.md` | `draft_feature_doc` |

Once the content type is identified:
- Use the corresponding **template** as the starting scaffold for the page.
- If a **type-specific skill** exists (listed above), read it for additional rules and examples specific to that content type.
- Follow the structure and rules for the identified type in `AGENTS.md`.

### 5. Research existing patterns
Read 2-3 strong examples in the target section to match existing patterns and conventions.

### 6. Research source code (if needed)
For technical accuracy, optionally look in Warp's source repositories:
- **warp-internal** - Client-side code (Rust, Swift, etc.)
- **warp-server** - Server-side code (Go)

To find these repos, search for directories named `warp-internal` and `warp-server` on the user's machine. If not found, ask the user where the repos are located.

Use source code to verify technical behavior, understand feature implementation, and find accurate terminology.

### 6.5. Critical formatting rules

These rules are frequently violated by agents. Apply them carefully during drafting:

- **Sentence case for all headings (H1–H4)** — Capitalize only the first word and proper feature names. ✅ `## How it works` ❌ `## How It Works`
- **Bold + dash format for list items** — `* **Term** - Description`, not `* Term: Description`
- **Bold for UI elements** — Use `**Save**` not `` `Save` `` after action verbs like "click"
- **Bold per-segment for Settings paths** — Use `**Settings** > **AI** > **Knowledge**` not `` `Settings > AI > Knowledge` ``

### 7. Draft the doc
Create the documentation using the appropriate template from `.warp/templates/`. Follow the structure for the identified content type and all rules in `AGENTS.md`. Each template includes visible bracketed instructions explaining what to put in each section.

### 8. Run style lint
Run `python3 .warp/skills/style_lint/style_lint.py --changed` on the drafted file to catch formatting and terminology issues before presenting to the user.

### 9. Review against checklist
Before presenting the draft, verify against the quality checklist in `AGENTS.md`:
- [ ] Frontmatter includes clear description written as a standalone summary
- [ ] Content follows the structure for its content type
- [ ] Terminology matches the glossary (`.warp/references/terminology.md`)
- [ ] Headers use sentence case (with proper feature name capitalization)
- [ ] Lists use bold term + dash + explanation format
- [ ] Cross-references to related features are included
- [ ] Instructions include expected outcomes
- [ ] Images have descriptive alt text

### 10. Update navigation and redirects
If this is a new page, remind the user to:
- Add it to the relevant section's `astro.config.mjs (sidebar config)`.

If this page replaces, renames, or moves an existing page, remind the user to add a redirect:
- **Same-space redirect**: Add an entry to the space's `vercel.json (redirects)` file under `redirects:`.
- **Cross-space redirect**: Add the redirect through the Astro Starlight UI (cross-space redirects cannot be managed via `vercel.json (redirects)`).

Always check the current list of redirects before adding a new one to avoid duplicates.

## Output

Present the drafted documentation as a complete markdown file that can be saved directly to the appropriate location in `docs/`.
