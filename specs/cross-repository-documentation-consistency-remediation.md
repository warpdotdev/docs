# Cross-repository documentation consistency remediation

## Summary

This work corrects factual drift across Warp documentation, the public pricing surface, and generated API reference content. It also extends the existing `missing_docs` skill so later audits account for stale and contradictory claims. The work changes documentation and detection only. It does not change product behavior, billing behavior, plan entitlements, privacy policy, or CLI compatibility.

The September 16, 2026 Falconer audit reported 19 contradictions and 5 content issues. Some reported claims have changed on `main` since that audit. Implementation must verify the current occurrence set before editing and must not restore an older claim merely to match the audit.

## Product behavior

1. A documented fact must agree with the shipped product behavior or released public API.
2. Every occurrence of a disputed fact must be found and classified before a correction merges.
3. A correction is incomplete while another owned public surface states an incompatible fact.
4. A surface outside `warpdotdev/docs`, such as `https://www.warp.dev/pricing`, must receive a coordinated change or an owner-approved blocker.
5. Product, Security, Privacy, Legal, Billing, Marketing, CLI, and Support decisions must not be inferred from implementation details.
6. Policy language must identify the data class, plan, setting, and provider to which the language applies.
7. Public documentation must use **Add-on Credits** as the product name.
8. Public documentation must use **auto-reload** only for the automatic purchase action.
9. Public API examples must use `POST /agent/runs` to create a run.
10. The deprecated `POST /agent/run` route must remain documented as deprecated compatibility only while the route remains released.
11. Cloud image attachment documentation must distinguish CLI run creation from the interactive cloud conversation UI.
12. Legacy `oz` documentation must remain available until a CLI owner confirms command parity and the final deprecation date.
13. The implementation must not change runtime behavior to make an existing documentation claim true.

## Technical design

### Evidence hierarchy

Use this order when resolving a factual conflict:

1. **Released public contract**
   - Use `developers/agent-api-openapi.yaml` for the released Agent API.
   - Use an approved policy or legal statement for privacy, training, retention, and provider commitments.
   - Use an owner-confirmed support matrix for support commitments.
2. **Shipped implementation**
   - Use the public `warpdotdev/warp` client for client defaults, limits, updater behavior, shell discovery, MCP startup, and CLI behavior.
   - Use shipped `warp-server` tier configuration for active plan limits and entitlements.
   - Use deployed server logic and tests for billing and deletion behavior.
3. **Product specifications**
   - Use product specifications for intent and terminology only after verifying behavior against shipped code and configuration.
   - Do not treat a merged specification as evidence that a feature shipped.
4. **Current public prose**
   - Treat documentation and marketing text as a surface to correct, not as independent proof of behavior.

The public documentation must not cite private `warp-server` source. Implementation PR descriptions can cite private source for reviewers.

### Occurrence and completeness workflow

For each finding:

1. Search the full docs repository for the quoted wording, close paraphrases, old terminology, route names, flags, and related links.
2. Search relevant implementation, configuration, tests, and released schemas.
3. Record every affected surface.
4. Classify the finding as one of:
   - `fix`
   - `policy_blocker`
   - `owner_confirmation`
   - `resolved_on_main`
   - `out_of_scope`
5. Record the authoritative source and the reason for the classification.
6. Apply the correction to every affected occurrence in the implementation batch.
7. Repeat the occurrence search after editing.
8. Do not close the finding if an incompatible owned occurrence remains unexplained.

The 24 Falconer findings below are the initial accounting set. New occurrences found during implementation belong to the same finding. They are not optional follow-up work.

### Billing, plan limits, and pricing

#### 1. Free codebase indexing limit

- **Status:** `fix`
- **Shipped behavior:** Free permits 5,000 files per repository.
- **Authority:** `../warp-server/billing/config/tiers/free.yaml:71-77`
- **Current docs:** `src/content/docs/agents/capabilities/codebase-context.mdx:93-98` already says at least 5,000 files.
- **Conflicting surface:** The public pricing page reported 3,000 files during the audit.
- **Required change:**
  - Keep the 5,000-file statement in the docs.
  - Update the public pricing surface to 5,000.
  - Do not reduce the docs value to match stale marketing copy.
- **Owner:** Product and Marketing for the pricing surface; Billing for entitlement confirmation.

#### 2. Scheduled and API-key run billing principal

- **Status:** `fix`
- **Shipped behavior:**
  - Unattended Build-family service-account traffic bills the team owner when individualized reload-credit behavior is enabled.
  - Free and Enterprise service-account traffic remains team-pooled.
- **Authority:** `../warp-server/logic/ai/ai_usage/cost_resolution.go:254-312`
- **Affected seeds:**
  - `src/content/docs/platform/triggers/scheduled-agents.mdx`
  - `src/content/docs/reference/cli/api-keys.mdx`
  - `src/content/docs/platform/team-access-billing-and-identity.mdx`
  - `src/content/docs/support-and-community/plans-and-billing/pricing-faqs.mdx`
- **Required change:**
  - State the plan-specific billing principal once in the canonical billing page.
  - Make schedule and API-key pages link to that canonical explanation.
  - Remove the blanket statement that all scheduled usage draws directly from a shared team balance.

#### 3. Add-on Credits pool for API-key runs

- **Status:** `fix`
- **Shipped behavior:** After applicable plan credits, bonus grants are selected in team, workspace, then user order.
- **Authority:** `../warp-server/model/ai_request_bonus_grants.go:101-151`
- **Required change:**
  - Remove the statement that the owner's personal Add-on Credits balance is always the second bucket.
  - Describe applicable team or workspace grants before legacy user-scoped grants.
  - Do not describe every applicable grant as a single “team-wide” pool when workspace or legacy user grants can apply.

#### 4. First bucket for a user-triggered cloud run

- **Status:** `fix`
- **Shipped behavior:**
  - An eligible grant restricted to cloud-agent usage is checked first for a cloud request with a user principal.
  - Plan credits are checked next.
  - Applicable bonus grants are checked after plan credits.
- **Authority:** `../warp-server/logic/ai/ai_usage/cost_resolution.go:166-212`
- **Terminology constraint:** Do not publish the internal name `ambient_only`.
- **Required wording:** Use a descriptive phrase such as “credits restricted to cloud agent runs” unless Product approves a dedicated customer-facing name.
- **Required change:** Consolidate the two incompatible waterfalls in `src/content/docs/platform/team-access-billing-and-identity.mdx`.

#### 5. Team deletion with remaining Add-on Credits

- **Status:** `fix`
- **Shipped behavior:** A positive remaining balance on active team grants blocks team deletion.
- **Authority:**
  - `../warp-server/logic/workspace_memberships.go:469-483`
  - `../warp-server/test/integration/delete_team_test.go:87-109`
- **Affected seeds:**
  - `src/content/docs/support-and-community/plans-and-billing/add-on-credits.mdx`
  - `src/content/docs/support-and-community/plans-and-billing/pricing-faqs.mdx`
- **Required change:** State that the admin must use or remove the remaining credits before deleting the team. Remove the claim that deletion succeeds and makes the credits unusable.

#### 6. “Reload credits” versus “Add-on Credits”

- **Status:** `fix`
- **Decision:** Use **Add-on Credits** as the product name. Use **auto-reload** for the automatic purchase action.
- **Affected surfaces:** Search all docs, UI-facing support copy, and public pricing copy for `reload credits`, `Reload credits`, and close variants.
- **Required change:**
  - Replace noun-form “reload credits” with “Add-on Credits.”
  - Keep “auto-reload” where it names the automatic purchase setting or action.
  - Do not rename API fields, schema identifiers, or historical changelog entries.

#### 7. Free third-party harness entitlement

- **Status:** `fix`
- **Shipped behavior:** Free cloud runs use the Warp Agent harness. Paid self-serve plans enable third-party harnesses.
- **Authority:**
  - `../warp-server/billing/config/tiers/free.yaml:149-152`
  - `../warp-server/billing/config/tiers/_base_self_serve_plan.yaml:46-48`
- **Affected seeds:**
  - `src/content/docs/platform/harnesses/index.mdx`
  - `src/content/docs/support-and-community/plans-and-billing/pricing-faqs.mdx`
  - Public pricing
- **Required change:**
  - Keep or restore the Build-or-higher requirement in product documentation.
  - Remove “available to all users” for third-party harness selection.
  - Correct the public pricing claim that Free can use any harness.
  - Do not announce a planned entitlement before its configuration ships.

### Privacy, training, telemetry, and Secret Redaction

#### 8. Customer-data training claims

- **Status:** `policy_blocker`
- **Conflicting seeds:**
  - `src/content/docs/agents/getting-started/faqs.mdx:22-26`
  - `src/content/docs/index.mdx:111-119`
- **Problem:** The pages conflate Warp's rights and practices with model-provider commitments.
- **Required owner input:** Privacy, Security, and Legal must provide approved statements for:
  - customer AI inputs and outputs;
  - console input and output;
  - product telemetry;
  - user-generated content collection;
  - model-provider training;
  - Warp model or product improvement;
  - plan and setting differences.
- **Merge gate:** No production correction for this finding can merge until the approved matrix exists.
- **Prohibited resolution:** Do not choose either existing absolute statement as the source of truth.

#### 9. Configurable AI Secret Redaction versus telemetry redaction

- **Status:** `fix`
- **Shipped behavior:**
  - User-configurable Secret Redaction for terminal and AI content defaults to disabled.
  - Enterprise policy can enable the user-visible behavior.
  - Telemetry payload redaction always includes default patterns and can include user and enterprise patterns.
- **Authority:**
  - `../warp/app/src/terminal/safe_mode_settings.rs:67-79`
  - `../warp/app/src/terminal/safe_mode_settings.rs:103-114`
  - `../warp/app/src/server/telemetry/secret_redaction.rs:11-59`
- **Affected seeds:**
  - `src/content/docs/support-and-community/privacy-and-security/secret-redaction.mdx`
  - `src/content/docs/support-and-community/privacy-and-security/privacy.mdx`
  - `src/content/docs/enterprise/security-and-compliance/security-overview.mdx`
- **Required change:**
  - Describe the two mechanisms separately.
  - Remove claims that user-configurable AI redaction is universally automatic or unconditional.
  - Do not state that sensitive data is “never” collected or sent unless Security approves that exact guarantee and scope.
  - Preserve Enterprise policy behavior without claiming that every Enterprise interaction has the same client-side default.

#### 10. Secret Redaction described as unconditional next to its toggle

- **Status:** `fix`
- **Conflicting surface:** `src/content/docs/support-and-community/privacy-and-security/privacy.mdx`
- **Problem:** The page calls Secret Redaction unconditional while its telemetry table documents an on/off setting for the same named feature.
- **Required change:**
  - Name configurable AI and terminal Secret Redaction separately from telemetry payload redaction.
  - Make each statement point to the applicable setting or unconditional telemetry path.
  - Remove the self-contradiction in both prose and the telemetry table.

#### 11. Secret Redaction regex case behavior

- **Status:** `fix`
- **Shipped behavior:** Regexes are case-sensitive by default. Prefixing a pattern with `(?i)` makes that pattern case-insensitive.
- **Authority:** `../warp/app/src/settings_view/privacy_page.rs:74-78`
- **Affected surface:** `src/content/docs/support-and-community/privacy-and-security/secret-redaction.mdx`
- **Required change:** Correct the second sentence and keep one example that matches `PASSWORD`, `Password`, and `password`.

#### 12. Free telemetry opt-out and AI availability

- **Status:** `policy_blocker`
- **Conflicting seeds:**
  - `src/content/docs/support-and-community/privacy-and-security/privacy.mdx:30-38`
  - `src/content/docs/support-and-community/plans-and-billing/pricing-faqs.mdx`
  - `src/content/docs/enterprise/security-and-compliance/security-overview.mdx`
- **Implementation evidence:** Free tier telemetry policy is not user-toggleable in `../warp-server/billing/config/tiers/free.yaml:54-57`, but code does not settle the complete customer-facing retention and AI-availability contract.
- **Required owner input:** Product, Privacy, and Legal must state:
  - whether a Free user can disable **Help improve Warp**;
  - whether disabling it disables Warp-provided AI, purchased-credit AI, BYOK, or custom endpoints;
  - whether “full ZDR” is the correct name for this setting;
  - what data still persists for cloud conversations and run operation.
- **Merge gate:** Do not rewrite this behavior from tier configuration alone.

#### 13. Fireworks AI in ZDR provider lists

- **Status:** `policy_blocker`
- **Affected seeds:**
  - `src/content/docs/enterprise/security-and-compliance/security-overview.mdx`
  - `src/content/docs/support-and-community/plans-and-billing/pricing-faqs.mdx`
  - `src/content/docs/agents/inference/model-choice.mdx`
- **Required owner input:** Security and Legal must confirm the current Fireworks contract and any model-specific exceptions.
- **Required change after approval:** Use one approved provider list and one approved qualification everywhere.
- **Prohibited resolution:** Do not add Fireworks to a contractual claim merely because a model page names Fireworks as a host.

### Agent API, legacy CLI, Warp Agent CLI, MCP, and attachments

#### 14. Canonical create-run route

- **Status:** `fix`
- **Released behavior:** Both routes work. `POST /agent/runs` is canonical. `POST /agent/run` is deprecated.
- **Authority:**
  - `../warp-server/router/handlers/public_api/agent_webhooks.go:271-327`
  - `developers/agent-api-openapi.yaml:118-234`
- **Affected seed:** `src/content/docs/reference/api-and-sdk/index.mdx`
- **Required change:**
  - Use the plural route in overview prose, endpoint lists, examples, and factory guidance.
  - Keep the singular route in the generated reference with its deprecation marker.
  - Do not remove server compatibility in this work.

#### 15. Run-list config-name filter

- **Status:** `fix`
- **Released behavior:** `GET /agent/runs` accepts `name`.
- **Authority:** `../warp-server/router/handlers/public_api/agent_webhooks.go:2810-2820`
- **Affected seed:** `src/content/docs/reference/api-and-sdk/index.mdx`
- **Required change:** Replace `config_name` with `name` in prose and endpoint summaries. Verify the OpenAPI parameter remains `name`.

#### 16. Cloud image attachments

- **Status:** `fix`
- **Shipped behavior:**
  - Legacy CLI cloud-run creation accepts repeated `--attach` inputs when the released feature is enabled.
  - A run accepts at most 25 attachments.
  - Each attachment accepts at most 10 MB.
  - The interactive cloud conversation UI does not expose toolbar, paste, or drag-and-drop image attachment.
- **Authority:**
  - `../warp/app/src/ai/agent_sdk/ambient.rs:380-421`
  - `../warp/app/src/ai/agent_sdk/driver/attachments.rs:18-25`
  - `../warp/app/src/ai/attachment_utils.rs:10-12`
- **Affected seeds:**
  - `src/content/docs/reference/cli/index.mdx`
  - `src/content/docs/platform/faqs.mdx`
- **Required change:**
  - Change the CLI maximum from 5 to 25.
  - Add the 10 MB per-attachment limit.
  - Keep the platform FAQ limitation, but scope it to the interactive cloud conversation UI.
  - Cross-link the CLI capability from the FAQ.
  - Keep this capability documented during the `oz` migration until a verified `warp` equivalent replaces it.

#### 17. MCP behavior under the default legacy CLI profile

- **Status:** `fix`
- **Shipped behavior:**
  - The default profile permits MCP actions but starts with an empty profile MCP allowlist.
  - Explicit `--mcp` specifications can start run-scoped servers.
  - A selected profile can start allowlisted installed servers.
  - Eligible file-based/global servers follow their own startup path.
  - The built-in Factory MCP server has separate feature, authentication, and name-collision gates.
- **Authority:**
  - `../warp/crates/cloud_object_models/src/ai_execution_profile.rs:375-448`
  - `../warp/app/src/ai/agent_sdk/driver/mcp_startup.rs:397-434`
  - `../warp/app/src/ai/agent_sdk/driver/mcp_startup.rs:564-651`
- **Affected seeds:**
  - `src/content/docs/reference/cli/quickstart.mdx`
  - `src/content/docs/reference/cli/agent-profiles.mdx`
  - `src/content/docs/reference/cli/mcp-servers.mdx`
- **Required change:**
  - Remove “loads any available MCP servers.”
  - Remove “does not have the ability to use MCP servers by default.”
  - Explain selection and startup separately.
  - Do not imply that every configured server starts for every run.

#### 18. Warp Agent CLI updater behavior

- **Status:** `fix`
- **Shipped behavior:**
  - Native managed installs check, download, and stage updates.
  - Recognized Homebrew installs check for updates and instruct the user to run `brew upgrade --cask warp-agent-cli`.
  - Unmanaged installs do not use either managed update path.
- **Authority:** `../warp/crates/warp_tui/src/autoupdate.rs:1-27` and `../warp/crates/warp_tui/src/autoupdate.rs:145-181`
- **Affected seeds:**
  - `src/content/docs/agents/cli/reference.mdx`
  - `src/content/docs/agents/cli/quickstart.mdx`
- **Required change:** Replace the unconditional updater statement in the reference with the install-method matrix already described in the quickstart.

#### 19. `oz` to `warp` migration

- **Status:** `owner_confirmation`
- **Current state:**
  - `src/content/docs/reference/cli/**` documents the legacy `oz` command tree and automation workflows.
  - `src/content/docs/agents/cli/**` documents the interactive `warp` TUI.
  - Existing notices state that `oz` remains supported through September 30, 2026.
  - Current repository terminology guidance reserves the `oz` CLI binary and Oz v1 web app names through October 6, 2026.
- **Decision:** Retain legacy documentation until a CLI owner confirms workflow parity and the final deprecation date.
- **Required work:**
  - Inventory every `oz` workflow and command in `src/content/docs/reference/cli/**`.
  - Map each workflow to a verified `warp` equivalent, `no equivalent`, or `owner confirmation required`.
  - Replace or redirect only verified equivalents.
  - Preserve one explicit migration or legacy page for unsupported automation workflows.
  - Keep factual corrections to legacy pages, including attachments and MCP, while those pages remain public.
  - Align transition notices to October 6, 2026 unless the CLI owner approves a later date before implementation.
- **Merge gate:** Do not remove the legacy section or change the support deadline without CLI-owner approval.
- **Owner:** Warp Agent CLI and Automation Platform.

### Terminal and support documentation

#### 20. Windows fish support

- **Status:** `owner_confirmation`
- **Implementation evidence:** Windows shell discovery can find MSYS2 bash, zsh, and fish when the relevant feature is enabled.
- **Authority for discovery:** `../warp/app/src/terminal/available_shells.rs:648-718` and `../warp/app/src/terminal/available_shells.rs:786-806`
- **Conflicting seeds:**
  - `src/content/docs/getting-started/supported-shells.mdx`
  - `src/content/docs/support-and-community/troubleshooting-and-support/known-issues.mdx`
- **Decision:** Discovery is not proof of an official support commitment.
- **Required change before confirmation:** Remove the broad statement that every named shell is supported across every operating system. Keep the explicit supported Windows list.
- **Required owner input:** Terminal and Support must confirm whether MSYS2 fish is officially supported.
- **Follow-up:** Add fish to the Windows list only after that confirmation.

#### 21. macOS Ventura updater warning

- **Status:** `fix`
- **Current state:** `known-issues.mdx` says the incident is resolved. `updating-warp.mdx` still presents an October 2022 warning.
- **Required change:**
  - Remove the active warning from `src/content/docs/support-and-community/troubleshooting-and-support/updating-warp.mdx`.
  - Keep historical context only in the changelog or a clearly historical note.
  - Remove obsolete prevention instructions from current known issues if they no longer help current releases.

#### 22. Remote shell selected by legacy SSH

- **Status:** `fix`
- **Shipped behavior:**
  - The legacy wrapper inspects and preserves the remote `$SHELL`.
  - Enhanced bootstrap supports bash and zsh.
  - Other remote shells continue without the enhanced Warp bootstrap.
- **Authority:**
  - `../warp/app/assets/bundled/bootstrap/bash_body.sh`
  - `../warp/app/assets/bundled/bootstrap/zsh_body.sh`
  - `../warp/crates/integration/src/test/ssh.rs`
- **Affected seeds:**
  - `src/content/docs/support-and-community/troubleshooting-and-support/known-issues.mdx`
  - `src/content/docs/terminal/warpify/ssh-legacy.mdx`
- **Required change:** Remove “we start a bash shell.” State that Warp preserves the remote login shell and only enhances supported bash or zsh sessions.

### Structural and already-resolved audit items

#### 23. Stale cloud concurrency placeholder

- **Status:** `resolved_on_main`
- **Audit claim:** Cloud FAQs said that concurrency and credit allocation were still being finalized.
- **Current result:** The quoted placeholder is absent from current `src/content/docs/platform/faqs.mdx`.
- **Required work:** Confirm the phrase and close paraphrases remain absent. Record the finding as resolved rather than editing unrelated current copy.
- **Detector requirement:** Preserve this as a regression seed so the stale placeholder cannot return.

#### 24. Session Sharing redirect stub and stale inbound links

- **Status:** `fix`
- **Current state:** `src/content/docs/knowledge-and-collaboration/session-sharing/index.mdx` is a move notice rather than a feature page. Secondary pages still link to the old path.
- **Canonical destinations:**
  - Use `/agents/local-agents/session-sharing/` for agent and terminal session sharing behavior.
  - Use the applicable cloud-run sharing page when the source sentence is specifically about cloud runs.
- **Affected seeds:**
  - `src/content/docs/support-and-community/plans-and-billing/pricing-faqs.mdx`
  - `src/content/docs/support-and-community/troubleshooting-and-support/using-warp-offline.mdx`
  - `src/content/docs/terminal/more-features/settings-sync.mdx`
  - `src/content/docs/support-and-community/troubleshooting-and-support/known-issues.mdx`
- **Required change:**
  - Search all inbound links to `/knowledge-and-collaboration/session-sharing/`.
  - Replace each link with the correct canonical destination.
  - Add or verify a repository redirect for old external URLs.
  - Do not create another duplicate explanation.

#### Audit summary note: broad security and GitHub permission scoping

- **Audit context:** The audit summary mentioned broad security and GitHub permission scoping, but its detailed finding set did not identify a separate reproducible GitHub-permission contradiction.
- **Required work:**
  - Search current integration and security pages for repository-scope and permission claims.
  - Record any concrete mismatch as a new finding with code or integration configuration evidence.
  - Do not invent a correction without a reproducible current occurrence.
  - Route broad security guarantees through the owner gate in findings 8, 12, and 13.

### Missing-docs consistency detection

Extend `.agents/skills/missing_docs` instead of creating a new skill.

#### Workflow changes

The skill must:

1. Accept an external audit or user-reported contradiction as a seed.
2. Normalize every seed into a stable identifier and concise claim pair.
3. Search beyond the quoted pages for all semantic and exact-string occurrences.
4. Require at least one authoritative source or an explicit owner blocker.
5. Emit one of the approved statuses for every seed.
6. Include all affected surfaces and remaining occurrences.
7. Fail completeness accounting when a seed has no status, evidence, or occurrence disposition.
8. Re-run deterministic consistency rules during drift-watch mode.
9. Report policy blockers without drafting policy language.
10. Leave style, broken-link, UI-path, OpenAPI synchronization, and weekly 404 checks with their existing skills.

#### Persistent rule and decision data

Add a machine-readable consistency seed file under `.agents/skills/missing_docs/references/`. Each entry must include:

```json
{
  "id": "api-create-run-path",
  "claim": "Create-run examples use the canonical plural route.",
  "status": "fix",
  "occurrence_queries": ["POST /agent/run", "POST /agent/runs"],
  "authoritative_sources": [
    "developers/agent-api-openapi.yaml",
    "../warp-server/router/handlers/public_api/agent_webhooks.go"
  ],
  "affected_surfaces": [
    "src/content/docs/reference/api-and-sdk/index.mdx"
  ],
  "recheck_condition": "Any create-run example changes."
}
```

The exact filename and internal Python type can follow repository conventions. The fields and accounting behavior are required.

Policy blockers must include:

- the functional owner;
- the exact unresolved question;
- the merge or recheck condition;
- the surfaces that remain inconsistent.

#### Audit output

Add `consistency` to the audit categories. JSON output must expose:

- the total seed count;
- counts by status;
- unaccounted seed IDs;
- findings with authority and affected surfaces;
- blockers with owners and recheck conditions;
- deterministic rules that passed or failed.

An unaccounted seed must add `integrity:consistency_accounting` to `audits_skipped` and exit with code 2.

#### Tests

Extend `test_audit_docs.py` with fixtures that prove:

- every seed enters exactly one status bucket;
- an unaccounted seed exits 2;
- a forbidden stale statement produces a finding;
- a resolved statement produces no active finding but remains tracked;
- a policy blocker remains visible and does not trigger drafting;
- multiple affected occurrences are all reported;
- existing category and severity filters still work;
- consistency mode does not duplicate broken-link or style-lint findings.

### Implementation decomposition

The draft spec PR is the approval anchor. No production change starts before approval.

After approval, reuse the spec branch and PR for the first implementation batch. Keep the specification in the branch as the durable contract. Use focused commits and reviewer checkpoints. If repository maintainers require smaller PRs, split later batches into linked PRs that reference this specification.

Recommended batches:

1. **API and CLI factual corrections**
   - Canonical create-run route.
   - `name` filter.
   - Attachment limits and UI distinction.
   - MCP startup semantics.
   - Install-method updater behavior.
2. **Billing and plan corrections**
   - Billing principals and waterfalls.
   - Team deletion.
   - Add-on Credits terminology.
   - Free index and harness entitlements.
   - Coordinated public pricing changes in the owning website repository.
3. **Terminal and navigation corrections**
   - Regex case behavior.
   - Ventura cleanup.
   - SSH shell behavior.
   - Session Sharing links and redirect.
   - Windows shell wording that does not require the unresolved fish decision.
4. **Consistency detector**
   - Seed store.
   - Consistency audit category.
   - Accounting.
   - Tests and skill instructions.
5. **Owner-gated privacy and security corrections**
   - Training and Warp data use.
   - Free telemetry and AI behavior.
   - Fireworks ZDR coverage.
   - Any absolute security guarantees.
6. **Owner-gated CLI migration**
   - Command-parity inventory.
   - Confirmed redirects.
   - Legacy landing page.
   - Final deprecation wording.
7. **Owner-gated Windows support follow-up**
   - MSYS2 fish support statement after Terminal and Support confirmation.

The privacy, CLI migration, and Windows fish batches must not block deterministic corrections in the other batches.

### Reviewer routing

Route review from the source file behind each fact:

- **Billing and credits:** `../warp-server/logic/ai/ai_usage/`, `../warp-server/model/ai_request_bonus_grants.go`, and `../warp-server/billing/`.
- **API:** `../warp-server/router/handlers/public_api/` and the OpenAPI owners.
- **MCP:** `../warp/app/src/ai/mcp/`, `../warp/app/src/ai/agent_sdk/driver/mcp_startup.rs`, and `../warp/crates/mcp/`.
- **Attachments and cloud CLI:** `../warp/app/src/ai/agent_sdk/` and `../warp/app/src/ai/attachment_utils.rs`.
- **Warp Agent CLI updater:** `../warp/crates/warp_tui/`.
- **Shells and SSH:** `../warp/app/src/terminal/available_shells.rs`, `../warp/app/src/terminal/warpify/`, and `../warp/app/assets/bundled/bootstrap/`.
- **Privacy and policy:** Privacy, Security, and Legal, regardless of code ownership.
- **Public pricing:** Product Marketing and Billing.

Use `.github/STAKEHOLDERS` and `.github/CODEOWNERS` through the existing reviewer resolver. Request at most one individual reviewer per focused PR when exactly one owner resolves. Do not guess a reviewer when ownership is unresolved or shared.

## Decisions

### Documentation correction versus product change

- **Option A:** Change runtime behavior to match current prose.
  - **Advantage:** Preserves public wording.
  - **Disadvantage:** Turns a documentation audit into unplanned product, billing, entitlement, and privacy work.
- **Option B:** Align documentation to shipped behavior and escalate policy conflicts.
  - **Advantage:** Corrects user guidance without hidden product changes.
  - **Disadvantage:** Requires coordinated changes to non-doc surfaces and owner decisions.
- **Decision:** Choose Option B.

### Runtime configuration versus public pricing

- **Option A:** Treat the pricing page as the intended future state.
  - **Advantage:** Avoids a marketing edit if a launch is imminent.
  - **Disadvantage:** Documents access that users do not have.
- **Option B:** Treat shipped configuration as the current entitlement.
  - **Advantage:** Users receive behavior that matches the docs.
  - **Disadvantage:** Requires public pricing corrections.
- **Decision:** Choose Option B until a product change ships.

### Credit terminology

- **Option A:** Rename all Add-on Credits to reload credits.
  - **Advantage:** Matches one pricing surface.
  - **Disadvantage:** Conflicts with current docs, app copy, API terminology, and purchase behavior.
- **Option B:** Keep Add-on Credits as the product name and auto-reload as the action.
  - **Advantage:** Matches the broadest shipped vocabulary and distinguishes product from automation.
  - **Disadvantage:** Requires a public pricing copy change.
- **Decision:** Choose Option B.

### Privacy conflict resolution

- **Option A:** Select the broadest privacy promise.
  - **Advantage:** Produces simple copy.
  - **Disadvantage:** Risks an unsupported legal or security guarantee.
- **Option B:** Select the most permissive data-use statement.
  - **Advantage:** Avoids overpromising.
  - **Disadvantage:** Can understate contractual protections and still lacks approved scope.
- **Option C:** Block the policy correction until owners supply a scoped matrix.
  - **Advantage:** Preserves factual and legal uncertainty.
  - **Disadvantage:** Leaves the policy batch open longer.
- **Decision:** Choose Option C.

### Legacy CLI migration

- **Option A:** Remove the `oz` section at the stated deadline.
  - **Advantage:** Removes stale product naming quickly.
  - **Disadvantage:** Drops workflows with no verified `warp` equivalent.
- **Option B:** Keep all legacy pages unchanged.
  - **Advantage:** Preserves every workflow.
  - **Disadvantage:** Leaves stale deadlines and duplicative navigation.
- **Option C:** Inventory parity, redirect verified equivalents, and retain one explicit legacy path for gaps.
  - **Advantage:** Prevents content loss and supports an evidence-based migration.
  - **Disadvantage:** Requires CLI-owner review.
- **Decision:** Choose Option C.

### Cloud attachment wording

- **Option A:** Say cloud agents do not support images.
  - **Advantage:** Matches the interactive UI limitation.
  - **Disadvantage:** Hides the working CLI capability.
- **Option B:** Say cloud agents support images.
  - **Advantage:** Advertises the CLI capability.
  - **Disadvantage:** Misleads interactive UI users.
- **Option C:** Document each input surface separately.
  - **Advantage:** States both behaviors without contradiction.
  - **Disadvantage:** Requires an extra qualification and cross-link.
- **Decision:** Choose Option C.

### Windows fish

- **Option A:** Treat discovery as official support.
  - **Advantage:** Matches the client path.
  - **Disadvantage:** Infers a support commitment from implementation.
- **Option B:** Keep calling fish unsupported.
  - **Advantage:** Preserves the current Support claim.
  - **Disadvantage:** Can conflict with enabled discovery and launch.
- **Option C:** Narrow the broad claim and wait for a Support-owner decision.
  - **Advantage:** Avoids both unsupported inferences.
  - **Disadvantage:** Leaves one explicit follow-up.
- **Decision:** Choose Option C.

### Detector placement

- **Option A:** Create a separate consistency skill.
  - **Advantage:** Isolates new behavior.
  - **Disadvantage:** Duplicates audit orchestration, source discovery, accounting, and drift-watch behavior.
- **Option B:** Extend `missing_docs`.
  - **Advantage:** Reuses the existing audit, source hierarchy, completeness accounting, and tests.
  - **Disadvantage:** Increases the skill's scope.
- **Decision:** Choose Option B with explicit boundaries against style and link checks.

## Assumptions

- **Assumption:** `warpdotdev/docs@main`, `warpdotdev/warp@master`, and `warp-server@develop` represent the current implementation baseline researched on September 24, 2026.
- **Assumption:** The public pricing claims observed during research are owned outside `warpdotdev/docs`.
- **Assumption:** The singular Agent API route remains released compatibility because the OpenAPI schema marks it deprecated rather than removed.
- **Assumption:** No approved customer-facing name exists for `ambient_only`; implementation will use descriptive wording.
- **Assumption:** The missing-docs consistency detector can use curated rules for deterministic claims and agent research for semantic claims.
- **Assumption:** A policy-blocked batch can remain open without blocking unrelated deterministic corrections.

## Out of scope

- Runtime billing, grant-order, deletion, entitlement, shell, updater, MCP, attachment, or API behavior changes.
- New privacy, retention, training, or contractual policy.
- Adding Fireworks to a contractual provider list without approval.
- Implementing missing `warp` CLI command parity.
- Ending `oz` support or removing server/API compatibility.
- Declaring MSYS2 fish supported without Terminal and Support approval.
- Duplicating style lint, broken-link checks, UI-reference validation, OpenAPI synchronization, or the weekly 404 monitor.
- Rewriting historical changelog entries to current terminology.
- Publishing private server implementation details in customer documentation.

## Validation criteria

### Finding accounting

- Check all 24 findings in this specification.
- Record one approved status, authority, affected-surface set, and disposition for each finding.
- Fail the implementation review if any current occurrence is unclassified.
- Run this command after the consistency detector batch is implemented. It is not expected to exist on the spec-only branch.
- Check with:

```bash
python3 .agents/skills/missing_docs/scripts/audit_docs.py --category consistency --output /tmp/consistency-audit.json
```

- Expected result: exit 0, an empty `unaccounted` list, and no unresolved `fix` finding in an implementation batch marked complete.

### Deterministic source checks

- Verify Free limits from `../warp-server/billing/config/tiers/free.yaml`.
- Verify paid harness override from `../warp-server/billing/config/tiers/_base_self_serve_plan.yaml`.
- Verify billing order and principals from the cited cost-resolution and grant-query files.
- Verify team deletion with the existing integration test.
- Verify API routes and query names from the released OpenAPI schema and handler.
- Verify attachment count and size constants from the client.
- Verify updater behavior from install-method tests.
- Verify MCP startup categories from profile and driver tests.

No runtime source file changes are expected.

### Repository tests

Run from the docs repository:

```bash
python3 .agents/skills/missing_docs/scripts/test_audit_docs.py
python3 .agents/skills/missing_docs/scripts/test_suggest_reviewers.py
python3 .agents/skills/missing_docs/scripts/test_check_new_release.py
npm run typecheck
npm run build
python3 .agents/skills/check_for_broken_links/check_links.py --internal-only
python3 .agents/skills/style_lint/style_lint.py --changed
```

Expected result: every command exits 0.

### API validation

- Run the existing OpenAPI synchronization workflow rather than hand-editing generated output.
- Confirm the generated API reference:
  - presents `POST /agent/runs` as canonical;
  - marks `POST /agent/run` deprecated;
  - documents `name`, not `config_name`.
- Search API prose and examples for `POST /agent/run` after editing. Every remaining singular occurrence must explicitly discuss deprecated compatibility.

### Billing validation

- Search all docs for scheduled-run, API-key, cloud-credit, plan-credit, add-on-credit, reload-credit, and team-deletion claims.
- Confirm the canonical billing page contains one complete waterfall.
- Confirm secondary pages link to the canonical explanation instead of restating a partial waterfall.
- Confirm no current page says team deletion succeeds with a positive remaining Add-on Credits balance.

### Privacy validation

- Require written approval from Privacy, Security, and Legal before merging findings 8, 12, or 13.
- The approval must cover the exact final statements, not only the general topic.
- Search the full docs repository for `never`, `unconditionally`, `all contracted`, `full ZDR`, `train`, `training`, `retain`, `stored`, and every named provider.
- Classify each relevant occurrence against the approved matrix.

### CLI migration validation

- Produce a command-parity inventory for every page under `src/content/docs/reference/cli/`.
- Require CLI-owner approval for the final deprecation date and every redirect that removes legacy detail.
- Confirm unsupported workflows remain reachable from one explicit legacy or migration page.

### Cross-repository validation

- Verify `https://www.warp.dev/pricing` after coordinated changes.
- Confirm the live surface shows:
  - 5,000 Free indexed files;
  - the Warp Agent as the only cloud harness on Free;
  - Add-on Credits as the product name.
- If a coordinated repository change cannot ship in the same release, attach an owner-approved blocker with a URL and expected completion condition.

### Visual proof

Documentation pages are static UI. After a successful build, use the computer-use tool to capture screenshots of the rendered changed states:

- canonical billing waterfall;
- Agent API create-run and filter guidance;
- CLI attachment or updater guidance;
- corrected shell or SSH guidance;
- privacy guidance only after policy approval.

Screenshots must show the relevant heading and corrected statement. A video is not required for static documentation.
