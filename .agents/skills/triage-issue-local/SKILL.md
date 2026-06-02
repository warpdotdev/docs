---
name: triage-issue-local
description: Triage new GitHub issues on the Warp docs repo. Classifies the issue, identifies affected pages, assesses priority, suggests a fix direction, checks for duplicates, and outputs structured JSON for the triage workflow to apply. Used by the Oz OSS repo management agent when a new issue is opened.
---

# Triage Docs Issue

Triage a newly opened GitHub issue on the Warp docs repository. Analyze the issue, classify it, assess priority, and output a structured `triage_result.json` for the triage workflow to apply labels and post comments.

## Workflow

### 1. Read the issue

Read the issue title and body. Extract:
- What the reporter is describing (bug, content problem, feature request, or support question)
- Any URLs or page references mentioned
- Specific product areas or features referenced

### 2. Classify the issue

Determine the issue type:
- **Site bug** — The docs website platform is broken (search not returning results, navigation links failing, pages not rendering, styling broken, build errors). This is about the site infrastructure, not the content.
- **Content issue** — Documentation is incorrect, outdated, missing, unclear, has typos, or has formatting problems
- **Feature request** — A request for new documentation, new content types, or site enhancements
- **Support question** — A question that belongs in the [Warp community Slack](https://go.warp.dev/join-preview), not the issue tracker

### 3. Identify affected pages

Cross-reference the issue body against the docs site structure to find the specific page(s) involved.

The documentation lives in `src/content/docs/` with these sections:
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

Use `codebase_semantic_search` and `grep` to locate the relevant file(s). If the issue includes a URL like `docs.warp.dev/agent-platform/capabilities/skills`, map it to `src/content/docs/agent-platform/capabilities/skills.mdx`.

### 4. Assess priority

Apply this rubric:
- **`priority/high`** — Factually incorrect information, broken page, security-related content, or a docs page that causes users to take a wrong action
- **`priority/medium`** — Outdated content, confusing instructions, incomplete coverage, or misleading screenshots
- **`priority/low`** — Typos, minor formatting issues, small clarifications, nice-to-have improvements

### 5. Suggest fix direction

Briefly describe what a fix would involve. Be specific enough that someone unfamiliar with the issue could act on it. Examples:
- "Update the CLI command on the environments page to match the current `oz environment create` syntax."
- "Add a note about the macOS-only limitation to the SSH agent forwarding section."
- "Replace the screenshot showing the old Settings UI with the current layout."

### 6. Check for duplicates

Search open issues for potential duplicates:
- Use `gh issue list --repo warpdotdev/docs --state open --limit 100` to list open issues (use `--limit` to avoid missing older issues)
- Compare titles and descriptions for overlap
- If a likely duplicate exists, include it in the `duplicates` field of the output

### 7. Write `triage_result.json`

Write a `triage_result.json` file with the triage results. The workflow reads this file to apply labels and post the issue comment. Do not apply labels or post comments directly.

Schema:

```json
{
  "classification": "content",
  "priority": "priority/medium",
  "labels": ["triage", "priority/medium"],
  "affected_pages": [
    "src/content/docs/agent-platform/cloud-agents/environments.mdx"
  ],
  "suggested_fix": "Update the `oz environment create` command example to use the current `--repo` flag instead of the deprecated `--repository` flag.",
  "duplicates": [],
  "summary": "The environment creation steps reference a deprecated CLI flag.",
  "issue_body": "Thanks for opening this issue! The Warp docs team has been notified and will review it within a few business days.\n\nIf you'd like to contribute a fix yourself, see our [contribution guide](https://github.com/warpdotdev/docs/blob/main/CONTRIBUTING.md). Minor fixes like typos and broken links can go straight to a pull request.\n\n## Triage\n\n- **Classification**: Content issue\n- **Affected pages**: `src/content/docs/agent-platform/cloud-agents/environments.mdx`\n- **Priority**: `priority/medium` — The environment creation steps reference a deprecated CLI flag\n- **Suggested fix**: Update the `oz environment create` command example to use the current `--repo` flag instead of the deprecated `--repository` flag. Verify the correct syntax against `oz environment create --help`.\n- **Duplicates**: No duplicates found\n\n---\n\n**Reviewers**: This issue needs triage. Remove the `triage` label once you've validated the issue, verified priority, and decided on next steps."
}
```

Field reference:
- **`classification`** — One of: `site-bug`, `content`, `feature-request`, `support-question`
- **`priority`** — The priority label name: `priority/high`, `priority/medium`, or `priority/low`
- **`labels`** — Always include `triage` plus the priority label
- **`affected_pages`** — File paths relative to the repo root
- **`suggested_fix`** — One-sentence fix direction from step 5
- **`duplicates`** — Array of issue numbers (e.g., `[16]`), or empty array if none found
- **`summary`** — One-sentence summary of the issue for Slack notifications
- **`issue_body`** — The full markdown comment to post on the issue, including the welcome preamble, triage analysis, and reviewer callout

The `issue_body` should follow this structure:
1. Welcome preamble (for the contributor)
2. Triage analysis (classification, affected pages, priority, suggested fix, duplicates)
3. Reviewer callout after a horizontal rule (for the docs team)

## Reference material

When analyzing issues, consult:
- **Style guide and terminology**: `AGENTS.md` at the repo root contains the docs style guide, content type guidance, and terminology standards.
- **Terminology glossary**: `.warp/references/terminology.md` has the full canonical glossary. Use it to validate that issue reports reference features by their correct names.
- **Site structure**: `astro.config.mjs` contains the sidebar configuration and all registered pages.
- **Source code** (when the issue reports incorrect documentation about a feature): Search `warp-internal` (client, Rust/Swift) and `warp-server` (server, Go) to verify actual product behavior. This helps confirm whether the docs are wrong or the reporter is mistaken. Use `codebase_semantic_search` on these repos, or `grep` for exact symbol names. Docs are the primary source of truth for user-facing answers, but source code is essential for validating accuracy when an issue disputes what the docs say.

## Validation

After creating `triage_result.json`:
- Validate JSON with `jq . triage_result.json` — if this fails, fix the JSON syntax and try again
- Verify `classification` is one of the four allowed values
- Verify `priority` matches one of the three priority labels
- Verify `labels` includes both `triage` and the priority label
- Verify `affected_pages` paths exist in the repo
