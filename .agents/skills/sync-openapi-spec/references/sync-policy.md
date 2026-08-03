# Sync Policy

This document records what `developers/agent-api-openapi.yaml` keeps from `warp-server/public_api/openapi.yaml`, and why. The exclusion lists live in `scripts/sync_openapi.py` as `EXCLUDED_TAGS`, `EXCLUDED_PATHS`, and `EXCLUDED_PATH_PREFIXES`. Update both this document and the script when the policy changes.

## Relationship to warp-server's release automation

warp-server publishes the same file through `script/generate-public-openapi` and the `sync_public_openapi_to_docs` workflow, which runs at release-candidate time and opens a PR on the `automation/sync-agent-api-spec` branch. That pipeline is the authoritative publisher, and it filters with `public_api/public-openapi-filter.yaml` (`flagValues: [x-internal: true]`).

This skill is the manual fallback for the same job, so its output has to match that pipeline's public/private decisions. Prefer letting the release automation land routine spec updates. Reach for `--mode apply` only when the docs copy needs a correction the automation won't deliver in time, and re-read this policy before doing so.

## How filtering works

`scripts/sync_openapi.py` applies these rules, top-down:

1. Drop every operation marked `x-internal: true`, and drop a path entirely when every one of its operations is internal.
2. Drop every tag listed in `EXCLUDED_TAGS`.
3. Drop every path whose tags are a subset of `EXCLUDED_TAGS`, plus every path listed explicitly in `EXCLUDED_PATHS` or matching a prefix in `EXCLUDED_PATH_PREFIXES`.
4. Keep top-level `openapi`, `info`, `servers`, and `components.securitySchemes` verbatim.
5. Keep only the `components.schemas` entries that are reachable from the surviving paths via `$ref` walking (recursive over `allOf`/`oneOf`/`anyOf`/`items`/`additionalProperties`/etc.).

Rule 1 mirrors warp-server's own filter, so a surface the server team marks private stays private here without anyone having to maintain a matching allowlist entry.

## Excluded tags

### `memory_stores` and `memory`
These tags back Agent Memory, which is a research preview. The tag was renamed `memory_stores` → `memory` upstream, so both names are excluded: keeping only the old name silently reopened the surface after the rename. Remove them from `EXCLUDED_TAGS` when Agent Memory ships publicly.

### `harness-support`
The `/harness-support/*` endpoints form the worker-to-server contract used by Oz workers (transcripts, snapshots, finish-task signaling, etc.). They are not part of the public API contract — customers should not call them directly. Excluded permanently.

### `factory`
Oz Factory has not shipped publicly. Its `FactoryMcp` flag is dogfood and the `@warp/factory` front end is internal, so none of its endpoints belong in the public reference. Remove this tag when Factory goes GA.

## Excluded paths (within otherwise-public tags)

These four `agent`-tag paths are excluded individually because the `agent` tag itself remains public:

- `/agent/runs/{runId}/handoff/attachments` — handoff plumbing tied to local-to-cloud session handoff.
- `/agent/handoff/upload-snapshot` — handoff plumbing (snapshot upload from a local worker).
- `/agent/conversations/{conversation_id}/fork` — conversation-forking primitive used by the harness, not stable public API.
- `/agent/conversations/{conversationId}/redirect` — internal redirect endpoint.

If any of these become stable public surfaces, remove them from `EXCLUDED_PATHS` and update this list.

## Excluded path prefixes

`EXCLUDED_PATH_PREFIXES` drops a path by prefix regardless of how its operations are tagged. Today it holds a single entry, `/factory`, because some Factory operations are tagged `agent` upstream — `GET /factory/scorers/{scorer_id}/results` is one — so a tags-only rule leaks them into the public reference. Use a prefix only when a whole URL namespace is private; prefer a tag or an explicit path everywhere else.

## `x-internal` operations are dropped

Operations marked `x-internal: true` are removed, and a path loses its entry when all of its operations are internal. This covers the `/agent/messages/*` and `/agent/events/*` orchestration-messaging operations, `/agent/runs/{runId}/client-events`, `/agent/conversations/{conversation_id}/rename`, and `/agent/sessions/{sessionUuid}/redirect`.

An earlier version of this policy kept those operations verbatim so the regenerated file matched the docs copy already on disk. That made this script disagree with warp-server's release filter, which strips them, and meant every newly marked-internal operation would be republished here. Matching the upstream marker is the safer default: it can only ever remove surfaces, never add one.

## Adding a new exclusion

Use the script's `_unknown_classifications` warnings as the trigger. When the diff flags a new tag or path with `!`:
1. Read the corresponding handler in `warp-server/router/handlers/public_api/` to determine intent.
2. If the endpoint should be hidden:
   - Prefer asking the server team to mark the operation `x-internal: true` upstream, which hides it from both publishers at once.
   - For an entire new tag, add the tag name to `EXCLUDED_TAGS` in `scripts/sync_openapi.py`.
   - For a single path, add it to `EXCLUDED_PATHS`; for a whole private URL namespace, add a prefix to `EXCLUDED_PATH_PREFIXES`.
3. Add a short rationale to this document under "Excluded tags" or "Excluded paths."
4. Re-run `--mode diff` to confirm there are no remaining `!` warnings.
5. Then run `--mode apply` and proceed with the normal PR flow.

## Removing an exclusion

When an internal endpoint becomes a stable public surface:
1. Remove it from `EXCLUDED_TAGS` or `EXCLUDED_PATHS`.
2. Remove its bullet from this document.
3. Run `--mode apply`. The path and its referenced schemas will be added to the docs file automatically.
4. Open the PR with the standard sync flow.
