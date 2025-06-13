---
description: >-
  Frequently asked questions about Warp's Agent Mode, including supported
  models, privacy practices, request limits, billing, and usage guidelines.
---

# AI FAQs

## General

### What data is sent and/or stored when using Agent Mode?

See our [Privacy Page](../privacy/privacy.md) for more information on how we handle data with Agent Mode.

### What happened to the old Warp AI chat panel?

Agent Mode has replaced the Warp AI chat panel. Agent Mode is more powerful in all of the chat panel's use cases. Not only can Agent Mode run commands for you, it can also gather context without you needing to copy and paste. To start a similar chat panel, click the AI button in the menu bar to start on a new AI pane.

### Is my data used for model training?

No, Warp nor its providers OpenAI or Anthropic train on your data.

### What model are you using for Agent Mode?

Warp supports a curated list of LLMs from providers like OpenAI, Anthropic, Google, and DeepSeek (hosted by Fireworks AI in the US). To view the full list of supported models and learn how to switch between them, visit the [model-choice.md](model-choice.md "mention") page.

### Is DeepSeek enabled by default?

No, DeepSeek is never enabled by default. By default, Agent Mode uses Claude 3.7 Sonnet. To use DeepSeek, you would need to manually select it from the model selector inside Agent Mode.

### How is my data handled for DeepSeek models?

We take privacy and security very seriously when it comes to models developed by foreign companies or hosted outside the US. DeepSeek models in Warp are hosted exclusively on US servers through our trusted provider, [Fireworks AI](https://fireworks.ai/). No requests are routed to servers outside the US.

### Can I use my own LLM API key?

Warp AI is tailored for the terminal so you can get optimal results and performance. It's suitable for AI power users and professional use cases.

For organizations with strict security requirements, a “Bring Your Own LLM” option is available on the Enterprise plan. At the Enterprise plan level, we can work closely with your team to ensure quality and compliance for your LLM of choice.

## Billing

Every Warp plan includes a set number of Warp AI requests per user per month. Please refer to [pricing](https://www.warp.dev/pricing) to compare plans.

AI Request limits apply to Agent Mode, [Generate](generate.md), and [AI autofill in Workflows](../knowledge-and-collaboration/warp-drive/workflows.md#ai-autofill). When you have used up your allotted requests for the cycle, you will not be able to issue any more AI requests until the cycle renews.

For questions around what counts as a Warp AI request, what counts as a token, and how often requests refresh, please refer to [#what-counts-as-a-warp-ai-request](../support-and-billing/plans-and-pricing.md#what-counts-as-a-warp-ai-request "mention")and more on the [plans-and-pricing.md](../support-and-billing/plans-and-pricing.md "mention")page.

### Exceeding Agent Mode request limits

#### **What is Lite?**

**Lite** is a basic AI model included with the Turbo plan that serves two purposes:

* **Fallback model**: If you reach your Turbo AI request limits, Warp automatically switches to Lite so you can keep using AI without interruption — at no additional cost.
* **Standalone option**: You can also choose to use Lite before hitting your limits. In this case, usage will still count toward your monthly request limits, but once those limits are reached, Lite remains available with unlimited usage for Turbo plan users only.

Lite is a more token-efficient model than other premium models and supports core AI workflows. Learn more about Lite in the [#what-is-lite](../support-and-billing/plans-and-pricing.md#what-is-lite "mention") section of our [plans-and-pricing.md](../support-and-billing/plans-and-pricing.md "mention") documentation.

#### **"Message token limit exceeded" error**

This error means your input (plus attached context) exceeds the maximum context window of the model you're using. For example, GPT-4o has a context window limit of 123,904 tokens. If you exceed that, you may receive no output.

To fix this, try:

* Starting a new conversation
* Reducing the number of blocks or lines attached to your query

#### **"Monthly request limit exceeded" error**

Once you exceed your AI requests on the Turbo plan (see [pricing](https://www.warp.dev/pricing) for current limits), premium models will be disabled, and Warp will automatically switch you to Lite. This allows you to continue using AI features with a more token-efficient model until your quota resets at the start of your next billing cycle.

If you have questions or need extended access, feel free to reach out to us at [feedback@warp.dev](mailto:feedback@warp.dev).
