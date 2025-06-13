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

### How to attach context to an Agent Mode conversation

Agent Mode can gather context from your terminal sessions and tailor every command to your session and environment.

You can supply a block of context to your conversation with Agent Mode as part of your query. From the block in the terminal, click the AI sparkles icon to "Attach as Agent Mode context."

<figure><img src="../../.gitbook/assets/remove_all_untracked_files.png" alt=""><figcaption><p>From a block of output, attach the block and ask Agent Mode to remove all untracked files.</p></figcaption></figure>

The most common use case is to ask the AI to fix an error. You can attach the error in a query to Agent Mode and type "fix it."

If you're already in Agent Mode, use the following ways to attach or clear context from your query:

{% tabs %}
{% tab title="macOS" %}
**Attach a previous block**

* To attach blocks to a query, you can use `CMD-UP` to attach the previous block as context to the query. While holding `CMD`, you can then use your `UP/DOWN` keys to pick another block to attach.
  * You may also use your mouse to attach blocks in your session. Hold `CMD` as you click on other blocks to extend your block selection.

**Clear a previous block**

* To clear blocks from a query, you can use `CMD-DOWN` until the blocks are removed from context.
  * You may also use your mouse to clear blocks in your session. Hold `CMD` as you click on an attached block to clear it.

{% hint style="info" %}
When using "Pin to the top" [Input Position](../../terminal/appearance/input-position.md), the direction for attaching or detaching is reversed (i.e. `CMD-DOWN` attaches blocks to context, while `CMD-UP` clears blocks from context).
{% endhint %}
{% endtab %}

{% tab title="Windows" %}
**Attach a previous block**

* To attach blocks to a query, you can use `CTRL-UP` to attach the previous block as context to the query. While holding `CTRL`, you can then use your `UP/DOWN` keys to pick another block to attach.
  * You may also use your mouse to select blocks in your session. Hold `CTRL` as you click on other blocks to extend your block selection.

**Clear a previous block**

* To clear blocks from a query, you can use `CTRL-DOWN` until the blocks are removed from context.
  * You may also use your mouse to clear blocks in your session. Hold `CTRL` as you click on an attached block to clear it.

{% hint style="info" %}
When using "Pin to the top" [Input Position](../../terminal/appearance/input-position.md), the direction for attaching or detaching is reversed (i.e. `CTRL-DOWN` attaches blocks to context, while `CTRL-UP` clears blocks from context).
{% endhint %}
{% endtab %}

{% tab title="Linux" %}
**Attach a previous block**

* To attach blocks to a query, you can use `CTRL-UP` to attach the previous block as context to the query. While holding `CTRL`, you can then use your `UP/DOWN` keys to pick another block to attach.
  * You may also use your mouse to select blocks in your session. Hold `CTRL` as you click on other blocks to extend your block selection.

**Clear a previous block**

* To clear blocks from a query, you can use `CTRL-DOWN` until the blocks are removed from context.
  * You may also use your mouse to clear blocks in your session. Hold `CTRL` as you click on an attached block to clear it.

{% hint style="info" %}
When using "Pin to the top" [Input Position](../../terminal/appearance/input-position.md), the direction for attaching or detaching is reversed (i.e. `CTRL-DOWN` attaches blocks to context, while `CTRL-UP` clears blocks from context).
{% endhint %}
{% endtab %}
{% endtabs %}

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
To start a new conversation manually, use `CMD-Y` or `BACKSPACE`.
{% endtab %}

{% tab title="Windows" %}
To start a new conversation manually, use `CTRL-Y` or `BACKSPACE`.
{% endtab %}

{% tab title="Linux" %}
To start a new conversation manually, use `CTRL-Y` or `BACKSPACE`.
{% endtab %}
{% endtabs %}

<figure><img src="../../.gitbook/assets/agent-mode-no-followup.png" alt=""><figcaption><p>A new conversation in Agent Mode with no follow-up indicator</p></figcaption></figure>

{% hint style="info" %}
**Context truncation**

You might notice that in long conversations, the AI loses context from the very beginning of the conversation. This is because Warp's models are limited by context windows (\~128K tokens) and it will discard earlier tokens.
{% endhint %}
