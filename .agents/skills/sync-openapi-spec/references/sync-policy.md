# Sync Policy

This document records what `developers/agent-api-openapi.yaml` keeps from `warp-server/public_api/openapi.yaml`, and why. The exclusion lists live in `scripts/sync_openapi.py` as `EXCLUDED_TAGS` and `EXCLUDED_PATHS`. Update both this document and the script when the policy changes.

## How filtering works

`scripts/sync_openapi.py` applies these rules, top-down:

1. Drop every tag listed in `EXCLUDED_TAGS`.
2. Drop every path whose tags are a subset of `EXCLUDED_TAGS`, plus every path listed explicitly in `EXCLUDED_PATHS`.
3. Strip any individual operation marked `x-internal: true` from surviving paths. A path whose every HTTP operation is marked internal is dropped entirely.
4. Keep top-level `openapi`, `info`, `servers`, and `components.securitySchemes` verbatim.
5. Keep only the `components.schemas` entries that are reachable from the surviving paths via `$ref` walking (recursive over `allOf`/`oneOf`/`anyOf`/`items`/`additionalProperties`/etc.).

## Excluded tags

### `memory_stores`
Memory stores are gated as `x-internal: true` server-side. They are not part of the public Oz Agent API surface today and are excluded from the docs reference until they ship publicly. If/when this tag goes public, remove it from `EXCLUDED_TAGS` and update this section.

### `harness-support`
The `/harness-support/*` endpoints form the worker-to-server contract used by Oz workers (transcripts, snapshots, finish-task signaling, etc.). They are not part of the public API contract — customers should not call them directly. Excluded permanently.

### `factory`
The `/factory/*` endpoints are the internal agent-orchestration API used by the factory pipeline (task management, Linear integrations, syncs, etc.). Not a public API surface; excluded until further notice.

### `memory`
The `/memory_stores` path is tagged `memory` in the server spec (renamed from the former `memory_stores` tag). Same rationale as `memory_stores` above: memory stores are gated and not a stable public API yet.

## Excluded paths (within otherwise-public tags)

These paths under otherwise-public tags are excluded individually:

- `/agent/runs/{runId}/handoff/attachments` — handoff plumbing tied to local-to-cloud session handoff.
- `/agent/handoff/upload-snapshot` — handoff plumbing (snapshot upload from a local worker).
- `/agent/conversations/{conversation_id}/fork` — conversation-forking primitive used by the harness, not stable public API.
- `/agent/conversations/{conversationId}/redirect` — internal redirect endpoint.
- `/factory/scorers` — factory-internal scorer creation endpoint; carries the `agent` tag but is not a public API surface.
- `/factory/scorers/{scorer_id}/results` — factory-internal scorer results endpoint; carries the `agent` tag but is not a public API surface.
- `/agent/sessions/{sessionUuid}/redirect` — session redirect plumbing (mirrors the excluded `/agent/conversations/{conversationId}/redirect`).
- `/agent/runs/{runId}/client-events` — internal telemetry endpoint for recording run client events; not a stable public API contract.

If any of these become stable public surfaces, remove them from `EXCLUDED_PATHS` and update this list.

## What the script filters that you might expect to be public

The script now strips individual operations marked `x-internal: true`, even when the operation lives under an otherwise-public path. This prevents internal inter-agent plumbing (the `/agent/messages/*` and `/agent/events/*` inter-agent messaging and event-polling operations, `/agent/conversations/{conversation_id}/rename`, etc.) from appearing in the public docs reference and `public/openapi.json`. These operations exist server-side but are not part of the stable customer-facing API contract. If an operation is promoted to public, remove its `x-internal: true` marker in `warp-server/public_api/openapi.yaml` and the next sync will include it automatically.

## Adding a new exclusion

Use the script's `_unknown_classifications` warnings as the trigger. When the diff flags a new tag or path with `!`:
1. Read the corresponding handler in `warp-server/router/handlers/public_api/` to determine intent.
2. If the endpoint should be hidden:
   - For an entire new tag, add the tag name to `EXCLUDED_TAGS` in `scripts/sync_openapi.py`.
   - For a single path, add it to `EXCLUDED_PATHS`.
3. Add a short rationale to this document under "Excluded tags" or "Excluded paths."
4. Re-run `--mode diff` to confirm there are no remaining `!` warnings.
5. Then run `--mode apply` and proceed with the normal PR flow.

## Removing an exclusion

When an internal endpoint becomes a stable public surface:
1. Remove it from `EXCLUDED_TAGS` or `EXCLUDED_PATHS`.
2. Remove its bullet from this document.
3. Run `--mode apply`. The path and its referenced schemas will be added to the docs file automatically.
4. Open the PR with the standard sync flow.
