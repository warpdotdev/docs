---
description: >-
  Active AI proactively recommends fixes and next actions based on your terminal
  errors, inputs, and outputs.
---

# Active AI

{% hint style="info" %}
Active AI features can be disabled in `Settings > AI` with the Active AI toggle.
{% endhint %}

## Prompt suggestions

Prompt suggestions are contextual, AI-powered suggestions that activate Agent Mode. These banners will provide suggestions for what to ask Agent Mode in specific scenarios, similar to how Warp already suggests commands to run.

* To disable, please visit `Settings > AI > Active AI > Prompt Suggestions`

<figure><img src="../../.gitbook/assets/prompt-suggestions-example (1).png" alt=""><figcaption><p>Example of inline banner popping up when relevant contextually.</p></figcaption></figure>

### Accepting a prompt suggestion

If you press `CMD-ENTER` (on Mac), `CTRL-SHIFT-ENTER` (on Linux/Windows), or click on the chip, the suggestion will be auto-populated into your input and run against [Agent Mode](agent-mode.md) (with the most recent block attached).

{% hint style="info" %}
Prompt Suggestions use an LLM to generate prompts based on your terminal session, specifically the most recent block. These AI requests do not contribute towards your AI limits, however, any accepted prompts run in Agent Mode contribute as normal. Visit Settings > AI > Agent Mode, if you'd like to turn it off.

[Secret Redaction](../secret-redaction.md) is automatically applied to any content sent to Active AI features to prevent any sensitive data being leaked.
{% endhint %}

<figure><img src="../../.gitbook/assets/prompt-suggestions-setting (1).png" alt=""><figcaption><p>Setting for Prompt Suggestions</p></figcaption></figure>

## Next command

Next command uses AI to suggest the next command to run based on your active terminal session and command history. It uses your active terminal session contents and an LLM to generate commands.

* To disable, please visit `Settings > AI > Active AI > Next Command`

<figure><img src="../../.gitbook/assets/next-command.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Next command is an LLM-based feature which utilizes your command history (enriched with git branch, exit code, and directory metadata) as well as recent block input and output to generate the next command suggestions.

[Secret Redaction](../secret-redaction.md) is automatically applied to any content sent to Active AI features to prevent any sensitive data being leaked.
{% endhint %}

### Accepting a next command suggestion

In order to use a next command suggestion, please use the `TAB` key , `→` key , or `CTRL-F` to add the suggested next command to your input buffer. `ENTER` executes the accepted command.

### Next command and billing

For the latest information on limits, visit [warp.dev/pricing](https://warp.dev/pricing). A next command only counts toward your limit if you explicitly accept the suggestion. If you enter a command that matches a suggested next command by typing it manually or rerunning it from your history, it will not count toward your usage.
