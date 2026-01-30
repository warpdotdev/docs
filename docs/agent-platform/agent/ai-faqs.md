---
description: >-
  Frequently asked questions about Warp's AI features, including supported
  models, privacy practices, credit limits, billing, and usage guidelines.
---

# AI FAQs

## General

### What data is sent and/or stored when using Agents in Warp?

See our [Privacy Page](https://docs.warp.dev/support-and-community/privacy-and-security/privacy) for more information on how we handle data used by Agents in Warp.

### What happened to the old Warp AI chat panel?

Agent Mode has replaced the Warp AI chat panel. Agent Mode is more powerful in all of the chat panel's use cases. Not only can Agent Mode run commands for you, it can also gather context without you needing to copy and paste. To start a similar chat panel, click the AI button in the menu bar to start on a new AI pane.

### Is my data used for model training?

Warp reserves the right to use data collected to train models and improve Warp. Warp has Zero Data Retention with all its model providers (e.g. Anthropic, OpenAI, etc.). Please learn more about telemetry in our [Privacy Page](https://docs.warp.dev/support-and-community/privacy-and-security/privacy).

### What model are you using for Agent Mode?

Warp supports a curated list of LLMs from providers like OpenAI, Anthropic, and Gemini. To view the full list of supported models and learn how to switch between them, visit the [Model Choice](using-agents/model-choice.md) page.

### Can I use my own LLM API key?

Organizations on the Enterprise plan can enable a “Bring Your Own LLM” option to meet strict security or compliance requirements. Our team will work closely with you to support your preferred LLM provider. This feature is not currently available on other plans.

## Billing

Every Warp plan includes a set number of AI credits per user per month. Please refer to [pricing](https://www.warp.dev/pricing) to compare plans.

AI credit limits apply to Agent Mode, [Generate](generate.md), and [AI autofill in Workflows](https://docs.warp.dev/knowledge-and-collaboration/warp-drive/workflows#ai-autofill). When you have used up your allotted credits for the cycle, you will not be able to issue any more AI credits until the cycle renews.

For questions around what counts as a AI credit, what counts as a token, and how often credits refresh, please refer to [AI Credits](https://docs.warp.dev/support-and-community/plans-and-billing/ai-credits) and more on the [Plans & Pricing](https://docs.warp.dev/support-and-community/plans-and-billing/plans-and-pricing) page.

## Common AI error messages

#### **"Message token limit exceeded" error**

This error means your input (plus attached context) exceeds the maximum context window of the model you're using. For example, GPT-4o has a context window limit of 123,904 tokens. If you exceed that, you may receive no output.

To fix this, try:

* Starting a new conversation
* Reducing the number of blocks or lines attached to your query

#### "Monthly request limit exceeded" or "Monthly credit limit exceeded" errors

Once you exceed your AI credits on the Turbo plan (see [pricing](https://www.warp.dev/pricing) for current limits), premium models will be disabled until your quota resets at the start of your next billing cycle.

**Request failed with error: QuotaLimit**

Once you exceed your AI token limits, all models will be disabled. Note that credits and tokens are calculated separately, and even though the plans may have a set number of credits, they also have a limited number of tokens.

**Request failed with error: ErrorStatus (403, "Your account has been blocked from using AI features")**

This message means your account has been blocked from using AI features, typically due to a violation of our [Terms of Service](https://www.warp.dev/terms-of-service) or suspected abuse (e.g. attempting to bypass credit or token limits).

To resolve or clarify this, please contact our team at [appeals@warp.dev](mailto:appeals@warp.dev) if you believe this was an error. We'll review your case and respond as soon as possible.

{% hint style="warning" %}
Note that any error that does not mention appeals@warp.dev isn't related to being blocked and should be reported as feedback or a bug. See [Sending Us Feedback](https://docs.warp.dev/support-and-community/troubleshooting-and-support/sending-us-feedback) for more.
{% endhint %}

## Gathering AI debugging ID

In cases where you have issues with the Agent, we may ask for the AI debugging ID to troubleshoot the specific conversation. To gather the debugging ID, see [Gathering AI Debugging ID](https://docs.warp.dev/support-and-community/troubleshooting-and-support/sending-us-feedback#gathering-ai-debugging-id) for detailed steps.
