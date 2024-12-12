---
description: >-
  Active AI proactively recommends fixes and next actions based on errors,
  inputs, and outputs.
---

# Active AI

## Features

### Prompt Suggestions

Prompt Suggestions are contextual, AI-powered suggestions that activate Agent Mode. These banners will provide suggestions for what to ask Agent Mode in specific scenarios, similar to how Warp already suggests commands to run.

<figure><img src="../../.gitbook/assets/spaces_-MbqIgTw17KQvq_DQuRr_uploads_git-blob-9068c40fd8eea9b45eebcda6f08832023b4e9fa0_prompt-suggestions-example.png" alt=""><figcaption><p>Example of inline banner popping up when relevant contextually.</p></figcaption></figure>

If you press `CMD-ENTER` (on Mac), `CTRL-SHIFT-ENTER` (on Linux/Windows), or click on the chip, the suggestion will be auto-populated into your input and run against Agent Mode (with the most recent block attached).

{% hint style="info" %}
Prompt Suggestions use an LLM to generate prompts based on your terminal session, specifically the most recent block. These AI requests do not contribute towards your AI limits, however, any accepted prompts run in Agent Mode contribute as normal. Visit Settings > AI > Agent Mode, if you'd like to turn it off.
{% endhint %}

<figure><img src="../../.gitbook/assets/spaces_-MbqIgTw17KQvq_DQuRr_uploads_git-blob-010f0d6e8d02c054768b2939c9d45cf84447b5e4_prompt-suggestions-setting.png" alt=""><figcaption><p>Setting for Prompt Suggestions</p></figcaption></figure>



### Next Command (coming soon)

Next Command uses AI to suggest the next command to run based on your active terminal session and command history. It uses your active terminal session contents and an LLM to generate commands.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2024-12-12 at 5.26.10 PM.png" alt=""><figcaption></figcaption></figure>
