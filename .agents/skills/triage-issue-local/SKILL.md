---
name: triage-issue-local
specializes: triage-issue
description: Repo-specific triage guidance for the Warp docs repo. Only the categories declared overridable by the core triage-issue skill may be specialized here.
---

# Repo-specific triage guidance for `docs`

This file is a companion to the core `triage-issue` skill. It does not
redefine the triage output schema, safety rules, or follow-up-question
contract. It only specializes the override categories the core skill
marks as overridable.

## Heuristics

- `docs` is the public Warp documentation repository, built with Astro Starlight. Content lives in `src/content/docs/` as MDX files. Treat public issue reports as potentially incomplete.
- Distinguish between **site bugs** (the docs platform is broken — search, navigation, rendering, styling, build errors) and **content issues** (documentation is incorrect, outdated, missing, unclear, has typos, or has formatting problems). Most issues will be content issues.
- When the reporter provides a `docs.warp.dev` URL, map it to the source file: `docs.warp.dev/agent-platform/capabilities/skills` → `src/content/docs/agent-platform/capabilities/skills.mdx`.
- When an issue claims documentation is wrong about a feature's behavior, verify against the source repos (`warp-internal` for client/Rust, `warp-server` for server/Go) before concluding the docs are incorrect. Docs are the primary source of truth for user-facing content, but source code is essential for validating accuracy when disputed.
- Check the docs style guide (`AGENTS.md`) and terminology glossary (`.agents/references/terminology.md`) to validate that issue reports reference features by their correct names and that any proposed fixes would align with current terminology.
- If the report is a support question (e.g., "How do I do X?") rather than an issue with the docs themselves, direct the reporter to the [Warp community Slack](https://go.warp.dev/join-preview) and the [docs site](https://docs.warp.dev).

## Follow-up question limit

Ask **at most 2 follow-up questions** per triage response. Each question must be high-value: it should meaningfully change the label assignment or reproduction confidence if answered. Do not ask questions whose answers can be inferred from the issue body, linked URLs, or screenshots.

## Label taxonomy

Use the following labels when triaging docs issues:

**Priority labels** (always apply exactly one):
- `priority/high` — Factually incorrect information, broken page, security-related content, or docs that cause users to take a wrong action
- `priority/medium` — Outdated content, confusing instructions, incomplete coverage, or misleading screenshots
- `priority/low` — Typos, minor formatting issues, small clarifications, nice-to-have improvements

**Status labels:**
- `triage` — Always apply on new issues. Signals the issue needs human review.
- `ready-to-implement` — Reserved for human maintainers. Do not apply automatically; mention implementation readiness in the triage analysis instead.

**Existing template labels** (applied automatically by issue templates — do not remove):
- `bug` — Applied by the "Docs site bug" template
- `improve or update documentation` — Applied by the "Docs content issue" template

Do not invent new labels.

## Information to check before asking follow-up questions

Before asking the reporter for more information, check the issue body, comments, and attachments for:

- The specific page URL(s) or topic area affected
- What is incorrect, outdated, missing, or unclear (for content issues)
- Browser and OS (for site bugs — search, rendering, navigation issues)
- Screenshots or recordings showing the problem
- Whether the reporter has already suggested a fix or correction
- Whether the affected page exists in `src/content/docs/` and what it currently says

## Recurring follow-up patterns

- Content issue with no page URL: ask which page or topic is affected.
- "Docs are wrong" with no source: ask for the expected behavior or a reference (release notes, CLI help output, changelog) that contradicts the current docs.
- Site bug with no reproduction details: ask for browser, OS, and whether the issue persists in incognito/private browsing.

## Content structure reference

Documentation lives in `src/content/docs/` with these sections:
- `terminal/` — Warp Terminal features (blocks, editor, sessions, appearance)
- `agent-platform/` — Agent Platform (local agents, cloud agents, capabilities, integrations)
- `code/` — Code editor, code review, git worktrees
- `getting-started/` — Installation, setup, quickstart
- `reference/` — CLI and API/SDK reference
- `guides/` — Guides and tutorials
- `knowledge-and-collaboration/` — Warp Drive, teams, Admin Panel
- `support-and-community/` — Troubleshooting, billing, privacy
- `enterprise/` — Enterprise features
- `changelog/` — Release changelog

The sidebar configuration is in `astro.config.mjs` at the repo root.
