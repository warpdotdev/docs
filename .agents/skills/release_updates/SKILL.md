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

## Agent-doc quality contract

Before requesting review on a PR this skill opens, follow the shared v1
agent-doc quality contract in `.agents/references/doc-quality-policy.md`:
add the `## Documentation risk` block
(`.agents/skills/doc_quality_policy/finalize_pr_contract.py build`) and apply
the `warpy-factory` label. Generated changelog/license/telemetry updates are
exempt from the compression word-budget rules but not from the risk/marker
contract — classify them per the low-risk allowlist (they are typically `low`
when the source-verification step passed).

## Environment requirements (Oz cloud)

### Required

- **Repo**: docs repo (this repo) containing the `release_updates` skill.
- **Runtime**: glibc-based Linux image (Debian/Ubuntu-style image recommended).
- **Commands**: `python3`, `git`.
- **Network access**: `releases.warp.dev` (channel versions fallback) and
  `app.warp.dev` (Warp AppImage download).

### Required for PR mode

- **Command**: `gh` CLI
- **Auth**: `gh auth status` must be healthy in the run environment.
- **GitHub repo write access** for branch push + PR create/update.

### Required for Slack PR notification

- `DOCS_SLACK_BOT_TOKEN` environment variable (Oz team secret — add to the docs agent environment).

### Recommended

- Local checkout of `warpdotdev/channel-versions` so changelog updates read local
  `channel_versions.json` instead of URL fallback.

## Bootstrap/check the environment

Use this helper script before running release updates:

```bash
python3 .agents/skills/release_updates/scripts/setup_environment.py \
  --docs-repo /docs \
  --clone-channel-versions-if-missing \
  --require-pr-flow
```

If you also want automatic reviewer assignment checks:

```bash
python3 .agents/skills/release_updates/scripts/setup_environment.py \
  --docs-repo /docs \
  --clone-channel-versions-if-missing \
  --require-pr-flow \
  --require-oncall-reviewer
```

## Scripts

All scripts are in `.agents/skills/release_updates/scripts/`:
- `setup_environment.py` - Validate/prepare repos, CLI auth, and reviewer
  assignment prerequisites before release runs
- `resolve_oncall_reviewers.py` - Resolve primary/secondary Grafana on-call
  users to GitHub reviewers
- `update_warp_app.py` - Download latest stable + preview Linux AppImages and
  build a manifest for downstream tasks. On Linux, it preflights
  `libasound.so.2` before telemetry usage.
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

On Linux/Oz, let `warp_app_update` auto-install a missing ALSA runtime package:

```bash
python3 .agents/skills/release_updates/scripts/run_release_updates.py \
  --tasks warp_app_update \
  --auto-install-missing-dependency
```

If your environment already guarantees dependencies, you can skip the check:

```bash
python3 .agents/skills/release_updates/scripts/run_release_updates.py \
  --tasks warp_app_update \
  --skip-dependency-preflight
```

Dry run:

```bash
python3 .agents/skills/release_updates/scripts/run_release_updates.py --dry-run
```

### Create or update a PR at the end

`run_release_updates.py` can commit generated changes, push the branch, and
create/update a PR automatically:

```bash
python3 .agents/skills/release_updates/scripts/run_release_updates.py \
  --create-pr \
  --pr-base main
```

You can customize commit/PR metadata:

```bash
python3 .agents/skills/release_updates/scripts/run_release_updates.py \
  --create-pr \
  --commit-message "docs: weekly release updates" \
  --pr-title "docs: weekly release updates" \
  --pr-body-file /tmp/release-pr-body.md
```

### Post Slack notification after creating a PR

After the PR is created, post a notification to the `#oncall-client` Slack channel (`C06MT1NRBFV`):

```python
import json, os, subprocess, sys, urllib.request

# Capture the URL of the PR you just created.
# If no PR exists (no-op run with no docs changes), skip silently.
try:
    pr_url = subprocess.check_output(
        ['gh', 'pr', 'view', '--json', 'url', '--jq', '.url'],
        text=True, stderr=subprocess.DEVNULL
    ).strip()
except subprocess.CalledProcessError:
    print('No PR found — skipping Slack notification (no-op run)')
    sys.exit(0)

token = os.environ.get('DOCS_SLACK_BOT_TOKEN')
channel = 'C06MT1NRBFV'  # #oncall-client
if not token:
    print('DOCS_SLACK_BOT_TOKEN not set — skipping Slack notification')
else:
    # Resolve the oncall-client-primary and oncall-client-secondary user group IDs
    req = urllib.request.Request(
        'https://slack.com/api/usergroups.list',
        headers={'Authorization': f'Bearer {token}'}
    )
    with urllib.request.urlopen(req) as resp:
        groups = json.loads(resp.read()).get('usergroups', [])
    primary_id = next((g['id'] for g in groups if g.get('handle') == 'oncall-client-primary'), None)
    secondary_id = next((g['id'] for g in groups if g.get('handle') == 'oncall-client-secondary'), None)
    primary = f'<!subteam^{primary_id}|oncall-client-primary>' if primary_id else '@oncall-client-primary'
    secondary = f'<!subteam^{secondary_id}|oncall-client-secondary>' if secondary_id else '@oncall-client-secondary'

    message = f':books: New release docs PR ready for review\n{pr_url}\n{primary} {secondary} please take a look when you get a chance.'
    body = json.dumps({'channel': channel, 'text': message, 'mrkdwn': True}).encode()
    req = urllib.request.Request(
        'https://slack.com/api/chat.postMessage',
        data=body,
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    if not result.get('ok'):
        print(f'Slack error: {result.get("error")}', file=sys.stderr)
    else:
        print(f'Slack notification sent to {channel}')
```

The GitHub Actions workflow handles assigning the last human reviewer from recent docs PRs — the agent does not need to assign reviewers.

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

