# Factory help links and standalone trigger documentation

## Summary

Correct links that send a factory user to standalone Oz setup. Complete the missing procedures before product help links depend on them. Keep supported standalone trigger, schedule, integration, CLI, and API workflows available. This work changes documentation and help destinations, not integration behavior.

- Work item and authoritative audit: [docs#1019](https://github.com/warpdotdev/docs/issues/1019).
- Origin and interview record: [requester thread](https://warpdev.slack.com/archives/C09BVK0PL3Y/p1794417742638899).
- Starting example: [warp-server#21630](https://github.com/warpdotdev/warp-server/pull/21630) already fixed the workspace Jira **Docs** button. Do not duplicate it.
- Spec status: **Awaiting approval.** Scope confirmation is not approval to implement.
- Spec baseline: docs `aa38334328a4a54b67d1058e1e615335ac20002f`.
- Audit source revisions: docs `bb1d0e5daaca849adebaadfaea37863ffce549a4`; warp-server `557cde19a04a5a0d8bf6e5ddf10c27a46136a53d`; warp `2b2ed236f087b47b463f1cd55598485dd7965338`.
- Source inspection does not establish the customer's deployed version or account access.

## Product behavior

1. A help link for configuring a factory opens instructions for that task. A destination under `/platform/` is valid when the instructions cover the shared task and provide a complete factory path.
2. Jira instructions distinguish site installation, connection to a Warp workspace, personal account linking, factory project selection, and automation setup. Completing one does not imply completion of the others.
3. Linear instructions distinguish workspace app authorization, personal identification, factory team selection, and automation routing. Reconnection and removal describe the affected connection, not an inferred reset of factory settings.
4. Cloud-provider help from a factory opens factory environment instructions. Those instructions reuse the shared AWS/GCP federation prerequisites and trust policies.
5. A reader can configure recurring work for a factory without following an Oz standalone schedule procedure. A reader who wants an Oz standalone schedule can still use its current web, CLI, and API documentation.
6. Existing shared billing, security, identity, session viewing, API, GitHub installation, and Slack workspace-app instructions remain accessible. Do not replace links only because their paths contain `/platform/` or their names contain Oz.
7. Retain all three `/platform/triggers/` pages and their purposes. Do not redirect, remove, or repurpose a supported page.
8. Record each audit finding as changed, intentionally retained, or incomplete. An incomplete finding names the missing verification and dependent links that remain unchanged.

## Technical design

### Documentation ownership and bounded setup additions

Update existing pages. No new public page or global product-name-variable change is planned.

| Owning page under `src/content/docs/` | Required addition or correction | Stable destination contract |
| --- | --- | --- |
| `factories/integrations/jira.mdx` | Provide the complete site-admin app installation and Warp workspace connection procedure. Include the existing alternate-admin request path, how to recognize a connected site, and the separate factory project-selection step. Exclude standalone `warp-agent` label retry instructions. | Add `#install-warp-for-jira`. Preserve `#connect-jira-and-add-an-automation` as the factory connection and automation entry point. |
| `factories/integrations/jira.mdx` | Add a personal-link procedure: where the user opens Warp in Jira personal settings, how they authorize the link, how to confirm it, and how to retry a factory assignment or mention. Distinguish unlinking a person from removing the site app. | Add `#connecting-your-jira-account-to-warp`. |
| `factories/integrations/linear.mdx` | Add workspace installation and authorization instructions; name required administrator access, confirm the workspace connection, and link forward to factory team selection. Add reconnection and removal procedures with provider-side access and routing consequences verified separately. Do not infer production OAuth scopes from the existing staging-only table. | Add `#install-linear-for-your-workspace`, `#reconnect-linear`, and `#remove-linear`. Preserve `#connect-linear` and `#route-agent-sessions`. |
| `factories/automations.mdx` | Add a bounded recurring-automation procedure. Cover selecting an existing agent, giving it instructions, selecting a schedule trigger, setting the cadence, saving, running a controlled test, locating the result, and disabling future runs. State verified timezone semantics. Cover repository-managed definitions by linking the existing schedule schema instead of promising an editable UI. | Add `#schedule-a-factory-automation`. Preserve the existing filter and webhook sections. |
| `platform/integrations/cloud-providers.mdx` | Add a factory entry section with separate AWS and GCP environment configuration paths. Explain how to create or edit the factory environment and enter the provider fields. Link to the shared provider/role/pool setup on the same page. Retain the Oz environment procedure, explicitly labeled standalone. Scope the current “only in the Oz web app” statements to the verified workflow instead of applying them to factories. | Add `#configure-a-factory-environment`, `#configure-aws-for-a-factory`, and `#configure-gcp-for-a-factory`. Preserve `#aws`, `#gcp`, and existing OIDC claim anchors. |

Keep one canonical copy of each AWS trust policy and GCP federation setup. Do not broaden its audience, subject conditions, IAM roles, or credential claims to make a walkthrough easier. State how to confirm saved configuration. A cloud access check must use an authorized test account and a non-mutating operation. Do not expose JWTs, credentials, or customer identifiers.

Every new procedure includes access prerequisites, a create-or-reuse path, the ordered actions, and an observable success check. Verify UI wording before writing exact labels. If verification is unavailable, follow the incomplete-delivery rule below rather than inventing steps.

### Factory documentation link changes

The audit line numbers below refer to the pinned audit revision. Re-resolve by surrounding task on the implementation branch.

| Source under `src/content/docs/` | Current destination | Required destination or treatment |
| --- | --- | --- |
| `factories/connect-your-factory.mdx:91` | `/platform/triggers/` | `/factories/automations/#schedule-a-factory-automation`; link `/factories/factory-as-code/#triggersschedule` for file-managed schedules. |
| `factories/factory-as-code.mdx:612` | `/platform/integrations/` | `/factories/connect-your-factory/`; retain its existing provider-specific factory links. |
| `factories/factory-agents/creating-custom-agents.mdx:23,135` | `/platform/secrets/` | `/factories/secrets/`. |
| `factories/factory-agents/creating-custom-agents.mdx:83` | `https://docs.warp.dev/platform/environments/configuring-environments/` | `/factories/environments/configuring-environments/`. Remove reliance on the old redirect. |
| `factories/integrations/linear.mdx:19` | `/platform/integrations/github/` | `/factories/integrations/github/` for factory repository access. |
| `factories/integrations/linear.mdx:21,135,144` | `/platform/integrations/linear/` | Local installation, reconnection, and removal sections, respectively. Keep the standalone fallback at line 53 and label it standalone. |
| `factories/integrations/jira.mdx:22` | `/platform/integrations/jira/#setup` | `#install-warp-for-jira`, after the full procedure exists. |
| `factories/integrations/jira.mdx:99,119` | `/platform/integrations/jira/#connecting-your-jira-account-to-warp` | `#connecting-your-jira-account-to-warp`. |
| `factories/guides/jira-to-pull-request.mdx:23` | `/platform/integrations/jira/#connecting-your-jira-account-to-warp` | `/factories/integrations/jira/#connecting-your-jira-account-to-warp`. |
| `factories/self-hosting/data-storage.mdx:287` | `/platform/secrets/` | `/factories/secrets/` for factory credentials. Keep a separately labeled standalone reference if the surrounding task needs it. |
| `factories/self-hosting/security-and-networking.mdx:114` | `/platform/integrations/gitlab/` and `/platform/integrations/bitbucket/` | Link `/factories/integrations/gitlab/` for the first-class factory GitLab connection. Link `/factories/code-forges/other-code-forges/` for self-managed/token access. Retain shared Bitbucket token instructions as such; do not imply a first-class factory Bitbucket integration. |
| `factories/environments.mdx:59` | `/platform/triggers/scheduled-agents/` without a workflow distinction | Prioritize `/factories/automations/#schedule-a-factory-automation`. Keep an explicitly labeled standalone alternative. |

Use relative links within a docs space and absolute docs URLs across spaces, following `AGENTS.md`. The paths in these tables define destinations, not a requirement to ignore that formatting convention. Preserve existing heading IDs; use an explicit compatibility anchor if a heading must change.

### Product help changes

Only modify active help destinations in `warpdotdev/warp-server`. No backend, permission, integration, or desktop-client behavior change is planned.

| Source under `client/packages/factory/src/` | Current destination | New destination, after publication |
| --- | --- | --- |
| `constants/urls.ts:119`, `DOCS_JIRA_SETUP`, consumed by `pages/FactorySettings/JiraIntegrationConnect.tsx:325` | `/platform/integrations/jira/#setup` | `/factories/integrations/jira/#install-warp-for-jira`. This modal needs installation, not only an automation description. |
| `utils/integrations/integration-education.ts:119`, personal Jira | `/platform/integrations/jira/#connecting-your-jira-account-to-warp` | `/factories/integrations/jira/#connecting-your-jira-account-to-warp`. |
| `utils/integrations/integration-education.ts:157`, workspace Linear and its team alias | `/platform/integrations/linear/#how-to-configure-the-integration` | `/factories/integrations/linear/#install-linear-for-your-workspace`. |
| `utils/integrations/integration-education.ts:74`, factory AWS | `/platform/integrations/cloud-providers/#aws` | `/platform/integrations/cloud-providers/#configure-aws-for-a-factory`. |
| `utils/integrations/integration-education.ts:81`, factory GCP | `/platform/integrations/cloud-providers/#gcp` | `/platform/integrations/cloud-providers/#configure-gcp-for-a-factory`. |
| `pages/FactorySettings/CloudProviderSetupModal.tsx:29` | `/platform/integrations/cloud-providers/` | `/platform/integrations/cloud-providers/#configure-a-factory-environment`. |

Use the existing documentation constants and scope-aware education map. Keep each caller's scope intact. Do not redirect personal or workspace GitHub help to a factory repository chooser. Do not redirect shared Slack app help to a factory's dedicated Slack app procedure.

Extend existing `components/integration-setup/__tests__/integration-education.test.tsx`, `constants/urls.test.ts`, `pages/FactorySettings/JiraIntegrationConnect.test.tsx`, and `pages/FactorySettings/CloudProviderSetupModal.test.tsx` where their rendered links change. Assert the literal destination and fragment, not only that the link starts with the docs origin. Preserve unchanged GitHub, Slack, factory Jira, personal Linear, and team-alias expectations.

### Trigger and setup page dispositions

| Page | Decision | Required change and retained purpose |
| --- | --- | --- |
| `/platform/triggers/` | Keep and update | Make standalone schedules, CLI/API entry points, CI, and standalone integrations explicit. Link factory intake to factory automations. Mark custom webhooks as a factory feature, not an equivalent standalone integration. |
| `/platform/triggers/scheduled-agents/` | Keep and update | Preserve the standalone CLI schedule reference and its supported create/list/get/update/pause/unpause/delete workflows. Add an early factory recurring-automation alternative. Keep `#scheduling-a-skill` and links to run identity. |
| `/platform/triggers/scheduled-agents-quickstart/` | Keep and update | Preserve the standalone Oz web schedule workflow. Add the factory alternative. Verify its exact current controls and example skill before changing procedural claims. Keep `#run-identity-and-pull-request-authorship`. Do not turn this page into a factory quickstart. |
| `/platform/integrations/` and `/platform/integrations/quickstart/` | Keep and narrowly update | State which task is standalone and direct factory configuration to the factory connection hub. Retain supported standalone setup and CLI instructions. |
| `/platform/integrations/slack/`, `linear/`, `jira/`, and `github/` | Keep and narrowly update | Add or refine the entry-point distinction between shared installation, standalone triggers, and factory routing. Link to each owning factory page. Preserve shared app and identity instructions and supported standalone fallback behavior. Do not replace these pages with redirects. |
| GitHub Actions, GitLab/Azure DevOps/Bitbucket token setup, CLI and API references, and shared cloud federation details | Keep | Preserve the distinct CI, standalone, token, and shared-provider tasks. Change only the factory-context links specified above. |

Support evidence in the audit includes `warp/crates/warp_cli/src/schedule.rs:51-140`, `warp-server/router/handlers/public_api/agent_schedules.go:96-124`, and `warp-server/client/packages/agents/src/pages/Schedules/NewSchedulePane.tsx:54-189`. These establish implemented standalone workflows, not universal customer availability. Integration fallback is event-specific: unclaimed Slack/Jira and Linear agent sessions do not establish support for every Linear issue/comment event.

### Inbound links and navigation

- Keep the three trigger pages in `src/sidebar.ts:696-705`. Do not move or hide them. `src/sidebar.ts`, not an inline `astro.config.mjs` list, owns this navigation.
- Change the factory connection-hub and environment links listed above.
- Keep the explicitly standalone link in `factories/automations.mdx:130`.
- Keep the standalone schedule continuation in `factories/api-and-sdk/quickstart.mdx:99`; clarify its standalone label without changing that page's API-run task.
- Keep schedule links in `factories/harnesses/claude-code.mdx:17`, `codex.mdx:17`, and the standalone trigger link in `factories/harnesses/index.mdx:24`. Clarify the standalone context of the mixed trigger lists; preserve factory harness instructions.
- Keep `factories/self-hosting/index.mdx:85` as a standalone host-routing reference; label the CLI/Oz example context explicitly.
- Keep non-factory inbound links enumerated in issue #1019: agent capability/skill/CLI pages, generic guides, platform pages, integration token/CI pages, and cross-links among the three trigger pages. Their reader tasks remain standalone or shared. Preserve the skill and identity fragments.
- Keep the standalone Oz featured read at `warp-server/client/packages/agents/src/config/featuredReads.ts:33-36`, its URL constants, and generic cloud-loading tips in `warp/app/src/terminal/view/ambient_agent/tips.rs`.
- Leave unconsumed factory schedule/platform constants alone. An unused constant is not evidence of a visible customer link.
- Keep historical redirects in `vercel.json` and schedule protection in `scripts/fixtures/article-retirements.json`. No new redirect is required.

The issue holds the complete pinned inbound inventory, including each existing URL and fragment. Implementation records an outcome against that inventory; it does not need to repeat the broad audit.

### Delivery order and incomplete work

1. Obtain written approval of this committed spec.
2. Reuse this docs branch and draft PR for the documentation changes. Reconcile human edits to the spec before changing its requirements.
3. Verify new procedural claims and add the destination sections. Apply independent link corrections and the bounded standalone clarifications. Keep evidence and unresolved claims in the PR.
4. Publish the approved docs changes. Check each dependent destination on `https://docs.warp.dev`, including the rendered heading ID and absence of an unintended redirect.
5. Open the separate `warp-server` help-link PR. Cross-link it to this docs PR and issue #1019. Do not ship a product link to an unpublished heading.
6. Update the issue inventory with final old-to-new mappings, retained links, verification evidence, and incomplete gaps.

If a workflow cannot be verified:

- Deliver unrelated verified corrections without claiming the whole audit is complete.
- Do not invent labels, supported skills, permissions, availability, or configuration behavior.
- Keep dependent help links unchanged until equivalent verified instructions exist.
- Record each unresolved claim and affected link on the issue and in the PR's `Unverified claims` section.
- Use the repository's `VERIFY` marker only for draft content permitted by its quality policy. Resolve or remove such content before merge; a marker is not permission to publish an unverified procedure.
- Request the precise missing confirmation through the orchestrator. Existing unchanged instructions are retained, not re-certified.

## Decisions

| Choice | Alternatives and trade-offs | Decision |
| --- | --- | --- |
| Fix causes, not only URLs | Retargeting alone is smaller but strands readers at pages missing setup. Completing every shared migration would expand scope beyond the reported task. | Add Jira, Linear, recurring-automation, and factory cloud-environment procedures on existing owners; fix their dependent links. Leave GitHub/Slack shared migrations out. |
| Own cloud setup once | A new factory cloud page gives a factory URL but duplicates security-sensitive federation details. Leaving the shared page unchanged preserves duplication risk at zero but still sends factory users through Oz setup. | Add factory-specific sections to the shared cloud-provider page and deep-link them. |
| Preserve supported Oz workflows | Redirecting/removing simplifies navigation but breaks supported standalone web/CLI/API tasks and identity links. Keeping pages without clarification preserves the ambiguity. | Keep and clarify; no removals, redirects, or purpose changes. |
| Publish destinations first | Shipping both repositories without a release gate can expose dead anchors. One cross-repository atomic release is not available. | Publish and validate docs before product help changes ship. |
| Permit partial verified delivery | Holding every correction blocks known fixes on unavailable account access. Publishing unverified setup can create new errors. | Ship verified independent work; explicitly track unresolved procedures and dependent links as incomplete. |

### User decisions

- The requester confirmed: “yes please fix any of these wrong links, missing setup instructions, etc”.
- The orchestrator relayed this as affirmative answers to the three interview recommendations: include missing procedures, use shared AWS/GCP canonical content with factory sections, and allow verified partial delivery with incomplete tracking.
- Keep the existing supported standalone workflows and shared references. The issue already established this constraint; it was not reopened as a retirement question.
- No instruction waived the spec or its approval. This record does not claim final spec approval.

## Assumptions

- **Assumption:** Existing page ownership is sufficient. The listed gaps need sections, not new public pages.
- **Assumption:** No redirect or navigation reorganization is necessary while current URLs and page purposes remain intact.
- **Assumption:** Local/mock UI can prove destination rendering and route interaction, but not real provider installation, current customer entitlement, or production availability. Record those evidence classes separately.

## Out of scope

- Reimplementing the merged workspace Jira button fix in warp-server#21630.
- New integration behavior, broader grants, permission changes, backend schedules, or provider rollout.
- Retiring or repurposing supported Oz pages, replacing all `/platform/` links, or changing the `oz` binary and legacy web-app name.
- Full GitHub installation or Slack workspace-app content migration.
- New first-class Bitbucket support.
- Unrelated stale branding, billing/security policy rewrites, and unused-constant cleanup.
- Changing a customer's production integration, IAM role, schedule, or app installation to obtain evidence.

## Validation criteria

### Objective content and link checks

- **V1 — Inventory closure:** For every wrong-link and setup-gap row in issue #1019, the implementation PR/issue states source, old destination, final destination, and changed/retained/incomplete outcome. Compare the final diff to the matrices above. Incomplete rows name the blocker and unchanged dependent links.
- **V2 — Complete task paths:** Walk each new Jira, Linear, recurring-automation, AWS, and GCP procedure from its prerequisites through its success check. Cite live-product confirmation or the relevant source and availability evidence for each changed technical claim. Run `python3 .agents/skills/doc_quality_policy/server_rollout.py check jira linear schedule federation` from docs; inspect each result for relevance. A successful helper result alone does not prove UI access or release.
- **V3 — Links and anchors:** Run `python3 .agents/skills/check_for_broken_links/check_links.py --internal-only`. After the build, inspect each changed target's generated HTML in `.vercel/output/static/` and assert its fragment ID exists. Include product-link targets, which the docs-source scan cannot discover. Report unrelated baseline failures separately; no changed target may remain broken.
- **V4 — Standalone compatibility:** Run `npm run test:article-retirements` and `npm run test:platform-reference-migration`. Confirm the three trigger pages remain in navigation, the historic schedule redirect remains, and `#scheduling-a-skill` and `#run-identity-and-pull-request-authorship` still resolve. Compare the retained inbound groups above to the diff; no retained workflow is removed.
- **V5 — Docs repository checks:** Run `python3 .agents/skills/style_lint/style_lint.py --changed`, then `npm run typecheck`, `npm run test:heading-vars`, `npm run build`, `npm run test:heading-tocs`, and `npm run test:homepage-json-ld` in that order. Apply the selected drafting skills and current compression/PR-contract checks to public content. Record exact commands, results, and baseline failures.
- **V6 — Publication gate:** Before shipping dependent product changes, request each published target and open its exact fragment in a browser. Confirm the requested task heading renders. A 200 response without the right section is insufficient.

### Product regression checks

- **V7 — Literal help destinations:** Run the changed Vitest files, including `integration-education.test.tsx`, `urls.test.ts`, `JiraIntegrationConnect.test.tsx`, and `CloudProviderSetupModal.test.tsx`. From `warp-server/client`, use `yarn workspace @warp/factory test --run` with their package-relative paths. Changed rows must assert the exact URLs above; unchanged GitHub/Slack and team-scope mappings must still pass.
- **V8 — Type, lint, and build:** Run `yarn workspace @warp/factory type-check`. Run package-local ESLint and Prettier checks on changed files. Run `yarn workspace @warp/factory build:dev` successfully before computer-use verification. Follow the repository's selective validation rules rather than adding unrelated package-wide fixes.
- **V9 — Visual proof:** Use the computer-use tool to exercise the affected Jira connect help, personal Jira help, workspace/team Linear help, and factory AWS/GCP help. Capture video of opening the help and arriving at its task heading; include before/after screenshots for changed product surfaces per the factory UI skill. Use the built docs locally for pre-publication checks and the published docs for V6. Test destination rendering in MSW when real authentication is unavailable, and label that limit. Do not treat mock rendering as proof of a successful provider installation.
- **V10 — No false completion:** List every unavailable live/provider check and unresolved claim in the handoff. Never report skipped checks as passed. A partial delivery leaves the work item open with the exact remaining gaps.
