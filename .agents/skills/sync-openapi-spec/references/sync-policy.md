# Sync Policy

This document records what `developers/agent-api-openapi.yaml` keeps from `warp-server/public_api/openapi.yaml`, and why. The exclusion lists live in `scripts/sync_openapi.py` as `EXCLUDED_TAGS`, `EXCLUDED_PATHS`, `EXCLUDED_PATH_PREFIXES`, and `PRUNABLE_COMPONENT_SECTIONS`. Update both this document and the script when the policy changes.

## Relationship to warp-server's release automation

warp-server publishes the same file through `script/generate-public-openapi` and the `sync_public_openapi_to_docs` workflow, which runs at release-candidate time and opens a PR on the `automation/sync-agent-api-spec` branch. That pipeline is the authoritative publisher, and it filters with `public_api/public-openapi-filter.yaml` (`flagValues: [x-internal: true]`).

This skill is the manual fallback for the same job, so its output has to match that pipeline's public/private decisions. Prefer letting the release automation land routine spec updates. Reach for `--mode apply` only when the docs copy needs a correction the automation won't deliver in time, and re-read this policy before doing so.

## How filtering works

`scripts/sync_openapi.py` applies these rules, top-down:

1. Recursively drop every object marked `x-internal: true`, wherever it
   appears in the tree — a path operation, a query/path parameter, a
   schema property, a whole schema, a tag entry, and so on — not only
   top-level path operations.
2. Drop every tag listed in `EXCLUDED_TAGS`.
3. Drop every path whose tags are a subset of `EXCLUDED_TAGS`, plus every path listed explicitly in `EXCLUDED_PATHS` or matching a prefix in `EXCLUDED_PATH_PREFIXES`.
4. Keep top-level `openapi`, `info`, `servers`, and `components.securitySchemes` verbatim.
5. Keep only the entries in each `PRUNABLE_COMPONENT_SECTIONS` section (`schemas`, `parameters`, `examples`, `headers`, `requestBodies`, `responses`, `mediaTypes`) that are reachable from the surviving paths via `$ref` walking (recursive over `allOf`/`oneOf`/`anyOf`/`items`/`additionalProperties`/etc., and across sections — a shared response pulls in the schemas it references).
6. Recursively strip every key in `STRIP_FLAGS` from whatever survives
   steps 1-5, wherever it appears in the tree (operations, schemas,
   individual properties, parameters).

Rule 1 mirrors warp-server's own filter, so a surface the server team marks private stays private here without anyone having to maintain a matching allowlist entry.

## `x-internal` deletes the whole marked object, not just the flag (`_prune_internal`)

`x-internal: true` mirrors openapi-format's `flagValues` semantics in
warp-server's filter: the entire object bearing the marker is deleted, not
just the `x-internal` key on it. An earlier version of this script only
applied that rule to top-level path operations (`strip_internal_operations`)
and left every other marked object's `x-internal` key to be stripped later
by the `STRIP_FLAGS` pass (rule 6 above). Stripping the key without deleting
the object it was marking leaves the object itself — now unmarked — in the
published spec. This let several server-internal fields leak through: the
`factory_uid` and `automation_id` query parameters on `GET /agent/runs`, and
the `factory_uid`/`agent_type` properties on `CreateAgentRequest`,
`UpdateAgentRequest`, and `AgentResponse`.

`_prune_internal` now runs first, before any other rule, and walks the
entire source tree deleting every marked object outright: a schema property
under `properties`, an item in a `parameters` array, a whole schema in
`components.schemas`, and so on, in addition to the path operations rule 1
already covered. `STRIP_FLAGS` (rule 6) then only has to clean up the
`x-internal` key on anything that rule 1 doesn't fully own removing (there
is normally nothing left, since every `x-internal: true` object is deleted
outright) plus the other seven implementation-only extensions.

## Every shared component section is pruned, not just `schemas` (`PRUNABLE_COMPONENT_SECTIONS`)

`PRUNABLE_COMPONENT_SECTIONS` mirrors the `unusedComponents` list in
`warp-server/public_api/public-openapi-filter.yaml`. An earlier version of
this script pruned `components.schemas` and copied every other section
verbatim, so a shared component referenced only by an excluded path stayed
in the published copy: `FactoryAccessDenied`, a `components.responses` entry
used solely by the private `/factory/*` operations, shipped in the Scalar
reference as an orphan definition.

Sections outside the set are copied verbatim. Today that means
`securitySchemes`, which no operation `$ref`s — pruning it by reachability
would delete it.

## Implementation-only extensions are stripped everywhere (`STRIP_FLAGS`)

`STRIP_FLAGS` mirrors the `stripFlags` list in
`warp-server/public_api/public-openapi-filter.yaml` verbatim: `x-internal`,
`x-enum-varnames`, `x-go-type`, `x-go-type-import`,
`x-go-type-skip-optional-pointer`, `x-oapi-codegen-extra-tags`,
`x-stainless-deprecation-message`, and `x-stainless-naming`. These
extensions are useful for server/SDK code generation (oapi-codegen,
Stainless) but carry no meaning for a docs reader, so none of them may
reach the published Scalar reference.

An earlier version of this script only removed `x-internal` from
top-level operation objects (the key that decides whether to drop the
operation entirely). It never stripped the *other* six keys, and it never
walked into schemas, so implementation-only markers on component schemas
and their properties — `x-go-type-skip-optional-pointer` and
`x-stainless-deprecation-message` in particular — leaked into the
published copy verbatim. `_strip_flags` now walks the entire regenerated
tree after filtering and removes every `STRIP_FLAGS` key it finds,
regardless of nesting depth, matching `generate-public-openapi`'s own
post-generation check that no `x-*` key remains in warp-server's
published copy.

When warp-server adds a new entry to its `stripFlags` list, add the same
key to `STRIP_FLAGS` here so the two filters stay in lockstep.

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
