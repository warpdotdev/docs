# Sync policy

`warp-server/public_api/openapi.yaml` owns the public API contract and its
descriptions. `developers/agent-api-openapi.yaml` is its generated public
export, rendered by Scalar at `docs.warp.dev/api`.

## One publisher

The release-candidate `sync_public_openapi_to_docs` workflow publishes through
`warp-server/script/generate-public-openapi`. The manual fallback invokes that
same script and copies its output verbatim after validating local `$ref`s.
It requires the server checkout and its pinned `openapi-format` dependency.
Use `--server-root` when the repositories are not siblings.

The generator accepts an output path followed by an optional input spec path.
Without the second argument it reads the canonical server spec. The fallback's
`--source` flag passes that second argument, so a historical source file can be
inspected without replacing the checkout's canonical spec.

## Public and internal surfaces

`public_api/public-openapi-filter.yaml` is the filtering policy:

- Drop objects explicitly marked `x-internal: true`, including operations,
  parameters, schema properties, schemas, and tag declarations.
- Strip the implementation-only extensions listed in `stripFlags`, including
  Go validation tags and Stainless naming annotations.
- Prune reusable components no longer reachable from public operations.

The exporter completes object exclusion before stripping extensions. It
retains publication markers across filter passes until no marked object
survives, including adjacent parameters in arrays.

The manual fallback has no additional tag, path, or enum exclusions. A new
unmarked API is included, even under a formerly excluded namespace. Review its
handler and source annotations if publication intent is unclear; mark private
objects upstream rather than maintaining a second docs-only allowlist.

The workload-token-only `/harness-support/transcript` GET is internal, as are
the other harness-support operations. Agent Memory operations retain their
upstream internal markers. Public handoff attachment retrieval, anonymous
session/conversation redirects, factory inbox, metrics, scorers, and benchmarks
follow their current operation-level markers, not historical docs exclusions.
The networking tag and its public egress-ranges operation are both published.

## Preserving content

Keep useful API descriptions, examples, product framing, and documentation
links in the server spec, then regenerate the docs file. The fallback neither
overrides `info` nor rewrites URLs. This keeps prose intact on the next release
sync and preserves server-only codegen annotations in the full source.

When reconciling independent docs edits, compare them against the recorded
server source of an earlier docs sync. Preserve accurate improvements upstream;
resolve behavior conflicts against the current handlers. Never copy a stale
constraint or change a runtime implementation merely to match old prose.

## Validation

Run `--mode self-test` before syncing. It exercises the actual exporter on a
fixture with mixed public/internal operations, nested internal properties and
parameters, codegen annotations, and transitive component references. It also
checks that unresolved references leave the target unchanged and that diff
diagnostics include reusable components and metadata.

Real-source coverage checks the annotated internal parameters and compares
every exported node with its public source counterpart.

`--mode diff` returns 1 for structural drift, including tags and every reusable
component section. `--mode apply` returns 3 for unresolved local references and
does not overwrite the target. Missing tooling or exporter failures return 2.
No unknown-classification warnings are needed: publication decisions live in
the canonical source.
