# GA inference pricing for agents
## Approved Phase 1 scope
The requester approved inference pricing only on 2026-10-13, limited to models Warp has shipped to general availability (GA) and offers to every customer. This supersedes the original two-page model-and-compute deliverable. The existing `/agents/inference/model-choice/` page remains the only public owner of named-model rates. No new Warp Factories billing page, sidebar entry, compute table, compute promise, or compute cross-link ships in Phase 1.
Source/rate agreement is necessary but insufficient. GA and universal access use the requester-approved combination of current public model-choice documentation and live production availability, with runtime gating checks. Production deployment and the billed path have separate evidence. Checked-in production flags and catalog presence never establish deployment or GA by themselves.
## Reader and ownership
* **Reader and job:** A developer choosing an agent model, including for a factory, who needs to compare its token categories and exceptional rates before running work.
* **Gap today:** Model choice lists capabilities and IDs but no verified customer rates.
* **Change:** Add qualified inference rates beside the existing provider configuration tables. Leave compute, subscription purchase prices, historical rates, and cost estimates out.
The update inherits the model-choice page's combined feature/reference structure. Preserve configuration IDs, defaults, selection instructions, and existing availability qualifications. Do not relabel the entire selectable catalog as GA.
## Publication contract
A numeric row is eligible only when all of the following hold:
1. Warp GA is confirmed by current public model-choice documentation listing the model and supported efforts without preview/EAP/restricted qualification, together with live unrestricted production selector visibility. The requester explicitly approved this combined availability criterion on 2026-10-13. Provider GA or catalog presence alone is insufficient.
2. Confirm all-customer access with the same public/live evidence and inspect plan/workspace eligibility: inspect rollout flags, tier restrictions, workspace grants, default Enterprise policy, and selector visibility. Preview, EAP, restricted, tier-gated, and otherwise non-universal models are excluded.
3. A live production check or deployment record proves the supported model IDs and serving host. Record the stable release separately; a current release version without model-specific evidence is not GA proof.
4. Customer-charge confirmation combines the requester's explicit no-markup attestation, scoped to every family in the shared evidence group and linked to the originating request, with the live serving host and checked token, threshold, promotion, and regional implementation/rate-card agreement. Keep the source revision distinct from the live deployment check; neither the attestation nor source agreement establishes a deployed binary SHA or an observed charge trace.
5. First-party numeric evidence agrees with the customer charge. Store the source URL and access date; do not silently normalize or choose one side of a discrepancy.
6. Regional qualifications identify every applicable multiplier, full model scope, and first-party source. Preserve the independent approved regional requirements and fail closed when qualification evidence is missing.
7. The lifecycle is active, verification is current, and any temporary rate is unexpired. Deprecated, automatically remapped, moving, or unconfirmed routes remain excluded.
`status: verified` alone cannot render a rate. Each published record is linked to explicitly model-scoped GA, all-customer access, production deployment, billed-path, and regional evidence with a reference, check date, and summary. Shared evidence groups name all applicable model keys and deployed effort IDs in the canonical inventory. The canonical inventory separately lists the approved published model keys. The public export, data validator, and built-HTML validator enforce the same eligibility contract.
## Public behavior
* Rename `Available models` to `Models and rates`, preserving the old anchor.
* Show one row per qualified named model, grouping identically priced effort IDs. A price-changing mode gets its own row only if it independently meets the publication contract.
* Use USD per million tokens with Model, Input, Cache write, Cache read, Output, and Notes columns. Anthropic cache writes show five-minute / one-hour rates when eligible.
* State the complete higher-context tuple, boundary, and whole-request application. Preserve promotional expiry and reverification deadlines without presenting internal commitments as public promotions.
* State that listed rates cover GA models available on every plan, global Warp-provided inference, and contract exceptions. Do not imply that an unlisted model is universally available or free.
* Keep Auto, custom routers, and moving aliases non-numeric; the concrete routed model determines cost.
* Link to the existing global usage breakdown and descriptive first-party sources. Show the source check date only when a rate is rendered.
* The factory-agent model-selection link points to model choice. Existing global compute and platform explanations retain their purpose but receive no new compute pricing promise.
## Technical design
Retain `src/data/model-pricing.ts`, `src/data/pricing-inventory.json`, and `src/components/ModelPricingTable.astro` for inference only. The rate data may retain excluded research records with precise blockers; these are never public rate rows. Inventory completeness compares research coverage with existing configuration IDs, not a promise to publish the entire catalog.
Remove `src/data/factories-compute-pricing.ts`, `src/components/ComputePricingTable.astro`, and `src/content/docs/factories/usage-and-billing.mdx`. Remove the sidebar item, all links to that page, shaped-compute keys, compute validators, and compute tests. Retain only CI steps necessary to validate inference data and rendered inference tables.
`scripts/validate-usage-pricing.mjs` retains duplicate/alias checks, first-party/date checks, lifecycle, cache durations, thresholds, promotions, regional requirements, sole public ownership, and built table accessibility. Add eligibility and approved-published-set checks. Tests exercise each missing evidence category, previews/restrictions, undeployed efforts, unqualified regions, and mutation of built qualification text, scope, source, and whole note. Built validation rejects numeric rows without eligible data.
Keep runtime references and source access dates maintainable. Private code is not available in public CI, so reviewers must confirm evidence validity and deployed charge agreement, not merely the structure of an attestation.
## Current evidence and published set
Research was refreshed 2026-10-13 against warp-server `904a56f6c11d15bae2fe44d3497ff4144e8c1153` and warp `21f0683284d122457bb9099c86e7a6b90beb32d8`.
The unauthenticated production `freeAvailableModels` GraphQL query at `https://app.warp.dev/graphql/v2`, with empty input and no referrer, returns all 40 efforts for GPT-6 Astra, GPT-6.1 Sol, GPT-6 Sol, GPT-6 Luna, GPT-5.6 Sol, GPT-5.6 Terra, GPT-5.6 Luna, GPT-5.5, and GPT-5.4. Each has no disable reason, direct API enabled, and Bedrock disabled. The onboarding endpoint bypasses authenticated tier policy and cannot establish universal access or GA.
The release accessor reports `v0.2026.10.07.08.29.stable_00` dated `2026-10-07`. It does not identify these models as GA, and the public changelog has no matching release entries. Under the requester-approved criterion, the currently published `/agents/inference/model-choice/#openai` section lists every one of these families and efforts without preview, EAP, or restricted-access qualification; live production corroborates each ID. All nine families have matching first-party Standard tuples, a strict greater-than-272000 input boundary, whole-request long-context pricing, and the applicable 1.1 direct-US regional qualification. These nine families form the approved published set (40 effort IDs). The other 33 research rows remain excluded; this is an inference-only release, not full catalog or compute pricing coverage.
In the [originating request](https://warpdev.slack.com/archives/C09BVK0PL3Y/p1791847986824229), the requester attests: "These are the rates we charge customers, without markup". The inventory records this statement and reference explicitly for all nine published families named above. This supplies customer-charge confirmation alongside, not instead of, public-doc availability, live DIRECT_API serving evidence, runtime tuple/threshold/regional agreement, and the first-party rate card. No actual charge trace or deployed binary SHA was verified.
Access research inspected `logic/ai/model_choices/model_choices.go`, `logic/ai/llm/model_choice.go`, `logic/llm_policy/llm_policy.go`, tier configuration, workspace-exclusive grants, model environment guards, and the client model catalog. Conditional tier allowlists and customer-admin opt-outs must not be confused with verified universal default entitlement. Fable Enterprise defaults and fast-mode preview status are explicit exclusions, in addition to unresolved route/rate qualifications documented below.
## Verification and acceptance criteria
* Publish exactly the independently qualified set under the requester-approved docs/live availability criterion and all numeric safeguards. Keep the PR draft for independent re-review.
* Every published named model and effort appears in the approved inventory with per-record dated evidence. Every excluded research record stays non-numeric publicly.
* Model choice is the sole numeric inference owner; no compute deliverable, new compute navigation, cross-link, data module, validator, or dormant component remains.
* All applicable regional notes, model scopes, multipliers, and source links remain present and accessible. Missing evidence fails validation and cannot promote a row.
* Add regression tests for missing GA/access/deployment/billed-path/source/regional evidence, preview and restricted status, undeployed IDs, lifecycle exclusion, and built-HTML leakage. Billed-path evidence must retain the exact requester attestation, originating-request reference, and complete family scope. Preserve the regional mutation tests.
* Run `npm run test:usage-pricing`, `npm run typecheck`, `npm run test:heading-vars`, `npm run build`, post-build pricing tests, `npm run test:heading-tocs`, and `npm run test:homepage-json-ld`.
* Run changed-file style lint, internal links, UI-reference validation, compression and PR-body/risk checks, and `git diff --check`. Record unavailable tooling, never call it passing.
* Capture fresh desktop and narrow-mobile visual proof of model choice and verify the factory navigation no longer includes the removed page. Verify column/row headers, captions, source links, and horizontal table behavior for any published rows.
* Update the same draft PR and branch, title it for GA inference rather than complete Factories pricing transparency, retain required labels, and keep it draft for independent re-review. Never merge.
## Future phase boundary
Hosted-compute pricing is deferred. The research below is preserved internally for a later separately approved phase; it does not authorize components, public copy, or CI complexity in Phase 1. Future approval must resolve billed shape rates, granularity, deployment, public sources, and route applicability before designing a compute surface.
## Research appendix
All rates below are USD. Model rates are per one million tokens. Threshold tuples use the order input / cache write / cache read / output. `Code match` compares the first-party public rate with the checked-out production billing implementation on 2026-10-12. It is research evidence, not approved customer copy.
### Status definitions
* **Confirmed, code match:** The first-party rate and runtime billing configuration agree.
* **Confirmed, code mismatch:** A first-party rate exists, but one or more runtime values differ. Publication is blocked.
* **Catalog mismatch:** Warp exposes a named choice whose provider lifecycle state or routing behavior has changed. Publication is blocked.
* **Internal verification:** The public source does not prove the customer charge or production applicability. Publication is blocked.
### OpenAI
Source for every OpenAI rate in this table: [OpenAI API pricing](https://developers.openai.com/api/docs/pricing), accessed 2026-10-12.

| Model | Input | Cache write | Cache read | Output | Threshold note | Research status |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| GPT-6 Astra | $10 | $12.50 | $1 | $50 | Over 272k input: $20 / $25 / $2 / $75 | Confirmed, code match |
| GPT-6.1 Sol | $2 | $2.50 | $0.10 | $10 | Over 272k input: $4 / $5 / $0.20 / $15 | Confirmed, code match |
| GPT-6 Sol | $2 | $2.50 | $0.20 | $10 | Over 272k input: $4 / $5 / $0.40 / $15 | Confirmed, code match |
| GPT-6 Luna | $0.10 | $0.125 | $0.01 | $0.50 | Over 272k input: $0.20 / $0.25 / $0.02 / $0.75 | Confirmed, code match |
| GPT-5.6 Sol | $4 | $5 | $0.40 | $20 | Over 272k input: $8 / $10 / $0.80 / $30. Reverify by 2026-11-21; no exact expiry is published. | Confirmed, code match |
| GPT-5.6 Terra | $2 | $2.50 | $0.20 | $12 | Over 272k input: $4 / $5 / $0.40 / $18 | Confirmed, code match |
| GPT-5.6 Luna | $0.20 | $0.25 | $0.02 | $1.20 | Over 272k input: $0.40 / $0.50 / $0.04 / $1.80 | Confirmed, code match |
| GPT-5.5 | $5 | — | $0.50 | $30 | Over 272k input: $10 / — / $1 / $45 | Confirmed, code match |
| GPT-5.4 | $2.50 | — | $0.25 | $15 | Over 272k input: $5 / — / $0.50 / $22.50 | Confirmed, code match |

OpenAI cache-write pricing is a separate billable category for GPT-5.6 and later. Earlier listed models do not publish a separate cache-write charge. OpenAI states that the long-context tuple applies to the full request.

The rates above are global standard rates. Warp runtime applies OpenAI's 1.1x data-residency multiplier to direct US inference for GPT-5.4 and later. The implementation must explain this modifier when an account can select US-only inference.

The current public Markdown rate card confirms GPT-5.6 Sol's numeric rate and says it is available at least through 2026-11-21, agreeing with the runtime minimum commitment. No exact expiry is published. Reverify by that date; do not present it as a fixed promotion end date.
### Anthropic
Sources for every Anthropic rate in this table: [Anthropic API pricing](https://platform.claude.com/docs/en/about-claude/pricing) and, for fast rows, [Anthropic fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode), accessed 2026-10-12. Cache-write cells show five-minute / one-hour rates.

| Model | Input | Cache write | Cache read | Output | Threshold note | Research status |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| Claude Opus 5.5 | $4 | $5 / $8 | $0.20 | $20 | None | Confirmed, code match |
| Claude Opus 5.5 Fast | $8 | $10 / $16 | $0.40 | $40 | Research preview | Confirmed, code match |
| Claude Opus 5 | $5 | $6.25 / $10 | $0.50 | $25 | None | Confirmed, code match |
| Claude Opus 5 Fast | $10 | $12.50 / $20 | $1 | $50 | Research preview | Confirmed, code match |
| Claude Fable 5.1 | $10 | $12.50 / $20 | $0.25 | $50 | None | Confirmed, code match |
| Claude Fable 5 | $10 | $12.50 / $20 | $1 | $50 | None | Confirmed, code match |
| Claude Sonnet 5.5 | $2 | $2.50 / $4 | $0.10 | $10 | None | Confirmed, code match |
| Claude Sonnet 5 | $2 | $2.50 / $4 | $0.20 | $10 | None | Confirmed, code match |
| Claude Opus 4.8 | $5 | $6.25 / $10 | $0.50 | $25 | None | Confirmed, code match |
| Claude Opus 4.8 Fast | $10 | $12.50 / $20 | $1 | $50 | Research preview | Confirmed, code match |
| Claude Opus 4.7 | $5 | $6.25 / $10 | $0.50 | $25 | None | Confirmed, code match |
| Claude Opus 4.6 | $5 | $6.25 / $10 | $0.50 | $25 | None | Confirmed, code match |
| Claude Sonnet 4.6 | $3 | $3.75 / $6 | $0.30 | $15 | None | Confirmed, code match |
| Claude Opus 4.5 | $5 | $6.25 / $10 | $0.50 | $25 | None | Confirmed, code match |
| Claude Sonnet 4.5 | $3 | $3.75 / $6 | $0.30 | $15 | None | Confirmed, code match |
| Claude Haiku 5.5 | $0.10 | $0.125 / $0.20 | $0.01 | $0.50 | Over 100k input: $0.50 / $0.625 (5m) or $1 (1h) / $0.05 / $2.50 | Confirmed, code match |
| Claude Haiku 4.5 | $1 | $1.25 / $2 | $0.10 | $5 | None | Confirmed, code match |

Production has the Fable 5 and Opus 5 50%-off promotion disabled. If a future promotion changes the customer charge, the public row must show the charged promotional rate and end date rather than only the provider list rate.

The rates above are global direct-API rates. Anthropic applies a 1.1x multiplier to direct US inference for Claude 4.6 and later, which matches Warp runtime. Anthropic separately documents 1.1x regional or multi-region pricing for partner cloud endpoints starting with Claude 4.5. AI Platform must confirm the serving host so the public note describes only the modifier Warp can pass through.
### Google
Sources for every Google rate in this table: [Gemini Developer API pricing](https://ai.google.dev/gemini-api/docs/pricing) and [Google Agent Platform generative AI pricing](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing), accessed 2026-10-12.

| Model | Input | Cache write | Cache read | Output | Threshold note | Research status |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| Gemini 3.1 Pro | $2 | — | $0.20 | $12 | Over 200k input: $4 / — / $0.40 / $18 | Confirmed, code match |
| Gemini 3.8 Flash | $0.75 | — | $0.075 | $3.75 | Promotional through 2026-12-31; then $1.50 / — / $0.15 / $7.50 | Confirmed, code match |
| Gemini 3.7 Flash | $0.75 | — | $0.075 | $3.75 | Promotional through 2026-12-31; then $1.50 / — / $0.15 / $7.50 | Catalog mismatch: Google deprecated this ID and automatically routes it to Gemini 3.8 Flash |
| Gemini 3.6 Flash | $0.75 | — | $0.075 | $3.75 | Promotional through 2026-12-31; then $1.50 / — / $0.15 / $7.50 | Confirmed, code mismatch: runtime uses the post-promotion tuple |
| Gemini 3.5 Flash | $1.50 | — | $0.15 | $9 | None | Confirmed, code match |

Google also publishes context-cache storage rates. The checked runtime price configuration accounts for cached tokens but does not expose a separate storage-time category. AI Platform and Billing must confirm whether Warp incurs or passes through storage-time charges before publication.

Google publishes a 1.1x non-global rate for the Cloud endpoint. Warp runtime does not apply a Google regional surcharge. AI Platform must confirm which endpoint and region serve each Warp model before Billing can decide whether this qualification affects customers.

Google's [Gemini 3.7 Flash migration guide](https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.7), accessed 2026-10-12, marks that model ID deprecated and states that requests automatically route to Gemini 3.8 Flash. Warp still exposes Gemini 3.7 Flash as a named choice.
### xAI
Source for every xAI rate in this table: [xAI API pricing](https://docs.x.ai/developers/pricing), accessed 2026-10-12. xAI does not publish a separate cache-write charge.

| Model | Input | Cache write | Cache read | Output | Threshold note | Research status |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| Grok 4.7 | $2 | — | $0.50 | $6 | At or above 200k input: $4 / — / $1 / $12 | Confirmed, code mismatch at exactly 200k input |
| Grok 4.6 | $2 | — | $0.50 | $6 | At or above 200k input: $4 / — / $1 / $12 | Confirmed, code mismatch at exactly 200k input |
| Grok 4.5 | $2 | — | $0.30 | $6 | At or above 200k input: $4 / — / $0.60 / $12 | Confirmed, code mismatch at exactly 200k input |
| Grok 4.3 | $1.25 | — | $0.20 | $2.50 | At or above 200k input: $2.50 / — / $0.40 / $5 | Confirmed, code mismatch: runtime has no threshold tuple |
| Grok Build 0.1 | $1 | — | $0.20 | $2 | At or above 200k input: $2 / — / $0.40 / $4 | Confirmed, code mismatch: runtime has no threshold tuple |

The public xAI source applies a 1.1x multiplier to its US regional endpoint. Warp runtime has no xAI regional surcharge. AI Platform must confirm whether Warp uses that endpoint. Billing must add the surcharge or confirm that it is not applicable before publication.
### Fireworks AI
Source for every Fireworks rate in this table: [Fireworks Serverless pricing](https://docs.fireworks.ai/serverless/pricing), accessed 2026-10-12. Fireworks does not publish a separate cache-write charge.

| Model | Input | Cache write | Cache read | Output | Research status |
| --- | ---: | ---: | ---: | ---: | --- |
| GLM 5.3 | $1.40 | — | $0.26 | $4.40 | Confirmed, code mismatch on cache read |
| GLM 5.3 Flash | $0.15 | — | $0.03 | $0.50 | Confirmed, code mismatch on input, cache read, and output |
| Kimi K3 | $3 | — | $0.30 | $15 | Confirmed, code match |
| MiniMax M3 | $0.30 | — | $0.06 | $1.20 | Confirmed, code mismatch on cache read |
| Qwen 3.8 Max | $2 | — | $0.25 | $6 | Confirmed, code mismatch on cache read |
| DeepSeek V4.1 Flash | $0.30 | — | $0.006 | $1.20 | Confirmed, code mismatch on input, cache read, and output |

The runtime helper states that Warp has a negotiated 90% Fireworks cache-read discount. A negotiated rate is not evidence of a public list rate. Billing must decide whether Warp passes the negotiated rate through, update the no-markup policy wording if necessary, and approve the exact customer rate before these rows publish.
### Third-party harness catalogs
Claude Code exposes moving aliases such as `best`, `fable`, `opus`, `sonnet`, and `haiku`, plus pinned models. Codex exposes pinned GPT models. Authentication and billing depend on the supported harness configuration; no blanket provider-billing statement is approved.

Moving harness aliases remain non-numeric. Any future authentication-specific billing statement requires confirmation for that supported authentication path. Third-party harness inference is outside the Phase 1 Warp-provided table.
## Future phase: Warp-hosted compute research
Namespace first-party source: [Namespace pricing](https://namespace.so/pricing), accessed 2026-10-12.

Namespace publicly lists an overage price of $0.0015 per unit-minute. One Linux unit is one vCPU and 2 GB memory for one minute. Windows uses a 2x platform multiplier. The checked runtime uses the same unit-minute rate and the formula `max(1, vCPU, memoryGB / 2)`.

| Runner | Shape | Runtime customer rate | First-party public rate | Research status |
| --- | --- | ---: | ---: | --- |
| Linux x86-64 or aarch64 | Configurable | $0.09 × `max(1, vCPU, memoryGB / 2)` per hour | Same formula at overage price | Confirmed, code match |
| Windows x86-64 | Configurable | $0.18 × `max(1, vCPU, memoryGB / 2)` per hour | Same formula at overage price | Confirmed, code match |
| macOS Apple Silicon | 4 vCPU, 7 GB | $4.50/hour | $3.60/hour | Confirmed, code mismatch |
| macOS Apple Silicon | 6 vCPU, 14 GB | $5.40/hour | $5.40/hour | Confirmed, code match |
| macOS Apple Silicon | 8 vCPU, 14 GB | $8.10/hour | $7.20/hour | Confirmed, code mismatch |
| macOS Apple Silicon | 12 vCPU, 28 GB | $10.80/hour | $10.80/hour | Confirmed, code match |
| macOS Apple Silicon | 12 vCPU, 56 GB | $16.20/hour | $16.20/hour | Confirmed, code match |

Resolve the two macOS mismatches before any compute rate publishes. Billing must also confirm whether the public page should use hourly normalization only or show the underlying per-minute granularity.

Namespace applies a one-minute minimum and then rounds each next 15-second interval down. Warp's current customer charge multiplies its rate by measured runtime without that minimum or interval rounding. Self-serve tier configuration adds no compute margin. Remote Platform and Billing must confirm that exact-runtime billing is intentional and define the customer-facing granularity.

Docker first-party sources: [Docker Sandboxes compute sizes](https://docs.docker.com/ai/sandboxes-api/limits/) and [Docker Agentic Platform billing](https://docs.docker.com/agentic-platform/signup/), accessed 2026-10-12.

Docker publicly confirms per-second CPU-and-memory metering and five shapes, but the accessible public docs do not publish numeric CPU and memory rates. Warp's runtime contains `$0.0000126` per vCPU-second and `$0.00000405` per GiB-second.

| Docker shape | Resources | Runtime-derived hourly rate | Public numeric evidence | Research status |
| --- | --- | ---: | --- | --- |
| micro | 1 vCPU, 2 GiB | $0.07452 | Not published | Internal verification |
| small | 2 vCPU, 4 GiB | $0.14904 | Not published | Internal verification |
| medium | 4 vCPU, 8 GiB | $0.29808 | Not published | Internal verification |
| large | 8 vCPU, 16 GiB | $0.59616 | Not published | Internal verification |
| xl | 16 vCPU, 32 GiB | $1.19232 | Not published | Internal verification |

Docker Sandbox has a 0% default production rollout. Do not publish these rates or imply customer availability unless Remote Platform confirms production use and Billing supplies first-party or contractual evidence.
### Future compute qualifications
The implementation must verify:

* minimum billable duration and rounding;
* whether provisioning and teardown time are billable;
* whether stopped or paused time is billable;
* whether storage, image transfer, egress, or cache storage adds a charge;
* whether the selected runner rate can change after provider failover;
* whether rate display and actual usage use decimal or binary memory units;
* whether Enterprise compute rates differ by contract.
