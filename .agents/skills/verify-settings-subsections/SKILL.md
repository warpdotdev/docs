---
name: verify-settings-subsections
description: Verify that sub_sections in valid_paths.json match the actual section headers visible in the live Warp Settings UI. Use when a validate_ui_refs snapshot update is proposed and you want to confirm sub-section accuracy before merging. Requires computer use.
---

# Verify Settings Sub-sections

This skill uses computer use to navigate the live Warp Settings UI and verify that the `sub_sections` entries in `valid_paths.json` accurately reflect what is actually visible as section headers in each Settings page.

## When to use

Run this skill after `--refresh-valid-paths` produces a new snapshot, before creating a PR. It catches cases where the extractor assigns incorrect sub-sections because multiple Settings subpages share the same Rust source file (`ai_page.rs`, `code_page.rs`, etc.), making code-only extraction unreliable.

## Background

The `validate_ui_refs.py` extractor generates sub-section lists from `Category::new("Name", ...)` calls in Rust source files. When multiple Settings subpages are rendered from the same source file, all `Category::new()` calls are assigned to all of those subpages — even though each subpage only shows a subset. This produces false positives: paths like `Settings > Agents > Profiles > AWS Bedrock` would pass validation even though "AWS Bedrock" is not a section on the Profiles page.

## Affected pages (shared source files as of April 2026)

All of these subpages use `ai_page.rs`:
- **Warp Agent** (also known as **Oz** — both names are valid aliases)
- **Profiles**
- **Knowledge**
- **Third party CLI agents**

Both of these subpages use `code_page.rs`:
- **Indexing and projects**
- **Editor and Code Review**

## Procedure

For each affected Settings page listed above:

1. **Open Warp Settings** on the machine running this agent. Navigate to **Settings** > **Agents** > [Subpage].

2. **Screenshot the full page** (scroll if needed to capture all content). Use the computer use tool to take a screenshot.

3. **Extract visible section headers** — these are the bold heading-level labels visible in the page body (e.g., "Active AI", "Input", "Voice"). Do **not** include:
   - Individual toggle names or setting labels
   - Sidebar navigation items
   - Page titles

4. **Compare against `valid_paths.json`**. Open `.agents/skills/validate_ui_refs/valid_paths.json` and check the `sub_sections` array for that page.

5. **Report any mismatch** — list sections in the snapshot that are absent from the UI, and sections visible in the UI that are missing from the snapshot.

6. **Propose corrections** — if corrections are needed, update `valid_paths.json` directly and include the changes in the snapshot update PR.

## Expected current state (as of July 2026)

After manual verification and correction, the correct sub-sections are:

```json
"Warp Agent": ["Active AI", "Input", "Voice", "Cloud Handoff", "Custom Inference", "Custom Routers", "Agent Attribution", "Other", "Experimental"],
"Oz":         ["Active AI", "Input", "Voice", "Cloud Handoff", "Custom Inference", "Custom Routers", "Agent Attribution", "Other", "Experimental"],
"Profiles":   [],
"Knowledge":  [],
"Third party CLI agents": []
```

Verify these match what you see. If the UI has changed, update accordingly.

## Integration with the automated workflow

This skill is invoked as an optional step in the `refresh-ui-paths` workflow after snapshot regeneration. The cloud agent that runs `validate_ui_refs --refresh-valid-paths` should:

1. Run `--refresh-valid-paths` to regenerate the snapshot
2. Check if any shared-source-file subpage now has sub-sections that differ from the last verified values
3. If they do, invoke this skill (requires computer use) to verify against the live UI before opening a PR
4. If they don't, proceed directly to `--all --fix --create-pr`

The shared-source-file pages that require verification are those with `source_file` pointing to `ai_page.rs` or `code_page.rs` in `valid_paths.json`.
