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

## Agent-doc quality contract

The PR this skill opens or updates follows the shared v1 agent-doc quality
contract in `.agents/references/doc-quality-policy.md`: apply the
`warpy-factory` label and add the `## Documentation risk` block
(`.agents/skills/doc_quality_policy/finalize_pr_contract.py build`). A
regenerated spec sync is `engineering-review-required` (changes API behavior
claims) unless the diff is provably a mechanical passthrough of the source
spec with no manual edits.

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

This rewrites `developers/agent-api-openapi.yaml` with the regenerated subset. Apply mode validates every `$ref` in the output before writing the file: if any reference is unresolved, the script exits with code 3 and refuses to write. On success it prints `All $refs resolve in the regenerated spec.`

### Step 5: Validate the regenerated spec

Apply mode already catches unresolved `$ref`s (see Step 4). Run these as belt-and-braces integration checks:

```bash
# Astro picks up the new YAML and parses it through Scalar's runtime.
npm run build
```

Optional, recommended when many schemas changed (full OpenAPI lint):
```bash
npx @redocly/cli lint developers/agent-api-openapi.yaml
```

If `npm run build` fails, the most common cause is a malformed path or missing `description` field. Schema-ref breakage is already prevented by Step 4's validator.

### Step 6: Commit and open a PR

This skill maintains **one** long-lived sync PR rather than one per run — see "One standing PR per automation" in `.agents/references/skill-authoring-guidelines.md`. A dated branch per run would produce multiple open PRs that all rewrite the same generated YAML file and conflict with each other.

```bash
# Is there already an open OpenAPI sync PR?
gh pr list --repo warpdotdev/docs --state open \
  --search 'sync agent-api-openapi.yaml from warp-server in:title' \
  --json number,headRefName

git fetch origin
# If the PR exists, continue on its branch and rebase; otherwise create it from main.
git checkout sync-openapi-spec 2>/dev/null || git checkout -b sync-openapi-spec origin/main
git rebase origin/main
```

Re-run `--mode apply` after the rebase so the regenerated subset reflects the latest `main`, then commit:

```bash
git add developers/agent-api-openapi.yaml
git commit -m "docs: sync agent-api-openapi.yaml from warp-server

Co-Authored-By: Oz <oz-agent@warp.dev>"
git push origin sync-openapi-spec
```

If a PR already exists for this branch, the push updates it — do not open a second one. Replace the diff summary in the existing body with the current run's output (this spec is regenerated wholesale each run, so the latest diff supersedes rather than accumulates) and note the date of the refresh. Re-run `check_pr_body.py` after editing.

If no PR exists, open a draft one. Write the body to a file before creating the PR — the diff output from Step 2 can be long and is prone to repetition-loop degeneration when passed inline:

```bash
cat > /tmp/sync-openapi-pr-body.md << 'EOF'
[Paste the full output from Step 2 here: paths/schemas added/removed/modified]

Co-Authored-By: Oz <oz-agent@warp.dev>
EOF

python3 .agents/skills/create_pr/check_pr_body.py /tmp/sync-openapi-pr-body.md
gh pr create --draft \
  --title "docs: sync agent-api-openapi.yaml from warp-server" \
  --label documentation \
  --body-file /tmp/sync-openapi-pr-body.md
```

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

### `--mode apply` exits with code 3 and "unresolved $refs"
Apply mode refuses to write the target if any `$ref` in the regenerated spec doesn't resolve to a defined component. The script's recursive `$ref` walker is supposed to keep transitive references (`allOf`/`oneOf`/`anyOf`/`items`/`additionalProperties`/etc.) reachable, so this means either:
- The source spec itself has a dangling reference (fix it in `warp-server`), or
- The walker is missing a reference shape (file a bug against the script).

The error output lists the offending JSON pointer paths so you can locate the reference quickly. Apply will not overwrite `developers/agent-api-openapi.yaml` while this fails.

### Diff shows changes that aren't in the source spec
Make sure `../warp-server` is on the branch you intended to compare against (usually `develop`). Run `cd ../warp-server && git status -sb && git --no-pager log -1` to confirm.

## References

- `scripts/sync_openapi.py` — the diff/apply tool
- `references/sync-policy.md` — exclusion policy and how to extend it
- `../warp-server/.agents/skills/update-open-api-spec/SKILL.md` — server-side workflow for editing the canonical spec
- `../../../src/pages/api.astro` — how the docs site loads the YAML into Scalar
