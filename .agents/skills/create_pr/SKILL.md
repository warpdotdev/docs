---
name: create_pr
description: Create a pull request in the docs repository for the current branch. Use when the user mentions opening a PR, creating a pull request, submitting changes for review, or preparing documentation for merge.
---

# create_pr

## Overview

This guide covers best practices for creating pull requests in the docs documentation repository, including syncing with main, running linting checks, validating links, and structuring your PR for effective review.

## Related Skills

- `draft_docs` - Draft new documentation pages or update existing ones using established style conventions
- `check_for_broken_links` - Check documentation for broken internal and external links before opening PR

## Pre-PR Checklist

### 1. Sync with main

**Always merge main into your feature branch before opening a PR.**

```bash
git fetch origin
git merge origin/main
```

Resolve any merge conflicts locally before opening the PR.

### 2. Run linting checks

This repo uses Trunk CLI for linting. Run these checks before opening or updating a PR:

```bash
# Check for linting issues
trunk check

# Auto-format files
trunk fmt
```

Enabled linters include:
- `markdownlint` - Markdown formatting and style
- `yamllint` - YAML file validation
- `gitleaks` - Secret detection
- `oxipng` - PNG optimization

:::note
Trunk CLI is not vendored in this repo. Install it separately: https://docs.trunk.io/check/usage
:::

### 3. Check for broken links

Run the link checker to validate all internal and external links:

```bash
# Quick internal-only check (fast, no HTTP requests)
python3 .agents/skills/check_for_broken_links/check_links.py --internal-only

# Full check including external links
python3 .agents/skills/check_for_broken_links/check_links.py
```

Fix any broken links before opening the PR. See the `check_for_broken_links` skill for detailed guidance on fixing different link types.

### 4. Review your changes

Before creating a PR, review what you're about to submit:

```bash
# View commits in your branch
git --no-pager log origin/main..HEAD --oneline

# View file statistics
git --no-pager diff origin/main...HEAD --stat

# View full diff
git --no-pager diff origin/main...HEAD
```

This helps you:
- Verify all intended changes are included
- Catch unintended changes before review
- Write an accurate PR description

### 5. Verify sidebar updates

If you added, moved, or renamed any documentation pages:

- Update the sidebar in `src/sidebar.ts`. That file is the source of truth; `astro.config.mjs` only imports it via `starlightSidebarTopics(sidebarTopics)`.
- Ensure the label matches the H1 title in the document, or omit the label and let Starlight derive it.
- Check that the slug is correct: no leading slash and no `.md`/`.mdx` extension.

### 6. Add redirects for moved/renamed pages

If you renamed or moved a page that's already published, add a redirect to the `redirects` array in `vercel.json` at the repo root. Every redirect lives in that one file, including redirects between top-level sections — there is no per-section redirect file and no external redirect tool.

Check existing redirects first to avoid duplicates.

```json
{
  "source": "/old/path",
  "destination": "/new/path/",
  "statusCode": 308
}
```

Include the trailing slash on `destination` and the `statusCode`, matching the existing entries.

## PR Description Guidelines

Structure your PR description with these sections:

### Summary
Brief explanation of what the PR accomplishes and why.

### Changes
Bulleted list of specific changes, organized by file or area:

```markdown
## Summary
This PR updates the Terminal and Agent modes documentation for the Oz launch.

## Changes

### src/content/docs/agent-platform/local-agents/interacting-with-agents/terminal-and-agent-modes.md
- Added Getting Started section with first-time and existing user experiences
- Updated keyboard shortcuts with comprehensive tables
- Added fork functionality documentation

### src/sidebar.ts
- Updated navigation entry title
```

### Unverified claims (required on drafting PRs)

Any PR that adds or updates page content must state which UI labels, Settings paths, CLI flags, permission defaults, plan eligibility, and platform-support claims could not be verified against `warp-internal`, `warp-server`, or a live build. See step 9.5 of the `draft_docs` skill.

Include the section even when nothing is outstanding:

```markdown
## Unverified claims
None — all UI labels, flags, defaults, and eligibility claims were verified against source.
```

When claims are outstanding, give the reviewer one bullet per claim with what would confirm it:

```markdown
## Unverified claims
- `--auto-approve` flag name — `cloud-agents.mdx`, "Run an agent" — taken from the PRD; confirm against `TuiArgs` in `warp-internal`.
- **Settings** > **Agents** > **Permissions** path — `permissions.mdx`, "Defaults" — source repos were not available in this environment.
```

### Additional context (optional)
- Link to related issues or discussions
- Screenshots for visual changes
- Notes for reviewers

## CLI Workflow

### Check if PR exists for current branch

```bash
gh pr view --json number,url
```

Exit code 0 if PR exists, 1 if not.

### Create a new PR

:::caution
**Always use `--body-file` instead of `--body` for PR descriptions.** Documentation PRs frequently contain backticks, quotes, and other special characters that get corrupted by shell escaping when passed inline. Write the description to a file first, then reference it.

`--body-file` avoids shell-escaping corruption, but it does **not** catch repetition-loop degeneration — a failure mode where the model repeats a phrase or bullet several times and cuts off mid-token (e.g. a sentence ending in an unclosed inline-code span like `` because `m ``). That corrupted text is already in the generated body and survives `--body-file` unchanged. Always run the body integrity checker (`check_pr_body.py`) before creating or editing a PR.
:::

```bash
# 1. Write the description to a temp file using the create_file tool or a heredoc
cat > /tmp/pr-body.md << 'EOF'
## Summary
Description of changes

## Changes
- Change 1
- Change 2

Co-Authored-By: Oz <oz-agent@warp.dev>
EOF

# 2. Verify the body for corruption before submitting (exits non-zero on failure)
python3 .agents/skills/create_pr/check_pr_body.py /tmp/pr-body.md

# 3. Create the PR using the file (only if the check passed)
gh pr create --title "docs: Add feature documentation" --body-file /tmp/pr-body.md

# Open in browser to fill details
gh pr create --web
```

### Update an existing PR

When updating the body of an existing PR, make the **smallest** change rather than regenerating the whole description from memory — re-emitting a long body is what invites repetition-loop degeneration. Fetch the current body, apply a minimal or additive edit, verify it, then submit.

```bash
# 1. Fetch the current body to a file
gh pr view 123 --json body --jq .body > /tmp/pr-body.md

# 2. Make a minimal/additive edit to /tmp/pr-body.md (e.g. append a new section)
#    with the edit_files or create_file tools — do not rewrite untouched sections.

# 3. Verify the body for corruption before submitting (exits non-zero on failure)
python3 .agents/skills/create_pr/check_pr_body.py /tmp/pr-body.md

# 4. Edit the body using the file (only if the check passed)
gh pr edit 123 --body-file /tmp/pr-body.md

# Edit title only
gh pr edit 123 --title "New title"

# Add reviewers or labels
gh pr edit 123 --add-reviewer username --add-label documentation
```

### View PR status

```bash
gh pr status
gh pr checks
```

## Co-Author Attribution

When creating commits or PRs with AI assistance, include attribution at the end of every commit message or PR description:

```
Co-Authored-By: Oz <oz-agent@warp.dev>
```

## After Opening the PR

1. **Monitor for merge conflicts** - If main is updated, merge it into your branch
2. **Respond to review comments** - Address feedback promptly
3. **Re-run checks after changes** - Run `trunk check` and link checker after making updates
4. **Verify Astro Starlight preview** - Astro Starlight automatically generates a preview for PRs; check that rendering looks correct

## Best Practices

- **Keep PRs focused** - One logical documentation change per PR when possible
- **Use descriptive titles** - Start with `docs:` prefix for documentation changes
- **Follow the style guide** - Refer to `AGENTS.md` for voice, tone, and formatting conventions
- **Test locally** - Use `npm run dev` to preview changes before opening PR
- **Include context** - Help reviewers understand why changes were made, not just what changed
