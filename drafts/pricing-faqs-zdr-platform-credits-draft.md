# Pricing FAQ — draft updates (ZDR + platform credits)
**Status:** Draft for review · **Author:** Oz (for Hong Yi Chen) · **Date:** 2026-06-09 · **Reconciled against** `main` @ 15efb41 (2026-06-09)
**Purpose:** Updated FAQ questions and answers covering (1) the three-credit-bucket model and platform credits, and (2) Zero Data Retention with the new retention-required-model carveout. Drafted so it can drop into the marketing `/pricing` FAQ (CMS) and/or reconcile into `support-and-community/plans-and-billing/pricing-faqs.mdx`.
> This is a non-published draft (lives under `drafts/`, outside `src/content/docs/`). It does not name any specific model; it uses general retention-carveout language per current docs guidance.
## Summary of changes
_Target: the marketing `/pricing` FAQ. The published docs (`support-and-community/plans-and-billing/pricing-faqs.mdx`) on `main` already carry the platform-credit entries and the exact ZDR carveout; only one small docs fix remains (see reviewer notes). The marketing page is the surface that's out of date._
- **Rewrites "What counts as a credit in Warp?"** to the current three-bucket model (AI / compute / platform). The live marketing answer still says credits are "inference costs and Platform fees" and defines "Platform fees" as *compute* — that conflicts with the new model where platform credits are a separate bucket from compute.
- **Adds platform-credit entries** (what they are, when they apply, when self-serve billing starts). The live marketing FAQ has none.
- **Updates the ZDR answer** with the general carveout: most models support ZDR, but availability may vary where a provider requires data retention; such models are off by default for Enterprise and an admin must enable them.
- **Adds "Are all models available with Zero Data Retention?"** to surface the carveout in the user's voice.
- **Fixes the Max credits figure** ("10×" is inconsistent with "18,000"; 18,000 = 12× Build's 1,500). Flagged for verification.
- **Terminology:** uses **"add-on credits"** (the docs term). The marketing page currently says "Reload credits" — pick one across surfaces (see reviewer notes).
- **Full live-FAQ audit (2026-06-09) found 3 more issues** the original draft missed: outdated **payment options** (says credit-card-only), an incomplete **student/non-profit/open-source discounts** answer (omits the Oz Open Source Partnership), and a **BYOLLM availability** overstatement (lists Vertex/Azure as if available). See "Additional corrections from the full live-FAQ audit."
---
## Credits & platform credits
### What counts as a credit in Warp?
A credit is a unit of usage consumed when you interact with Warp's agents. Warp meters usage across three buckets, and a single agent run can draw from more than one:
- **AI credits** cover inference — the LLM call itself. Consumed when Warp pays for the model call through Warp-managed providers.
- **Compute credits** cover compute — the sandbox a cloud agent runs in. Consumed when a run uses Warp-hosted compute (in practice, cloud agent runs). Local agent runs use your own machine and don't consume compute credits.
- **Platform credits** cover Warp's platform layer — run lifecycle, integrations, dashboard, APIs, and observability.
All three draw from the same balance — your monthly Warp credits first, then [add-on credits](/support-and-community/plans-and-billing/add-on-credits/) once those are exhausted. Credit usage is non-deterministic: it depends on the model, task size and complexity, amount of context, codebase size, tool calls, and prompt caching. See [credits](/support-and-community/plans-and-billing/credits/) for details.
### What are platform credits?
Platform credits cover the infrastructure Warp provides to coordinate, observe, and integrate agent runs — run lifecycle, integrations, dashboard, APIs, and observability — separate from the model call (AI credits) and the sandbox (compute credits). They apply to:
- **Every cloud agent run, on any plan**, regardless of which agent (Warp Agent, Claude Code, Codex), inference source (Warp-managed, BYOK, or BYOLLM), or compute source.
- **Local agent runs on Business and Enterprise that use customer-supplied inference** — BYOK, a custom inference endpoint, or BYOLLM. Warp isn't paying for the model call, but its platform infrastructure still runs the agent.
Local agent runs on Free, Build, or Max — and local runs on Business or Enterprise that use Warp-managed inference — don't consume platform credits. See [platform credits](/support-and-community/plans-and-billing/platform-credits/).
### When do platform credits start being charged on self-serve plans?
For self-serve plans (Free, Build, Max, Business), platform-credit billing **doesn't start until July 1, 2026**. Between May 21 and June 30, 2026, self-serve plans are in a **preview period**: platform credits are not consumed, so they don't draw from your monthly Warp credits, your add-on credit balance, or your spend cap.
On **July 1, 2026**, Warp begins consuming platform credits for every cloud agent run on Free, Build, Max, or Business, and for local agent runs on Business that use BYOK or a custom inference endpoint. On **Enterprise**, platform-credit usage is governed by your contract — see [enterprise billing](/enterprise/support-and-resources/billing/).
### Do local agent runs consume platform credits?
Only on Business and Enterprise, and only when the run uses customer-supplied inference (BYOK, a custom inference endpoint, or BYOLLM). Local runs on Free, Build, and Max never consume platform credits, and local runs on Business or Enterprise that use Warp-managed inference don't either (Warp already charges AI credits for the model call). For self-serve plans, billing on eligible local runs begins July 1, 2026.
---
## Zero Data Retention
### Does Warp have Zero Data Retention policies with LLM providers?
Yes. Warp integrates with multiple LLM providers — including Anthropic, OpenAI, Google, and Fireworks AI — and has executed Zero Data Retention (ZDR) agreements with them. By default, across all plans:
- Providers commit not to train their models on any customer-generated data processed through Warp.
- Providers commit to delete inputs and outputs after generating the relevant output, within a fixed time period.
Warp enforces these commitments through both technical and contractual safeguards. **Zero data retention is available for supported models. Model availability may vary where providers require data retention for safety, abuse monitoring, or compliance reasons.**
### Are all models available with Zero Data Retention?
Most are. Zero data retention is available for supported models, but availability may vary where a provider requires data retention for safety, abuse monitoring, or compliance reasons. For Business and Enterprise teams that enforce ZDR, any such model is **off by default**, and a team admin must explicitly enable it in the [Admin Panel](/enterprise/team-management/admin-panel/) before members can use it. See [model choice](/agent-platform/inference/model-choice/) for which models are supported.
### How can I enable Zero Data Retention in Warp?
Two ways:
- **Individual** — Any user can enable full ZDR for their account by disabling **Help Improve Warp** in **Settings** > **Privacy**.
- **Organization-wide** — On Business and Enterprise, admins can enforce ZDR for all members from the [Admin Panel](/enterprise/team-management/admin-panel/), so compliance doesn't rely on individual settings.
Regardless of plan, for any model offered under Zero Data Retention, Warp never allows the provider to store, retain, or train on your data. Some models are available only where the provider requires data retention; those are clearly indicated, and on Business and Enterprise they're off by default until an admin enables them. To discuss organization-wide ZDR, [contact sales](https://www.warp.dev/contact-sales).
---
## Related May 2026 changes (corrected for consistency)
### Should I subscribe to the Build, Max, or Business plan?
- **Build** — Flexible, usage-based access for individuals or small teams. Includes monthly credits, full Warp Agent access, BYOK and custom inference endpoint support, collaboration features, and high codebase indexing limits, plus access to add-on credits with volume discounts.
- **Max** — For heavy AI users who consistently need more capacity. Includes **12× Build's included monthly credits** (18,000/month at current allowances) and a better effective credit rate than buying add-on credits on Build.
- **Business** — For teams that need SSO, team usage metrics, admin-configurable data controls, and centralized spend management. Supports up to the seat limit shown on [Warp pricing](https://www.warp.dev/pricing), with per-seat monthly credits.
For unlimited seats, advanced governance, custom credit pools and usage terms, the Enterprise Analytics API, BYOLLM, per-user spend controls, or self-hosted cloud agents, see Enterprise. For current per-plan seat limits and credit allowances, see [Warp pricing](https://www.warp.dev/pricing).
### How do credits and add-on credits work for multi-seat teams?
- **Plan-included monthly credits** — Each seat gets its own monthly allowance that resets every 30 days on the team's renewal date.
- **Add-on credits** — As of May 21, 2026, add-on credits are scoped to the individual user who purchased or was allocated them, not pooled across the team, so one heavy user can't drain the team's balance. Teams that purchased add-on credits before May 21, 2026 keep their existing pooled balance until it's exhausted; it drains first.
- **Team-wide spend cap** — Admins set one team-wide monthly cap that governs auto-reload across the team.
Enterprise plans support team-scoped credit pools and per-user spend limits — see [enterprise billing](/enterprise/support-and-resources/billing/).
### Can I bring my own API key?
Yes. As of May 21, 2026, BYOK is available on all plans, including Free. Configure your OpenAI, Anthropic, or Google key in **Settings** > **AI** > **Manage models**. Requests routed through your own key don't consume Warp credits — you're billed directly by the provider. BYOK and custom inference endpoints are available to individual users and organizations with 10 or fewer employees; larger organizations need a Business or Enterprise plan, subject to Warp's [Terms of Service](https://www.warp.dev/legal/terms-of-service). On Business and Enterprise, local runs that use BYOK consume platform credits (self-serve billing begins July 1, 2026).
---
## Additional corrections from the full live-FAQ audit
_These live marketing answers are also out of date — found in the 2026-06-09 full pass, not in the original draft above._
### What payment options are available?
Warp uses Stripe and accepts credit card, debit card, Link, Apple Pay, and Google Pay. We don't accept ACH, checks, PayPal, or cryptocurrency. (For Apple Pay, use Safari on an Apple device; for Google Pay, use Chrome with Google Wallet enabled.)
_Live page says credit card is the **only** method and doesn't mention debit card, Link, Apple Pay, or Google Pay — outdated vs the docs._
### Are there any Warp discounts for students, non-profits, or open-source teams?
Warp doesn't offer student or non-profit discounts — the Free plan is the best starting point. For open-source teams, the [Oz Open Source Partnership](/support-and-community/community/open-source-partnership/) offers free agent credits to high-impact projects, and Warp's client is open source under AGPL v3.
_Live page flatly says "no discounts" and omits the Oz Open Source Partnership._
### Does Warp support other model routers or "Bring your own LLM"?
On Enterprise, BYOLLM routes inference through your cloud provider's Model-as-a-Service. It currently supports **AWS Bedrock, with Azure AI Foundry and Google Vertex AI coming soon.** Warp manages model support, routing, and orchestration; inference runs in your cloud so you keep data locality and existing cloud commitments.
_Live page lists Bedrock, Vertex, and Azure as if all are available; the docs say only Bedrock is live today. Confirm current availability before publishing._
### Individual BYOK / custom inference endpoints — add the eligibility caveat
The live "Can I bring my own LLM API key?" and "custom inference endpoints" answers omit the organization-size rule. Add: BYOK and custom inference endpoints are available to individuals and organizations with 10 or fewer employees; larger organizations need Business or Enterprise, per Warp's [Terms of Service](https://www.warp.dev/legal/terms-of-service).
### ZDR answers — append the carveout
The live "Does Warp have ZDR policies…" answer is missing the carveout. Append: "Zero data retention is available for supported models. Model availability may vary where providers require data retention for safety, abuse monitoring, or compliance reasons." Also replace the "How can I enable ZDR" closing line — "…never allows OpenAI, Anthropic, Google, or other model providers to store, retain, or train their models on your data. Warp has full Zero Data Retention policies with all LLM providers." — with: "Regardless of plan, for any model offered under Zero Data Retention, Warp never allows the provider to store, retain, or train on your data. Some models are available only where the provider requires data retention; those are clearly indicated, and on Business and Enterprise they're off by default until an admin enables them."
---
## Reviewer notes / open items
- **Max multiplier — confirmed 12×.** The May 2026 changelog on `main` states Max "comes with 12× more monthly credits than Build," and 1,500 × 12 = 18,000 — so the live marketing FAQ's "10×" is wrong. Use **18,000 / 12×**, or mirror the docs and avoid a hardcoded number ("a larger monthly allowance — see pricing") to prevent future drift.
- **Terminology — marketing-only fix.** The docs already standardize on **"add-on credits"**; only the marketing `/pricing` page still says **"Reload credits"** (~51 instances). Switch the marketing copy to "add-on credits" to match docs and in-app.
- **Don't name the retention-required model** in any FAQ — keep the general carveout language. The specific model is documented only on the model-choice page (already merged on `main`).
- **Platform-credit rates:** intentionally omitted. Keep "see [Warp pricing](https://www.warp.dev/pricing) for current rates," and ensure the pricing page actually publishes a rate before/at July 1, 2026 (today it doesn't).
- **Docs status (on `main`):** `pricing-faqs.mdx` already has the platform-credit entries and the exact ZDR carveout sentence (line 245). **One docs inconsistency remains:** lines 266 and 276 state that Business/Enterprise local BYOK / custom-endpoint runs "still consume platform credits" in present tense, which contradicts the same file's July 1, 2026 self-serve start (lines 401–413). Add the preview/July-1 caveat there. (Happy to do this on a branch.)
- **Where this lands:** the marketing `/pricing` FAQ is CMS-managed (not in this repo) — that's the surface you're updating today. Use the answers above as the source.
