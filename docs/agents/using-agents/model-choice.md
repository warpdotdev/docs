---
description: >-
  Choose from a curated set of top LLMs for Warp's Agents (or let Warp
  auto-select the best model).
---

# Model Choice

## Available models

Warp lets you choose from a curated set of Large Language Models (LLMs) to power your Agentic Development Environment.

**Warp supports the following models:**

* OpenAI:
  * `GPT-5.2` (_low, medium,_ _high_ and _extra high_ reasoning)
  * `GPT-5.2 Codex` (_low, medium, high_, and _extra high_ reasoning)
  * `GPT-5.1 Codex Max` (_low, medium, high_, and _extra high_ reasoning)
  * `GPT-5.1 Codex` _(low, medium,_ and _high_ reasoning)
  * `GPT-5.1` (_low, medium,_ and _high_ reasoning)
  * `GPT-5` (_low, medium,_ and _high_ reasoning)
* Anthropic:
  * `Claude Opus 4.5` with thinking mode
  * `Claude Sonnet 4.5` with thinking mode
  * `Claude Opus 4.1`
  * `Claude Haiku 4.5`
  * `Claude Sonnet 4`
* Google:
  * `Gemini 3 Pro`
  * `Gemini 2.5 Pro`
* z.ai: `GLM 4.6` (hosted in the US, by [Fireworks AI](https://fireworks.ai/models/fireworks/glm-4p6))

### Auto Models

Warp also offers two _Auto_ modes that intelligently select the best model for your task based on the context and request type:

1. **Auto (Cost-efficient)**: Optimizes for lower credit consumption while maintaining strong output quality, helping extend your available usage.
2. **Auto (Responsive)**: Prioritizes the highest-quality results using the fastest available model, though it may consume credits more quickly.
3. **Auto (Genius)**: Adapts to the complexity of your task and selects Warp’s most capable model when it’s worth it. Best for deep debugging, architecture decisions, and /plan-style sessions where you want maximum reasoning quality.

Both Auto models perform well across all agent workflows and are ideal if you prefer Warp to manage model selection dynamically.

### How to change models

You can use the model picker in your prompt input to quickly switch between models. The currently active model appears directly in the input editor.

<figure><img src="../../.gitbook/assets/new-models-oct-2025.png" alt=""><figcaption><p>Model selector in Warp's Universal Input.</p></figcaption></figure>

To change models, click the displayed model name (for example, _Claude Sonnet 4.5_) to open a dropdown with all supported options. Your selection will automatically persist for future prompts.

### Configuring models per Agent Profile

You can configure the base and planning models for each [agent-profiles-permissions.md](agent-profiles-permissions.md "mention"), defining the Agent’s autonomy, tool access, and other permissions.

Edit your default profile or more profiles directly in `Settings > AI > Agents > Profiles`.

<figure><img src="../../.gitbook/assets/base-planning-model-pickers.png" alt=""><figcaption><p>Model choice example, where the base model is Auto (Claude 4 Sonnet) and the planning model is o3.</p></figcaption></figure>

### Zero Data Retention Policies

Warp integrates with multiple Large Language Model (LLM) providers to power its AI-driven features.

**These providers include, but are not limited to:**

* OpenAI
* Anthropic
* Google
* Fireworks AI

Warp has executed **Zero Data Retention (ZDR)** agreements with these providers. This means that, by default across all plans:

* LLM providers commit not to train their models on any customer-generated data processed through Warp’s services.
* LLM providers commit to delete inputs and outputs after generating the relevant output, within a fixed time period.

Warp enforces these commitments through both technical measures and contractual safeguards with the LLM providers.
