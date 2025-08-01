---
description: >-
  Agent Mode organizes your AI interactions into conversations tied to terminal
  panes, allowing you to attach context blocks, follow up on previous queries,
  or start fresh threads for distinct tasks.
---

# Agent Conversations

## Conversations with Agent Mode

Conceptually, a conversation refers to a sequence of AI queries and blocks. Conversations are tied to panes and you can have multiple Agent Mode conversations running at the same time in different panes.

You will get more accurate results from AI queries if the conversation is relevant to the query you ask. When you start an AI query unrelated to the previous conversation, start a new conversation. When you start an AI query related to the previous conversation, ask a follow-up and stay in the same conversation.

{% hint style="info" %}
Long conversations can have high latency. We recommend creating a new conversation when possible for distinct tasks or questions where the previous context isn't relevant.
{% endhint %}

### **How to ask a follow-up to stay in a conversation**

By default, if you ask an AI query right after any interaction in Agent Mode, your query will be sent as a follow-up. The follow-up ↳ icon is a bent arrow, to indicate your query is continuing the conversation.

{% tabs %}
{% tab title="macOS" %}
To enter follow-up mode manually, press `CMD-Y`.
{% endtab %}

{% tab title="Windows" %}
To enter follow-up mode manually, press `CTRL-SHIFT-Y`.
{% endtab %}

{% tab title="Linux" %}
To enter follow-up mode manually, press `CTRL-Y`.
{% endtab %}
{% endtabs %}

<figure><img src="../../.gitbook/assets/agent-mode-with-followup.png" alt=""><figcaption><p>A continuing conversation in Agent Mode with a follow-up indicator</p></figcaption></figure>

### **How to start a new conversation**

If there is no follow-up ↳ icon next to your input, this indicates a new conversation. If you ask an AI query after running a shell command you will be placed in a new conversation. Agent Mode will also kick you out to a new conversation after 3 hours.

{% tabs %}
{% tab title="macOS" %}
To start a new conversation manually, use `CMD-I` or when using the Universal input enable auto detection mode with `BACKSPACE`.
{% endtab %}

{% tab title="Windows" %}
To start a new conversation manually, use `CTRL-I` or when using the Universal input enable auto detection mode with `BACKSPACE`.
{% endtab %}

{% tab title="Linux" %}
To start a new conversation manually, use `CTRL-I` or when using the Universal input enable auto detection mode with `BACKSPACE`.
{% endtab %}
{% endtabs %}

<figure><img src="../../.gitbook/assets/agent-mode-no-followup.png" alt=""><figcaption><p>A new conversation in Agent Mode with no follow-up indicator</p></figcaption></figure>

{% hint style="info" %}
**Context truncation**

You might notice that in long conversations, the AI loses context from the very beginning of the conversation. This is because Warp's models are limited by context windows (\~128K tokens) and it will discard earlier tokens.
{% endhint %}
