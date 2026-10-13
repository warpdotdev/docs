# Warp Factories pricing transparency
## Summary
Update the existing [Agent model choice](/agents/inference/model-choice/) page with the canonical named-model rate tables after this specification is approved. Add a central `/factories/usage-and-billing` page that explains Warp Factories charge categories, links to model choice for inference rates, and owns the Warp-hosted compute table. This keeps model capability, configuration, and token cost together without duplicating rates. The implementation must resolve every public-rate and runtime discrepancy in this specification before publishing a value.
## Research scope and current state
The current public documentation explains the three usage components but does not publish the model or hosted-compute rates:

* `src/content/docs/support-and-community/plans-and-billing/credits.mdx:2` is the existing global `Usage and billing` page. It defines inference, compute, and platform charges.
* `src/content/docs/support-and-community/plans-and-billing/credits.mdx:30` states that paid self-serve inference uses public API rates.
* `src/content/docs/agents/inference/model-choice.mdx:17` lists Warp Agent models and model IDs.
* `src/content/docs/factories/factory-agents.mdx:86` explains that each factory agent can use the Warp Agent, Claude Code, or Codex harness.
* `src/content/docs/factories/runners.mdx:12` defines runner resources and `src/content/docs/factories/runners.mdx:63` lists the supported macOS shapes.
* `src/sidebar.ts:386` starts the Warp Factories navigation. Its `Overview` group is the evidence-based home for a central product-scoped usage page.

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
1. The existing `/agents/inference/model-choice/` page is the only public owner of concrete named-model rates.
2. Rename its `Available models` section to `Models and rates`.
3. Keep model IDs, defaults, reasoning or effort options, availability qualifications, and adjacent token-rate tables in the same provider subsection. A reader can compare configuration and cost without leaving the provider section.
4. The model rate tables use USD per one million tokens.
5. Each model rate table has these columns:
   * Model
   * Input
   * Cache write
   * Cache read
   * Output
   * Notes
6. The tables have one row per named model. Effort or reasoning IDs that share a price use one row.
7. A selectable mode with a different price uses its own row. This applies to Anthropic fast mode.
8. A model with threshold pricing keeps one primary row and states the threshold and complete alternate rate tuple in Notes. The note states that the higher rate applies to the whole request, not only excess tokens.
9. The tables show global standard inference rates. A note identifies each regional or data-residency multiplier that Warp can pass through and the models it affects.
10. Anthropic cache-write cells show both five-minute and one-hour prices in that order.
11. A dash means the provider does not publish or charge that category for the selected mode. A dash never means that the missing category is free unless the accompanying note says so.
12. Auto models, custom routers, and moving harness aliases do not receive a fixed-price row. The model-choice page states that their cost is the rate of the concrete model selected for each request.
13. A named model that the provider has deprecated remains blocked until the product catalog owner confirms whether the choice is removed, remapped, or retained with an explicit note.
14. The rate tables do not duplicate every effort-specific `model_id`. The existing configuration tables remain authoritative for IDs and availability.
15. Add `/factories/usage-and-billing/` as the central Warp Factories usage page.
16. Title the page `Usage and billing for Warp Factories`. Use `Usage and billing` as its sidebar label.
17. The page opens with the two pricing choices controlled directly by factory configuration:
   * model inference;
   * Warp-hosted runner time.
18. The `Model inference` section explains that Warp-provided inference is charged by token category. It deep-links to `/agents/inference/model-choice/#models-and-rates` for the concrete model tables instead of reproducing them.
19. The `Model inference` section states that customer-supplied API keys, provider subscriptions, custom inference endpoints, and supported third-party harness credentials are billed under their own terms.
20. The `Warp-hosted runner time` section shows Warp runner configurations and the exact hourly USD rate Warp charges.
21. The compute table describes the customer-visible runner platform and shape. It does not present an infrastructure provider as a contractual availability guarantee.
22. Linux and Windows use a formula because supported shapes are configurable. macOS uses one row per supported shape.
23. The compute section states the billing granularity after Remote Platform and Billing confirm it against production metering.
24. The compute section states that local and self-hosted runs do not incur Warp-hosted compute charges.
25. The page links to the existing global [Usage and billing](/support-and-community/plans-and-billing/credits/) page and [Platform usage](/support-and-community/plans-and-billing/platform-credits/) page for account balances and other applicable charges. It does not duplicate platform rates.
26. Both canonical pricing surfaces state the last verification date and link to applicable first-party rate cards.
27. Both surfaces link to the usage breakdown as the authority for categories consumed by a completed run.
28. Enterprise contracts can define different rates or credits. The central page directs Enterprise customers to their contract when it differs from the public tables.
29. The first release contains no cost calculator. The rate tables and usage breakdown provide the required transparency without adding estimated task-cost assumptions.
## Technical design
### Canonical pages and navigation
Update `src/content/docs/agents/inference/model-choice.mdx` in place:

* Rename `## Available models` to `## Models and rates`.
* Keep the existing Auto explanation and model ID or default tables.
* Add each provider's named-model token-rate table immediately after its configuration table and provider-specific qualifications.
* Add a short link from the rate introduction to `/factories/usage-and-billing/#model-inference` for how inference contributes to a factory run's bill.
* Keep `/agents/inference/model-choice/#models-and-rates` as the canonical destination for model capability, availability, IDs, and token rates.

Create `src/content/docs/factories/usage-and-billing.mdx`:

* Use the title `Usage and billing for Warp Factories`.
* Add `## Model inference` and `## Warp-hosted runner time` as the primary sections.
* Link `Model inference` to `/agents/inference/model-choice/#models-and-rates`; do not render a model-rate table on the Warp Factories page.
* Render the compute pricing table under `Warp-hosted runner time`.
* Link to `/factories/runners/#operating-systems` for runner configuration and supported shapes.
* Link to the global `/support-and-community/plans-and-billing/credits/` page for balances, purchase behavior, and account-wide charge definitions.
* Link to `/support-and-community/plans-and-billing/platform-credits/` for platform usage instead of copying its table.

Update cross-links:

* In `src/content/docs/factories/runners.mdx`, add a link near the first explanation of right-sized hardware to `/factories/usage-and-billing/#warp-hosted-runner-time`.
* In `src/content/docs/factories/factory-agents.mdx`, change the current model-choice link to `/agents/inference/model-choice/#models-and-rates` and add a nearby link to `/factories/usage-and-billing/#model-inference`.
* In `src/content/docs/support-and-community/plans-and-billing/credits.mdx`, add a link from `## Compute usage` to `/factories/usage-and-billing/#warp-hosted-runner-time`.
* In `src/sidebar.ts`, add `factories/usage-and-billing` with label `Usage and billing` to the Warp Factories `Overview` group after `Quickstart`.

Do not add either rate table to the broad pricing FAQ. The FAQ answers plan questions. Model choice and Warp Factories usage and billing are the two operational pricing owners.
### Checked-in pricing data
Create two data modules so each canonical page owns the records it renders:

* `src/data/model-pricing.ts` contains named-model token rates for `model-choice.mdx`.
* `src/data/factories-compute-pricing.ts` contains Warp-hosted runner rates for `usage-and-billing.mdx`.

Keep prose, caveats, IDs, capability guidance, and links in the owning MDX page. Do not copy model rate values into the Warp Factories data module or page.

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

The public pages render only records with `verified` status. The implementation must not render `catalog-mismatch`, `code-mismatch`, `public-source-missing`, or `internal-verification` records.
### Validation script
Create `scripts/validate-usage-pricing.mjs` and add `test:usage-pricing` to `package.json`. The validator reads both data modules.

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
* a compute row has neither an exact hourly rate nor a complete formula;
* a named-model rate appears in the Warp Factories compute module;
* either canonical page contains a handwritten numeric rate that bypasses its data module.

Private server repositories are not available in public docs CI. Before each pricing change merges, the owning engineer must attach a fresh runtime inventory comparison to the PR. Do not copy private symbols or feature flags into public prose.
### Source-of-truth and update ownership
Use this precedence:

1. The production billing configuration determines what Warp charges.
2. The production selectable catalog determines which Warp-provided models need rows.
3. The provider's first-party public rate card supplies the no-markup public rate evidence.
4. The checked-in model and compute data modules supply their owning public tables after the first three sources agree.

If the sources disagree, do not choose one silently. Mark the record blocked, ask the owning team to resolve the runtime or policy, and publish only after the production charge and public statement agree.

Ownership:

* AI Platform and Billing approve model inventory, token categories, routing surcharges, promotions, and billed rates.
* Remote Platform and Billing approve hosted-compute shapes, metering, and billed rates.
* Docs owns both checked-in data shapes, both pages' wording, navigation, cross-links, source links, and verification dates.

Cadence:

* Update the owning page in the same release that adds, removes, or reprices a customer-selectable model or runner shape.
* Review temporary prices before their end dates.
* Review provider deprecations and automatic remaps in the same release that changes the upstream lifecycle state.
* Run a monthly source audit even when no product change is planned.
* Remove retired rows in the same release that removes customer selection. Historical rates belong in billing records, not the current tables.
### Implementation sequence
1. Resolve every blocker in the research appendix with AI Platform, Remote Platform, and Billing.
2. Export the current production model and compute inventories.
3. Add `model-pricing.ts`, extend `model-choice.mdx`, and validate the named-model inventory.
4. Add `factories-compute-pricing.ts` and create `factories/usage-and-billing.mdx` with verified compute rows only.
5. Add the shared validator, Warp Factories sidebar entry, and deep cross-links.
6. Run content, build, data, anchor, and link validation.
7. Capture visual proof for both canonical pages.
8. Request Billing and owning-engineering approval before making the implementation PR ready for review.
## Decisions
### Separate rate ownership by user decision
Options:

* Add every rate to one Warp Factories pricing page. This gives one link but separates model cost from the model capability and configuration reference.
* Put model rates on model choice and compute rates on runners. This keeps each rate near its control but gives no central explanation of how the two charges combine for a factory run.
* Keep named-model rates on model choice and add one central Warp Factories usage page that owns compute rates and links to model choice. This adds one deliberate deep link while avoiding duplicate model tables.

Decision: use model choice as the only named-model rate owner. Use Warp Factories usage and billing as the charge overview and compute-rate owner.
### Keep operational rates with their product references
Options:

* Put every current price only on [Warp pricing](https://www.warp.dev/pricing), following the general billing guidance in `AGENTS.md`. This preserves one commercial pricing page but does not give technical teams enough space for model thresholds, cache categories, runner formulas, and source qualifications.
* Put operational token rates on model choice and hosted-compute rates on Warp Factories usage and billing. Link the two pages and the existing global billing surfaces. This keeps subscription positioning on Warp pricing while placing each technical rate next to the decision it informs.

Decision: use `/agents/inference/model-choice/#models-and-rates` for named-model rates and `/factories/usage-and-billing/#warp-hosted-runner-time` for compute rates. The main Warp pricing page remains canonical for subscription and plan prices. No rate table is duplicated.
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
### Use separate checked-in structured data
Options:

* Write tables directly in MDX. This has the smallest initial diff but cannot enforce completeness, access dates, or expired promotions.
* Fetch provider pages during every docs build. This creates a network dependency and cannot prove that a provider rate matches Warp production billing.
* Put model and compute rows in one shared module. This reduces file count but couples separate owners and update cadences.
* Check in separate typed model and compute modules and validate both together. Human and owning-engineering review still resolve source disagreements.

Decision: use separate checked-in model and compute data with one deterministic validator.
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
* Implementing customer-facing changes before this specification revision is approved.
* Duplicating named-model rates on the Warp Factories usage and billing page.
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

* Run `npm run test:usage-pricing`. It must validate all data invariants in this specification.
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
* Run the repository's broken-link check against `/factories/usage-and-billing/` and every new deep link.
* Confirm `model-choice.mdx` is the only public page that renders named-model rates.
* Confirm the Warp Factories page renders no named-model numeric rate.
* Confirm the sidebar exposes `Usage and billing` in the Warp Factories `Overview` group after `Quickstart`.
* Confirm both pages contain no `VERIFY` markers before merge.
* Use computer use to capture scrolling videos of both rendered pages at desktop and narrow mobile widths. The model-choice video must show configuration and token rates for every provider plus horizontal table behavior. The Warp Factories video must show the inference explanation, deep link, compute table, source links, and last-verified date.
* Confirm with a screen reader or accessibility tree that each table has column headers, section deep links reach the intended heading, and source links have descriptive text.
* Request final approval from Billing, AI Platform, Remote Platform, and Docs.

This specification PR needs no rendered-page video because it does not change public documentation.
