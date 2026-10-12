# Warp Factories pricing transparency
## Summary
Add one concise `/factories/pricing` reference page after this specification is approved. The page will show the exact model inference and Warp-hosted compute rates that Warp charges through Warp Factories. It will use concrete named-model rows, exclude moving aliases from fixed pricing, and link from the existing Warp Factories and billing documentation. The implementation must resolve every public-rate and runtime discrepancy in this specification before publishing a value.
## Research scope and current state
The current public documentation explains the three usage components but does not publish the model or hosted-compute rates:

* `src/content/docs/support-and-community/plans-and-billing/credits.mdx:23` defines inference, compute, and platform charges.
* `src/content/docs/support-and-community/plans-and-billing/credits.mdx:29` states that paid self-serve inference uses public API rates.
* `src/content/docs/agents/inference/model-choice.mdx:26` lists Warp Agent models and model IDs.
* `src/content/docs/factories/factory-agents.mdx:115` explains that each factory agent can use the Warp Agent, Claude Code, or Codex harness.
* `src/content/docs/factories/runners.mdx:12` defines runner resources and `src/content/docs/factories/runners.mdx:64` lists the supported macOS shapes.

The runtime inventory and prices are split across private server sources:

* `warp-server/logic/ai/llm/model_choice.go` owns the selectable Warp Agent catalog.
* `warp-server/model/types/ai/types.go` owns model IDs.
* `warp-server/logic/ai/llm/llm.go:1837` owns token price categories, threshold pricing, provider adjustments, and customer-pricing multipliers.
* `warp-server/model/types/ai/internal_llm_types.go:590` owns direct-API regional surcharges.
* `warp-server/config/prod.yaml:155` owns production model flags and pricing-related flags.
* `warp-server/config/harness_models.go:31` owns pinned Claude Code and Codex harness catalogs.
* `warp-server/logic/harness_cost/harness_cost.go` estimates third-party harness cost.
* `warp-server/logic/ai/ambient_agents/billing/compute_rate.go:12` owns Warp-hosted compute rates.
* `warp-server/logic/ai/ambient_agents/billing/compute.go:150` applies each compute rate to measured runtime and the account's compute margin.
* `warp-server/config/prod.yaml:808` configures Namespace as the production default. Docker Sandbox billing exists, but its default production rollout is 0%.

Cursor's [Models & Pricing](https://cursor.com/docs/models-and-pricing) page, accessed 2026-10-12, provides useful information architecture:

* It explains billing context before the rate table.
* It uses one row per named model.
* It normalizes token prices to USD per one million tokens.
* It separates input, cache write, cache read, output, and exceptional notes.
* It explains dynamic routing separately instead of assigning one rate to a moving alias.

Warp should use those structural choices without copying Cursor's wording, usage-pool model, or product-specific caveats.
## Product behavior
1. The canonical page route is `/factories/pricing`.
2. The page opens with a short explanation of the three independent charge components:
   * model inference;
   * Warp-hosted compute;
   * platform usage.
3. The page states that model rates apply to Warp-provided inference. Customer-supplied API keys, provider subscriptions, and custom inference endpoints are billed under their own terms.
4. The model table uses USD per one million tokens.
5. The model table has these columns:
   * Model
   * Provider
   * Input
   * Cache write
   * Cache read
   * Output
   * Notes
6. The model table has one row per named model. Effort or reasoning IDs that share a price use one row.
7. A selectable mode with a different price uses its own row. This applies to Anthropic fast mode.
8. A model with threshold pricing keeps one primary row and states the threshold and complete alternate rate tuple in Notes. The note states that the higher rate applies to the whole request, not only excess tokens.
9. The table shows global standard inference rates. A note identifies each regional or data-residency multiplier that Warp can pass through and the models it affects.
10. Anthropic cache-write cells show both five-minute and one-hour prices in that order.
11. A dash means the provider does not publish or charge that category for the selected mode. A dash never means that the missing category is free unless the accompanying note says so.
12. Auto models, custom routers, and moving harness aliases do not receive a fixed-price row. The page states that their cost is the rate of the concrete model selected for each request.
13. A named model that the provider has deprecated remains blocked until the product catalog owner confirms whether the choice is removed, remapped, or retained with an explicit note.
14. The page does not duplicate every effort-specific `model_id`. It links to [Agent model choice](/agents/inference/model-choice/) for IDs and availability.
15. The compute section shows Warp runner configurations and the exact hourly USD rate Warp charges.
16. The compute section describes the customer-visible runner platform and shape. It does not present an infrastructure provider as a contractual availability guarantee.
17. Linux and Windows use a formula because supported shapes are configurable. macOS uses one row per supported shape.
18. The compute section states the billing granularity after Remote Platform and Billing confirm it against production metering.
19. The compute section states that local and self-hosted runs do not incur Warp-hosted compute charges.
20. The page links to [Platform usage](/support-and-community/plans-and-billing/platform-credits/) instead of reproducing platform rates.
21. The page states the last verification date and links to the first-party rate card for each provider.
22. The page links to the usage breakdown as the authority for the model and token categories consumed by a completed run.
23. Enterprise contracts can define different rates or credits. The page directs Enterprise customers to their contract when it differs from the public table.
24. The first release contains no cost calculator. The rate card and usage breakdown provide the required transparency without adding estimated task-cost assumptions.
## Technical design
### Canonical page and navigation
Create `src/content/docs/factories/pricing.mdx` with the title `Factories pricing`.

Add links from:

* `src/content/docs/factories/factory-agents.mdx` after the model and harness overview;
* `src/content/docs/factories/runners.mdx` after the runner-cost explanation;
* `src/content/docs/support-and-community/plans-and-billing/credits.mdx` after the three charge components;
* the Warp Factories sidebar section after `Runners`.

Do not add the complete table to the broad pricing FAQ. The FAQ answers plan questions. The new page is the canonical operational rate reference.
### Checked-in pricing data
Create `src/data/factories-pricing.ts` as the only public-doc source for rows rendered on the page. Keep prose, caveats, and links in the MDX page.

Each model record contains:

* stable row key;
* display name;
* provider;
* applicable Warp model families or modes;
* input rate;
* cache-write rate or rates;
* cache-read rate;
* output rate;
* threshold token count and complete threshold rates when applicable;
* regional or data-residency multiplier and model applicability when applicable;
* provider lifecycle status and deprecation date when applicable;
* public source URL;
* source access date;
* time-limited price end date when applicable;
* verification status.

Each compute record contains:

* platform;
* architecture;
* vCPU and memory shape or formula;
* hourly USD rate or formula;
* runtime-source reference;
* public-source URL;
* source access date;
* verification status.

The public page renders only records with `verified` status. The implementation must not render `catalog-mismatch`, `code-mismatch`, `public-source-missing`, or `internal-verification` records.
### Validation script
Create `scripts/validate-factories-pricing.mjs` and add `test:factories-pricing` to `package.json`.

The script fails when:

* a row key or named model is duplicated;
* a concrete model in the approved production inventory has no row;
* an Auto model, custom router, or moving harness alias has a fixed rate;
* a numeric rate lacks a first-party URL and access date;
* an access date is not an ISO date;
* a temporary price has no end date;
* a temporary price end date has passed;
* a threshold row omits one of its alternate billable categories;
* a regional multiplier in production lacks first-party evidence or an explicit customer note;
* a provider-deprecated model is marked `verified`;
* a rendered record does not have `verified` status;
* an Anthropic row omits a supported cache-write duration;
* a compute row has neither an exact hourly rate nor a complete formula.

Private server repositories are not available in public docs CI. Before each pricing change merges, the owning engineer must attach a fresh runtime inventory comparison to the PR. Do not copy private symbols or feature flags into public prose.
### Source-of-truth and update ownership
Use this precedence:

1. The production billing configuration determines what Warp charges.
2. The production selectable catalog determines which Warp-provided models need rows.
3. The provider's first-party public rate card supplies the no-markup public rate evidence.
4. The checked-in docs data supplies the rendered public table after the first three sources agree.

If the sources disagree, do not choose one silently. Mark the record blocked, ask the owning team to resolve the runtime or policy, and publish only after the production charge and public statement agree.

Ownership:

* AI Platform and Billing approve model inventory, token categories, routing surcharges, promotions, and billed rates.
* Remote Platform and Billing approve hosted-compute shapes, metering, and billed rates.
* Docs owns the checked-in data shape, page wording, navigation, source links, and verification dates.

Cadence:

* Update the page in the same release that adds, removes, or reprices a customer-selectable model or runner shape.
* Review temporary prices before their end dates.
* Review provider deprecations and automatic remaps in the same release that changes the upstream lifecycle state.
* Run a monthly source audit even when no product change is planned.
* Remove retired rows in the same release that removes customer selection. Historical rates belong in billing records, not the current table.
### Implementation sequence
1. Resolve every blocker in the research appendix with AI Platform, Remote Platform, and Billing.
2. Export the current production model and compute inventories.
3. Add the typed pricing data and validator.
4. Add the canonical page with verified rows only.
5. Add sidebar and cross-page links.
6. Run content, build, data, and link validation.
7. Capture visual proof.
8. Request Billing and owning-engineering approval before making the implementation PR ready for review.
## Decisions
### Use one canonical page
Options:

* Add rates to the general pricing FAQ. This keeps billing content together but makes a broad page longer and harder to maintain.
* Split model and compute pricing into separate pages. This reduces individual table size but forces a Warp Factories customer to navigate between two references.
* Use one concise Factories pricing page. This gives one canonical link while preserving provider-grouped sections.

Decision: use one Factories pricing page.
### Keep operational rates in the Warp Factories docs
Options:

* Put every current price only on [Warp pricing](https://www.warp.dev/pricing), following the general billing guidance in `AGENTS.md`. This preserves one commercial pricing page but does not give technical teams enough space for model thresholds, cache categories, runner formulas, and source qualifications.
* Put the operational rate card at `/factories/pricing` and link to it from the main pricing and billing surfaces. This keeps subscription and plan positioning on Warp pricing while giving Factories usage one detailed canonical reference.

Decision: use `/factories/pricing` as the canonical operational rate card. The main Warp pricing page remains canonical for subscription and plan prices. This is an intentional, requester-approved exception to the repository's default rule against duplicate current-price tables.
### Use concrete named models
Options:

* Repeat every effort-specific model ID. This is exhaustive but duplicates identical prices and creates a noisy table.
* Show one row per named model and separate only price-changing modes. This is concise and preserves every distinct price.
* Show provider-family ranges. This is shorter but does not answer what a selected model costs.

Decision: show one row per named model and one additional row for each price-changing selectable mode.
### Do not assign fixed rates to moving routes
Options:

* Publish one representative rate for Auto and moving aliases. This is easy to scan but can be wrong for every request.
* Publish a range. The range changes whenever the route pool changes and still cannot predict a request.
* Explain that the concrete routed model determines cost and direct customers to the usage breakdown.

Decision: do not publish a fixed rate or range for moving routes.
### Show Warp rates, not provider infrastructure branding
Options:

* Lead with provider products and public list cards. This exposes research detail but implies that Warp guarantees a specific backend.
* Show customer-visible runner shapes and Warp's exact charge. Keep provider evidence in source links and internal verification.

Decision: show customer-visible runner shapes and Warp's exact charge.
### Use checked-in structured data
Options:

* Write tables directly in MDX. This has the smallest initial diff but cannot enforce completeness, access dates, or expired promotions.
* Fetch provider pages during every docs build. This creates a network dependency and cannot prove that a provider rate matches Warp production billing.
* Check in typed rate data and validate its schema and dates. Human and owning-engineering review still resolve source disagreements.

Decision: use checked-in typed data with deterministic validation.
### Block publication on disagreement
Options:

* Publish provider list prices even when Warp code differs. This can misstate the customer's actual charge.
* Publish runtime prices without public evidence. This conflicts with the promise of no-markup public pricing.
* Resolve the discrepancy before publishing the affected row.

Decision: block an affected row until Billing and the owning engineering team resolve the discrepancy.
## Assumptions
* **Assumption:** The page applies to current public paid self-serve pricing. Current self-serve tier configuration applies zero inference and compute margin. Enterprise contract terms remain authoritative when different.
* **Assumption:** Warp Agent models use Warp-provided inference unless a customer configures a supported subscription, API key, or custom endpoint.
* **Assumption:** Claude Code and Codex factory harnesses use customer-owned provider credentials. Their model API charges are provider-billed and do not belong in the Warp-provided inference table.
* **Assumption:** Provider search, grounding, and other tool-call charges are not included in the token table. The implementation will add a short note and link to the usage breakdown if Warp passes through those charges.
* **Assumption:** No separate egress or persistent-storage charge is currently passed through for Warp-hosted runner compute. Remote Platform and Billing must confirm this before implementation.
* **Assumption:** Provider names can appear in model tables and source citations. Compute-provider names remain in verification evidence, not the primary customer table.
## Out of scope
* Implementing the customer-facing page before this specification is approved.
* Changing model, provider, routing, compute, or billing behavior.
* Publishing negotiated provider terms or confidential discounts.
* Predicting the price of an Auto route before the concrete model runs.
* A task-cost calculator or sample prompt-cost estimator.
* Historical price tables.
* Subscription seat prices, included usage, taxes, or Enterprise contract terms.
* Self-hosted infrastructure costs.
* Provider-billed inference through customer API keys, subscriptions, or custom endpoints.
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
| GPT-5.6 Sol | $4 | $5 | $0.40 | $20 | Over 272k input: $8 / $10 / $0.80 / $30. Reverify by 2026-11-21; the public rate card does not publish an expiry. | Confirmed, code match |
| GPT-5.6 Terra | $2 | $2.50 | $0.20 | $12 | Over 272k input: $4 / $5 / $0.40 / $18 | Confirmed, code match |
| GPT-5.6 Luna | $0.20 | $0.25 | $0.02 | $1.20 | Over 272k input: $0.40 / $0.50 / $0.04 / $1.80 | Confirmed, code match |
| GPT-5.5 | $5 | — | $0.50 | $30 | Over 272k input: $10 / — / $1 / $45 | Confirmed, code match |
| GPT-5.4 | $2.50 | — | $0.25 | $15 | Over 272k input: $5 / — / $0.50 / $22.50 | Confirmed, code match |

OpenAI cache-write pricing is a separate billable category for GPT-5.6 and later. Earlier listed models do not publish a separate cache-write charge. OpenAI states that the long-context tuple applies to the full request.

The rates above are global standard rates. Warp runtime applies OpenAI's 1.1x data-residency multiplier to direct US inference for GPT-5.4 and later. The implementation must explain this modifier when an account can select US-only inference.

The current public rate card confirms GPT-5.6 Sol's numeric rate but does not state an expiry. A runtime comment says OpenAI committed to that rate through at least 2026-11-21. Treat that date as an internal reverification deadline, not a confirmed public promotion end date.
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
Claude Code exposes moving aliases such as `best`, `fable`, `opus`, `sonnet`, and `haiku`, plus pinned models. Codex exposes pinned GPT models. These harnesses require customer-owned provider credentials in the current factory workflow.

Do not mix their provider-billed API cost into Warp-provided inference rows. Add one short note:

* Claude Code and Codex inference uses the provider account connected to the harness.
* A moving alias uses the concrete model selected by the provider.
* Provider invoices and terms are authoritative for that inference.

AI Platform and Billing must confirm this behavior for every supported harness authentication method before publication.
### Warp-hosted compute
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
### Compute qualifications
The implementation must verify:

* minimum billable duration and rounding;
* whether provisioning and teardown time are billable;
* whether stopped or paused time is billable;
* whether storage, image transfer, egress, or cache storage adds a charge;
* whether the selected runner rate can change after provider failover;
* whether rate display and actual usage use decimal or binary memory units;
* whether Enterprise compute rates differ by contract.
## Validation criteria
The documentation implementation is complete only when all checks pass:

* Run `npm run test:factories-pricing`. It must validate all data invariants in this specification.
* Compare the checked-in named-model inventory with the production catalog. The 2026-10-12 baseline contains 42 public rows: 9 OpenAI, 17 Anthropic including 3 fast-mode rows, 5 Google, 5 xAI, and 6 Fireworks. If Gemini 3.7 Flash is removed before implementation, the expected count is 41 and the comparison records the approved removal.
* Verify every reasoning or effort ID maps to exactly one named rate row unless its mode changes price.
* Verify Auto models, custom routers, and moving harness aliases have no fixed-price record.
* Verify provider lifecycle state for every named row. Resolve the Gemini 3.7 Flash deprecation before publication.
* Verify every numeric model rate against the linked first-party page and record the check date.
* Verify every rendered model rate against production billing code with AI Platform and Billing.
* Verify every regional multiplier and model scope against the first-party source and production routing.
* Verify every compute formula and exact macOS rate against production billing code with Remote Platform and Billing.
* Resolve all `catalog mismatch`, `code mismatch`, and `internal verification` statuses before rendering an affected row.
* Run `npm run typecheck`.
* Run `npm run build`.
* Run `python3 .agents/skills/style_lint/style_lint.py --all --output /tmp/style-lint.json`.
* Run `git diff --check`.
* Run the repository's broken-link check against the new route and cross-links.
* Confirm the sidebar exposes `Factories pricing` after `Runners`.
* Confirm the page contains no `VERIFY` markers before merge.
* Use computer use to capture a scrolling video of the rendered page at desktop and narrow mobile widths. The video must show the opening explanation, every provider section, horizontal table behavior, the compute section, source links, and the last-verified date.
* Confirm with a screen reader or accessibility tree that each table has column headers and that source links have descriptive text.
* Request final approval from Billing, AI Platform, Remote Platform, and Docs.

This specification PR needs no rendered-page video because it does not change public documentation.
