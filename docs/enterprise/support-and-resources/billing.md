---
description: >-
  Learn about billing for Warp Enterprise, including credits, cloud agent costs, and billing management.
---

# Billing

This page covers general information about credits, cloud agent costs, and BYOLLM billing for enterprise teams. If you have specific questions about custom pricing, credit allocation, or contract terms, contact your Warp account manager.

## Credits

Warp uses a credit-based billing model. Any interaction with Oz agents consumes credits based on the complexity of the task, the model used, and the amount of context processed.

### How credits work

* Each agent interaction consumes **at least one credit**, though complex interactions may use multiple credits.
* Credit usage is influenced by the LLM model used, the number of tool calls, task complexity, amount of context, and prompt caching behavior.
* Credit usage is **non-deterministic**. Two similar prompts may consume different numbers of credits.

For details on how credits are calculated, see [Credits](https://docs.warp.dev/support-and-community/plans-and-billing/credits).

### Credit allocation

Enterprise plans include a custom team-wide credit pool as part of your contract. Credits are primarily shared across the entire team rather than allocated per seat. Individual credit grants may also occur (e.g., support refunds), but the core allocation is team-wide.

{% hint style="info" %}
Credit allocations vary by contract. Contact your account manager for details on your team's specific allocation.
{% endhint %}

## Cloud agent billing

Oz cloud agents consume credits that include a small hosting fee in addition to AI usage costs.

### How credits are consumed

On Enterprise plans, both local and cloud agent usage draw from the same team credit pool. There are no separate "cloud agent credits" or "local credits" — all agent usage consumes from your available credit sources.

For team API key runs (e.g., CI/CD pipelines, scheduled tasks), credits also draw from the team's shared pool since these runs are not tied to any individual user.

For more details, see [Access, Billing, and Identity](https://docs.warp.dev/agent-platform/cloud-agents/team-access-billing-and-identity).

## BYOLLM billing

When using [Bring Your Own LLM (BYOLLM)](../enterprise-features/bring-your-own-llm.md), Warp routes requests through your cloud infrastructure (AWS Bedrock, Google Vertex, or Azure Foundry). BYOLLM requests **consume credits at a reduced rate** which is approximately 80% slower than standard usage. Inference costs are also billed directly to your cloud account.

If a BYOLLM request fails and Warp falls back to a direct API model, that fallback request consumes Warp credits at the standard rate.

## Managing billing

Your Warp account manager handles all billing for your Enterprise contract. Contact your account manager or dedicated Slack/Teams channel for:

* Invoices and payment changes
* Contract modifications
* Credit allocation adjustments

For urgent billing issues, email [billing@warp.dev](mailto:billing@warp.dev).

### Spending controls

Admins can configure spending limits to control costs:

* **Monthly spending limit** - Cap the total amount that can be spent on Add-on Credits per month. Configure in **Settings** > **Billing and usage**.
* **Usage monitoring** - Track credit consumption by team in **Settings** > **Billing and usage**.

## Related resources

* [Credits](https://docs.warp.dev/support-and-community/plans-and-billing/credits) - How credits are calculated and consumed
* [Add-on Credits](https://docs.warp.dev/support-and-community/plans-and-billing/add-on-credits) - Purchase additional credits and configure auto-reload
* [Pricing FAQs](https://docs.warp.dev/support-and-community/plans-and-billing/pricing-faqs) - Common billing questions
* [Bring Your Own LLM](../enterprise-features/bring-your-own-llm.md) - BYOLLM billing and configuration
* [Admin Panel](../team-management/admin-panel.md) - Configure spending limits and billing settings
