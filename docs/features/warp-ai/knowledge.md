---
description: >-
  Provide more context to your Agent Mode interactions.
---

# Knowledge

Warp's Knowledge feature allows you to create and store rules that provide context to Agent Mode interations for smarter and more tailored assistance. These rules can include: 
* Coding standards and best practices
* Project and workspace guidelines
* User-specific preferences

### How to access it
* From the [Warp Drive](../warp-drive/README.md), under "Personal" > "Rules"
* From the [Command Palette](command-palette.md), search for "Open AI Rules"
* From the Settings panel, `Settings > AI > Manage Rules`
* From the macOS Menu, `AI > Open Rules`

### Managing Knowledge
In the Rules pane, users can add, edit, delete any number of rules. Each rule includes a name (optional) and description.

{% embed url="https://www.loom.com/share/3a49462c01e149cf9c040130cebe1184?hideEmbedTopBar=true&hide_owner=true&hide_share=true&hide_title=true" %}
Knowledge Demo
{% endembed %}

### Knowledge as Agent Mode context
Agent Mode can leverage the rules you created to tailor its responses. Rules that are pulled as context will be displayed in the conversation as a citation under "References" or "derived from".

<figure><img src="../../.gitbook/assets/context-derived-from-memory.png" alt="Context derived from memory"><figcaption><p>Derived from memory</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/context-references-memory.png" alt="Context derived from memory"><figcaption><p>Memory as references</p></figcaption></figure>

### Knowledge Privacy

See our [Privacy Page](../../getting-started/privacy.md) for more information on how we handle data with Knowledge.
