---
name: validate_ui_refs
description: Scan Warp Astro Starlight documentation for UI menu paths and Command Palette command names, then validate them against the warp-internal codebase for accuracy. Catch and surface outdated steps automatically.
---

# Validate UI References

This skill scans Warp's Astro Starlight documentation for references to UI paths (e.g. `Settings > AI > Active AI`) and Command Palette command names (e.g. "Open Theme Picker"), then validates them against a snapshot of known-valid paths extracted from the `warp-internal` codebase.

## Running the Check

From the docs repo root:

```bash
python3 .warp/skills/validate_ui_refs/validate_ui_refs.py --all
```

### Options

- `--check-paths`: Only validate UI menu paths (Settings, File, View, Warp Drive)
- `--check-commands`: Only validate Command Palette names
- `--check-format`: Check that UI paths use the canonical bold format: **Settings** > **AI** > **Active AI**
- `--all`: Run all checks (default)
- `--fix`: Auto-fix high-confidence issues (e.g. case mismatches)
- `--create-pr`: Create a branch and PR with auto-fixes (requires `gh` CLI)
- `--slack-notify`: Post results to Slack (only sends when issues are found; requires `SLACK_BOT_TOKEN` and `SLACK_CHANNEL_ID` env vars)
- `--slack-channel ID`: Override default Slack channel
- `--include-changelog`: Include `changelog/` in the scan (excluded by default since it's a historical record)
- `--refresh-valid-paths`: Re-extract valid paths from `warp-internal` and update `valid_paths.json`
- `--warp-internal-path PATH`: Path to the `warp-internal` repo (default: `../warp-internal` relative to docs root, or `WARP_INTERNAL_PATH` env var)
- `--output FILE`: Save results to a JSON file

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

⚠️ "active ai" is not a known sub-section of AI
  codebase-context.md:34
  Path: Settings > AI > active ai
  Suggestion: Did you mean "Active AI"? (score: 0.92)

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
- `Category::new(...)` and `build_sub_header(...)` calls from settings page files
- `EditableBinding::new(...)` registrations from `terminal/view/init.rs` and `workspace/mod.rs`

The macOS menu bar and Warp Drive sections are maintained as manual lists in `valid_paths.json` since they change infrequently.

## What Gets Validated

### UI Paths
- **Settings paths**: `Settings > [Section] > [Sub-section]` — validates section and sub-section names against the `SettingsSection` enum
- **macOS menu bar**: `File > ...`, `View > ...`, `Warp > ...` — validates against known menu items
- **Warp Drive**: `Warp Drive > ...`, `Personal > ...` — validates against known spaces and object types
- **Multiple markdown formats**: backtick-wrapped, bold, italic, and bare inline paths

### Format Consistency
- All UI paths should use per-segment bold formatting: **Settings** > **AI** > **Active AI**
- Backtick formatting (`` `Settings > AI` ``), full bold wrapping (`**Settings > AI**`), italic, and bare formats are flagged
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
- **Case mismatches**: e.g. `Settings > ai` → `Settings > AI`
- **Non-canonical UI path formats**: backtick, italic, bare → per-segment bold
- **Backtick UI elements**: e.g. Click `Save` → Click **Save**
- Only path case fixes with confidence ≥ 0.9 are applied; format fixes are always applied

Fixes that require manual review (e.g. renamed sections, removed features) are reported but not auto-fixed.

## Slack Notifications

Slack notifications are designed for scheduled/automated runs, not ad-hoc usage. When running the skill manually (e.g., during a PR review or docs update), you can review results directly in the terminal output.

### Current behavior

The `--slack-notify` flag posts a summary to the configured Slack channel when unfixed issues remain after a run. If the scan is clean (0 issues), no notification is sent.

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

1. Configure the environment with the docs repo
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
