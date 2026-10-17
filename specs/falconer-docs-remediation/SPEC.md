# Falconer documentation remediation
## Summary
Remediate all 24 findings in the current Falconer audit of Warp documentation. The work corrects billing, plan entitlement, privacy, security, API, CLI, and product-behavior claims. It also restores canonical terminal Session Sharing documentation. The implementation must use current released behavior as its source of truth, preserve provider-scoped Zero Data Retention language, and avoid changes to the consistency-audit tooling in docs PR #829 or the automation in docs-factory-config PR #14.
## Current state and source authority
The Falconer report contains 19 contradictions and 5 content issues. The findings were checked against the current `warpdotdev/docs` `main` branch, released billing-tier configuration, the released OpenAPI document, the public Warp client, the Warp server, and duplicate occurrences in the docs.

Use these source-authority rules during implementation:

* **Billing and plan behavior** - Use the effective released tier configuration in `../warp-server/billing/config/tiers/` and the released billing behavior. Do not change a released entitlement to match marketing copy.
* **API behavior** - Use `developers/agent-api-openapi.yaml`. The plural `POST /agent/runs` path is canonical. The singular `POST /agent/run` path is deprecated.
* **CLI and product behavior** - Use visible released behavior in `../warp/`. Do not publish an unreleased symbol or hidden feature as current behavior.
* **Privacy and security** - Use the policy decisions in this specification. Source code can establish settings behavior, but it cannot establish a legal promise.
* **Terminology** - Use `.agents/references/terminology.md`. “Add-on credits” names purchased credit grants. “Auto-reload” names the mechanism that purchases another add-on credit bundle.
* **Conflicting public marketing copy** - Keep docs aligned with released behavior. Record the marketing mismatch as an external follow-up. Do not introduce incorrect docs copy for temporary cross-surface consistency.

No implementation PR may modify these paths:

* `.agents/skills/docs_consistency_audit/`
* `.agents/logs/docs_consistency_audit_runs.md`
* any path in `warpdotdev/docs-factory-config`

## Product behavior
1. The Codebase Context page states that Free supports 5,000 files per repository and Build, Max, and Business support 100,000 files per repository. The page links to pricing for other plan details.
2. On self-serve team plans, scheduled runs and agent-API-key runs charge the team owner. They consume the owner’s plan-included credits first, then the team’s shared add-on credit pool.
3. A user-triggered cloud run consumes an applicable cloud-agent grant before the user’s plan-included credits. It then consumes the team’s shared add-on credit pool. The cloud-agent grant does not apply to local runs, schedules, or agent-API-key runs.
4. Warp-owned docs do not claim that Warp trains models on collected customer data. Docs state only that contracted model providers do not train on Warp-managed traffic under their ZDR agreements.
5. Secret Redaction is off by default for an individual user. An Enterprise administrator can enforce Secret Redaction for the organization. An enforced setting cannot be disabled by an individual member.
6. A Free user can turn off **Help improve Warp**. A user on another plan can also turn it off unless an organization policy enforces the setting. Turning it off stops eligible user-generated content from being sent for Warp analytics and improvement. It does not disable AI.
7. Provider ZDR and Warp’s **Help improve Warp** setting remain separate concepts:
   * Provider ZDR applies to Warp-managed traffic sent to contracted model providers.
   * **Help improve Warp** controls Warp’s collection of eligible user-generated content for analytics and product improvement.
   * Docs do not call the user toggle “full ZDR.”
8. Third-party cloud harnesses require Build or a higher plan. Free cloud runs use Warp Agent.
9. A cloud agent prompt accepts image attachments. The CLI and API support up to five image attachments per request.
10. New API examples use `POST /agent/runs`. Existing references to `POST /agent/run` identify it only as a deprecated compatibility path.
11. `GET /agent/runs` uses the `name` query parameter to filter by agent configuration name.
12. The inline regex flag `(?i)` makes a Secret Redaction pattern case-insensitive.
13. Fish is supported on macOS and Linux. Fish is not supported on Windows.
14. The macOS Ventura auto-update issue is resolved and is not presented as an active limitation.
15. Warp blocks team deletion while the team has remaining add-on credits. The docs do not state that team deletion silently forfeits those credits.
16. A direct Warp Agent CLI installation can update itself. A Homebrew installation updates through Homebrew and does not self-update.
17. The default legacy Agent Profile loads available MCP servers. Command execution uses **Agent decides**, subject to the profile’s denylist.
18. The legacy SSH wrapper supports bash or zsh on the remote host.
19. Cloud-agent concurrency limits are published. The FAQ links to the hosting and pricing pages instead of saying that limits are still being finalized.
20. The legacy `oz` CLI remains a quiet compatibility surface:
   * Remove the expired “supported through the end of September 2026” deadline.
   * Do not call `oz` unsupported.
   * Keep the legacy reference available for existing users.
   * Use `warp` in new and current guidance when the `warp` command supports the workflow.
   * Do not add a prominent deprecation banner to every legacy reference page.
21. “Add-on credits” remains the canonical noun in docs and product UI. “Reload” is a verb for purchasing another bundle. A temporary reference to “Reload credits” is allowed only when it helps a reader find the label on the external pricing page.
22. Generic terminal Session Sharing remains documented as a current feature. Agent Session Sharing extends that generic feature instead of replacing it.
23. Fireworks appears in every exhaustive list of contracted model providers covered by provider ZDR.
24. All corrected claims use one canonical explanation and short cross-references. FAQ pages do not become a second source of truth for billing, privacy, or security policy.
## Finding disposition and required edits
### Fixed in an authority source
#### Falconer 10: create-run path
`developers/agent-api-openapi.yaml:175` already marks `POST /agent/run` deprecated, and `developers/agent-api-openapi.yaml:234` defines canonical `POST /agent/runs`.

Required docs work:

* In `src/content/docs/reference/api-and-sdk/index.mdx`, replace general and example uses of `POST /agent/run` with `POST /agent/runs`.
* If the deprecated path remains mentioned, label it as deprecated and direct readers to `POST /agent/runs`.
* Do not change the OpenAPI deprecation during this remediation.

### Invalidated audit pair
#### Falconer 1: codebase file limit
The reported `3,000` value came from deleted `src/content/docs/pricing.mdx`. The current Codebase Context page says all plans support at least 5,000 files. Released tier configuration sets Free to 5,000 and Build-family plans to 100,000.

Required docs work:

* Replace the qualitative sentence in `src/content/docs/agents/capabilities/codebase-context.mdx` under **File and codebase limits** with exact current caps:
  * Free: 5,000 files per repository.
  * Build, Max, and Business: 100,000 files per repository.
* Keep the pricing link for plan changes and other limits.
* Do not recreate `src/content/docs/pricing.mdx`.

### Safe-to-fix billing and entitlement findings
#### Falconer 2: scheduled-run billing owner
Update `src/content/docs/platform/triggers/scheduled-agents.mdx` so self-serve schedules charge the team owner. State the owner-plan-credits then team-shared-add-on-credits order. Link to the canonical billing explanation in `src/content/docs/platform/team-access-billing-and-identity.mdx`.

#### Falconer 3: agent API key credit waterfall
Update `src/content/docs/reference/cli/api-keys.mdx` so agent-key runs consume the owner’s plan-included credits, then the team’s shared add-on credit pool. Remove the phrase “owner’s add-on credits.”

#### Falconer 4: user-triggered credit waterfall
Make `src/content/docs/platform/team-access-billing-and-identity.mdx` the canonical explanation:

1. An applicable cloud-agent grant.
2. The triggering user’s plan-included credits.
3. The team’s shared add-on credit pool.

Apply the cloud-agent grant only to user-triggered cloud runs. Align summaries in:

* `src/content/docs/support-and-community/plans-and-billing/pricing-faqs.mdx`
* `src/content/docs/reference/api-and-sdk/troubleshooting/errors/insufficient-credits.mdx`

Use a short cross-reference instead of repeating the full waterfall when the page does not need every step.

#### Falconer 8: Free third-party cloud harnesses
Released `../warp-server/billing/config/tiers/free.yaml` disables third-party harnesses. Released self-serve paid plans enable them.

Required docs work:

* Keep the Build-or-higher requirement in `src/content/docs/platform/harnesses/index.mdx`.
* Correct `src/content/docs/support-and-community/plans-and-billing/pricing-faqs.mdx`, which currently says the beta is available to all users.
* Add the external pricing-page mismatch to the implementation PR description. Do not change the released entitlement in docs to match that page.

#### Falconer 15: team deletion with add-on credits
Update `src/content/docs/support-and-community/plans-and-billing/pricing-faqs.mdx` to match `src/content/docs/support-and-community/plans-and-billing/add-on-credits.mdx`: Warp blocks deletion until remaining add-on credits are used or removed. Delete the statement that credits become unusable after deletion.

#### Falconer 21: finalized concurrency limits
Replace “still being finalized” in `src/content/docs/platform/faqs.mdx` with a short statement that limits vary by plan. Link to:

* `src/content/docs/platform/warp-hosting.mdx`
* the public pricing page

Do not duplicate a numeric plan matrix in the FAQ.

#### Falconer 22: reload-credit terminology
Keep “add-on credits” throughout docs. Keep “auto-reload” for the purchase mechanism. If implementation confirms that the external pricing page still labels the object “Reload credits,” add at most one parenthetical locator near the pricing-page link. Record a marketing follow-up to rename the external label.

### Policy-resolved privacy and security findings
These findings were blocked on policy during triage. The requester resolved the policy questions. They are now safe to implement with Privacy, Security, and Legal review.

#### Falconer 5: customer-data training
The approved claim is provider-scoped: contracted model providers do not train on Warp-managed traffic.

Required docs work:

* Rewrite `src/content/docs/agents/getting-started/faqs.mdx` to remove “Warp reserves the right to use data collected to train models.”
* Scope the homepage statement in `src/content/docs/index.mdx` to contracted model providers.
* Audit provider-training statements in `src/content/docs/enterprise/security-and-compliance/security-overview.mdx`, `src/content/docs/support-and-community/privacy-and-security/privacy.mdx`, and `src/content/docs/support-and-community/plans-and-billing/pricing-faqs.mdx`. Every statement must name model providers as the subject.
* Do not add a new explanation of Warp-side training rights or privacy-policy interpretation.

#### Falconer 6 and Falconer 17: Secret Redaction default and unconditional claim
Treat these as one correction.

Required docs work:

* In `src/content/docs/support-and-community/privacy-and-security/privacy.mdx`, remove claims that Warp unconditionally applies Secret Redaction in all AI interactions.
* In `src/content/docs/enterprise/security-and-compliance/security-overview.mdx`, distinguish the user setting from organization enforcement.
* Keep `src/content/docs/support-and-community/privacy-and-security/secret-redaction.mdx` canonical:
  * individual setting off by default;
  * user can enable it;
  * Enterprise admin can enforce it;
  * enforced patterns apply regardless of the user preference.
* Link to the canonical page instead of maintaining duplicate lists of redacted secret classes.

#### Falconer 7: Free telemetry and AI
Current released behavior keeps the user toggle on all plans and does not gate AI execution on telemetry.

Required docs work:

* Remove the note in `src/content/docs/support-and-community/privacy-and-security/privacy.mdx` that requires telemetry for Free AI.
* Rewrite the individual-level answer in `src/content/docs/support-and-community/plans-and-billing/pricing-faqs.mdx` so disabling **Help improve Warp** is not called “full ZDR.”
* State that disabling the toggle stops eligible UGC analytics collection while AI remains available.
* Keep provider ZDR in a separate paragraph.

#### Falconer 12: regex case-insensitive flag
In `src/content/docs/support-and-community/privacy-and-security/secret-redaction.mdx`, state that regex matching is case-sensitive by default and that prefixing a pattern with `(?i)` makes that pattern case-insensitive.

#### Falconer 24: Fireworks provider-ZDR gap
Legal confirmed that Fireworks is covered by an enforced ZDR agreement.

Required docs work:

* Add Fireworks to the provider-ZDR list in `src/content/docs/enterprise/security-and-compliance/security-overview.mdx`.
* Add Fireworks to every other exhaustive provider-ZDR list touched by this remediation, including `src/content/docs/support-and-community/plans-and-billing/pricing-faqs.mdx`.
* Use “contracted model providers do not retain or train on Warp-managed traffic” or narrower wording.
* Do not imply that provider ZDR governs BYOK, custom endpoints, or customer-managed inference.

### Safe-to-fix API, CLI, and product findings
#### Falconer 9: cloud image attachments
Remove the unsupported claim from `src/content/docs/platform/faqs.mdx`. State that cloud agent prompts support up to five image attachments and link to the CLI or API reference for accepted inputs. Keep the limit aligned with:

* `src/content/docs/reference/cli/index.mdx`
* `developers/agent-api-openapi.yaml`

#### Falconer 11: run filter parameter
In `src/content/docs/reference/api-and-sdk/index.mdx`, replace `config_name` with `name` in the list-runs filter list and all examples. Keep the existing explanation that `name` filters by agent configuration name.

#### Falconer 13: fish on Windows
Update the opening claim in `src/content/docs/getting-started/supported-shells.mdx`. Do not say all four shells work on every operating system. Use an operating-system-specific list or table that excludes fish from Windows and agrees with `src/content/docs/support-and-community/troubleshooting-and-support/known-issues.mdx`.

#### Falconer 14: Ventura update status
Remove the active Ventura warning from `src/content/docs/support-and-community/troubleshooting-and-support/updating-warp.mdx`. Keep resolved history only in `src/content/docs/support-and-community/troubleshooting-and-support/known-issues.mdx` if that history still helps users.

#### Falconer 16: CLI auto-update and Homebrew
Qualify the auto-update statement in `src/content/docs/agents/cli/reference.mdx` by install method:

* direct or install-script builds can update automatically;
* Homebrew builds update with `brew update` and `brew upgrade`.

Keep `src/content/docs/agents/cli/quickstart.mdx` canonical for installation and update commands.

#### Falconer 18: default profile and MCP
Update `src/content/docs/reference/cli/agent-profiles.mdx` to match the released default profile:

* available MCP servers load by default;
* command execution uses **Agent decides**;
* the denylist still blocks matching commands.

Keep `src/content/docs/reference/cli/quickstart.mdx` aligned. Do not describe the default as unrestricted.

#### Falconer 19: legacy SSH wrapper shell
Update `src/content/docs/support-and-community/troubleshooting-and-support/known-issues.mdx` to say the legacy SSH wrapper starts or supports bash or zsh. Keep `src/content/docs/terminal/warpify/ssh-legacy.mdx` canonical for legacy SSH limitations.

#### Falconer 20: stale legacy CLI migration deadline
Remove the expired September 2026 support deadline from the shared caution or note in:

* `src/content/docs/reference/cli/index.mdx`
* `src/content/docs/reference/cli/quickstart.mdx`
* `src/content/docs/reference/cli/troubleshooting.mdx`
* `src/content/docs/reference/cli/federate.mdx`
* `src/content/docs/reference/cli/artifacts.mdx`
* `src/content/docs/reference/cli/mcp-servers.mdx`
* `src/content/docs/reference/cli/warp-drive.mdx`
* `src/content/docs/reference/cli/integration-setup.mdx`
* `src/content/docs/reference/cli/api-keys.mdx`
* `src/content/docs/reference/cli/agent-profiles.mdx`
* `src/content/docs/reference/cli/skills.mdx`
* `src/content/docs/reference/api-and-sdk/index.mdx`

Keep a quiet note on the legacy reference landing page that:

* `oz` remains available for compatibility;
* current guidance uses `warp`;
* not every legacy `oz` workflow has a documented `warp` equivalent.

Do not duplicate that note on every child page. Do not bulk-replace executable examples when `warp` does not have an equivalent command.

#### Falconer 23: Session Sharing redirect stub
Replace the redirect-only content in `src/content/docs/knowledge-and-collaboration/session-sharing/index.mdx` with canonical generic terminal Session Sharing documentation. The page must include:

* what a shared terminal session contains;
* how to open **Share current session**;
* the choices to share without scrollback, from the current screen or block, from a selected block, or from the start of the session when those options are available;
* viewer and editor access;
* link and team access controls;
* session limits by plan via a pricing link rather than copied numbers;
* the one-week expiry behavior;
* the warning that Secret Redaction is not applied to Session Sharing;
* how to stop sharing;
* links to Agent Session Sharing and cloud run sharing.

Update `src/content/docs/agents/local-agents/session-sharing.mdx` so it describes agent-specific visibility and steering as an extension of the generic page. Remove the circular “regular Session Sharing” link relationship. Existing links from `src/content/docs/support-and-community/plans-and-billing/pricing-faqs.mdx` and `src/content/docs/support-and-community/troubleshooting-and-support/using-warp-offline.mdx` should resolve to the restored canonical page.
## Implementation PR split
Use three implementation PRs. This is the smallest safe split because the changes have three independent review classes and different rollback risks.

### PR 1: billing, credits, and plan entitlements
Include findings 1, 2, 3, 4, 8, 15, 21, and 22.

Required review:

* Billing or Monetization owner for waterfalls, team deletion, and terminology.
* Platform Product owner for harness and concurrency entitlements.
* Docs review.

Reason for separation:

* A billing correction can affect purchase and spend expectations.
* External marketing mismatches need explicit follow-up without blocking unrelated API and CLI corrections.

### PR 2: privacy and security
Include findings 5, 6, 7, 12, 17, and 24.

Required review:

* Privacy or Legal owner for provider-ZDR wording.
* Security owner for Secret Redaction behavior.
* Docs review.

Reason for separation:

* These statements are policy commitments.
* Review and rollback must not depend on product-reference edits.

### PR 3: API, CLI, product behavior, and Session Sharing
Include findings 9, 10, 11, 13, 14, 16, 18, 19, 20, and 23.

Required review:

* API owner for endpoints and filters.
* CLI owner for updater, default profile, and legacy `oz` compatibility.
* Client or Collaboration owner for shells, updates, SSH, and Session Sharing.
* Docs review.

Reason for separation:

* These changes are source-verifiable and can ship without policy approval.
* Session Sharing is the only substantial content restoration. Keeping it with the product-reference corrections avoids a fourth small PR while retaining one engineering review class.

A single 24-finding PR is not recommended. It would combine Billing, Privacy, Legal, Security, API, CLI, and Collaboration approval in one merge decision. Three PRs preserve cohesive review without creating one PR per finding.
## Decisions
### Publish exact indexing caps
Options considered:

* Keep the current “at least 5,000” wording. This avoids numeric drift but does not answer the audited contradiction.
* Link only to the qualitative pricing page. This leaves no current public numeric authority.
* Publish the released Free and self-serve paid caps in the owning Codebase Context page.

Decision: publish 5,000 for Free and 100,000 for Build, Max, and Business. Keep a pricing link for other limits.

### Follow released harness entitlement
Options considered:

* Change docs to say Free supports third-party cloud harnesses because the marketing page says so.
* Keep Build-or-higher based on released tier configuration and correct conflicting docs.
* Remove plan information until marketing and released behavior agree.

Decision: document Build-or-higher. Correct the pricing FAQ and track the public marketing page as an external dependency.

### Separate Warp collection from provider ZDR
Options considered:

* Keep the broad Warp-training reservation and the broad no-training claim.
* Attempt to define Warp-side training rights in product docs.
* Remove the broad Warp-training assertion and scope ZDR claims to contracted model providers.

Decision: use provider-scoped ZDR only. Do not expand product docs into interpretation of Warp-side training rights.

### Keep `oz` as quiet compatibility documentation
Options considered:

* Declare `oz` unsupported because the published date passed.
* Extend the deadline without an approved new date.
* Remove the expired date, keep the reference, and prefer `warp` for current guidance.

Decision: remove the deadline and keep quiet compatibility documentation. Do not disrupt existing users or add loud callouts.

### Restore generic Session Sharing documentation
Options considered:

* Keep the redirect stub and treat all sharing as agent sharing.
* Retire generic Session Sharing links.
* Restore the generic terminal workflow and make the agent page an extension.

Decision: restore the generic page. Released tier configuration and current client behavior confirm that generic terminal Session Sharing remains supported.

### Keep “add-on credits” canonical
Options considered:

* Rename docs to the marketing label “Reload credits.”
* Use both names everywhere.
* Keep the product and docs term, and use one locator only if the external label remains.

Decision: keep “add-on credits.” Use “auto-reload” for the action. Marketing should adopt the product term.
## Assumptions
* **Assumption:** The three implementation PRs can merge independently. Each PR must keep every page it touches internally consistent.
* **Assumption:** The released tier configuration at implementation time remains authoritative. If a tier changes before implementation, the implementer must stop and request a spec revision instead of silently changing the values in this specification.
* **Assumption:** The implementation does not change product behavior, pricing configuration, API schemas, or CLI behavior.
* **Assumption:** Marketing-site edits are owned outside `warpdotdev/docs`. The implementation PR describes the mismatch and links an external follow-up when one exists.
* **Assumption:** No new screenshot asset is required for Session Sharing. Existing UI labels and images can be reused only when they match the current product.
## Out of scope
* Implementing any public docs correction in this specification PR.
* Editing the live marketing or pricing website.
* Changing billing tiers, credit routing, product entitlements, privacy settings, Secret Redaction defaults, API behavior, CLI behavior, or Session Sharing behavior.
* Defining Warp’s legal rights to train on collected data.
* Renaming the `oz` harness identifier in API schemas, factory files, or stored configurations.
* Removing the deprecated `POST /agent/run` endpoint.
* Rewriting historical changelog entries.
* Modifying docs consistency-audit code, benchmark fixtures, state, or automation from docs PR #829 or docs-factory-config PR #14.
## Validation criteria
### Every implementation PR
* Run `npm run typecheck`. The command must exit 0.
* Run `npm run build`. The command must exit 0.
* Run `git diff --check`. The command must produce no output and exit 0.
* Run `python3 .agents/skills/style_lint/style_lint.py --all --output /tmp/style-lint.json`. Review every new or changed finding in the edited files. The implementation must not add a deprecated term or style violation.
* Verify every changed internal link against the built site. No changed link may resolve to a 404 page or redirect loop.
* Search all files named in that PR for the superseded quote or value. The search must return no current-behavior occurrence unless the spec explicitly preserves a deprecated compatibility reference.
* Include the exact source commit for `../warp-server/` or `../warp/` used to verify each source-backed claim in the PR description.

### PR 1: billing, credits, and plan entitlements
* Verify the effective released values in `../warp-server/billing/config/tiers/free.yaml`, `../warp-server/billing/config/tiers/build.yaml`, `../warp-server/billing/config/tiers/build_max.yaml`, and the applicable Business tier before editing.
* Search changed docs for `3,000`, `owner's add-on credits`, `owner’s add-on credits`, `still being finalized`, and the statement that deletion forfeits remaining team credits. No stale current-behavior claim may remain.
* Search `src/content/docs/platform/`, `src/content/docs/reference/`, and `src/content/docs/support-and-community/plans-and-billing/` for descriptions of scheduled, API-key, and user-triggered waterfalls. Every matching current-behavior description must use the actor-specific order in this specification.
* Confirm that Free and paid third-party-harness statements agree inside the docs. Record the external pricing mismatch without blocking the docs correction.

### PR 2: privacy and security
* Search current docs for `train models`, `used for training`, `full ZDR`, `unconditionally applies`, and provider lists containing Anthropic, OpenAI, Google, or xAI. Review every result.
* Every no-training statement must name contracted model providers as the subject.
* Every exhaustive contracted-provider list must include Fireworks.
* The privacy page must not say that Free AI requires telemetry.
* The privacy, security overview, and Secret Redaction pages must agree that the individual Secret Redaction setting is off by default and that an Enterprise organization can enforce it.
* Ask the Privacy or Legal reviewer to confirm the final provider-ZDR sentences in the PR review. A code-only approval is insufficient.

### PR 3: API, CLI, product behavior, and Session Sharing
* Search current guidance for `POST /agent/run` and `config_name`. Each result must be either removed, changed to the canonical value, or explicitly labeled deprecated.
* Compare API examples with `developers/agent-api-openapi.yaml`.
* Search the legacy CLI reference for `September 2026` and `supported through the end`. No expired support deadline may remain.
* Verify each changed `oz` example against the current `warp` command before replacing it. Keep the `oz` form when parity is not documented.
* Search supported-shells and known-issues pages for universal fish-on-Windows language. No such claim may remain.
* Confirm that the restored Session Sharing page has no redirect loop and that links from the Agent Session Sharing, pricing FAQ, and offline pages resolve to it.
* Build the docs site and use the computer-use tool to capture static screenshots of:
  * the restored generic Session Sharing page at desktop width;
  * the Session Sharing page at a narrow mobile width;
  * the legacy CLI landing page with the quiet compatibility note.
* The screenshots must show readable headings, lists, callouts, and links without overflow or broken media. A video is not required because these are static documentation changes.
## Approval gate
Do not implement the three remediation PRs until the requester approves this specification. After approval, create the PRs in the order above unless reviewer availability requires a different order. Do not combine the privacy and security changes with another review class without requester approval.
