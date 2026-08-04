# Marketing /pricing FAQ — final copy (all questions)
**Status:** Ready-to-paste draft · **Date:** 2026-06-09 · **Source of truth:** `main` docs (`pricing-faqs.mdx`, `credits.mdx`, `platform-credits.mdx`, `model-choice.mdx`)
Full pass through every question on warp.dev/pricing, in page order. Terminology standardized to **"add-on credits"** (was "Reload credits"). Does **not** name any retention-required model. Verify the two flagged items in the footer before publishing.
---
### What counts as a credit in Warp?
Interactions with Warp's agents consume credits. Warp meters usage across three buckets, and a single run can draw from more than one:
- **AI credits** — the model (inference) call, when Warp pays for it through Warp-managed providers.
- **Compute credits** — the sandbox a cloud agent runs in (Warp-hosted compute). Local runs use your own machine and don't consume compute credits.
- **Platform credits** — Warp's platform layer: run lifecycle, integrations, dashboard, APIs, and observability.
All three draw from the same balance — your monthly credits first, then add-on credits. Usage is non-deterministic and depends on the model, task size and complexity, context gathered, codebase size, and whether the agent runs locally or in the cloud. For self-serve plans (Free, Build, Max, Business), platform-credit billing begins July 1, 2026 (preview until then). See Warp pricing for current rates.
### Does Warp have a SOC 2 Type 2 attestation?
Yes. Warp has obtained a SOC 2 Type 2 attestation from an accredited third party. Visit Warp's Trust Center to request the report.
### Should I subscribe to the Build plan, Max plan, or the Business plan?
**Build** is a good fit for individuals or small teams that want flexible access to Warp AI. It includes 1,500 monthly credits, add-on credits, full Warp Agent access, BYOK, custom inference endpoint support, collaboration features, and higher codebase indexing limits.
**Max** is for heavy AI users who consistently need more capacity. It includes 18,000 monthly credits (12× Build's included credits) and a ~17% better effective credit rate than the best add-on credit tier.
**Business** is for teams that need SSO, team usage metrics, admin-configurable data controls, and centralized spend management. It supports up to 25 members and includes 1,500 credits per seat per month.
For unlimited seats, advanced governance, custom credits and usage terms, the Enterprise Analytics API, BYOLLM, per-user spend controls, or self-hosted cloud agents, contact us about Enterprise.
### How can I subscribe to a Warp Business or Enterprise plan?
You can subscribe to Business directly from the upgrade page or in-app under **Settings > Billing and usage**. For larger organizations that need advanced compliance, governance, custom usage terms, or dedicated support, Warp offers an Enterprise plan with custom pricing and deployment options — contact us at sales@warp.dev or submit a request.
### Does Warp have Zero Data Retention policies with LLM providers?
Warp integrates with multiple LLM providers — including Anthropic, OpenAI, Google, and Fireworks AI — and has executed Zero Data Retention (ZDR) agreements with them. By default, across all plans:
- Providers don't train their models on any customer-generated data processed through Warp.
- Providers delete inputs and outputs after generating the relevant output, within a fixed time period.
Warp enforces these commitments through technical and contractual safeguards. Zero data retention is available for supported models; availability may vary where a provider requires data retention for safety, abuse monitoring, or compliance reasons.
### How can I enable Zero Data Retention in Warp?
ZDR can be enabled in two ways:
- **Individual** — Any user can enable full ZDR for their account by disabling **Help Improve Warp** in **Settings > Privacy**.
- **Organization-wide** — On Business and Enterprise, admins can enforce ZDR for all members from the Admin Panel, so compliance doesn't depend on individual settings.
To request organization-wide ZDR, contact sales@warp.dev or use our Contact Sales form. Regardless of plan, for any model offered under Zero Data Retention, Warp never allows the provider to store, retain, or train on your data. Some models are available only where the provider requires data retention; those are clearly indicated, and on Business and Enterprise they're off by default until an admin enables them.
### Do paid plans support additional AI usage beyond the included credits?
Yes. Build, Max, and Business support additional usage through add-on credits. After your included monthly credits are used, you can keep using AI features with add-on credits. Add-on credits are tied to individual users, roll over month to month, remain valid for 12 months, and offer discounts at larger denominations. Admins can configure team-wide spend caps and auto-reload.
### How often do AI credit limits reset?
Your included plan credits reset every 30 days from your subscription or renewal date. View your remaining balance under **Settings > Billing and usage**. If you run out before your next reset, purchase add-on credits to keep using AI features without interruption. On eligible plans, admins can also configure auto-reload and team-wide spend caps.
### How does auto-reload work for teams?
On Build, Max, and Business, admins can configure auto-reload for add-on credits. When auto-reload is **on**, the admin selects the add-on credit denomination, and Warp automatically reloads when a user's balance drops below 100 credits, subject to the team-wide spend cap. When auto-reload is **off**, eligible members can purchase add-on credits manually, as long as the team stays below the cap.
### How do add-on credits work for multi-seat teams?
For teams on Build, Max, or Business, included monthly credits are tied to each paid seat and reset monthly based on the subscription or renewal date. Add-on credits are also tied to individual users rather than pooled across the team. If a user runs out of included credits, they can purchase more, tied to their account. Admins can configure team-wide spend caps and auto-reload to manage overall usage. Pooled add-on credits purchased before May 21, 2026 remain available and are used first; after those are exhausted, new add-on credits are attributed to individual users.
### How are service account or team-scoped API key requests billed on self-serve plans?
On self-serve plans, add-on credits are tied to individual users. Some requests — for example, those made through a team-scoped API key — can't be attributed to a specific user. When Warp can't identify an individual billing user, usage is billed to the team owner: the owner's included credits first, then their add-on credits. If auto-reload is enabled, this usage may trigger auto-reload on the owner's pool, subject to the team-wide spend cap.
### What payment options are available?
Warp uses Stripe and accepts credit card, debit card, Link, Apple Pay, and Google Pay. We don't accept ACH, checks, PayPal, or cryptocurrency. (For Apple Pay, use Safari on an Apple device; for Google Pay, use Chrome with Google Wallet enabled.)
### Are there any Warp discounts for students, non-profits, or open-source teams?
Warp doesn't currently offer student or non-profit discounts — the Free plan includes all core terminal features and enough AI usage to get started. For open-source teams, the Oz Open Source Partnership offers free agent credits to high-impact projects, and Warp's client is open source under AGPL v3.
### I'm an individual developer. Can I bring my own LLM API key?
Yes. You can bring your own API key for supported providers — OpenAI, Anthropic, and Google — and keep using Warp's agent experience, tools, and interface. Add your key in **Settings > AI**. BYOK is available to individuals and organizations with 10 or fewer employees; larger organizations need a Business or Enterprise plan, subject to Warp's Terms of Service.
### Does Warp support custom inference endpoints?
Yes. Warp supports custom inference endpoints for OpenAI-compatible providers and gateways — connect endpoints such as OpenRouter, LiteLLM, z.ai, or an internal gateway, as long as the endpoint supports the OpenAI Chat Completions API. Use this to route Warp's AI features through your own provider, router, or internal gateway. Like BYOK, custom inference endpoints are available to individuals and organizations with 10 or fewer employees; larger organizations need a Business or Enterprise plan, subject to Warp's Terms of Service.
### Does Warp support other model routers or "Bring your own LLM"?
On the Enterprise plan, Warp connects to major cloud providers' Model-as-a-Service offerings. BYOLLM currently supports AWS Bedrock, with Azure AI Foundry and Google Vertex AI coming soon. Warp still manages model support, routing, and orchestration, but inference runs in your cloud environment so you can maintain data locality, security controls, and existing cloud spend commitments. Custom or in-house model routers outside this list aren't supported by default today — reach out to sales@warp.dev with your requirements.
### What features are available during multi-harness orchestration beta?
During beta, multi-harness orchestration is available to all users. You can use Claude Code, Codex, and the Warp Agent in Oz cloud environments, and mix and match harnesses across workflows. Agent Memory is currently in Research Preview, letting preferences, project knowledge, and learnings from past sessions carry across harnesses and future agent runs — contact sales to request access. As these features move out of beta or Research Preview, availability, limits, and pricing may change.
---
## Other /pricing surfaces (tooltips & cards)
Same ZDR carveout, kept to a ~3-word scope so tooltips stay short. The full carveout detail stays in the FAQ, not here.
- **"Your data, secure and private." card** — change "These providers do not retain, store, or train models on customer data processed through Warp." → "For supported models, these providers don't retain, store, or train on your data."
- **Admin-configurable data-controls tooltip** — change "Warp does not allow contracted model providers to retain, store, or train models on your data." → "For supported models, contracted providers don't retain, store, or train on your data."
- **Individually-configured data-controls tooltip** — change "Configure app telemetry and data settings in Settings > Privacy. Warp does not allow contracted model providers to retain, store, or train models on your data." → "Configure app telemetry and data settings in Settings > Privacy. For supported models, contracted providers don't retain, store, or train on your data."
- **"Zero data retention policy for AI" comparison-row tooltip** — leave as-is ("Control whether AI request data is retained. Business and Enterprise plans enforce this across all team members."). It describes the setting, not an absolute provider claim, and it's already short.
---
## Verify before publishing
- **BYOLLM availability** (model-routers answer): docs say only AWS Bedrock is live today, with Azure Foundry and Google Vertex "coming soon." If Vertex/Azure have since shipped, update that line.
- **Max numbers** (plan-comparison answer): 18,000/month and 12× are from the May 2026 changelog and pricing card; confirm against the live registry, or drop the hardcoded number ("a larger monthly allowance — see pricing") to avoid future drift.
## What changed vs the current live page
- Rewrote the credit definition (old "inference + Platform fees = compute" → three buckets: AI / compute / platform, + July 1 2026 self-serve timing).
- Fixed Max "10×" → "12× (18,000)".
- Added the ZDR retention carveout; softened "full ZDR with all providers" → "for supported models."
- Fixed payment options (added debit card, Link, Apple Pay, Google Pay).
- Added the Oz Open Source Partnership to the discounts answer.
- Corrected BYOLLM availability (Vertex/Azure "coming soon").
- Added the org-size eligibility caveat to the individual-BYOK and custom-endpoint answers.
- Renamed "Reload credits" → "add-on credits" throughout.
