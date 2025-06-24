---
description: >-
  Create reusable guidelines that help Warp’s agents respond with your preferred
  coding standards, project conventions, and personal preferences.
---

# Rules

Warp’s Rules feature lets you create and manage reusable guidelines that inform how agents respond to your prompts. These rules help tailor responses based on your coding standards, project conventions, or personal preferences.&#x20;

Warp can also suggest rules based on your usage patterns to make future agent interactions smarter and more consistent.

**What Rules Can Include**

* Coding standards and best practices
* Project or workspace-specific guidelines
* Personal preferences or tool configurations

### How to access Rules

* From [Warp Drive](warp-drive/): Personal > Rules
* From the [Command Palette](../terminal/command-palette.md): search for "Open AI Rules"
* From the Settings panel: `Settings > AI > Knowledge > Manage Rules`
* From the macOS Menu: `AI > Open Rules`

### Managing Rules

In the Rules pane, users can add, edit, delete any number of rules. Each rule includes a name (optional) and description.

{% embed url="https://www.loom.com/share/3a49462c01e149cf9c040130cebe1184?hideEmbedTopBar=true&hide_owner=true&hide_share=true&hide_title=true" %}
Rules Demo
{% endembed %}

### Rules as Agent context

When relevant, Warp agents will automatically pull in applicable rules to guide their responses. Rules used in an interaction will appear in the conversation under **References** or marked as **derived from** a specific rule.

<figure><img src="../.gitbook/assets/context-derived-from-memory.png" alt="Context derived from memory"><figcaption><p>Derived from rules</p></figcaption></figure>

<figure><img src="../.gitbook/assets/context-references-memory.png" alt="Context derived from memory"><figcaption><p>Rules as references</p></figcaption></figure>

### Rules Privacy

See our [Privacy Page](../privacy/privacy.md) for more information on how we handle data with Rules.
