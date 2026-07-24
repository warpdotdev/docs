*Spec: Docs OpenAPI — expose precise setup-command operations (REMOTE-1063, docs repo)*

== PRODUCT ==
*Summary:* After the warp-server canonical public API adds precise setup-command
update operations for cloud environments, the generated docs OpenAPI at
`developers/agent-api-openapi.yaml` must mirror those operations — paths,
parameters, request/response shapes, and index semantics — so the Scalar API
reference at `docs.warp.dev/api` and the raw `docs.warp.dev/openapi.json`
document them. This spec covers *only* the docs repo's generated OpenAPI file
and the sync mechanics that keep it aligned to the warp-server canonical
contract; the warp-server spec owns the canonical contract shape and is the
source of truth.

*Key design choices:*
1. **Mirror, don't hand-author.** `developers/agent-api-openapi.yaml` is a
   generated curated subset of `warp-server/public_api/openapi.yaml`
   (`sync-openapi-spec` skill → `scripts/sync_openapi.py`). The docs change is
   produced by running the existing sync tool against an updated canonical
   source, not by editing the docs YAML by hand. This keeps the two specs
   structurally identical for the included surface.
2. **REST-only public contract.** The existing public environment surface is
   REST (`GET /agent/environments`); the OpenAPI spec and the Scalar reference
   are REST. The new precise setup-command operations are REST endpoints
   committed to `warp-server/public_api/openapi.yaml` and flow through the sync
   to docs. GraphQL remains internal and is not part of the documented public
   contract (see Design alternatives).
3. **Index semantics live in the contract, not just the CLI.** The documented
   operations carry zero-based index parameters with explicit append-at-length
   and out-of-range rules, so the CLI, server, and docs all agree on the same
   shape (the cross-repo alignment requirement).

*Behavior* (numbered, testable invariants from the docs consumer's view):
1. The Scalar reference at `docs.warp.dev/api` lists the new precise
   setup-command operation(s) for cloud environments alongside the existing
   `GET /agent/environments` operation, with HTTP method, path, parameters,
   request body, and response codes rendered.
2. The documented surface exposes the setup-commands sub-resource as
multiple verbs under `/agent/environments/{uid}/setup-commands`: `GET` (list),
`PUT` (replace / clear-and-rebuild the whole list), `POST` (add — append when
index omitted, insert at `0..=len`), `PATCH /{index}` (edit one command by
index without resending the rest), `DELETE /{index}` (remove one by index),
and `DELETE` (clear all). The index-based ops (`POST` insert,
`PATCH /{index}`, `DELETE /{index}`) address a single command by index
without the caller resending the unchanged full list.
3. Index parameters are documented as **zero-based**; a `POST` insert at
`index == length` appends (preserves order); an edit (`PATCH /{index}`) or
remove (`DELETE /{index}`) whose index is out of range (`[0, length)`) is
documented as a `404`; a malformed/bad index (e.g. non-integer, negative) is
documented as a `400`.
4. Duplicate setup commands (same text, different positions) are addressable by
   index in the documented operations; the docs do not require command text to
   be unique.
5. The existing `GET /agent/environments` operation and the
   `CloudEnvironmentConfig` schema (including its `setup_commands` array field)
   remain present and unchanged in the regenerated docs file — the change is
   purely additive for the public surface.
6. `docs.warp.dev/openapi.json` (served from the same source via
   `src/pages/api.astro`) reflects the new operations after deploy.

== TECH ==
*Context:* how the docs OpenAPI surface works today (commit-pinned):
- `developers/agent-api-openapi.yaml:1155` (@ `aca5ecce`) — the only environment
  path today: `GET /agent/environments` (`operationId: listEnvironments`, tag
  `agent`, `bearerAuth`, `sort_by` query param). Mirrors the canonical.
- `developers/agent-api-openapi.yaml:2908` — `CloudEnvironmentConfig` schema;
  `setup_commands` at `:2927` is `array of string` ("Shell commands to run
  during environment setup"). No setup-command CRUD operations exist.
- `src/pages/api.astro:16` reads `developers/agent-api-openapi.yaml` and feeds
  Scalar; `:213` links the raw `openapi.json`. So one YAML file powers both the
  rendered reference and the JSON download.
- Canonical source of truth: `warp-server/public_api/openapi.yaml:3980`
  (`GET /agent/environments`) and `:7774` (`CloudEnvironmentConfig`,
  `setup_commands` at `:7793`) @ `21fbda3f`. The server REST handler
  `warp-server/router/handlers/public_api/agent_environments.go:48`
  (`RegisterAgentEnvironmentRoutes`) registers only the GET route today — no
  update/create/delete/setup-command handlers exist yet. GraphQL
  `warp-server/graphql/v2/cloud_environment.graphqls:49` exposes
  `setupCommands: [String!]` but is internal, not the documented public
  contract.
- Sync tool: `docs/.agents/skills/sync-openapi-spec/scripts/sync_openapi.py`
  (`EXCLUDED_TAGS` at `:44` = `{memory_stores, harness-support}`;
  `EXCLUDED_PATHS` at `:48`; `KNOWN_TAGS` at `:343` = `{agent, schedules}` ∪
  excluded). Policy doc: `references/sync-policy.md`. Direction is
  warp-server → docs; apply mode validates every `$ref` resolves before
  writing (exit 3 on failure).

*Design alternatives* (per decision point with more than one reasonable
approach):
- **REST vs GraphQL vs both for the public contract** — options:
  (a) *REST only* (chosen): matches the existing `GET /agent/environments`
  public surface, the OpenAPI/Scalar reference, and `docs.warp.dev/api`. The
  server already wraps a GraphQL resolver for listing but exposes REST
  publicly; adding REST precise-update ops keeps the documented contract
  consistent and reviewable in one spec. (b) *GraphQL only*: would require a
  new public GraphQL surface and a different docs rendering path; Scalar
  renders OpenAPI/REST, so this would not flow through the existing sync. (c)
  *Both*: doubles the documented surface and the cross-repo alignment cost for
  no user-facing benefit today. → REST only.
- **Where index semantics live** — options:
  (a) *In the contract* (chosen): the documented operations carry index
  parameters and explicit bounds, so CLI/server/docs agree on one shape (the
  brief's cross-repo requirement). (b) *Contract is full-replacement only
  (`PUT` the whole `setup_commands` list), CLI computes the final list*: simpler
  contract but moves index semantics out of the shared contract, so the three
  specs cannot "agree on the same index semantics" — rejected for this
  multi-repo task. → contract carries index semantics.
- **Endpoint shape** — **binding per warp-server's committed REST contract**
  (the docs file mirrors it verbatim via the sync): a multi-verb sub-resource
  under `/agent/environments/{uid}/setup-commands` (mounted at
  `/api/v1/agent/environments/{uid}/setup-commands`): `GET` (list), `PUT`
  (replace / clear-and-rebuild), `POST` (add — append when index omitted,
  insert at `0..=len`), `PATCH /{index}` (edit by index), `DELETE /{index}`
  (remove by index), `DELETE` (clear all). Alternatives weighed before
  warp-server committed: (a) a single `PATCH` with an ordered `operations`
  array body (insert/edit/remove/append/clear/replace) — fewer endpoints but a
  less standard REST shape and a compound request body; (b) a whole-config
  `PATCH /agent/environments/{uid}` with a setup-commands patch nested under
  config — broader blast radius implying a general environment update
  contract. warp-server chose the multi-verb sub-resource; the docs file
  mirrors that exact surface, so the validation criteria below check for those
  verbs and the `{uid}` path parameter.
- **New tag or reuse `agent`** — options:
  (a) *Reuse the `agent` tag* (proposed): the new operations flow through the
  sync automatically (`agent` ∈ `KNOWN_TAGS`, path not in `EXCLUDED_PATHS`) —
  no policy change needed. (b) *Introduce an `environments` tag*: would require
  extending `KNOWN_TAGS`/`EXCLUDED_TAGS` and `references/sync-policy.md` or the
  diff flags it with `!` for triage. → reuse `agent` unless the warp-server
  spec introduces a new tag, in which case the sync policy MUST be updated
  (criterion 2).

*Proposed changes* (docs repo):
1. **Regenerate** `developers/agent-api-openapi.yaml` by running
   `scripts/sync_openapi.py --mode apply --source <updated warp-server
   public_api/openapi.yaml> --target developers/agent-api-openapi.yaml` once
   the warp-server canonical lands the setup-commands sub-resource. The
   regenerated file adds the new paths — `/agent/environments/{uid}/setup-commands`
   and `/agent/environments/{uid}/setup-commands/{index}` — the per-verb
   operations (`GET`/`PUT`/`POST`/`PATCH`/`DELETE`), their request/response
   schemas (e.g. add/replace/edit request bodies and the list response), and
   the `Error`-referenced error responses — mirroring the canonical verbatim
   for the included surface.
2. **Sync policy** (only if needed): if the warp-server spec introduces a new
   tag (not `agent`/`schedules`) or a path that should stay hidden, update
   `EXCLUDED_TAGS`/`EXCLUDED_PATHS` in `scripts/sync_openapi.py` and record the
   rationale in `references/sync-policy.md`. If the new ops reuse the `agent`
   tag and are public, no policy change is required.
3. **No hand-edits** to the generated YAML outside the sync tool's output; the
   file remains a generated artifact so future syncs are clean.
4. **Sequencing note (for the foreman/implementation):** the docs sync
   `--mode apply` step requires a `warp-server/public_api/openapi.yaml` that
   already contains the new operations. The docs implementation child therefore
   runs the sync against the warp-server branch/commit that lands the contract
   (or waits until that contract is merged). The docs PR may land in two phases:
   (i) this spec file (+ any sync-policy update), (ii) the regenerated YAML
   once the canonical source is available. Both phases land on this same PR
   branch.

*Open questions resolved* (each ambiguity and how it was settled; the
warp-server spec is the source of truth for the exact contract, these are the
docs-side assumptions that keep all three specs aligned — surfaced in the
approval request for ben to confirm):
- **Index base: zero-based.** Settled from the JSON array model
  (`setup_commands: array of string`) and OpenAPI/JSON conventions; avoids
  off-by-one translation between the API and the underlying model. The CLI may
  display one-based indexes in help text, but the *contract* is zero-based and
  all three specs agree on zero-based. *Assumption to confirm:* ben may prefer
  one-based for CLI ergonomics — if so, the CLI maps one-based→zero-based at the
  edge and the contract stays zero-based.
- **Insert permits append-at-length: yes.** `POST` insert at `index == length`
  appends and preserves order; an insert `index > length` is out of range.
  Per warp-server's binding contract: edit/remove out of range → `404`; a bad
  (malformed/negative) index → `400`. Settled as standard list-insert
  semantics; supports `--insert-setup-command <len> <cmd>` as an append.
- **Duplicate-command addressing: by index.** Setup commands may legitimately
  repeat, so the precise ops address by index, not by text. The existing
  text-based `--remove-setup-command` CLI flag is preserved for compatibility
  and is translated client-side (find first text match → its index →
  `DELETE /{index}`); the public contract is index-based only. Settled from the
  ticket's "edit one setup command by index without resending" requirement.
- **Public contract: REST.** Settled from the existing REST public surface and
  the Scalar/OpenAPI docs pipeline; GraphQL stays internal. See Design
  alternatives.
- **Exact endpoint path/shape: binding per warp-server.** Multi-verb
  sub-resource under `/agent/environments/{uid}/setup-commands` (mounted at
  `/api/v1/...`): `GET` list, `PUT` replace/clear-and-rebuild, `POST` add
  (append when index omitted, insert at `0..=len`), `PATCH /{index}` edit,
  `DELETE /{index}` remove, `DELETE` clear. The docs file mirrors this exact
  surface verbatim via the sync; the validation criteria check for these verbs
  and the `{uid}` path parameter.

*Risks / blast radius:*
- The docs file is generated; a hand-edit would be overwritten on the next
  sync. Mitigation: only change it via `sync_openapi.py --mode apply`.
- If the warp-server contract introduces a new tag/path, the sync diff flags it
  `!` and the docs PR must update the sync policy or the build/sync is blocked.
  Mitigation: criterion 2 enforces zero `!` flags before merge.
- Cross-repo drift: if the docs file diverges from the canonical (e.g. stale
  schema names or index semantics), the Scalar reference would document a
  contract the server doesn't implement. Mitigation: criterion 10 enforces
  `--mode diff` shows the docs file equals the curated canonical subset.
- The docs sync depends on the warp-server contract landing first; the docs PR
  cannot be merged with a regenerated YAML until that source exists
  (criterion 1 runs against the updated canonical).

*Validation & verification criteria* (must ALL pass before merge of the docs
PR; criteria 1–4 run against a `warp-server/public_api/openapi.yaml` that
already contains the new setup-command operations):
1. `python3 .agents/skills/sync-openapi-spec/scripts/sync_openapi.py --mode apply --source ../warp-server/public_api/openapi.yaml --target developers/agent-api-openapi.yaml` regenerates the docs file containing the new setup-command operation(s) and exits 0 with "All $refs resolve in the regenerated spec." (every `$ref` resolves). - verifies behavior #1, #2.
2. `python3 .agents/skills/sync-openapi-spec/scripts/sync_openapi.py --mode diff --source ../warp-server/public_api/openapi.yaml --target developers/agent-api-openapi.yaml` reports **no `!` unclassified items**: the new operations either reuse the `agent` tag (no policy change) OR `EXCLUDED_TAGS`/`KNOWN_TAGS` in `scripts/sync_openapi.py` and `references/sync-policy.md` have been updated with a rationale for any new tag/path. - verifies the sync policy stays consistent.
3. The regenerated `developers/agent-api-openapi.yaml` contains the setup-commands sub-resource the warp-server canonical commits: paths `/agent/environments/{uid}/setup-commands` and `/agent/environments/{uid}/setup-commands/{index}`, with `GET` (list), `PUT` (replace/clear-and-rebuild), `POST` (add; append when index omitted, insert at `0..=len`), `PATCH /{index}` (edit by index), `DELETE /{index}` (remove by index), and `DELETE` (clear all) operations — each with `bearerAuth` security, the appropriate request body schema, and `200`/`201`/`204`/`400`/`401`/`403`/`404`/`500` responses (error responses `$ref` `#/components/schemas/Error`). - verifies behavior #1, #2; checked by grepping the regenerated YAML for the committed operationIds/paths and schema names.
4. The regenerated docs file documents the **zero-based** index semantics in the operation/schema `description` fields, matching the warp-server canonical verbatim: `POST` insert at `index == length` appends; edit (`PATCH /{index}`) / remove (`DELETE /{index}`) out of range → `404`; a bad (malformed/negative) index → `400`; duplicate command text allowed and addressed by index. - verifies behavior #3, #4; checked by reading the regenerated schema descriptions and confirming they equal the canonical's.
5. `npm run build` succeeds (Astro picks up the regenerated YAML and Scalar parses it at build time). - verifies behavior #1, #6; the docs repo's documented build check.
6. (Recommended when schemas changed) `npx @redocly/cli lint developers/agent-api-openapi.yaml` passes with no errors. - belt-and-braces OpenAPI lint.
7. No regressions to the existing public surface: the regenerated docs file still contains `GET /agent/environments` (`operationId: listEnvironments`) and the `CloudEnvironmentConfig` schema with its `setup_commands` array field, unchanged; `--mode diff` shows the new operations as **additions** only (no removals of existing public paths/schemas). - verifies behavior #5.
8. The docs PR records the warp-server source commit SHA used for the sync and the count of paths/schemas added/modified (per the sync-openapi-spec skill's reporting step). - traceability of the generated artifact to its source.
9. Cross-repo alignment: the docs sub-resource paths (`/agent/environments/{uid}/setup-commands` and `.../{index}`), the `{uid}` path parameter name, the per-verb operationIds, request/response schema `$ref` names, HTTP status codes (`404` out-of-range edit/remove, `400` bad index), and zero-based index semantics exactly match `warp-server/public_api/openapi.yaml`. - verifies the three specs agree on one contract; checked by `--mode diff` reporting the docs file equals the curated subset of the canonical (no docs-only divergence).
10. After deploy, `docs.warp.dev/api` (Scalar) and `docs.warp.dev/openapi.json` expose the new operations. For the PR itself, verify via the `npm run build` output that the new path is present in the built spec; live deploy verification is post-merge. - verifies behavior #1, #6.
