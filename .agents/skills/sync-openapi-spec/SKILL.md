---
name: sync-openapi-spec
description: >-
  Sync the public Oz Agent API OpenAPI spec from warp-server into the docs
  repo, regenerating `developers/agent-api-openapi.yaml` (the file that
  powers the Scalar API reference at `docs.warp.dev/api`). Use when the
  warp-server public API has changed, when the Scalar reference looks
  stale, or on a scheduled cadence to keep the public API docs aligned
  with the canonical spec.
---

# Sync OpenAPI Spec

Keep `developers/agent-api-openapi.yaml` in sync with the canonical spec at `warp-server/public_api/openapi.yaml`.

**Direction:** warp-server → docs. The server spec is the source of truth. The docs file is a curated subset (drops `memory_stores`/`harness-support` and a handful of internal `agent` paths) that Scalar renders on `docs.warp.dev/api`.

## Repos

This skill requires two repos in the agent's environment:

- `warpdotdev/warp-server` — source of truth (`public_api/openapi.yaml`)
- `warpdotdev/docs` — Scalar-facing copy (`developers/agent-api-openapi.yaml`)

## Prerequisites

- Both repos checked out, with `warp-server` reachable from the docs repo (default assumption: sibling directories — `../warp-server/public_api/openapi.yaml`)
- Python 3 with `pyyaml` installed (`pip install pyyaml` or `pip install --break-system-packages pyyaml` in managed environments)
- `gh` CLI authenticated against `warpdotdev/docs`

## Workflow

### Step 1: Self-test

Run the script's self-test first to confirm `pyyaml` is available and the transform logic still passes:

```bash
python3 .agents/skills/sync-openapi-spec/scripts/sync_openapi.py --mode self-test
```

Expected output: `self-test: OK`. If this fails, fix the script before going further.

### Step 2: Diff source against target

```bash
python3 .agents/skills/sync-openapi-spec/scripts/sync_openapi.py \
  --mode diff \
  --source ../warp-server/public_api/openapi.yaml \
  --target developers/agent-api-openapi.yaml
```

The script prints structural drift grouped into:
- Paths added/removed/modified relative to the expected docs subset
- Component schemas added/removed/modified
- Top-level changes (`openapi`, `info`, `servers`)
- Unclassified tags or paths (anything not covered by `EXCLUDED_TAGS` or the `agent`/`schedules` allowlist)

If the script reports `In sync. No changes needed.`, stop here.

### Step 3: Triage unclassified items

Any line prefixed with `!` flags a tag or path the policy doesn't recognize. Do NOT auto-include or auto-drop these. For each one:
1. Read the corresponding handler in `warp-server/router/handlers/public_api/` to confirm whether the endpoint is intended to be public.
2. If the endpoint is public-facing, leave the policy alone — the script will include it on the next `apply`.
3. If the endpoint should remain hidden, extend `EXCLUDED_TAGS` or `EXCLUDED_PATHS` in `scripts/sync_openapi.py` and update `references/sync-policy.md` to record the rationale.
4. Re-run `--mode diff` until no `!` lines remain.

### Step 4: Apply the regenerated subset

```bash
python3 .agents/skills/sync-openapi-spec/scripts/sync_openapi.py \
  --mode apply \
  --source ../warp-server/public_api/openapi.yaml \
  --target developers/agent-api-openapi.yaml
```

This rewrites `developers/agent-api-openapi.yaml` with the regenerated subset.

### Step 5: Validate the regenerated spec

```bash
# YAML parses
python3 -c "import yaml; yaml.safe_load(open('developers/agent-api-openapi.yaml'))"

# Astro + Scalar boot succeed (catches dangling $refs, malformed paths)
npm run build
```

Optional, recommended when many schemas changed:
```bash
npx @redocly/cli lint developers/agent-api-openapi.yaml
```

If `npm run build` fails, inspect the build error, fix the underlying spec issue (most often a `$ref` to a schema that the script pruned because nothing public references it), and re-run.

### Step 6: Commit and open a PR

```bash
git checkout -b sync-openapi-spec/YYYY-MM-DD
git add developers/agent-api-openapi.yaml
git commit -m "docs: sync agent-api-openapi.yaml from warp-server

Co-Authored-By: Oz <oz-agent@warp.dev>"
git push origin sync-openapi-spec/YYYY-MM-DD
```

Open a draft PR with:
- **Title:** `docs: sync agent-api-openapi.yaml from warp-server`
- **Body:** include the full output from Step 2 (paths/schemas added/removed/modified) so reviewers can see exactly what changed and why.
- **Labels:** `documentation`

Use `report_pr` to surface the PR link.

### Step 7: Report

Summarize:
- Source commit SHA used (capture with `cd ../warp-server && git rev-parse HEAD`)
- Number of paths added / removed / modified in the regenerated subset
- Number of schemas added / removed / modified
- Any items flagged for triage and how they were resolved
- Or confirm `In sync. No changes needed.`

## Sync policy

The policy is encoded in `scripts/sync_openapi.py` as `EXCLUDED_TAGS` and `EXCLUDED_PATHS`. See `references/sync-policy.md` for the rationale behind each entry and the rules for adding new ones.

## Schedule

Run on demand whenever `warp-server/public_api/openapi.yaml` has changed materially since the last docs sync, or on a weekly cadence as a safety net.

## Troubleshooting

### `ModuleNotFoundError: No module named 'yaml'`
Install pyyaml: `pip install pyyaml`. On Debian-based images with externally managed Python, use `pip install --break-system-packages pyyaml`.

### `error: source spec not found at ...`
The `warp-server` repo isn't where the script expected. Pass `--source /absolute/path/to/warp-server/public_api/openapi.yaml`.

### `npm run build` fails after `--mode apply` with a missing-schema error
The script's `$ref` walker missed a transitive reference. Inspect the failing `$ref`, confirm the schema exists in the source spec, and check whether the path holding the reference was supposed to be kept. If the path is genuinely public, the schema should follow automatically — file a bug against the script (the walker should be transitive over `allOf`/`oneOf`/`anyOf`/`items`/`additionalProperties`).

### Diff shows changes that aren't in the source spec
Make sure `../warp-server` is on the branch you intended to compare against (usually `develop`). Run `cd ../warp-server && git status -sb && git --no-pager log -1` to confirm.

## References

- `scripts/sync_openapi.py` — the diff/apply tool
- `references/sync-policy.md` — exclusion policy and how to extend it
- `../warp-server/.agents/skills/update-open-api-spec/SKILL.md` — server-side workflow for editing the canonical spec
- `../../../src/pages/api.astro` — how the docs site loads the YAML into Scalar
