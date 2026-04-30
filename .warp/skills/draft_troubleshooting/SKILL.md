---
name: draft_troubleshooting
description: Draft a new troubleshooting documentation page or update an existing one. Use for known issues, common errors, and diagnostic guides. Troubleshooting pages follow a problem → cause → solution format, leading with the symptom the user sees.
---

# Draft troubleshooting page

Draft a troubleshooting page that helps users diagnose and fix common issues.

## Workflow

Follow the workflow in `.warp/skills/draft_docs/SKILL.md`, using the **troubleshooting template** at `.warp/templates/troubleshooting.md`.

## Content type rules

These rules are specific to troubleshooting pages (from the "Drafting by content type" section of `AGENTS.md`):

- Use the problem or error message as the header — this helps with search.
- Group related issues under broader category headers (e.g., "SSH", "Shells").
- Lead with the symptom — the reader arrived because something broke. Don't make them read context before getting to the fix.
- Provide workarounds when a fix isn't available.
- Link to related troubleshooting pages and support channels.
- Include workarounds even when no fix exists — documenting a known issue without a workaround still saves the user time searching.
- Title convention: "Troubleshooting [feature]" or "Error: [error name]"

## Heading case

All headings (H1–H4) must use **sentence case**: capitalize only the first word and proper feature names.

- ✅ `# Troubleshooting environments`
- ✅ `## Agent fails to start`
- ❌ `# Troubleshooting Environments`
- ❌ `## Agent Fails To Start`

## Existing examples

Read 2-3 of these strong examples to match the existing pattern:
- `src/content/docs/support-and-community/troubleshooting-and-support/known-issues.md`
- `src/content/docs/reference/cli/troubleshooting.md`
