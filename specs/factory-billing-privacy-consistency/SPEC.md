# Factory billing, privacy, and support corrections

## Summary

Correct the remaining plan, inference, privacy, and support inconsistencies inventoried in [docs issue #1048](https://github.com/warpdotdev/docs/issues/1048). Update existing pages. Keep billing and privacy rules with their canonical owners. Preserve the distinction between provider retention, Warp's collection for service improvement, and product storage.

- Status: proposed; requester approval is pending. Do not start implementation until Foreman records written approval or an explicit scoped override.
- Requester: Hong Yi Chen (`hongyi-chen`).
- Baseline: docs `f117c4215f1a61786034bf2941ea3ca095d88750`, fetched November 18, 2026.
- Request: [originating Slack thread](https://warpdev.slack.com/archives/C09BVK0PL3Y/p1794942142115919).
- Resolved policy answers: [requester follow-up](https://warpdev.slack.com/archives/C09BVK0PL3Y/p1795040067702699), [additional linked-billing launch guidance](https://warpdev.slack.com/archives/C09BVK0PL3Y/p1795040813403879), and [scoped warning instruction](https://warpdev.slack.com/archives/C09BVK0PL3Y/p1795041007059219), relayed by Foreman. These revise P1 and resolve the warning-scope question; they are not spec approval.
- Deliverable: focused public-doc fixes on this spec's branch and PR, with a per-page change-and-reason record and verification evidence. This commit contains only the spec.

## Product behavior

The implementation changes documentation, not the product.

1. Readers distinguish Warp Terminal and local-agent plans from Warp Factories plans. Team-managed inference eligibility does not establish model-blocking or content-collection permissions.
2. Eligible Enterprise readers can find Claude linked billing from factory inference, Enterprise billing, platform usage, and the existing agent subscription FAQ. Each points to the canonical linked-billing page instead of reproducing setup or plan tables.
3. Readers distinguish Claude linked billing from consumer subscriptions, provider keys, BYOLLM, and Claude Code authentication. They understand the personal-key exception and the separate Warp charges.
4. Readers understand that only the Claude API billing relationship moves to the customer's Claude organization. Requests remain in Warp's organization. Warp's organization settings govern retention, including applicable ZDR, rate limits, and enabled features. The customer's ZDR settings, IP allowlists, and encryption keys do not transfer. This does not expand supported-model coverage.
5. Before authorizing a link, readers encounter the public-preview restriction described below. The warning gives an explicit action, not a claim that a technical control prevents linking. Its scope is Claude linked billing during public preview, not a general Warp compliance statement.
6. Readers understand that organization policy can restrict privacy controls. A browser-only reader receives conditional Admin Panel instructions and a contact fallback, not an unverified entitlement promise.
7. Factory users can report a failure without a Terminal block or local app logs. Terminal users retain their existing diagnostic instructions.
8. The public refund policy applies to self-serve plans. The collection and diagnostic prerequisites apply only to product-defect refund or credit requests. Enterprise contracts and refunds remain separate.

## Content design plan

- **Reader and job:** A factory user reporting a failed browser-based run, or an admin choosing the team's inference and privacy configuration.
- **Gap today:** Existing entry points omit linked billing, do not explain which organization's settings survive linking, overstate some controls, and assume Terminal diagnostics.
- **Change:** Correct existing answers and inference-table entries. Add the pre-link preview warning to the canonical linked-billing page and link it from relevant choice points. Add a short browser support section within the existing support pages. Preserve their content types, diagnostic teaching, and canonical owners; exclude new pages, new FAQs, and duplicated setup procedures.

## Per-page changes and reasons

Paths below are relative to `src/content/docs/`. Line references identify the baseline location, not immutable edit coordinates. Preserve published headings and explicit anchor aliases unless a correction requires changing them.

| Page and baseline location | Required change | Why |
| --- | --- | --- |
| `factories/zero-data-retention.mdx:18-24,51-53` (C1, P1) | Replace the stale Business provider-key statement with a link to eligibility by product. Keep Enterprise model restrictions separate. Add the billing-only linked-billing distinction beside the provider-account choices. Explain that Warp's applicable retention settings remain and the customer's ZDR does not transfer. Link the canonical pre-link preview warning. | Factory key access uses Scale and Enterprise, not Terminal's Business label. Who pays Anthropic does not determine whose settings apply. |
| `enterprise/team-management/admin-panel.mdx:193-205,220-228` (C1, P3) | Make the provider-credentials bullet product-neutral and link to the product-qualified eligibility table. Replace the unconditional Business/Enterprise browser-collection introduction with the conditional procedure specified below. Revise the nearby factory-plans TODO to record only evidence still missing. | Key eligibility is known. Collection-control editability has not been established for each product and plan. |
| `factories/infrastructure-and-security.mdx:77-92` (C2, P1) | Add Claude linked billing as a separate inference-table option. Identify Enterprise agreement/access requirements and Warp Agent factory-run scope, not Claude Code authentication. State that only billing moves; Warp's organization still governs requests. Link the canonical preview warning beside this choice, before readers follow setup. | The current table omits the option and does not distinguish its billing and organization-settings boundaries from keys. |
| `enterprise/support-and-resources/billing.mdx:32-48` (C2, P1, P2) | Add a short linked-billing subsection. State the billing-only move and link the organization-settings explanation, pre-link preview warning, fallback, and separate Warp charges to their owner. State that Enterprise refunds follow the contract/account-team route rather than the self-serve rules. | Paying Anthropic directly does not transfer the customer's controls or remove Enterprise contract terms. |
| `support-and-community/plans-and-billing/platform-credits.mdx:10-14` (C2) | Include linked billing in the customer-supplied-inference examples with a link. Adjust the factory caveat so it does not imply that team keys and harness credentials exhaust the alternatives. Preserve the existing product-qualified charge rules and contract exceptions. | Changing who pays for inference does not remove applicable platform or hosted-compute charges. |
| `agents/getting-started/faqs.mdx:38-44` (C2, P1) | Preserve the answer that Claude consumer subscriptions cannot fund the Warp Agent. Link eligible Enterprise organizations to Claude linked billing and its preview limitations without duplicating the warning. Keep personal BYOK local-only; link team credentials for factory readers if the answer mentions that path. Do not add another FAQ question. | The current answer presents an API key as the only way to use an Anthropic account. A new entry point must not bypass the linking limitation. |
| `enterprise/enterprise-features/team-managed-keys-and-endpoints.mdx:48-59,96-107` (C3) | Qualify the personal-key-first rule with the team linked-billing exception. Check the nearby first-party-key, member-experience, and billing summaries for the same universal claim. Link to the linked-billing owner for enabling and stopping it. | Team-enabled linked billing cannot be overridden with a personal Anthropic key. Ordinary key routing must remain clear. |
| `enterprise/index.mdx:9-27,50-64,81-92` (C4, polish) | Replace “unlimited parallelization” with parallel-run wording linked to hosted concurrency limits and queuing. Remove “powerful,” “state-of-the-art,” “Perfect for,” the meta section introduction, and repeated audience/benefit sales lists. Replace the platform name in the harness list with “the Warp Agent.” Keep the Enterprise overview's orientation, admin/developer/security routes, and useful capability links. | The hosting reference documents limits. A platform is not a harness. Repeated selling obscures the reader's next action. |
| `enterprise/security-and-compliance/security-overview.mdx:11-20,24-28` (C5, P1) | Replace the unconditional opt-out/full-functionality promise with organization-qualified collection preferences. Keep the admin route. Add a concise link from the provider-retention explanation to linked billing's organization-settings boundary and pre-link preview warning; do not duplicate its compliance list. | Enforced settings limit personal controls. Security readers must also find the linked-billing limitation without inferring that their Claude controls carry over. |
| `enterprise/support-and-resources/feedback-and-feature-requests.mdx:8,21-46,63` (C6, P2, polish) | Add factory/browser diagnostic intake, distinguish it from Terminal diagnostics, and retain private Enterprise support channels. Do not require enabling collection for ordinary support or import the self-serve defect-refund rule. Remove the meta opener. Use “Related pages” for the closing section. | Browser users need a usable report path. Enterprise support is not a self-serve refund request. |
| `support-and-community/troubleshooting-and-support/sending-us-feedback.mdx:29-44,258-274` (C6) | Add a short factory/browser reporting section and link to it from the general intake checklist. Scope Terminal block, version, and app-log instructions to app issues. Preserve their anchors and platform-specific procedures. | Factory reports must not depend on installing Terminal. |
| `support-and-community/privacy-and-security/privacy.mdx:18-28,78-86` (P1, P3) | Separate linked billing from customer-account inference: only billing moves, Warp's applicable ZDR remains, and customer ZDR settings do not transfer. Link the complete organization-settings boundary and pre-link preview warning. Preserve model limits, conditional browser collection instructions, and the privacy contact fallback. Apply the compliance evidence rule below. | Billing ownership is not the retention boundary. The current browser intro also overstates collection-control eligibility. |
| `agents/inference/claude-platform-linked-billing.mdx:8-26,44-64` (P1) | Put the required preview warning immediately after Enterprise eligibility, before OAuth linking instructions. Explain the billing-only move, Warp-governed requests/retention/rate limits/features, and non-transferring customer ZDR/IP allowlists/encryption keys. Replace the ambiguous “existing ... restrictions still apply” sentence. Preserve all eligibility, surface, consumer-subscription, Claude Code, personal-key, fallback, and separate-charge limits. | This page owns the warning and boundary. Its current sentence does not identify which organization's settings apply and can suggest customer settings transfer. |
| `support-and-community/plans-and-billing/plans-pricing-refunds.mdx:81-109` (P2) | State self-serve scope before the refund rules. Keep “Help improve Warp,” Conversation ID, and logs together under the product-defect condition. Preserve purchase-type, consumption, timing, and expiration rules. Link Enterprise readers to the account-team/contract route. | A defect investigation prerequisite must not read as a requirement for all refunds or Enterprise support. |
| `factories/quickstart.mdx:104-108` (polish) | Remove bold from closing link labels and use the standard link-first format. Do not change setup steps or its purpose. | This is a narrow style correction, not a new consistency finding. |

### Linked-billing settings and pre-link warning (expanded P1)

Explain the boundary in **How linked billing works**, before procedural detail:

| Boundary | Required explanation |
| --- | --- |
| Billing | Eligible Claude API usage is billed directly to the customer's linked Claude organization. Only this billing relationship moves. Preserve fallback and separate Warp charges. |
| Requests and Warp settings | Requests run in Warp's organization. Warp's retention configuration, including applicable ZDR, rate limits, and enabled features apply. Do not promise particular rate limits, features, or coverage beyond verified support. |
| Customer settings | The linked Claude organization's ZDR settings, IP allowlists, and encryption keys do not carry over. Billing authorization does not transfer these controls. |

Place one caution immediately after the canonical page's eligibility paragraph. It must precede **Linking your workspace** and the action **Link your Claude organization**. Give it the explicit anchor `#public-preview-limitations` and link directly to `/agents/inference/claude-platform-linked-billing/#public-preview-limitations` from the inventory's Factory, privacy, and Enterprise entry points.

- The requester-supplied launch instruction is explicit: customers who need HIPAA, FERPA, or customer-managed encryption keys (CMEK) must not link during public preview.
- Hong Yi Chen resolved the HIPAA wording scope with the exact instruction: “you should only talk about HIPAA in this context, related to this specific claude linked billing feature”. This is a user-requested exception to the repository's omission rule only for the negative feature-specific warning. It is not Security/Legal approval or evidence of supported compliance.
- Use this warning sentence in the canonical caution:

  > If your workload requires HIPAA or FERPA compliance, or customer-managed encryption keys (CMEK), do not use Claude linked billing during public preview.

- Keep HIPAA mention confined to this warning. Related Factory, privacy, and Enterprise pages must link to the warning without repeating the compliance list. Do not weaken the instruction to a general “review your settings” notice.
- No technical block enforces this warning. Do not describe a disabled control, validation error, entitlement rejection, or automatic protection.
- Restrict the warning to Claude linked billing during public preview. Do not present it as a universal compliance statement about Warp, Anthropic, or all inference paths. Do not promise a BAA or suggest that HIPAA, FERPA, or CMEK support becomes available after preview. Existing Enterprise agreement/access requirements still apply.
- The warning-scope question is answered. Do not ask it again or retain it as a publication blocker. Keep the general compliance guidance unchanged; other compliance commitments still need the evidence specified below.
- P1 requires the warning to be present before linking. The scoped wording instruction does not authorize public-doc implementation before spec approval.

### Browser support intake

Both support pages must tell a factory user to include:

- A link to the affected run or work item, and the factory involved.
- What happened, what they expected, reproduction steps, and the time of failure.
- Relevant visible error text and context that support can use to identify the run.
- Browser and OS details for browser-specific failures.

Link to `factories/factory-dashboard.mdx:49-57` for finding and inspecting runs. Do not invent a copy-ID button, browser log-download control, or universal log location. Local app logs are relevant only when the app is involved. Keep security and privacy inquiries on the existing private contact routes. Do not instruct users to publish credentials or sensitive transcripts in a public issue.

### Conditional browser collection procedure (P3)

- Address team admins. Name the Admin Panel, team selection, and **Privacy** page.
- Say to change “UGC Data Collection” only if their plan permits changes and no workspace policy locks it.
- Preserve the existing **Disabled** and **Respect User Setting** choices and reload-to-confirm step.
- Direct workspace-locked cases to a workspace admin.
- Preserve `privacy@warp.dev` for plan-locked controls and personal browser-only opt-out requests.
- Do not claim that Start, Scale, Business, or Enterprise has an editable control solely because its plan supports inference keys.

This conditional procedure is the implementation path with the evidence available now. A definitive collection-control matrix is deferred. To replace the condition with a plan claim, obtain a redacted production entitlement response and current deployed Admin Panel evidence for the relevant Terminal Business, factory Start/Scale, and Enterprise cases. Route existence, source code, and a successful flag check do not prove edit permission.

## Decisions

| Decision | Alternatives and trade-offs | Selected direction |
| --- | --- | --- |
| Content ownership | Duplicate full rules at each entry point for local completeness, or add bounded summaries and canonical links to reduce drift. | Use summaries and links. Keep necessary exceptions beside the affected choice. |
| Scope | Rewrite all requested families, or correct the confirmed inventory and targeted polish. A rewrite risks changing valid instructions and colliding with other audits. | Correct the listed pages. Record each fixed or deferred item. Escalate genuinely new semantic conflicts rather than silently expanding scope. |
| Linked billing (expanded requester decision P1) | Treat the payer as the settings owner, or distinguish billing from the organization that serves requests. | Preserve the original ZDR answer and the additional instruction: “only the billing relationship moves to your customer”. Requests and retention, including ZDR, rate limits, and features remain Warp-org governed. Customer ZDR, IP allowlists, and encryption keys do not transfer. |
| Preview warning (expanded P1) | Warn before authorization, rely on a technical block, or bury the limitation after setup. | Use the explicit HIPAA/FERPA/CMEK public-preview stop instruction above before linking. There is no technical block. Do not generalize the restriction or imply support after preview. |
| Scoped wording exception (requester decision) | Omit HIPAA everywhere under the general rule, or make the narrow negative-warning exception the requester expressly directed. | Exact instruction: “you should only talk about HIPAA in this context, related to this specific claude linked billing feature”. Mention it only in that warning; link from other pages. Do not edit general policy, claim Security/Legal approval, or treat this exception as spec approval. |
| Refunds (requester decision P2) | Require collection for all refunds/support, or scope diagnostics to defect-related self-serve requests. | Follow the requester: “Help improve Warp” is required only for refund or credit requests tied to a product defect. Require the Conversation ID and logs there too. Other refunds depend on purchase type and elapsed time. Enterprise contracts/refunds are separate. |
| Collection permissions (P3) | Infer Scale eligibility from key access, wait for a full matrix, or keep conditional instructions and a contact route. | Use conditional instructions. They correct the overclaim without inventing permissions or blocking unrelated fixes. |
| Capacity | Replace “unlimited” with a guessed number, or link the hosting limit and queuing guidance. | Link `factories/warp-hosting.mdx:31-33`; do not pin a number. |
| Privacy assurance | Treat the requester answer or code as approval of every retention promise, or separate configuration confirmation from compliance approval. | Apply the compliance policy below. Spec approval does not waive it. |

## Evidence and publication constraints

- Use #1048 as the existing investigation record. The additional P1 launch excerpt was supplied by the verified requester in the originating thread; it has not been independently validated against implementation or a Security/Legal approval source. The original cross-post source was inaccessible to Foreman. Cite the readable requester copy, not a claim of reading the original. This spec does not claim a new exhaustive audit or live production verification.
- Follow `AGENTS.md`, `.agents/rules/warp-positioning.md`, `.agents/references/terminology.md`, and `src/data/vars.ts`. Describe Warp Factories as infrastructure and distinguish it from the Warp Agent harness.
- Apply `.agents/references/compliance-claims-policy.md` to every compliance commitment added or retained in rewritten passages. Record the current Security/Legal-approved source, date/revision, approving authority, and exact product, plan, provider, model, deployment, and data scope in PR evidence. Existing docs, implementation, the requester answer, and general PR approval are not substitutes.
- The requester's scoped instruction permits the HIPAA mention in the negative linked-billing warning only. It does not authorize a positive compliance or BAA claim, a policy-source edit, or a claim about post-preview support. The omission-scope question is resolved; unrelated assurance and technical evidence requirements remain.
- If that evidence is unavailable, omit the unsupported promise from public prose and list the precise missing evidence in `Unverified claims`. Do not leave an unsupported compliance promise behind a `VERIFY` marker. Preserve valid instructions and bounded links; report the assurance item as deferred rather than claiming it complete.
- For other unresolved technical assertions, omit them or use the repository's `VERIFY` accounting while the PR remains draft. Resolve or remove those markers before publication.
- Verify any new availability claim with current shipped/public evidence. Run `server_rollout.py check` with the user-facing terms for server-backed claims and record the verdict and source revision separately from release evidence. Do not publish private rollout details.
- Recheck overlapping work before public drafting: issues [#1034](https://github.com/warpdotdev/docs/issues/1034), [#1019](https://github.com/warpdotdev/docs/issues/1019), and [#1010](https://github.com/warpdotdev/docs/issues/1010); PRs [#836](https://github.com/warpdotdev/docs/pull/836), [#833](https://github.com/warpdotdev/docs/pull/833), [#978](https://github.com/warpdotdev/docs/pull/978), and [#912](https://github.com/warpdotdev/docs/pull/912). Do not copy their unapproved claims. In particular, #836 has unresolved feedback about telemetry defaults and full-functionality promises.
- The public pricing-site naming discrepancy recorded on #1048 is outside this checkout. Do not revert Start/Scale docs to match a stale external page or infer a collection entitlement from its generic “data controls” wording.

## Assumptions

- **Assumption A1:** The supplied C1–C6/P1–P3 inventory, expanded P1 launch guidance, and delegated polish define this bounded pass. No full API, legal, or corpus-lifecycle audit is requested.
- **Assumption A2:** Preserve existing pages, URLs, and reader tasks. No navigation, redirect, pricing-table, or product-name-variable change is needed.
- **Assumption A3:** The requester answers resolve the product-policy forks, including the warning's narrow HIPAA mention. Production-permission evidence and evidence for other compliance commitments remain separate prerequisites; the answered wording question does not.

## Out of scope

- Changes to product behavior, pricing, contracts, entitlements, or the pricing website.
- A new plan-permission matrix, universal ZDR guarantee, model-coverage expansion, or customer-provider-agreement interpretation of linked billing.
- New FAQs, new public pages, wholesale Enterprise rewrites, or changing a page's purpose.
- Resolution of all pre-existing style/link warnings or the saved consistency-audit state associated with #876.
- Duplicating merged work from #1002, #1021, #1022, or #1038.

## Validation criteria

Record the implementation head, exact command results, and evidence limits in the same PR. A skipped check is not a pass.

### Content checks

Perform the following named checks against the diff and rendered pages. Record each result in the PR validation record.

| Check | Passing condition |
| --- | --- |
| V1: inventory accounting | Every table row above has a fix or an explicit deferral with reason and owner-evidence need. The record states affected page, change, and why. C1–C6, P1–P3, and all three polish targets are accounted for. |
| V2: product and configuration boundaries | Check Terminal Business, factory Scale, and Enterprise examples against the canonical eligibility table. Check ordinary local key precedence, team-enabled linked billing, and a factory Warp Agent run. No personal-device-key availability or universal personal-key-first promise leaks into factory/linked-billing guidance. |
| V3: linked billing and privacy | From each listed inference, Factory ZDR, privacy, and Enterprise entry point, follow working links to the canonical settings boundary and pre-link warning. Confirm Enterprise/access qualification, no consumer-subscription funding, no Claude Code support, fallback limits, and separate charges remain intact. Check a customer Claude organization with different ZDR, IP allowlist, encryption-key, rate-limit, and feature settings: the text says only billing moves, requests use Warp's settings, and customer settings do not transfer. No model coverage, numeric rate limit, or unverified feature availability is added. Apply the compliance evidence rule before declaring P1 publishable. |
| V4: collection controls and storage | Read the editable, workspace-locked, plan-locked, and personal browser-only cases. Each has the conditional action or contact route specified above. No new entitlement matrix appears. Provider retention, collection for improvement, personal conversation sync, and factory run storage remain distinct. |
| V5: support and refunds | A browser-only factory user can assemble a report without Terminal logs. A Terminal user can still follow existing diagnostics. Compare a self-serve defect request, a mistaken unused purchase, a time-based subscription refund, and an Enterprise contract request: only the first gets the collection/Conversation ID/log prerequisites; existing refund thresholds remain unchanged. |
| V6: capacity and tone | No unlimited hosted-concurrency promise remains in the changed overview. Its capacity link states limits and queuing without a guessed number. Apply the read-aloud and deletion-only passes. Preserve useful actions, exceptions, and page purpose. Closing links use the established format. |
| V7: preview warning before linking | In the rendered canonical page, the specified HIPAA/FERPA/CMEK public-preview stop instruction appears after eligibility and before the first OAuth/linking action. Trace its narrow mention exception to the requester's exact instruction. HIPAA appears in no other changed public passage; related pages link to the caution. Confirm no positive compliance/BAA promise, future-support implication, technical block, universal Warp/Anthropic restriction, or general policy edit was introduced. A missing or generic warning fails this check; no further requester wording decision is required. |

### Deterministic checks

Run from the docs repository root after committing the public-doc changes:

1. `git --no-pager diff --check origin/main...HEAD`
2. `python3 .agents/skills/style_lint/style_lint.py --changed`
3. `python3 .agents/skills/validate_ui_refs/validate_ui_refs.py --changed --all --require-provenance`
4. `python3 .agents/skills/check_for_broken_links/check_links.py --internal-only`
5. In repository order: `npm run typecheck`, `npm run test:heading-vars`, `npm run build`, `npm run test:heading-tocs`, `npm run test:homepage-json-ld`.
6. `python3 .agents/skills/doc_quality_policy/check_compression_contract.py src/content/docs/factories/quickstart.mdx --content-type quickstart`; run the same helper for any other changed page with its inherited content type. Explain necessary pre-existing budget exceptions rather than removing instructions to satisfy a number.
7. `python3 .agents/skills/doc_quality_policy/check_pr_contract.py --body "$PR_BODY_FILE"` using the actual saved PR body. Classify the public-content update as `engineering-review-required`, account for every remaining technical marker, and record evidence gaps. Apply `warpy-factory` as well as `factory:docs-factory`.

Style and link checks may expose unrelated baseline failures. Compare them with the unchanged base, fix introduced failures, and report remaining failures accurately. The 34 audit tests and 415-file UI scan on #1048 belong to earlier triage; they are not results for this implementation.

### Visual proof

After a successful build, use `computer_use` to inspect the rendered factory inference table, linked-billing warning, browser support intake, and refund scope. Report screenshots of these genuinely static changes in the PR; verify readable table columns, correct callout scope, and usable links. The linked-billing capture must show the warning's position above the first linking procedure and its public-preview scope. If implementation changes an interactive procedure or asserts newly verified deployed control behavior, use a video of that flow instead of static-only proof. Never authorize a real link or expose account, billing, or diagnostic secrets for this docs check.

## Approval

- Interview: the requester decisions supplied by Foreman resolve the launch facts and feature-specific HIPAA warning scope. No warning-scope question remains open.
- Spec approval: pending. Only written requester confirmation or draft-PR approval satisfies this prerequisite.
- The scoped wording exception is not a spec-approval override. Spec approval covers this bounded documentation plan; it does not establish production collection-control permissions or approve unsupported compliance commitments.
