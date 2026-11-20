# Plan for artifact documentation

## Summary and authorization

Create one canonical documentation page for finding, retrieving, and sharing artifacts, with a home in the factory docs. Explain plans, screenshots, recordings, uploaded files, and linked outputs without treating every output as a downloadable file or a public link.

- Work item: [docs issue #1072](https://github.com/warpdotdev/docs/issues/1072).
- Requester: `rachaelrenk`.
- Placement decision from `hongyi-chen`: “Let's put this under the factories docs”.
- Decision record: [placement confirmation](https://github.com/warpdotdev/docs/issues/1072#issuecomment-7027387053).
- Current deliverable: this implementation plan only.
- Approval status: pending written approval of this plan.
- Approval of this plan does not authorize public-documentation or product changes. Obtain a separate instruction before starting the implementation sequence.

## Evidence and current coverage

Use issue #1072 and the supplied research as the starting record. Do not repeat the broad artifact investigation. The research establishes a documentation gap, not a product defect.

Evidence baseline:

- Docs revision: `0074ba82260ecbbbd762e31fb3bb1730e13691ea`.
- Research date: November 20, 2026.
- Supporting server-source revision recorded on the issue: `74e90c8e9d87470c51a14f5758abcad00d2e86c7`.
- No live product UI or authenticated artifact API test was performed for this plan.
- Existing documentation proves coverage exists. Source behavior and rollout configuration do not, by themselves, prove customer availability.
- Before drafting publishable procedures, complete the availability checks below. Keep private rollout details out of this public repository.

| Existing owner | Coverage now | Bounded change |
| --- | --- | --- |
| `src/content/docs/factories/factory-dashboard.mdx`, “Inspect runs” | Run relationships and session inspection, but no artifact workflow. | Add a verified artifact entry point in one or two sentences. Link to the canonical page for the full procedure, types, and access. |
| `src/content/docs/factories/index.mdx`, “Work items” | Work-item context and worker contributions. | Add a short outcome-focused artifact link beside the work-item explanation. |
| `src/content/docs/agents/capabilities/computer-use/artifacts-in-prs.mdx`, “Attachment modes” and “Sharing captures outside pull requests” | Media links, public embeds, team policy, and child-run limits. | Keep policy and attachment instructions here. Replace generic artifact orientation with a pointer to the canonical page. |
| `src/content/docs/agents/capabilities/planning.mdx`, “Saving and sharing” | Plan persistence, links, and Markdown export. | Add a crosslink. Keep editing, version history, and export instructions here. |
| `src/content/docs/agents/cli/oz-cli/artifacts.mdx` | Legacy `oz artifact get` and `download`. | Add a canonical-page link and clarify retrieval scope. Preserve supported legacy commands. |
| `src/content/docs/platform/viewing-cloud-agent-runs.mdx` | Shared session and run inspection. | Link artifact discovery to the canonical page without equating a session link with artifact publication. |
| `src/content/docs/factories/api-and-sdk/index.mdx` and `developers/agent-api-openapi.yaml` | API orientation, run schemas, artifact types, and retrieval endpoints. | Add an orientation crosslink. Keep endpoint and schema reference authoritative; no schema change is planned. |
| `.agents/references/terminology.md`, “Platform terms” | “Artifacts” currently describes uploaded files only. | Clarify the distinction between uploaded files and the broader API output model. Preserve exact API identifiers. |

Public source anchors:

- [`ArtifactItem` union and variants](https://github.com/warpdotdev/docs/blob/0074ba82260ecbbbd762e31fb3bb1730e13691ea/developers/agent-api-openapi.yaml#L9762).
- [Artifact metadata and download operations](https://github.com/warpdotdev/docs/blob/0074ba82260ecbbbd762e31fb3bb1730e13691ea/developers/agent-api-openapi.yaml#L3742-L3848).
- [Existing media-sharing documentation](https://docs.warp.dev/agents/capabilities/computer-use/artifacts-in-prs/).
- [Existing CLI retrieval documentation](https://docs.warp.dev/agents/cli/oz-cli/artifacts/).

## Content design plan

**Audience and JTBD:** A developer or support engineer reviewing a factory work item needs to locate its plan, evidence, or generated report and send the correct reference to a colleague. An API consumer needs to retrieve a selected downloadable artifact. Readers of standalone cloud-run docs need the same shared model.

**Problem:** A customer asked about shareable artifacts, and the reporter could not find one page to link. Existing pages separate media attachment policy, planning, and legacy CLI retrieval. The factory dashboard page does not connect those pieces.

**Goals:**

- Find an output from a work item or run and distinguish it from conversation text or a file left only in the sandbox.
- Choose a plan link, access-checked media link, downloadable file, or external reference without assuming that the recipient has access.
- Discover a supported artifact UID and retrieve its metadata or content through the existing API reference.

**Purpose and value:** No existing page owns the cross-type workflow. Extending Computer Use alone excludes plans and reports. Extending the dashboard page alone overloads a surface overview with API and access detail. One canonical page supports the reported customer question; surrounding pages provide short entry points.

**Content type:** Combined feature documentation. Readers need a short artifact model and task-focused procedures.

**Skill and template:** `.agents/skills/draft_feature_doc/SKILL.md`, following `.agents/skills/draft_docs/SKILL.md`, and `.agents/templates/feature-doc.md`.

**High-impact scenarios:**

- Covers: review a plan, inspect screenshots or recordings, retrieve an uploaded report, and choose a link whose access model fits the recipient.
- Covers: factory work-item aggregation and the shared behavior of ordinary cloud runs.
- Excludes: new sharing controls, a new API tutorial, a full Computer Use setup guide, and plan-editor instruction duplication.

**Worthiness:** This is a direct human request, so Gate 0 applies before public drafting. The released OpenAPI reference establishes the documented API contract. UI availability and exact procedures remain pending. This plan is not a Gate 0 clearance for every proposed claim.

## Proposed documentation behavior

1. Create `src/content/docs/factories/artifacts.mdx` at `/factories/artifacts/`.
2. Use the title “Finding and sharing artifacts” and sidebar label “Artifacts”.
3. State near the opening that artifacts also belong to ordinary cloud agent runs. The factory docs home does not make artifact support factory-exclusive.
4. Explain the relationships in user terms:
   - A conversation contains the agent's messages, actions, and reported results.
   - A run is one agent execution.
   - A factory work item can involve multiple runs and workers.
   - Factory output views aggregate relevant results. Do not describe them as only the foreman's conversation output.
   - A file on a worker's filesystem is not automatically a persisted artifact. The agent must upload or report the result.
5. Explain uploaded artifacts separately from links to PRs, issues, or other external resources.
6. Place access constraints next to the sharing choice. A copied link does not grant access.
7. Point readers to specialized owners instead of repeating their full policies.

### Inventory and access matrix

Use reader-facing names in the public inventory. Introduce exact API discriminators only in the API section. UI group names are not an API enum.

| Reader-facing result | API representation | Retrieval or destination | Access constraint |
| --- | --- | --- | --- |
| Plan | `PLAN` | Plan URL; metadata retrieval can return current plan content. | Verify plan and Warp Drive sharing separately. Do not assume media-sharing permissions apply or promise an immutable snapshot. |
| Screenshot | `SCREENSHOT` | Supported artifact retrieval and a media-page link. | Private access is checked. Only explicitly public artifacts support anonymous access. |
| Video recording | `FILE` with video content | Supported file retrieval; media-sharing workflow for supported captures. | Video is not a sixth API artifact type. Do not assume every uploaded video is a Computer Use capture. |
| Uploaded report or other file | `FILE` | Metadata and downloadable content. | Do not promise anonymous publication, generic browser previews, allowed extensions, size limits, or retention periods without evidence. |
| Pull request | `PULL_REQUEST` | Open the code host's URL. | The code host controls access. The artifact download endpoint is not a PR archive service. |
| Issue or other external link | `EXTERNAL_REFERENCE` | Open the referenced system's URL. | The destination controls access. An output entry does not copy its contents into Warp or make them public. |

Describe link choices separately:

- **Private artifact or media reference:** Requires the recipient's applicable access. Do not promise that every factory member can open every artifact.
- **Public media embed:** Requesting permitted embed URLs publishes the selected media for anyone with the URL. Link to the existing attachment-policy page for controls and defaults. Do not generalize this mechanism to arbitrary files.
- **Plan link:** Opens a plan with its own sharing rules. Verify these rules before writing an access claim.
- **Signed download URL:** Temporary content access, not a stable share link. Tell API consumers to request a fresh URL rather than store it as the durable reference.
- **External output URL:** Retains the destination system's permissions.

### Canonical page outline

Keep the combined page within 1,500 words unless a reviewer approves a justified exception.

1. Opening: locate and share a factory result; mention ordinary cloud-run applicability.
2. “Artifacts and linked outputs”: short inventory and the relationship explanation.
3. “Finding artifacts”: verified factory workflow first; link the standalone run-inspection path.
4. “Requesting a saved result”: uploaded-report example and a plan example.
5. “Sharing an artifact”: access choices, with the media policy and plan-sharing links beside the relevant actions.
6. “Retrieving an artifact with the API”: discovery, type selection, metadata, and download.
7. “Related pages”: links to the existing owners.

Do not add a new FAQ, a second artifact page under Agents, or a new standalone tutorial.

### Examples to prepare and test

- **Uploaded report:** Ask the agent to create `dependency-audit.csv` from non-sensitive sample package data and upload it as a task artifact. Expected result: a file artifact survives as a reported result and downloads with the expected rows. State that writing the file alone is insufficient.
- **Plan:** Ask for a plan to add a CSV export, explicitly without implementation. Expected result: a plan reference is available for review. Link to planning for editing and export. Check whether retrieval reflects a later edit before describing current-content behavior.
- **Media:** Ask the agent to capture a demo application's export flow and return links in the current conversation. Use non-sensitive fixtures. Start with access-checked links; demonstrate public embedding only with explicit permission and policy support. Link the PR-attachment workflow instead of restating it.
- **API:** Start with a known authorized run and its documented response. Discover its artifact entries, select a supported type, then use the artifact UID with `GET /agent/artifacts/{artifactUid}`. For a downloadable result, follow `GET /agent/artifacts/{artifactUid}/download`. Handle an empty list, missing UID, and a linked output without attempting to download it. Do not select the first entry blindly or substitute a document UID for an artifact UID.

Keep authentication setup in its existing owner. Do not print tokens or signed URLs in verification logs or committed examples.

## File-level implementation sequence

This sequence starts only after separate implementation authorization.

1. **Verify the proposed claims.** Complete the checklist below using non-sensitive fixtures. Record the revision, product environment, date, observed result, and evidence link. If a core workflow cannot be verified, stop that part of drafting and request source-owner confirmation. Omit unverified optional controls and limits.
2. **Draft the canonical page.** Add only `src/content/docs/factories/artifacts.mdx`. Apply the content design plan and matrix. Use product-name variables from `src/data/vars.ts`. Keep raw tool names out of reader instructions unless they are a supported public interface.
3. **Connect factory discovery.** Update the dashboard's “Inspect runs” section and the overview's “Work items” section. Add the canonical slug to `src/sidebar.ts` under Factories, “Management & observability”, immediately after Factory dashboard. Navigation lives in `src/sidebar.ts`; do not modify `astro.config.mjs` for this entry.
4. **Connect existing owners.** Make only the bounded crosslinks and scope clarifications in the coverage table. In the media page, replace its generic “Where else artifacts appear” list with a canonical-page pointer after verifying the destinations. Preserve all specialized instructions and published URLs.
5. **Align terminology.** Update only the artifact entry in `.agents/references/terminology.md`. Keep “output” broad and distinguish persisted content from external references. Do not run a repository-wide terminology sweep.
6. **Validate and request review.** Run the checks below. Coordinate dashboard edits with [audit #1034](https://github.com/warpdotdev/docs/issues/1034); do not absorb its unrelated work.

No page moves or removals are planned. No redirects, API schema edits, site configuration changes, or product changes are required.

## Decisions and trade-offs

- **Canonical home:** Agent capabilities would expose the shared primitive, but the requester chose the factory docs. Use `/factories/artifacts/` and make shared applicability explicit. This avoids a competing canonical page.
- **One combined page:** A dashboard-only update would bury cross-type access and retrieval guidance. Separate pages for each type would duplicate existing owners. One feature page plus bounded crosslinks addresses the gap.
- **Human names before API types:** The inventory helps readers find a report or recording. Exact discriminators belong beside API type selection, where they affect behavior.
- **Verification before specificity:** Exact UI steps are useful but become incorrect when inferred from source. Verify customer-visible navigation before writing steps. Do not publish instructions for unavailable UI.
- **Reuse API reference:** One tested retrieval example teaches the workflow. A copied schema or endpoint catalog would add a second reference to maintain.

## Assumptions and unresolved verification

These are not product guarantees:

- **Editorial assumption:** Use the proposed slug, title, and bounded crosslinks within the confirmed factory-docs home. Requester approval of this plan resolves these editorial choices.
- **Example assumption:** A dependency-audit report and a CSV-export plan represent the original customer's needs. They use sample data and do not require customer data.
- **Verification prerequisite:** Exact labels, artifact entry points, available actions, and work-item/run aggregation require live observation.
- **Verification prerequisite:** Plan-link ACLs and their relationship to artifact retrieval require source-owner confirmation or controlled recipient tests.
- **Verification prerequisite:** Arbitrary-file limits and any public-file control remain unknown. Omit them unless verified; do not copy media policy to files.
- **Verification prerequisite:** Available UI previews vary by artifact type. Do not promise that generic files use the media-only preview.
- **Verification prerequisite:** Current production availability needs fresh evidence. Re-check at implementation time; the research baseline is not deployment proof.

## Validation criteria

### This plan PR

- `git diff --check` passes.
- The PR changes only `specs/artifact-documentation/PLAN.md`; no public page, navigation, or product file changes.
- The placement decision, coverage inventory, access matrix, file sequence, assumptions, and future validation tasks appear in this committed file.
- The draft PR references issue #1072 without closing it. Written plan approval and later implementation authorization remain separate.
- Site build, product UI capture, and authenticated API tests are not claimed as completed checks for this plan-only PR.

### Future documentation implementation

- **Availability:** Run `python3 .agents/skills/doc_quality_policy/server_rollout.py check artifact artifacts screenshot video plan` at the implementation revision. Inspect relevant matches. Record only the verdict and revision publicly. A clean result rules out known disabled flags; also obtain applicable release evidence or explicit owner confirmation.
- **Product workflow proof:** Use `computer_use` with required video to record finding a non-sensitive factory result, opening its plan or media, and retrieving its file. Record a standalone-run inspection separately if it uses a different procedure. Describe observed labels and outcomes. No staging-only or mocked surface counts as customer-availability proof.
- **Access proof:** Test an authorized user, a signed-out viewer, and a signed-in user without access to a private fixture. Private content must not be exposed. If permitted, test a deliberately public media fixture separately. Do not turn a private artifact public merely to complete a test.
- **Content proof:** Use a controlled plan edit to check current-content retrieval. Compare the downloaded sample report with the expected rows. Verify recordings appear as `FILE` and linked outputs are not passed to download retrieval. Record missing-fixture limits instead of declaring a pass.
- **API proof:** Test the documented discovery and retrieval example using authorized fixtures. Confirm the expected metadata response and download redirect. Verify unsupported output handling against the reference. Redact credentials and temporary URLs.
- **Discoverability proof:** After the docs build succeeds, use `computer_use` to follow the factory navigation entry and dashboard crosslink to the canonical page. Static screenshots can prove final render; use video for the navigation flow.
- **Repository checks:** Run the following from the docs root and record each result:
  - `python3 .agents/skills/style_lint/style_lint.py --changed`
  - `python3 .agents/skills/check_for_broken_links/check_links.py --internal-only`
  - `npm run typecheck`
  - `npm run test:heading-vars`
  - `npm run build`
  - `npm run test:heading-tocs`
  - `npm run test:homepage-json-ld`
  - `python3 .agents/skills/doc_quality_policy/check_compression_contract.py src/content/docs/factories/artifacts.mdx --content-type feature-doc`
  - `trunk check`, if available; record an unavailable tool as skipped.
- **UI references:** If the draft adds Settings paths or Command Palette names, run `python3 .agents/skills/validate_ui_refs/validate_ui_refs.py --all`. This does not replace live verification of factory dashboard labels.
- **Review contract:** Classify the future content PR as `engineering-review-required`. Apply the current agent-doc contract, include the content design plan and unverified-claim accounting, and attach visual evidence to its PR description. Resolve or remove uncertain publishable instructions before merge.
