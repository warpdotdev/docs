---
name: validate_ui_refs
description: Scan Warp GitBook documentation for UI menu paths and Command Palette command names, then validate them against the warp-internal codebase for accuracy. Catch and surface outdated steps automatically.
---

# Validate UI References

This skill scans Warp's GitBook documentation for references to UI paths (e.g. `Settings > Agents > Oz > Active AI`) and Command Palette command names (e.g. "Open Theme Picker"), then validates them against a snapshot of known-valid paths extracted from the `warp-internal` codebase. It also catches paths that reference deprecated Settings sections (e.g. the old `Settings > AI` before it became the `Agents` umbrella) and auto-migrates them to the current structure.

## Source files: UI menu paths vs settings.toml schema

Warp has two separate sources of truth for "settings." Don't conflate them when drafting docs:

- **`.warp/skills/validate_ui_refs/valid_paths.json`** (this skill) — describes the in-app **Settings sidebar**, **umbrellas**, **subpages**, and **sub-section headers** that users click through (e.g. `Settings` > **Agents** > **Profiles**). Extracted from `app/src/settings_view/` (sidebar enum, `SettingsUmbrella`, `Category::new`, `build_sub_header`). Use this when validating a navigation step in a doc.
- **`.warp/references/settings-schema.json`** (separate reference) — JSON Schema for the user's `settings.toml` file. Section keys here are TOML keys (e.g. `[agents.profiles]`, `[agents.warp_agent.active_ai]`), not what the user clicks. Use this (and `docs/warp/terminal/settings/all-settings.md`) when documenting a `settings.toml` snippet.

The two mostly align after the umbrella migration (top-level `agents` matches the **Agents** umbrella), but they can drift — e.g. the schema groups settings under `agents.warp_agent.active_ai`, while in the UI those settings live on the **Warp Agent** subpage with **Active AI** as a sub-header. This skill only validates the UI-menu side; it does not check whether a `[section.subsection]` TOML path in a doc matches the schema.

## Running the Check

From the gitbook repo root:

```bash
python3 .warp/skills/validate_ui_refs/validate_ui_refs.py --all
```

### Options

- `--check-paths`: Only validate UI menu paths (Settings, File, View, Warp Drive)
- `--check-commands`: Only validate Command Palette names
- `--check-format`: Check that UI paths use the canonical bold format: **Settings** > **Agents** > **Oz** > **Active AI**
- `--all`: Run all checks (default)
- `--fix`: Auto-fix high-confidence issues (e.g. case mismatches)
- `--create-pr`: Create a branch and PR with auto-fixes (requires `gh` CLI)
- `--slack-notify`: Post results to `#growth-docs` Slack channel (only sends when issues are found)
- `--slack-channel ID`: Override default Slack channel
- `--include-changelog`: Include `changelog/` in the scan (excluded by default since it's a historical record)
- `--refresh-valid-paths`: Re-extract valid paths from `warp-internal` and update `valid_paths.json`
- `--warp-internal-path PATH`: Path to the `warp-internal` repo (default: `../warp-internal` relative to gitbook root, or `WARP_INTERNAL_PATH` env var)
- `--output FILE`: Save results to a JSON file
- `--self-test`: Run internal sanity checks (snapshot invariants, `_is_external_path` regressions, `refresh_valid_paths` preservation) and exit

### Quick path-only check:

```bash
python3 .warp/skills/validate_ui_refs/validate_ui_refs.py --check-paths
```

### Full check with auto-fix and PR:

```bash
python3 .warp/skills/validate_ui_refs/validate_ui_refs.py --all --fix --create-pr
```

## Output Format

The script outputs a report like:

```
=== UI REFERENCE VALIDATION REPORT ===
Generated: 2026-02-19T00:17:00Z
Files scanned: 174

### SETTINGS PATH ISSUES (5 found)
❌ "Current Theme" is not a known sub-section of Appearance
  themes.md:26
  Path: Settings > Appearance > Current Theme
  Suggestion: Valid sub-sections: Themes, Icon, Window, Input, Panes, Blocks, Text, Cursor, Tabs, Full-screen Apps

⚠️ "Settings > AI" has moved under the "Agents" umbrella
  codebase-context.md:34
  Path: Settings > AI > Active AI
  Suggestion: Settings > Agents > Oz > Active AI

### COMMAND PALETTE ISSUES (1 found)
❌ UNMATCHED COMMAND
  themes.md:26
  Reference: "Open Theme Creator"
  Did you mean "Open theme picker"? (score: 0.85)
```

## Refreshing Valid Paths

The `valid_paths.json` file is a static snapshot of valid UI paths. To update it from the latest `warp-internal` source:

```bash
python3 .warp/skills/validate_ui_refs/validate_ui_refs.py --refresh-valid-paths --warp-internal-path /path/to/warp-internal
```

This parses:
- `SettingsSection` enum and `Display` impl from `settings_view/mod.rs`
- `SettingsUmbrella::new("Label", vec![...])` calls from `mod.rs` (resolved to subpage display names via the `Display` impl)
- `Category::new(...)` and `build_sub_header(...)` calls from settings page files
- `EditableBinding::new(...)` registrations from `terminal/view/init.rs`, `workspace/mod.rs`, and `pane_group/pane/view/mod.rs`

### Preserved fields

Refreshing is a **merge**, not an overwrite. The following fields in `valid_paths.json` are hand-maintained and preserved across refreshes:

- `umbrellas` — auto-detected umbrellas from `SettingsUmbrella::new(...)` are merged in, but any existing entry in the snapshot wins on conflict so hand-authored `subpages` ordering and notes aren't lost.
- `deprecated_sections` — the migration rules for old top-level labels (`AI`, `Platform`, `MCP Servers`, `Environments`, etc.) are entirely hand-maintained and copied forward unchanged.
- `top_level_sidebar` — order of top-level entries in the Settings sidebar.
- `macos_menu_bar` and `warp_drive` — stable UI surfaces that change infrequently; maintained manually.

If you add a brand-new umbrella in `warp-internal`, `--refresh-valid-paths` will pick it up automatically and stamp `umbrella:` on the affected subpage entries in `settings_sections`. You may still want to review the generated umbrella entry to confirm the subpage order matches the UI.

### Self-test

The `--self-test` flag runs three quick sanity checks against the current snapshot and a synthetic `warp-internal` fixture:

1. `umbrellas` and `deprecated_sections` in the shipped `valid_paths.json` are non-empty.
2. `_is_external_path()` does NOT suppress a legitimate Warp Settings path in sentences that also mention external products (e.g. a GitHub/Linear callout on the same line as `Settings > MCP Servers`).
3. `refresh_valid_paths()` preserves the hand-maintained fields above when run against a synthetic warp-internal with the new enum layout, and the new umbrella subpage entries show up in `settings_sections`.

Run it before landing any change to `validate_ui_refs.py` or `valid_paths.json`:

```bash
python3 .warp/skills/validate_ui_refs/validate_ui_refs.py --self-test
```

## What Gets Validated

### UI Paths
- **Settings paths**: `Settings > [Section] > [Sub-section]` — validates section and sub-section names against the `SettingsSection` enum.
- **Settings umbrella paths**: `Settings > [Umbrella] > [Subpage] > [Sub-section]` — validates umbrella + subpage against the `umbrellas` object in `valid_paths.json`. Current umbrellas are **Agents** (Oz / Profiles / MCP servers / Knowledge / Third party CLI agents), **Code** (Indexing and projects / Editor and Code Review), and **Cloud platform** (Environments / Oz Cloud API Keys).
- **Deprecated Settings sections**: paths that start with deprecated top-level labels (e.g. `Settings > AI`, `Settings > Platform`, `Settings > MCP Servers`, `Settings > Environments`) are flagged as `deprecated_section` with an auto-fixable migration to the current umbrella path.
- **macOS menu bar**: `File > ...`, `View > ...`, `Warp > ...` — validates against known menu items.
- **Warp Drive**: `Warp Drive > ...`, `Personal > ...` — validates against known spaces and object types.
- **Multiple markdown formats**: backtick-wrapped, bold, italic, and bare inline paths.

### Format Consistency
- All UI paths should use per-segment bold formatting: **Settings** > **Agents** > **Oz** > **Active AI**
- Backtick formatting (`` `Settings > Agents > Oz` ``), full bold wrapping (`**Settings > Agents > Oz**`), italic, and bare formats are flagged
- Auto-fix with `--fix` converts non-canonical paths to the correct bold format

### UI Element Formatting
- Clickable UI elements (buttons, toggles, links, dropdowns) should be bold, not backtick: Click **Save**, not Click `Save`
- Detected via action keywords: click, select, toggle, enable, disable, choose, check, uncheck, expand, collapse, open, close, tap
- Handles prepositions: "click on `X`", "click the `X`" are also caught
- Keyboard keys stay in backticks (press `Enter`, hit `Esc`) — "press" and "hit" are excluded from the check
- Code-like content (CLI flags, paths, CamelCase identifiers, keyboard shortcuts) is automatically excluded
- Auto-fix with `--fix` converts backtick UI elements to bold

### Command Palette Names
- Quoted strings near "Command Palette" mentions
- `Command Palette > CommandName` arrow patterns
- Fuzzy matching with suggestions for near-misses

### Exclusions
- `changelog/` directory (historical record; use `--include-changelog` to opt in)
- `_book/` and `node_modules/` build artifacts
- External product paths (GitHub, Slack, etc.) are filtered by context

## Auto-Fix

When run with `--fix`, the script automatically corrects:
- **Case mismatches**: e.g. `Settings > keyboard shortcuts` → `Settings > Keyboard shortcuts`
- **Deprecated-section migrations**: e.g. `Settings > AI > Input` → `Settings > Agents > Oz > Input`, `Settings > Platform` → `Settings > Cloud platform > Oz Cloud API Keys`. Governed by the `deprecated_sections` object in `valid_paths.json`.
- **Non-canonical UI path formats**: backtick, italic, bare → per-segment bold. Deprecated-section migrations also upgrade the formatting to canonical bold in the same replace.
- **Backtick UI elements**: e.g. Click `Save` → Click **Save**
- Only path case fixes and deprecated-section migrations with confidence ≥ 0.9 are applied; format fixes are always applied.

Fixes that require manual review (e.g. umbrella-only paths like `Settings > Code` that need a specific subpage chosen, fuzzy matches below 0.9 confidence, or removed features) are reported but not auto-fixed.

## Slack Notifications

Slack notifications are designed for scheduled/automated runs, not ad-hoc usage. When running the skill manually (e.g., during a PR review or docs update), you can review results directly in the terminal output.

### Current behavior

The `--slack-notify` flag posts a summary to `#growth-docs` when unfixed issues remain after a run. If the scan is clean (0 issues), no notification is sent.

### Intended behavior for scheduled runs

When this skill is configured as a scheduled Oz agent, Slack notifications should alert the team in two cases:

1. **Auto-fixes applied** — the script found and corrected issues, and created a PR. The notification should include the PR link so the team can review and merge.
2. **Unfixed issues remain** — some issues could not be auto-corrected (e.g., a renamed or removed section) and require manual attention. The notification should list these for triage.

If a scheduled run finds no issues at all, the notification should be skipped (no noise).

> **Note:** This two-condition notification logic is not yet implemented. The current `--slack-notify` flag only covers condition 2 (unfixed issues). When we set up scheduled runs, the script should be updated to also notify on condition 1 (auto-fixes with PR link).

### Setup (one-time)

Create a Warp team secret for the Slack bot token:

```bash
oz secret create SLACK_BOT_TOKEN --team --description "Slack bot token for UI ref validation reports"
```

The token needs `chat:write` scope.

### Usage

```bash
python3 .warp/skills/validate_ui_refs/validate_ui_refs.py --all --slack-notify
```

## Cloud Agent / Scheduling

For scheduled Oz cloud agent runs:

1. Configure the environment with the gitbook repo
2. Keep `valid_paths.json` up-to-date by running `--refresh-valid-paths` as a pre-step (requires `warp-internal` in the environment)
3. Set the `SLACK_BOT_TOKEN` secret in the environment
4. Run: `python3 .warp/skills/validate_ui_refs/validate_ui_refs.py --all --fix --create-pr --slack-notify`

A typical scheduled agent would:
1. Run `--refresh-valid-paths` to update the snapshot
2. Run `--all --fix --create-pr --slack-notify` to check, fix, and report

## Dependencies

- Python 3.7+
- `requests` (for Slack notifications): `pip3 install requests`
- `gh` CLI (for PR creation)
- Access to `warp-internal` repo (only for `--refresh-valid-paths`)
