---
name: draft_guide
description: Draft a new guide page for the Guides section (src/content/docs/university/). Use for practical, task-oriented walkthroughs that help developers accomplish a specific goal — like setting up a tool, completing a workflow, or learning a technique. Guides focus on the "how" with real prompts and reproducible results, targeting non-branded search queries.
---

# Draft guide page

Draft a practical guide that walks a developer through accomplishing a specific goal.

## Workflow

Follow the workflow in `.warp/skills/draft_docs/SKILL.md`, using the **guide template** at `.warp/templates/guide-page.md`.

Guide pages live in `src/content/docs/university/` (the Guides Astro Starlight space), not in `docs/`. When placing the file, use these directories:
- `src/content/docs/university/integrations/` — Setup guides for external tools (Claude Code, Codex, MCP servers)
- `src/content/docs/university/developer-workflows/` — Workflow and technique guides (code review, parallel agents, voice input)
- `src/content/docs/university/end-to-end-builds/` — Full app builds from start to finish
- `src/content/docs/university/mcp-servers/` — MCP-specific guides

The sidebar nav is defined in `src/content/docs/university/astro.config.mjs (sidebar config)`, which organizes guides into topic-based sections. When adding a new guide, place the file in the appropriate directory above and add the nav entry under the matching section in `astro.config.mjs (sidebar config)`:
- **Getting started** — First steps with Warp: setup, appearance, key features
- **Agent workflows** — Using coding agents to explain code, review PRs, run parallel tasks
- **Configuration** — Rules, agent profiles, saved prompts, monorepo sync
- **External tools & integrations** — MCP servers, Ollama, third-party tool setup
- **Build an app in Warp** — End-to-end app builds with AI coding workflows
- **DevOps & infrastructure** — Cloud logs, Docker, Kubernetes, testing, database optimization
- **Frontend & UI** — Building and refining UI components with coding agents

## Content type rules

These rules are specific to guide pages (from the "Drafting by content type" section of `AGENTS.md`):

- **Titles should be task-oriented** and read like a search query. Use shortened titles in the Astro Starlight nav and full descriptive titles in the article H1.
- **For SEO: capture the non-branded query.** Write the title a developer would actually search for, not "How to do X in Warp." Example: "How to Set Up Claude Code" not "How to Set Up Claude Code in Warp."
- All procedural rules apply (focused steps, motivate steps, expected outcomes).
- Link to relevant feature documentation in the main docs (`docs/`) where concepts need deeper explanation.
- When a guide has a companion video, the written content should stand alone.
- The optional **Productivity tips** section should showcase Warp features as natural extensions of the workflow — not as a separate pitch.

## SEO and AEO optimization

When drafting a guide, check for relevant SEO and AEO data:

1. **Use SEO and AEO data** to inform titles, descriptions, and content coverage. The `docs-seo-audit` skill (`.warp/skills/docs-seo-audit/`) can identify technical SEO issues.
2. **Write the frontmatter `description`** to include the primary target keyword naturally. Keep under 160 characters.
3. **Frame the title for non-branded search.** The page should answer the user's actual question, with Warp features as the natural solution in the guide body.

## Third-party tool accuracy

When a guide documents a third-party tool (Claude Code, Codex, OpenCode, etc.):

- **Always verify claims against the tool's official documentation.** Do not infer implementation details (programming language, architecture, framework) from GitHub repo language stats or third-party blog posts. These are frequently wrong or outdated.
- **Link to official docs rather than reproducing install steps.** Installation commands, plan names, pricing, model names, and permission/approval modes change frequently. Link to the tool's official quickstart or setup page and keep the guide focused on the Warp-specific workflow.
- **If you must include specific details** (e.g., exact commands, plan tier names, approval mode names), fetch and verify them from the tool's current official documentation before publishing. Add a note or link so readers can check for updates.
- **Do not include pricing information** for third-party tools — it changes and is hard to keep evergreen.
- **Avoid brand-specific product mentions** that date quickly or exclude users. Use generic terms: "Bluetooth audio device" not "AirPods", "code editor" not a specific IDE unless the guide is about that IDE.
- **Avoid specific model version numbers** (e.g., "GPT-5.4") unless directly relevant. Link to the tool's model documentation instead.

## Link verification

Before adding any internal documentation link:

- **Verify the target page exists.** Check the relevant `astro.config.mjs (sidebar config)` file (`src/content/docs/astro.config.mjs (sidebar config)`, `src/content/docs/agent-platform/astro.config.mjs (sidebar config)`, `src/content/docs/university/astro.config.mjs (sidebar config)`) to confirm the page is listed. Do NOT generate plausible-looking URLs to pages that don't exist.
- **If a target page is planned but not yet published**, link to the closest existing page and add a TODO comment with the intended future path: `<!-- TODO: Update to [future-path] once [page name] is live -->`
- **For third-party agent pages**, the current paths are under `src/content/docs/agent-platform/third-party-agents/` (e.g., `claude-code.mdx`, `codex.mdx`, `opencode.mdx`).

## Cross-linking

Every guide should link to:
- At least one other guide in the Guides section
- Relevant feature documentation in the main docs (`src/content/docs/` or `src/content/docs/agent-platform/`)
- If applicable, pages in the Coding Agents section (`src/content/docs/agent-platform/third-party-agents/`)

## Existing examples

Read 2-3 of these strong examples to match the existing pattern:
- `university/mcp-servers/sentry-mcp-fix-sentry-error-in-empower-website.mdx`
- `university/end-to-end-builds/building-a-real-time-chat-app-github-mcp-+-railway.mdx`
- `university/developer-workflows/beginner/how-to-explain-your-codebase-using-warp-rust-codebase.mdx`
