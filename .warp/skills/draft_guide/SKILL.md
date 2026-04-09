---
name: draft_guide
description: Draft a new guide page for the Guides section (guides/). Use for practical, task-oriented walkthroughs that help developers accomplish a specific goal — like setting up a tool, completing a workflow, or learning a technique. Guides focus on the "how" with real prompts and reproducible results, targeting non-branded search queries.
---

# Draft guide page

Draft a practical guide that walks a developer through accomplishing a specific goal.

## Workflow

Follow the workflow in `.warp/skills/draft_docs/SKILL.md`, using the **guide template** at `.warp/templates/guide-page.md`.

Guide pages live in `guides/` (the Guides GitBook space), not in `docs/`. When placing the file, use these directories:
- `guides/integrations/` — Setup guides for external tools (Claude Code, Codex, MCP servers)
- `guides/developer-workflows/` — Workflow and technique guides (code review, parallel agents, voice input)
- `guides/end-to-end-builds/` — Full app builds from start to finish
- `guides/mcp-servers/` — MCP-specific guides

The sidebar nav is defined in `guides/SUMMARY.md`, which organizes guides into topic-based sections. When adding a new guide, place the file in the appropriate directory above and add the nav entry under the matching section in `SUMMARY.md`:
- **Getting started** — First steps with Warp: setup, appearance, key features
- **Agent workflows** — Using coding agents to explain code, review PRs, run parallel tasks
- **Configuration** — Rules, agent profiles, saved prompts, monorepo sync
- **External tools & integrations** — MCP servers, Ollama, third-party tool setup
- **Build an app in Warp** — End-to-end app builds with AI coding workflows
- **DevOps & infrastructure** — Cloud logs, Docker, Kubernetes, testing, database optimization
- **Frontend & UI** — Building and refining UI components with coding agents

## Content type rules

These rules are specific to guide pages (from the "Drafting by content type" section of `AGENTS.md`):

- **Titles should be task-oriented** and read like a search query. Use shortened titles in the GitBook nav and full descriptive titles in the article H1.
- **For SEO: capture the non-branded query.** Write the title a developer would actually search for, not "How to do X in Warp." Example: "How to Set Up Claude Code" not "How to Set Up Claude Code in Warp."
- All procedural rules apply (focused steps, motivate steps, expected outcomes).
- Link to relevant feature documentation in the main docs (`docs/`) where concepts need deeper explanation.
- When a guide has a companion video, the written content should stand alone.
- The optional **Productivity tips** section should showcase Warp features as natural extensions of the workflow — not as a separate pitch.

## SEO and AEO optimization

When drafting a guide, check for relevant SEO and AEO data:

1. **Check the buzz repo** for Peec AI visibility data (`buzz/data/peec/`) and Google Search Console data (`buzz/data/gsc/`). These contain keyword performance and AI engine visibility scores for Warp-related queries.
2. **Write the frontmatter `description`** to include the primary target keyword naturally. Keep under 160 characters.
3. **Frame the title for non-branded search.** The page should answer the user's actual question, with Warp features as the natural solution in the guide body.

<!-- TODO: Update this section with specific data lookup instructions once the buzz repo data directory structure is finalized. -->

## Cross-linking

Every guide should link to:
- At least one other guide in the Guides section
- Relevant feature documentation in the main docs (`docs/warp/` or `docs/agent-platform/`)
- If applicable, pages in the Coding Agents section (`docs/warp/coding-agents/`)

## Existing examples

Read 2-3 of these strong examples to match the existing pattern:
- `guides/mcp-servers/sentry-mcp-fix-sentry-error-in-empower-website.md`
- `guides/end-to-end-builds/building-a-real-time-chat-app-github-mcp-+-railway.md`
- `guides/developer-workflows/beginner/how-to-explain-your-codebase-using-warp-rust-codebase.md`
