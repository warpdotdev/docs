---
name: style_lint
description: Scan Warp Astro Starlight documentation for style guide violations including formatting issues (Settings path format, UI element format, link quality, VideoEmbed titles, header case, missing frontmatter, image alt text, standardized screenshot widths, callout syntax) and terminology issues (product name casing, Oz terms to avoid, deprecated terms). Run with --changed for PR workflows or --all for periodic audits. Optionally auto-fix high-confidence issues with --fix.
---

# Style Lint

Scan Warp Astro Starlight documentation for formatting and terminology issues defined in the style guide (`AGENTS.md`).

## Running the check

From the docs repo root:

```bash
python3 .agents/skills/style_lint/style_lint.py
```

### Options

- `--all`: Scan all markdown files in `src/content/docs/` (default)
- `--changed`: Scan only files changed in the current branch (fast, for PR workflows)
- `--fix`: Auto-fix high-confidence issues (optional, off by default)
- `--create-pr`: Create a branch and PR with auto-fixes (requires `gh` CLI, implies `--fix`)
- `--output FILE`: Save results to JSON file
- `--slack-notify`: Send results to Slack (only sends when issues are found; requires `SLACK_BOT_TOKEN` and `GROWTH_DOCS_SLACK_CHANNEL_ID` env vars)
- `--slack-channel ID`: Override the default Slack channel

### Quick check on changed files:

```bash
python3 .agents/skills/style_lint/style_lint.py --changed
```

### Full audit with auto-fix and PR:

```bash
python3 .agents/skills/style_lint/style_lint.py --all --fix --create-pr
```

## What it checks

### Formatting checks

- **Settings paths**: Backtick-wrapped Settings paths (`` `Settings > X` ``) → should be per-segment bold (**Settings** > **X**)
- **UI elements after action verbs**: `click \`X\`` → should be `click **X**`
- **Header case**: Title Case in H2/H3/H4 headers (should be sentence case, with exceptions for proper feature names)
- **Missing frontmatter**: Pages without YAML `description` field
- **Link anchor quality**: Empty anchors, raw URL anchors, and generic anchors like "here," "this page," "learn more," or "read more"
- **Link context quality**: Redundant bold prefixes that repeat the link text, and named Oz web app page links missing articles like "the"
- **VideoEmbed titles**: Missing `title` props and generic or numbered titles like "Video," "GitHub Actions video," or "Codebase Context video 1"
- **Image alt text**: `<img>` or `<figure>` without alt text or with generic alt text ("screenshot", "image")
- **Screenshot widths**: Likely UI/product screenshots must use `<figure style={{ maxWidth: "..." }}>` with a standard width (`300px`, `350px`, `375px`, or `563px`)
- **Callout syntax**: Leftover GitBook `{% hint %}` tags that should be migrated to Starlight `:::note` / `:::caution` / `:::danger` asides
- **List format**: Bulleted feature/capability lists missing the bold term + dash pattern (report only, never auto-fixed)

### Terminology checks

- **Product name casing**: "Warp Terminal" (→ "Warp"), "agent mode" (→ "Agent Mode"), "warp drive" (→ "Warp Drive"), "codebase context" (→ "Codebase Context"), "agent management panel" (→ "Agent Management Panel")
- **Oz terms to avoid**: "agent identity", "agent identities", "Oz agent", "Oz cloud agent", "Oz subagent", "Oz conversation", "Ozzies", "Deploying an Oz", "The Oz Agent", "Oz is running", "AI agents"
- **Deprecated terminology**: "whitelist" (→ "allowlist"), "blacklist"/"blocklist" (→ "denylist")
- **External product names**: "Github" (→ "GitHub"), "github actions" (→ "GitHub Actions"), "MacOS" (→ "macOS"), "A.I." (→ "AI")
- **Unrecognized terms** (warning): Bolded terms that look like product names but aren't in `terminology.md`. Flags candidates for glossary addition — not errors, just suggestions.
- **Warp Factories naming**: A bare capitalized "Factory" used as a proper noun. "Warp Factories" is the product and is written in full; an individual "factory" is lowercase. Sentence-, heading-, bullet-, quote-, and cell-initial capitals are positional and stay, as do frontmatter titles and labels, the shipped feature name "Factory MCP", and verbatim UI strings such as **Factory name** and **Add your Factory to your team**. Regression cases live in `test_factory_proper_noun.py`.
- **Hardcoded product name strings**: Product name strings that have a corresponding key in `src/data/vars.ts` but appear as literal text rather than variable syntax. Reports instances of known strings like "Oz CLI", "Oz web app", "oz.warp.dev", "Oz dashboard", "Oz run" (any value currently in `src/data/vars.ts`) in body prose and frontmatter. These are flagged as `⚠️ [IMPORTANT]` in PR context and reported (not auto-fixed) — they should use `{VARS.KEY}` in prose and `{{TOKEN}}` in frontmatter.

### Tone checks (report-only, never auto-fixed)

These enforce the "Voice & tone" section of `AGENTS.md`. Every hit needs a human rewrite, so they are always warnings and never auto-fixed:

- **Buzzwords** (`tone-buzzword`): AI-ism words like "seamless", "powerful", "robust", "comprehensive", "leverage", "streamline", "empower", "delve", abstract metaphors ("landscape", "realm", "tapestry", "testament to"), and filler frames ("it's important to note", "designed to", "ensures that", "allows you to", "in order to"). Words with legitimate technical uses in these docs ("harness", "unlock", "elevated", "journey") are deliberately excluded from the lint and covered by prose guidance only.
- **Meta-openers** (`tone-meta-opener`): Page-narrating text like "This page covers/explains/walks through...". The fix is to cut the sentence and state the thing itself.
- **Consecutive callouts** (`callout-consecutive`): Two `:::` asides back to back with nothing between them. Merge them or move one into body prose.
- **Callout budget** (`callout-density`): More than 4 callouts on one page. The style guide allows at most one per section; the per-page count is the lintable proxy.

## Auto-fix behavior

When run with `--fix`:
- **High-confidence fixes applied automatically**: Settings path format, UI element format, product name casing, external product name casing
- **Low-confidence issues reported but not auto-fixed**: link quality, VideoEmbed title specificity, list format, header case (due to feature name exceptions), ambiguous terminology
- **Tone checks are never auto-fixed**: buzzwords, meta-openers, and callout budget issues always need a human rewrite

## Relationship to validate_ui_refs

This skill checks broader formatting and terminology. The `validate_ui_refs` skill validates UI paths and Command Palette names against the warp-internal codebase. They complement each other with no overlap. Both can run in scheduled cloud agent workflows.

## Tests

Several checks have regression suites, because each is a narrow rule where the
hard part is not firing on legitimate text. Run the relevant one(s) after
touching the corresponding check:

```bash
python3 .agents/skills/style_lint/test_platform_determiner.py
python3 .agents/skills/style_lint/test_factory_proper_noun.py
python3 .agents/skills/style_lint/test_hardcoded_var_exemptions.py
python3 .agents/skills/style_lint/test_header_case_sentence_boundary.py
python3 .agents/skills/style_lint/test_product_casing_word_boundary.py
python3 .agents/skills/style_lint/test_proper_feature_names_third_party.py
python3 .agents/skills/style_lint/test_tone_checks.py
```

## Dependencies

Requires Python 3.7+. Optional: `requests` (for Slack notifications), `gh` CLI (for PR creation).

## Cloud agent / scheduling

For scheduled cloud agent runs:
1. Configure the environment with the docs repo
2. Set the `SLACK_BOT_TOKEN` secret in the environment (for `--slack-notify`)
3. Run: `python3 .agents/skills/style_lint/style_lint.py --all --fix --create-pr --slack-notify`
