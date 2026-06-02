---
name: release_updates
description: >-
  Run weekly release docs updates with standalone scripts for changelog,
  licenses, and telemetry, plus Linux/Oz Warp artifact preparation. Defaults to
  running all tasks in order, and supports running only selected tasks.
---

# Release updates

Use this skill to update docs for weekly releases.

The scripts are designed for Oz cloud runs (Linux) and local testing.
They support the following:

- docs repo checkouts in different locations
  (`/docs`, sibling repo, current repo)
- optional channel-versions repo checkouts
  (`/channel-versions`, sibling repo)
- running one task or all tasks in the required order

## Scripts

All scripts are in `.agents/skills/release_updates/scripts/`:

- `update_warp_app.py` - Download latest stable + preview Linux AppImages and
  build a manifest for downstream tasks
- `update_changelog.py` - Incrementally update
  `src/content/docs/changelog/{year}.mdx` from channel versions
- `update_licenses.py` - Regenerate
  `src/content/docs/support-and-community/community/open-source-licenses.mdx`
- `update_telemetry.py` - Regenerate
  `src/content/docs/support-and-community/privacy-and-security/privacy.mdx`
  telemetry table
- `run_release_updates.py` - Orchestrates selected tasks (defaults to all, in
  order)

## Default workflow (all tasks, ordered)

```bash
python3 .agents/skills/release_updates/scripts/run_release_updates.py
```

Default order:

1. `warp_app_update`
2. `changelog`
3. `licenses`
4. `telemetry`

## Run only selected tasks

Changelog-only (useful while rolling out incrementally):

```bash
python3 .agents/skills/release_updates/scripts/run_release_updates.py \
  --tasks changelog
```

Specific subset:

```bash
python3 .agents/skills/release_updates/scripts/run_release_updates.py \
  --tasks warp_app_update changelog
```

## Useful options

### Local testing

On non-Linux machines, skip AppImage extraction:

```bash
python3 .agents/skills/release_updates/scripts/run_release_updates.py \
  --skip-warp-app-extract \
  --tasks changelog
```

Dry run:

```bash
python3 .agents/skills/release_updates/scripts/run_release_updates.py --dry-run
```

### Explicit repo paths

If auto-detection is not enough:

```bash
python3 .agents/skills/release_updates/scripts/run_release_updates.py \
  --docs-repo /docs \
  --channel-versions-repo /channel-versions
```

Or point directly to a specific channel versions file:

```bash
python3 .agents/skills/release_updates/scripts/run_release_updates.py \
  --channel-versions-file /channel-versions/channel_versions.json
```

## Artifact handoff between scripts

`update_warp_app.py` writes a manifest at:

`/tmp/release-updates/warp_artifacts.json` (by default)

`update_licenses.py` and `update_telemetry.py` read that manifest unless
explicit input paths are provided.

