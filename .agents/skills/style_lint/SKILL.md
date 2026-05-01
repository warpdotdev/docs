---
name: style_lint
description: Scan Warp Astro Starlight documentation for style guide violations including formatting issues (Settings path format, UI element format, header case, missing frontmatter, image alt text, callout syntax) and terminology issues (product name casing, Oz terms to avoid, deprecated terms). Run with --changed for PR workflows or --all for periodic audits. Optionally auto-fix high-confidence issues with --fix.
---

# Style Lint

Scan Warp Astro Starlight documentation for formatting and terminology issues defined in the style guide (`AGENTS.md`).

## Running the check

From the docs repo root:

```bash
python3 .warp/skills/style_lint/style_lint.py
```

### Options

- `--all`: Scan all markdown files in `docs/` (default)
- `--changed`: Scan only files changed in the current branch (fast, for PR workflows)
- `--fix`: Auto-fix high-confidence issues (optional, off by default)
- `--create-pr`: Create a branch and PR with auto-fixes (requires `gh` CLI, implies `--fix`)
- `--output FILE`: Save results to JSON file
- `--slack-notify`: Send results to Slack (only sends when issues are found; requires `SLACK_BOT_TOKEN` and `SLACK_CHANNEL_ID` env vars)
- `--slack-channel ID`: Override the default Slack channel

### Quick check on changed files:

```bash
python3 .warp/skills/style_lint/style_lint.py --changed
```

### Full audit with auto-fix and PR:

```bash
python3 .warp/skills/style_lint/style_lint.py --all --fix --create-pr
```

## What it checks

### Formatting checks

- **Settings paths**: Backtick-wrapped Settings paths (`` `Settings > X` ``) → should be per-segment bold (**Settings** > **X**)
- **UI elements after action verbs**: `click \`X\`` → should be `click **X**`
- **Header case**: Title Case in H2/H3/H4 headers (should be sentence case, with exceptions for proper feature names)
- **Missing frontmatter**: Pages without YAML `description` field
- **Image alt text**: `<img>` or `<figure>` without alt text or with generic alt text ("screenshot", "image")
- **Callout syntax**: Leftover GitBook `{% hint %}` tags that should be migrated to Starlight `:::note` / `:::caution` / `:::danger` asides
- **List format**: Bulleted feature/capability lists missing the bold term + dash pattern (report only, never auto-fixed)

### Terminology checks

- **Product name casing**: "Warp Terminal" (→ "Warp"), "agent mode" (→ "Agent Mode"), "warp drive" (→ "Warp Drive"), "codebase context" (→ "Codebase Context"), "agent management panel" (→ "Agent Management Panel")
- **Oz terms to avoid**: "Ozzies", "Deploying an Oz", "The Oz Agent", "Oz is running", "AI agents"
- **Deprecated terminology**: "whitelist" (→ "allowlist"), "blacklist"/"blocklist" (→ "denylist")
- **External product names**: "Github" (→ "GitHub"), "github actions" (→ "GitHub Actions"), "MacOS" (→ "macOS"), "A.I." (→ "AI")
- **Unrecognized terms** (warning): Bolded terms that look like product names but aren't in `terminology.md`. Flags candidates for glossary addition — not errors, just suggestions.

## Auto-fix behavior

When run with `--fix`:
- **High-confidence fixes applied automatically**: Settings path format, UI element format, product name casing, external product name casing
- **Low-confidence issues reported but not auto-fixed**: list format, header case (due to feature name exceptions), ambiguous terminology

## Relationship to validate_ui_refs

This skill checks broader formatting and terminology. The `validate_ui_refs` skill validates UI paths and Command Palette names against the warp-internal codebase. They complement each other with no overlap. Both can run in scheduled Oz agent workflows.

## Dependencies

Requires Python 3.7+. Optional: `requests` (for Slack notifications), `gh` CLI (for PR creation).

## Cloud agent / scheduling

For scheduled Oz cloud agent runs:
1. Configure the environment with the docs repo
2. Set the `SLACK_BOT_TOKEN` secret in the environment (for `--slack-notify`)
3. Run: `python3 .warp/skills/style_lint/style_lint.py --all --fix --create-pr --slack-notify`
