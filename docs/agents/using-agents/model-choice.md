---
description: >-
  Warp lets you choose from a curated set of LLMs for Agent Mode (or let Warp
  auto-select the best model) so you can tailor responses to your specific tasks
  and preferences.
---

# Model Choice

Warp lets you choose from a curated list of LLMs for use in Agent Mode. By default, Warp uses `Claude 4 Sonnet` for Auto and `Claude 3.5 Sonnet` for Lite, but you can switch to other supported models, including:

* **OpenAI**: `GPT-4o`, `GPT-4.1` ,`o4-mini`, `o3`,
* **Anthropic**: `Claude Sonnet 4` ,`Claude Opus 4.1` ,`Claude Sonnet 3.5`
* **Google**: `Gemini 2.5 Pro`

### **Model choice**

* **Base model**: this model serves as the core engine for your Agentic Development Environment. It drives most interactions and invokes other models as necessary. There's an option in the app to show the model picker as well.
* **Planning model**: responsible for breaking down complex tasks into actionable steps and creating structured execution plans.

You can also select "Auto" to let Warp automatically choose the best model for your task based on factors like query type and context.

When you start an agent mode conversation, you will be able to see the model being used.

<figure><img src="../../.gitbook/assets/agent-mode-prompt-sonnet.png" alt=""><figcaption><p>Agent mode prompt using Sonnet</p></figcaption></figure>

To change the model being used, click the current model name, 'claude 3.5 sonnet' in the example image above, to open a dropdown menu with the supported models. Your model choice will persist in future prompts.&#x20;

You can also go to `Settings > AI > Models` and choose your preferred base and planning models which are automatically used by the Agents.

<figure><img src="../../.gitbook/assets/base-planning-model-pickers.png" alt=""><figcaption><p>Model choice example, where the base model is Auto (claude 4 sonnet( and the planning model is o3.</p></figcaption></figure>
