# Blueprint documentation and runnable examples

## Summary

Draft documentation that explains Blueprints and takes a reader through one issue-to-PR workflow. Convert the existing SDLC example to Blueprint-based routing. Keep agent definitions as workers that execute stages. Deliver reviewable drafts, not a claim that the feature is ready to publish.

- Work item: [docs #1045](https://github.com/warpdotdev/docs/issues/1045).
- Requester: `hongyi-chen`.
- Status: proposed specification; requester approval is pending.
- Implementation must reuse this docs branch and draft PR.
- No spec approval or approval waiver has been received.

## Requester decisions

The requester supplied these instructions after the initial research:

> • update examples to use blueprints instead of agents like before
> • can you please provision it for checkout or whatever? add the warp factory examples repo to your repos

These instructions:

- Select an update to the existing examples rather than a second, overlapping workflow.
- Authorize adding `warpdotdev/warp-factory-examples` to this factory's configured repositories.
- Do not remove the worker definitions that Blueprint stages require.
- Do not authorize a patch-only substitute for a draft PR in the examples repository.
- Do not waive approval of this specification.

The original request explicitly authorizes drafts and reviewer questions. That authorization does not clear publication requirements.

## Evidence and current state

| Source | Revision | Finding |
| --- | --- | --- |
| `warpdotdev/docs` | `f00cc4e082f22bce78f42522d14f8e7b23644dc1` | The factory pages have no Blueprint explanation. Existing owners cover lifecycle, definitions, setup, and run inspection. |
| `warpdotdev/warp-factory-examples` | `76f0f06f59a3c3d5fc29eb7699fe281073fa58c1` | Example 02 already covers triage, optional specification, implementation, independent review, and human merge through foreman instructions. |
| `warpdotdev/warp-server` | `d51fa3c62f9b7b4be4d72d8128facc6b4a616851` | The parser and runtime implement stages, workers, ordered prose conditions, gates, and frozen run definitions. Source verification does not establish release availability. |

Implementation references are research inputs for maintainers, not text to copy into public pages:

- `logic/factoryfile/registry.go:10-13`: `v1alpha1` has no Blueprint; `v1alpha2` requires one.
- `logic/factoryfile/blueprint.go`: `decodeBlueprint`, `decodeBlueprintStage`, `decodeBlueprintEdges`, and `validateBlueprintProfiles` define the authored grammar and reference checks.
- `logic/ai/ambient_agents/templates/factory_blueprint_scope_prompt.tmpl`: the scope worker selects the first matching route, binds inputs, executes or delegates, and relays human questions.
- `logic/ai/ambient_agents/templates/factory_blueprint_stage_agent_prompt.tmpl`: a delegated stage reports outputs and does not choose its own outgoing route.
- `client/packages/factory/src/pages/FactorySetup/steps/BlueprintStep.tsx`: setup provides a read-only Blueprint preview, not an editor.
- `client/packages/factory/src/pages/FactoryBlueprint/blueprint-introduction.tsx`: existing factories have a generation entry point.
- `client/packages/factory/src/pages/FactoryBlueprint/blueprint-human-review.tsx`: human review opens the run conversation.
- `specs/factory-blueprint-read-contract/{PRODUCT,TECH}.md`, `specs/factory-blueprint-transition-ledger/{PRODUCT,TECH}.md`, and `specs/blueprint-catalog/TECH.md`: design context only. Prefer current implementation when terminology or behavior differs.

Publication readiness remains unresolved. A server availability check did not clear Gate 0 at the recorded server revision. No live UI walkthrough or end-to-end Blueprint run has been performed. Keep private rollout details out of public files, PR descriptions, and comments.

## Product behavior to teach

1. A Blueprint defines a factory's workflow: its stages, stage workers, instructions, routes, and human decision points. Agent definitions configure the workers; a Blueprint does not replace execution configuration or grant access.
2. Use a Blueprint when a standing workflow needs explicit branching, review loops, or human decisions. Do not imply that every small request must pass every stage or that an ad-hoc agent task requires a factory.
3. The user chooses the workflow, repositories, workers, instructions, transition conditions, and gates. The scope-driving worker evaluates prose conditions in order and selects the first match.
4. A stage names its worker and describes its inputs and outputs. Inputs and outputs are prose contracts, not typed schemas that the server verifies.
5. A stage with the scope's worker runs in that conversation. A stage with a different worker is delegated. The scope-driving worker receives its outputs and chooses the next route.
6. A route either names a sibling stage or ends the current scope. Routes can return to an earlier stage for revisions. Do not teach parallel branching or nested scopes in the beginner walkthrough.
7. A gate pauses departure from a stage while the user supplies the requested answer. A conditional gate opens when its condition holds; a gate without a condition opens after the stage's work. “Changes requested” answers a review gate; it does not approve the work.
8. The foreman relays stage questions to the user and returns answers to the stage. Instructions, tools, credentials, and repository permissions remain separate controls.
9. A new run uses the applied Blueprint selected when that run starts. Editing the current definition does not reroute an existing run. Follow-ups to the same run retain its Blueprint.
10. The user inspects the run, the proposed diff, tests, and independent review. Agent review is advisory. Merge remains a human decision, enforced by repository permissions and branch protection rather than by prose alone.

## Documentation design

### Canonical concept page

- File: `src/content/docs/factories/blueprints.mdx`.
- Proposed title: `About Blueprints`.
- Audience and job: a developer configuring a factory who must decide how to express routing and human decisions.
- Problem: current pages describe foreman instructions but do not explain the Blueprint workflow model or its relationship to workers.
- Goals: decide when to use a Blueprint; understand routing and gates; distinguish configuration changes from active work.
- Purpose and value: own the concept once instead of repeating it in lifecycle, setup, and reference pages.
- Content type: conceptual. Link to the walkthrough instead of embedding a tutorial.
- Skill and template: `draft_conceptual` and `.agents/templates/conceptual.md`.
- Cover: a small issue-to-PR diagram, the user/foreman/stage-worker responsibilities, conditions, revision loops, gates, and the new-run boundary.
- Exclude: hosted catalog versions and subscriptions, nested orchestration, internal routing APIs, and advanced migration.

### End-to-end walkthrough

- File: `src/content/docs/guides/agent-workflows/running-an-issue-to-pr-blueprint.mdx`.
- Proposed title: `Running an issue-to-PR Blueprint`.
- Audience and job: a developer who has access to Warp Factories and wants to try a workflow before adapting it to application code.
- Problem: a configuration fragment alone does not show how to apply the workflow, supply an input, answer a gate, or judge the result.
- Goals: configure and apply example 02; run a concrete issue; inspect the gate, revision, and resulting draft PR.
- Purpose and value: provide one continuous worked example without expanding the general factory quickstart.
- Content type: tutorial. The existing factory quickstart supplies first-time account and connection setup.
- Skill and template: `draft_guide` and `.agents/templates/guide-page.md`.
- Cover: the bounded workflow below, expected results, and recovery from failed validation or missing intake conditions.
- Exclude: a new application fixture, a completion-time promise, alternative trackers, optional iOS work, and every supported setup path.

### Existing pages

Keep each page's purpose. Do not rewrite unrelated sections.

| File | Narrow change |
| --- | --- |
| `src/content/docs/factories/factory-as-code.mdx` | Add version-scoped Blueprint syntax and a short valid example. Preserve legacy-version guidance. Link the full example instead of copying it. |
| `src/content/docs/factories/how-factories-work.mdx` | Explain Blueprint routing and gates beside the lifecycle. Distinguish authored stages from legacy status labels. Remove conflicting claims that routing lives only in foreman prose. |
| `src/content/docs/factories/index.mdx` | Introduce Blueprints where stages and checkpoints are introduced; link the concept. |
| `src/content/docs/factories/quickstart.mdx` | Add a next-step link. Change setup steps only when verified live behavior requires it. Do not add the full walkthrough here. |
| `src/content/docs/factories/factory-dashboard.mdx` | Add concise, verified instructions for inspecting a Blueprint/run and opening the human-review conversation. |
| `astro.config.mjs` and `src/sidebar.ts` | Register the concept and walkthrough in their existing sections. Verify which file owns each navigation tree. |

Apply the repository's full content-design-plan form to each new page and the three-line short form to updates that introduce a concept. Include those plans in the content PR body. This specification presents the proposed plans for requester approval before public prose is drafted.

## Example design

### Workflow

Update `examples/02-sdlc-issue-to-pr`, not every example.

- Set `schemaVersion: v1alpha2` for example 02.
- Put workflow routing in `factory.yaml` under `blueprint`.
- Keep `agents/<name>/agent.md` for worker roles and execution settings. Remove conflicting routing instructions from the foreman's procedure.
- Use the existing worker names: `foreman`, `triage`, `spec`, `implementer`, and `reviewer`.
- Use a flat workflow: triage → optional specification → implementation → optional mobile build → independent review → human handoff.
- Enter specification for large or ambiguous work and when the requester explicitly requires a plan.
- Add a named specification-review gate with answers that distinguish approval from requested changes. Route requested changes back to specification.
- Route actionable review findings back to implementation on the existing branch and PR.
- Keep human handoff open for requested revisions or merge confirmation. A closed, unmerged PR does not complete the work.
- Keep the rule order explicit. Conditions are prose. When no rule applies, the worker asks for the missing decision instead of silently finishing.
- Keep stage prompts inline for this example so a reader can inspect routing and procedures together. Do not add a second copy of the graph in worker instructions.
- Keep iOS as an explicitly optional extension. Route to `mobile-build` after implementation only when the request touches the iOS repository. The implementer handles non-iOS changes; the mobile worker handles iOS changes. Review waits for both results and checks every resulting PR.
- Route non-iOS or mixed review findings to implementation first, then to mobile build if mobile changes remain. Route mobile-only findings directly to mobile build. Preserve the existing worker/runner/repository cleanup instructions and add removal of the mobile stage and its routes to that checklist.

### Concrete reader exercise

Use a disposable, reader-owned fork of `warp-factory-examples` as the work repository. Use examples revision `76f0f06f59a3c3d5fc29eb7699fe281073fa58c1` as the exercise's starting point; its root README has a general validation command but not the requested SDLC-specific instructions or exit-code explanation. Give explicit instructions to enable GitHub Issues, create a `blueprint-demo` branch at that revision, and select it as the fork's default branch. Do not change the upstream repository. Copy the updated example 02 into the root of a separate, reader-owned factory-definition repository. Explain that these repositories have different purposes.

1. Link to the factory quickstart for account, team role, funding, GitHub access, and definition hosting prerequisites. State required repository write and PR permissions. Link billing requirements without copying plan tables.
2. Substitute the reader's work repository and factory alias everywhere they appear, including trigger filters and setup commands. For this non-iOS exercise, omit the optional mobile configuration using the documented coordinated removal.
3. Connect only the integrations used by the exercise. GitHub is the primary intake. Remove unused integration declarations and their automations together, or retain them only after completing their setup.
4. Validate the complete definition, then commit and apply it through the supported GitHub-backed definition path. Confirm that implementation starts from the fork's `blueprint-demo` default branch and targets the PR there. Verify that behavior before publishing the steps. A commit or parser pass is not proof that apply succeeded.
5. Create a GitHub issue titled `Document single-example validation`. Apply the factory routing label before mentioning the foreman.
6. Supply this concrete request, retaining its human and merge limits:

   > In the root README, document how to validate only the SDLC example with `python3 scripts/validate_factory_files.py examples/02-sdlc-issue-to-pr`. Explain that exit code 2 means validation did not run and is not a pass. Keep the change to README.md. Propose a short plan and wait for my approval before editing. Run the repository's convention check and report the validator result honestly. Open a draft pull request. Do not merge.

7. Inspect the plan and the pending gate. Reply with approval. Confirm that implementation did not begin before the answer.
8. Inspect the draft PR and independent review. Ask the foreman: `Revise the same pull request to explain that validation needs network access. Keep the README-only scope and rerun the convention check.`
9. Verify that the revision updates the same PR and is reviewed again. Inspect the final diff and test evidence. Stop before merging unless the reader independently chooses to merge.

The exercise must provide a concrete next action after a validation failure, missing label, unmatched event, unavailable integration, or unresolved human question. Do not present a completed run alone as proof of correct work.

### Files and compatibility

Update the example README, root example index, and relevant worker instructions together with `factory.yaml`. Add links between the docs and the example.

Preserve the current GitHub intake constraints: repository filters, mention/assignment handles, and `factory:<alias>` label. Preserve the merged/closed follow-up filter and its distinction between merged and closed without merge. Adding a Blueprint must not widen intake.

Inspect `.github/workflows/validate.yml` and the helper scripts before editing. CI currently pins a single schema version. Make only the compatibility changes required to validate example 02 as `v1alpha2` while retaining unrelated `v1alpha1` examples. Do not relabel a rejected or unvalidated tree as valid. If prompt files or another new resource layout are introduced despite the inline-prompt decision, update collection and tests so validation includes those files.

## Repository provisioning and delivery

The requester authorized provisioning, not bypassing checkout preparation.

1. Create a minimal companion draft PR in `warpdotdev/docs-factory-config` that adds this repository:

   ```yaml
   repositories:
     # Preserve every existing entry.
     - owner: warpdotdev
       name: warp-factory-examples
   ```

2. Do not treat that PR as applied configuration. A person reviews and merges it through the factory's normal definition-update path.
3. Confirm successful activation. Current runs retain their prepared repository inventory; configuration activation does not retroactively authorize a checkout in this run.
4. Obtain an execution prepared with the examples checkout, or use an explicitly supported checkout mechanism with a matching frozen deferred inventory entry. Read `factory-deferred-repositories` before using that mechanism.
5. Verify an unused checkout path and actual writable branch/PR delivery access. An all-false repository permission payload is not conclusive; the docs new-branch push dry run succeeded despite that payload.
6. If no supported preparation mechanism exists, report the runtime provisioning blocker to the foreman. Do not raw-clone, silently fork, or deliver only a sandbox patch.
7. Open a draft PR in each changed repository. Reuse the spec PR for docs implementation. Cross-link the docs, examples, and provisioning PRs and record them on issue #1045.

## Decisions and alternatives

| Decision | Selected option and reason | Alternative and trade-off |
| --- | --- | --- |
| Example location | Convert example 02, as requested. It already owns the complete lifecycle. | A new example isolates Blueprints but duplicates the workflow and leaves the old primary example misleading. |
| Workers | Retain agent definitions; move routing into the Blueprint. This matches the implemented model. | Deleting agents would leave stage workers undefined. Leaving routing only in foreman prose would not demonstrate Blueprints. |
| Content structure | One concept plus one linked tutorial, with narrow reference updates. Each owns a distinct reader job. | One long combined page hides the continuous exercise; adding the tutorial to the quickstart changes its purpose. |
| Teaching input | A README improvement in the reader's examples fork. Its files and checks are inspectable and it needs no new app fixture. | An invented application bug requires extra code, dependencies, and a second set of maintenance tests. |
| Schema scope | Migrate example 02 and only necessary helper compatibility. | Migrating the whole repository increases unrelated scope and makes legacy behavior harder to inspect. |
| Availability | Draft now; retain publication holds and reviewer questions. | Treating source or staging behavior as shipped would make unsupported public promises. |

## Assumptions

- Assumption: the reader has already completed basic factory setup or follows the linked quickstart.
- Assumption: a GitHub-backed definition and GitHub issue intake provide the single primary path. Other supported sources remain in example 02 as optional configuration.
- Assumption: the requester will review the concept/tutorial split and the README exercise through this specification. The quoted reply explicitly chooses the example upgrade but does not independently approve every editorial choice.
- Assumption: publication availability will be rechecked at the implementation head. This specification does not predict a release date or public access tier.

## Reviewer questions and publication holds

- Confirm current public Blueprint availability and required access. Record evidence at the checked revision; do not expose private rollout details.
- Verify actual UI names and the setup → apply → run → gate → revision → PR path in an authorized environment. Source reads and screenshots from other tasks do not satisfy this check.
- Confirm that the public validation service accepts the exact example schema and complete file tree. Report parser diagnostics or an unavailable check without weakening validation.
- Confirm successful examples-repository provisioning and a newly prepared execution before attempting its checkout.

Record unresolved technical claims as adjacent MDX `VERIFY` comments and in the docs PR's `Unverified claims` section. Use a reviewer checklist in the examples draft. Do not present unresolved availability or fabricated command/UI instructions as runnable facts. Leave a blocked step explicitly unverified rather than filling it with a guess.

## Out of scope

- Product implementation, new Blueprint features, or fixes to the runtime.
- Internal transition-ledger APIs, advanced nested scopes, parallel branches, hosted-catalog versions/subscriptions, and a general migration manual.
- A repo-wide examples rewrite, new application fixture, or new trigger family.
- Production runs against a repository the requester does not control.
- Automatic merge, publication, or declaring draft content production-ready.

## Validation criteria

Report each check as passed, failed, or not run with its reason. Retain exact commands, revisions, and evidence in the draft PRs.

### Documentation and example correctness

- Confirm all ten product behaviors above against the recorded implementation and the current source before finalizing prose. Record claim-to-source references in reviewer evidence.
- In the concept, identify the user, foreman, and stage worker responsibilities. In every walkthrough step, name the actor and the result the reader can check.
- Read the Blueprint and worker instructions together: each worker reference resolves, every stage has a valid exit, gate answers drive the intended revision path, and no obsolete procedure contradicts the graph.
- Reconcile docs snippets, example files, schema versions, placeholder substitutions, and trigger conditions. Confirm that public pages contain no private rollout details.

### Docs commands

Run from the docs repository:

```bash
python3 .agents/skills/style_lint/style_lint.py --changed
python3 .agents/skills/check_for_broken_links/check_links.py --internal-only
npm run typecheck
npm run test:heading-vars
npm run build
npm run test:heading-tocs
npm run test:homepage-json-ld
```

Run `check_compression_contract.py FILE --content-type TYPE` for each changed content page using the selected type. Run `check_pr_contract.py --body BODY_FILE CHANGED_CONTENT_FILES` with the actual PR body and paths. Read the current policy before choosing overrides or review requests. Use `engineering-review-required`, the `warpy-factory` marker, and complete `VERIFY` accounting for the content PR.

### Examples commands

Run from an authorized examples checkout:

```bash
python3 scripts/validate_factory_files.py examples/02-sdlc-issue-to-pr
python3 scripts/check_conventions.py
python3 scripts/test_verify_default_agents.py -v
python3 scripts/test_check_conventions.py -v
```

- Run the existing validation workflow against every example after changing shared helpers or CI. Add focused regression tests for helper behavior changed by this work.
- Record the server URL and schema version used by validation. Exit code 2 is “not validated,” never a pass.
- Apply the substituted definition to a reader-controlled test factory and record the applied revision. Syntax validation does not establish team access, credentials, or successful application.

### Runtime and visual evidence

Use computer use after the relevant build succeeds. Capture a video of the authorized setup/definition inspection, request submission, human gate, approval, draft PR, and same-PR revision. Record observed UI labels and outcomes; do not infer a live result from source. Add static screenshots only when a configuration or graph view needs separate proof.

Check these cases with concrete inputs:

| Case | Expected result |
| --- | --- |
| Labeled GitHub issue plus the configured mention | One intended intake path reaches the workflow; it asks for the explicitly required plan approval. |
| A PR follow-up that matches mention/assignment conditions | Confirm the existing automation's multiple triggers do not duplicate work for the same delivery; distinct deliveries must not be assumed deduplicated. |
| Missing routing label or a repository outside the filter | The specialized GitHub automation does not start work. Do not claim another route handles it without evidence. |
| Requested plan changes | Implementation stays blocked; specification is revised and asks for a new answer. |
| Human revision after the first draft PR | The same work and PR continue through implementation and independent review. |
| Definition edit while that run exists | The existing run retains its Blueprint. A separately started run selects the newly applied definition. |
| PR closed without merging | The foreman reports closure and does not mark the work merged or complete. |

These are implementation acceptance checks, not checks already passed during specification. If authorized access or provisioning prevents a runtime case, record the exact missing prerequisite and retain the publication hold.
