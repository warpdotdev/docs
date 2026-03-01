---
name: create_pr
description: Create a pull request in the gitbook repository for the current branch. Use when the user mentions opening a PR, creating a pull request, submitting changes for review, or preparing documentation for merge.
---

# create_pr

## Overview

This guide covers best practices for creating pull requests in the gitbook documentation repository, including syncing with main, running linting checks, validating links, and structuring your PR for effective review.

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

{% hint style="info" %}
Trunk CLI is not vendored in this repo. Install it separately: https://docs.trunk.io/check/usage
{% endhint %}

### 3. Check for broken links

Run the link checker to validate all internal and external links:

```bash
# Quick internal-only check (fast, no HTTP requests)
python3 .warp/skills/check_for_broken_links/check_links.py --internal-only

# Full check including external links
python3 .warp/skills/check_for_broken_links/check_links.py
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

### 5. Verify SUMMARY.md updates

If you added, moved, or renamed any documentation pages:

- Update the relevant section's `SUMMARY.md` file (e.g., `docs/warp/SUMMARY.md`, `docs/agent-platform/SUMMARY.md`)
- Ensure the page title in SUMMARY.md matches the H1 title in the document
- Check that the file path is correct

### 6. Add redirects for moved/renamed pages

If you renamed or moved a page that's already published:

- Add a redirect entry to the appropriate `.gitbook.yaml` file
- For cross-space redirects, use the `scripts/gitbook_redirects.py` tool
- Check existing redirects first to avoid duplicates

```yaml
# Example redirect in .gitbook.yaml
redirects:
    old/path/without/extension: new/path/to/file.md
```

## PR Description Guidelines

Structure your PR description with these sections:

### Summary
Brief explanation of what the PR accomplishes and why.

### Changes
Bulleted list of specific changes, organized by file or area:

```markdown
## Summary
This PR updates the Agent Modality documentation for the Oz launch.

## Changes

### docs/agent-platform/agent/agent-modality-beta.md
- Added Getting Started section with first-time and existing user experiences
- Updated keyboard shortcuts with comprehensive tables
- Added fork functionality documentation

### docs/agent-platform/SUMMARY.md
- Updated navigation entry title
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

{% hint style="warning" %}
**Always use `--body-file` instead of `--body` for PR descriptions.** Documentation PRs frequently contain backticks, quotes, and other special characters that get corrupted by shell escaping when passed inline. Write the description to a file first, then reference it.
{% endhint %}

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

# 2. Create the PR using the file
gh pr create --title "docs: Add feature documentation" --body-file /tmp/pr-body.md

# Open in browser to fill details
gh pr create --web
```

### Update an existing PR

```bash
# Edit body using a file (recommended — avoids shell escaping issues)
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
Co-Authored-By: Warp <agent@warp.dev>
```

## After Opening the PR

1. **Monitor for merge conflicts** - If main is updated, merge it into your branch
2. **Respond to review comments** - Address feedback promptly
3. **Re-run checks after changes** - Run `trunk check` and link checker after making updates
4. **Verify GitBook preview** - GitBook automatically generates a preview for PRs; check that rendering looks correct

## Best Practices

- **Keep PRs focused** - One logical documentation change per PR when possible
- **Use descriptive titles** - Start with `docs:` prefix for documentation changes
- **Follow the style guide** - Refer to `AGENTS.md` for voice, tone, and formatting conventions
- **Test locally** - Use `npx honkit serve docs` to preview changes before opening PR
- **Include context** - Help reviewers understand why changes were made, not just what changed
