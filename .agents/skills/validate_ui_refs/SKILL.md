---
name: validate_ui_refs
description: Scan Warp Astro Starlight documentation for UI menu paths and Command Palette command names, then validate them against the public warp client codebase for accuracy. Catch and surface outdated steps automatically.
---

# Validate UI References

This skill scans Warp's Astro Starlight documentation for references to UI paths (e.g. `Settings > AI > Active AI`) and Command Palette command names (e.g. "Open Theme Picker"), then validates them against a snapshot of known-valid paths extracted from the public warp client repo ([warpdotdev/warp](https://github.com/warpdotdev/warp)).

## Running the Check

From the docs repo root:

```bash
python3 .agents/skills/validate_ui_refs/validate_ui_refs.py --all
```

### Options

- `--check-paths`: Only validate UI menu paths (Settings, File, View, Warp Drive)
- `--check-commands`: Only validate Command Palette names
- `--check-format`: Check that UI paths use the canonical bold format: **Settings** > **AI** > **Active AI**
- `--all`: Run all checks (default)
- `--fix`: Auto-fix high-confidence issues (e.g. case mismatches)
- `--create-pr`: Create a branch and PR with auto-fixes (requires `gh` CLI)
- `--slack-notify`: Post results to `#growth-docs` Slack channel when unfixed issues remain (requires `SLACK_BOT_TOKEN` env var; channel is hardcoded in the script)
- `--slack-channel ID`: Override the default Slack channel (`C09BVK0PL3Y`)
- `--self-test`: Run internal sanity checks against the current snapshot and exit (no warp checkout needed)
- `--include-changelog`: Include `changelog/` in the scan (excluded by default since it's a historical record)
- `--refresh-valid-paths`: Re-extract valid paths from the warp client repo and update `valid_paths.json`
- `--warp PATH`: Path to the public warp client repo (auto-detected as a sibling of the docs repo named `warp`, with `warp-internal` as a fallback, or the `WARP_REPO_PATH` env var). `--warp-internal-path` is a deprecated alias, and `WARP_INTERNAL_PATH` is still honored as a deprecated env var fallback.
- `--output FILE`: Save results to a JSON file

### Quick path-only check:

```bash
python3 .agents/skills/validate_ui_refs/validate_ui_refs.py --check-paths
```

### Full check with auto-fix and PR:

```bash
python3 .agents/skills/validate_ui_refs/validate_ui_refs.py --all --fix --create-pr
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

The `valid_paths.json` file is a static snapshot of valid UI paths. To update it from the latest warp client source:

```bash
python3 .agents/skills/validate_ui_refs/validate_ui_refs.py --refresh-valid-paths --warp /path/to/warp
```

This parses:
- `SettingsSection` enum and `Display` impl from `settings_view/mod.rs`
- `Category::new(...)` and `build_sub_header(...)` calls from settings page files
- `EditableBinding::new(...)` registrations from `terminal/view/init.rs` and `workspace/mod.rs`

The macOS menu bar and Warp Drive sections are maintained as manual lists in `valid_paths.json` since they change infrequently.

### Sub-section accuracy for shared-source-file pages

The extractor assigns sub-sections by reading `Category::new(...)` calls from each page's source file. When multiple Settings subpages share the same source file (e.g. `ai_page.rs` is used by Warp Agent, Profiles, Knowledge, and Third party CLI agents), all category calls in that file are assigned to all of those subpages — producing incorrect sub-section lists.

After running `--refresh-valid-paths`, manually verify the sub-sections for these pages against the live Warp Settings UI, or invoke the `verify-settings-subsections` skill (requires computer use) which automates this check. See `.agents/skills/verify-settings-subsections/SKILL.md`.

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

Slack notifications are designed for automated runs, not ad-hoc usage. When running the skill manually, review results directly in the terminal output.

The `--slack-notify` flag posts a summary to `#growth-docs` when unfixed issues remain after a run. If the scan is clean (0 issues), no notification is sent.

### Setup

For **automated runs**, the Slack token is provided by the Docs Agent Oz environment via `BUZZ_SLACK_TOKEN` — no GHA secret needed.

For **manual runs** from the command line, export a Slack bot token with `chat:write` scope before running:

```bash
export SLACK_BOT_TOKEN=xoxb-...
python3 .agents/skills/validate_ui_refs/validate_ui_refs.py --all --slack-notify
```

## Automated refresh

`valid_paths.json` is refreshed automatically via the `refresh-ui-paths` GitHub Actions workflow (`.github/workflows/refresh-ui-paths.yml`).

### How it works

1. A push to `master` in `warpdotdev/warp` that touches `app/src/settings_view/**` sends a `repository_dispatch` event (`settings-ui-changed`) to `warpdotdev/docs`.
2. The `refresh-ui-paths` GHA workflow fires and dispatches an Oz cloud agent to the Docs Agent environment (`K5KStCm5aYvhfBJb8cHol6`).
3. The cloud agent runs `--refresh-valid-paths` using the `warpdotdev/warp` checkout available in that environment.
4. If the snapshot changed, the agent runs `--all --fix --create-pr --slack-notify` to validate, auto-fix, open a PR, and post to `#growth-docs` if issues remain.
5. If the snapshot is unchanged, the agent exits with no-op.

### Secrets required

| Secret | Where | Status | Notes |
|---|---|---|---|
| `DOCS_REPOSITORY_DISPATCH_TOKEN` | `warpdotdev/warp` GHA secrets | ✅ Already provisioned | Sends the `settings-ui-changed` event to docs via `peter-evans/repository-dispatch` |
| `WARP_API_KEY` | `warpdotdev/docs` GHA secrets | ✅ Already provisioned | Used by the GHA workflow to dispatch the Oz cloud agent |
| `BUZZ_SLACK_TOKEN` | Docs Agent Oz environment | ✅ Already provisioned | Used by the cloud agent for `#growth-docs` Slack notifications (same bot that posts 404 reports, etc.) |

`warpdotdev/warp` (the OSS repo) is used for snapshot extraction since that's also where the trigger fires from. The Docs Agent Oz environment has `warpdotdev/warp` in its configured repos, or the agent will clone it if not present. No private repo access needed.

### Manual trigger

To trigger the workflow manually (e.g., if the PAT expired or a migration was missed):

1. In the `warpdotdev/docs` repo, go to **Actions** > **Refresh UI paths snapshot** > **Run workflow**.
2. Or run locally:

```bash
python3 .agents/skills/validate_ui_refs/validate_ui_refs.py \
  --refresh-valid-paths \
  --warp /path/to/warp
```

## Dependencies

- Python 3.7+
- `requests` (for Slack notifications): `pip3 install requests`
- `gh` CLI (for PR creation)
- A checkout of the public warp client repo ([warpdotdev/warp](https://github.com/warpdotdev/warp)) (only for `--refresh-valid-paths`)
