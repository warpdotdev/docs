# OpenAPI publication

`warp-server/public_api/openapi.yaml` owns the API contract.
`public_api/public-openapi-filter.yaml` owns the public/internal boundary.
The sole publisher is warp-server's
[`sync_public_openapi_to_docs.yml`](https://github.com/warpdotdev/warp-server/blob/develop/.github/workflows/sync_public_openapi_to_docs.yml),
which runs `script/generate-public-openapi`.

Docs agents detect and report drift only. Report the affected route or field,
release evidence, source commit, and existing sync PR or workflow result to the
release owner. Correct contract errors upstream with warp-server's
`update-open-api-spec` skill. Do not hand-edit the generated docs YAML, run a
local docs publisher, or create an agent-owned spec-sync PR.

Release-candidate deployment calls the workflow with its source commit. Manual
`source_ref` defaults to the latest RC tag. The selected ref supplies the spec,
policy, and exporter; current `develop` does not replace that checkout.
Use a released ref containing the intended API content and corrected exporter.
Exporter regressions run in the server's OpenAPI PR CI job, not during
publication. An older source ref still uses its older exporter, even when the
workflow definition is current.

The workflow installs the server's pinned Node dependencies and needs configured
server-read and docs-write credentials. It proposes a docs PR on
`automation/sync-agent-api-spec`; it does not merge docs `main`. Review the
generated diff and recorded source commit before landing it.
