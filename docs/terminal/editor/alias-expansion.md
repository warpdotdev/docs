---
description: Warp will automatically expand your aliases as you type in the input editor.
---

# Alias Expansion

## How to use it

{% tabs %}
{% tab title="macOS" %}
When Alias Expansion is enabled, type an alias and then hit `SPACE` will expand the alias.

To insert a space without expanding an alias, the default keybinding is `OPT-SPACE`.
{% endtab %}

{% tab title="Windows" %}
When Alias Expansion is enabled, type an alias and then hit `SPACE` will expand the alias.

To insert a space without expanding an alias, the default keybinding is `ALT-SPACE`.
{% endtab %}

{% tab title="Linux" %}
When Alias Expansion is enabled, type an alias and then hit `SPACE` will expand the alias.

To insert a space without expanding an alias, the default keybinding is `ALT-SPACE`.
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Aliases will not be expanded when the command in the expanded form is the same as the alias itself. e.g. if you have an alias `ls='ls -G'`, `ls` will not be expanded in the input editor.
{% endhint %}

## How to access it

Alias expansion is disabled by default. There are two ways to toggle this on and off:

* From Settings: Navigate to `Settings > Features > Editor` and toggle “Expand aliases as you type”.
* From the [Command Palette](../command-palette.md#windows): Search for the “Enable/disable alias expansion” option and hit `ENTER`.

## How it works

{% embed url="https://www.loom.com/share/2267657c033e482890eea75a8a6c5373?hideEmbedTopBar=true&hide_owner=true&hide_share=true&hide_title=true" %}
Alias Expansion Demo
{% endembed %}
