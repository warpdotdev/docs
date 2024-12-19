---
description: >-
  Active AI proactively recommends fixes and next actions based on your terminal
  errors, inputs, and outputs.
---

# Active AI

{% hint style="info" %}
Active AI features can be disabled in `Settings > AI` with the Active AI toggle.
{% endhint %}

## Prompt Suggestions

Prompt Suggestions are contextual, AI-powered suggestions that activate Agent Mode. These banners will provide suggestions for what to ask Agent Mode in specific scenarios, similar to how Warp already suggests commands to run.

<figure><img src="../../.gitbook/assets/spaces_-MbqIgTw17KQvq_DQuRr_uploads_git-blob-9068c40fd8eea9b45eebcda6f08832023b4e9fa0_prompt-suggestions-example.png" alt=""><figcaption><p>Example of inline banner popping up when relevant contextually.</p></figcaption></figure>

If you press `CMD-ENTER` (on Mac), `CTRL-SHIFT-ENTER` (on Linux/Windows), or click on the chip, the suggestion will be auto-populated into your input and run against Agent Mode (with the most recent block attached).

{% hint style="info" %}
Prompt Suggestions use an LLM to generate prompts based on your terminal session, specifically the most recent block. These AI requests do not contribute towards your AI limits, however, any accepted prompts run in Agent Mode contribute as normal. Visit Settings > AI > Agent Mode, if you'd like to turn it off.
{% endhint %}

<figure><img src="../../.gitbook/assets/spaces_-MbqIgTw17KQvq_DQuRr_uploads_git-blob-010f0d6e8d02c054768b2939c9d45cf84447b5e4_prompt-suggestions-setting.png" alt=""><figcaption><p>Setting for Prompt Suggestions</p></figcaption></figure>



## Next Command&#x20;

Next Command uses AI to suggest the next command to run based on your active terminal session and command history. It uses your active terminal session contents and an LLM to generate commands.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2024-12-12 at 5.26.10 PM.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
&#x20;Next Command proactively utilizes an LLM together with your command history and recent block input and output to generate the next command suggestions. \
\
**To disable, please visit Settings > AI > Next Command**
{% endhint %}

#### **Accepting a Next Command Suggestion**

In order to use a next Command Suggestion, please use the `TAB` or `→` key to add the suggested next command to your input buffer. `ENTER` execute the accepted command.

#### **Next Command And Billing**

For the latest information on limits, visit [warp.dev/pricing](https://warp.dev/pricing). A Next Command only counts toward your limit if you explicitly accept the suggestion. If you enter a command that matches a suggested Next Command by typing it manually or rerunning it from your history, it will not count toward your usage.



