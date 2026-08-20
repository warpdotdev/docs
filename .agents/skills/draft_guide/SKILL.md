---
name: draft_guide
description: Draft a tutorial for the Guides section (src/content/docs/guides/). Use for a full workflow walkthrough that helps a developer solve a real problem end to end - setting up a tool, completing a workflow, or learning a technique. Tutorials focus on the "how" with real prompts and reproducible results, targeting non-branded search queries. For a five-minute essential-steps path, use draft_quickstart instead.
---

# Draft tutorial page

Draft a tutorial that walks a developer through an entire workflow, start to finish.

## Tutorial or quickstart?

"Guides" is the name of the section, not a content type. It holds both, and the choice is about scope:

- **Quickstart** — about five minutes, ~600 words, essential steps only, for someone who already knows the product. Use `draft_quickstart`.
- **Tutorial** — a full workflow with context at the decision points, for someone extending a basic understanding to solve a real problem. This skill.

**A tutorial requires that a quickstart already exists** for the product area. Check before drafting. If there is no quickstart, write that first — otherwise the tutorial absorbs setup content that belongs in a shorter page, and readers who only wanted to get started have to wade through the whole workflow.

Tutorials are more conversational than other content: a developer-to-developer conversation that stays accessible to varied technical backgrounds.

## Workflow

Follow the workflow in `.agents/skills/draft_docs/SKILL.md`, using the **guide template** at `.agents/templates/guide-page.md`.

Guide pages live in `src/content/docs/guides/` (the Guides Astro Starlight space), not in the main product reference sections. When placing the file, use these directories:
- `src/content/docs/guides/agent-workflows/` — Using coding agents to explain code, review PRs, run parallel tasks, and attach session context
- `src/content/docs/guides/configuration/` — Rules, agent profiles, saved prompts, and related setup guides
- `src/content/docs/guides/external-tools/` — MCP servers, third-party tools, and integrations
- `src/content/docs/guides/build-an-app-in-warp/` — End-to-end app builds from start to finish
- `src/content/docs/guides/devops/` — Cloud logs, Docker, Kubernetes, testing, and database optimization
- `src/content/docs/guides/frontend/` — Building and refining UI components with coding agents

The sidebar nav is defined in `src/sidebar.ts`, which organizes guides into topic-based sections. When adding a new guide, place the file in the appropriate directory above and add the nav entry under the matching section in `src/sidebar.ts`:
- **Getting started** — First steps with Warp: setup, appearance, key features
- **Agent workflows** — Using coding agents to explain code, review PRs, run parallel tasks
- **Configuration** — Rules, agent profiles, saved prompts, monorepo sync
- **External tools & integrations** — MCP servers, Ollama, third-party tool setup
- **Build an app in Warp** — End-to-end app builds with AI coding workflows
- **DevOps & infrastructure** — Cloud logs, Docker, Kubernetes, testing, database optimization
- **Frontend & UI** — Building and refining UI components with coding agents

## Frontmatter description

One sentence, 50-160 characters, saying what the reader will build or accomplish, using the non-branded phrasing they would search for.
- ✅ `Set up Claude Code and run your first agentic coding session from the terminal.`
- ❌ `A guide to using Claude Code with Warp.`

See "Descriptions by content type" under Frontmatter in `AGENTS.md` for the full rules.

## Content type rules

These rules are specific to guide pages (from the "Drafting by content type" section of `AGENTS.md`):

- **Titles should be task-oriented** and read like a search query. Use shortened titles in the Astro Starlight nav and full descriptive titles in the article H1. Do not put "tutorial" or "guide" in the title.
- **For SEO: capture the non-branded query.** Write the title a developer would actually search for, not "How to do X in Warp." Example: "How to set up Claude Code" not "How to set up Claude Code in Warp."
- All procedural rules apply (focused steps, motivate steps, expected outcomes).
- **Give real examples, not placeholders.** Do not write "enter a commit message" — supply an appropriate one that matches the preceding steps.
- **Include troubleshooting.** Name what commonly goes wrong in this workflow and how to recover. This is the clearest line between a tutorial and a quickstart, which only links to existing troubleshooting.
- **End with a conclusion, then next steps.** Review what the reader built, referring back to the example from the introduction, then give 2-3 actionable next steps.
- **Do not state an expected completion time.** It varies too much by experience level. (Quickstarts do state one; tutorials do not.)
- Link to relevant feature documentation in the main docs where concepts need deeper explanation.
- When a tutorial has a companion video, the written content should stand alone.
- The optional **Productivity tips** section should showcase Warp features as natural extensions of the workflow — not as a separate pitch.

## SEO and AEO optimization

When drafting a guide, check for relevant SEO and AEO data:

1. **Create an AEO brief when source data drives the guide.** If the guide request mentions AEO, Peec, AI search prompts, answer-engine visibility, search-query vocabulary, or content gaps, read `.agents/skills/aeo_brief/SKILL.md` before drafting. Use the brief to map source-data language to natural docs language and to decide whether this should be a new guide or an update to an existing guide.
2. **Use SEO and AEO data** to inform titles, descriptions, and content coverage. The `docs-seo-audit` skill (`.agents/skills/docs-seo-audit/`) can identify technical SEO issues.
3. **Write the frontmatter `description`** to include the primary target keyword naturally. Keep under 160 characters.
4. **Frame the title for non-branded search.** The page should answer the user's actual question, with Warp features as the natural solution in the guide body.
5. **Avoid keyword stuffing.** Preserve high-intent query terms only where they make the guide clearer or more discoverable. Rewrite awkward source-data phrasing into natural developer language.

## Oz CLI and GitHub Actions accuracy

When a guide includes Oz CLI commands or GitHub Actions workflows using `warpdotdev/oz-agent-action`:

- **Verify Oz CLI commands against `/reference/cli/`.** Do not infer flag names or argument formats. Use only flags documented in the CLI reference. When in doubt, link to the reference page instead of showing a command.
- **`oz-agent-action` input format**: `warp_api_key` is a `with:` input to the action, not an `env:` variable. `GITHUB_TOKEN` goes in `env:`. The correct pattern is:
  ```yaml
  - uses: warpdotdev/oz-agent-action@v1
    with:
      skill: SKILL_NAME
      environment: YOUR_OZ_ENVIRONMENT_SLUG
      warp_api_key: ${{ secrets.WARP_API_KEY }}
    env:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  ```
- **Every GitHub Actions workflow example that performs write operations must include a `permissions:` block** at the workflow level, before `jobs:`. Use the minimum permissions for the task:
  - Triage (label/comment on issues): `issues: write`
  - Spec/implementation (push branches, open PRs): `contents: write`, `pull-requests: write`
  - Review (post PR comments): `pull-requests: write`
  Without an explicit `permissions:` block, workflows fail in repositories with restricted default permissions.
- **`oz secret create` must not include `--value` on the command line.** The `--value` flag exposes secrets in shell history and process arguments. Show `oz secret create --name SECRET_NAME` and note that the CLI prompts for the value interactively.
- **Slash commands** (`/command-name`) in standalone code fences should use `bash` as the language identifier, consistent with the docs style guide for terminal input.

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

- **Verify the target page exists.** Check `src/sidebar.ts` for sidebar entries and the corresponding file under `src/content/docs/` to confirm the page exists. Do NOT generate plausible-looking URLs to pages that don't exist.
- **If a target page is planned but not yet published**, link to the closest existing page and add a TODO comment with the intended future path: `<!-- TODO: Update to [future-path] once [page name] is live -->`
- **For third-party CLI agent pages**, the current paths are under `src/content/docs/agent-platform/cli-agents/` (e.g., `claude-code.mdx`, `codex.mdx`, `opencode.mdx`).

## Cross-linking

Every guide should link to:
- At least one other guide in the Guides section
- Relevant feature documentation in the main docs (`src/content/docs/` or `src/content/docs/agent-platform/`)
- If applicable, pages in the Third-Party CLI Agents section (`src/content/docs/agent-platform/cli-agents/`)

## Pre-handoff self-review

Before presenting a guide draft, do an editorial pass focused on the issues that often create avoidable review back-and-forth:
- **Scannability** - Break dense procedure sections into numbered steps, short bullets, or concise subsections. Avoid long H2 sections that mix multiple actions.
- **Usefulness** - Confirm the guide teaches a real workflow and does not become a junk drawer of loosely related AEO topics.
- **Vocabulary translation** - Check that Peec/search phrasing is translated into natural docs language while preserving accurate high-intent terms like third-party product names.
- **Product and UI names** - Check product surfaces against `.agents/references/terminology.md` and validate UI paths or command names when the guide depends on exact navigation.
- **Human-review questions** - Surface unresolved questions about product behavior, placement, or terminology instead of hiding them in the draft.

## Existing examples

Read 2-3 of these strong examples to match the existing pattern:
- `src/content/docs/guides/external-tools/sentry-mcp-fix-sentry-error-in-empower-website.mdx`
- `src/content/docs/guides/build-an-app-in-warp/building-a-real-time-chat-app-github-mcp-railway.mdx`
- `src/content/docs/guides/agent-workflows/how-to-explain-your-codebase-using-warp-rust-codebase.mdx`
