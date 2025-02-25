---
description: >-
  Warp will automatically suggest commands as you type based on shell history
  and possible completions.
---

# Autosuggestions

## How to access it

* From the [Command Palette](../command-palette.md), type in "Autosuggestions" to toggle.

{% hint style="info" %}
**Terminal Tip**

You can change the keybinding for accepting autosuggestions to `Tab`. Configure this in the "Tab key behavior" setting under Features > Editor. _Note: This will update the keybinding for opening the completions menu to `CTRL-SPACE`. You can also enable the "Open completions menu as you type" in Settings > Features so that the completions menu opens automatically._
{% endhint %}

## How to use it

{% tabs %}
{% tab title="macOS" %}
There are several ways to accept autosuggestions, either completely or partially:

* Complete an autosuggestion using the `RIGHT` arrow or `CTRL-F`.
* `CTRL-E` also, completes the autosuggestion when your cursor is at the end of the buffer.
* `CTRL-RIGHT` can be used to partially complete the autosuggestion one component at a time.
{% endtab %}

{% tab title="Linux" %}
There are several ways to accept autosuggestions, either completely or partially:

* Complete an autosuggestion using the `RIGHT` arrow or `CTRL-F`.
* `CTRL-E` jumps to the last character in the Input Editor, then `RIGHT` completes the autosuggestion.
* `CTRL-RIGHT` can be used to partially complete the autosuggestion one component at a time.
{% endtab %}
{% endtabs %}

## How it works

{% embed url="https://www.loom.com/share/5e87c52ae855486ab88ffb2f89aeaf73?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" %}
Autosuggestion Demo
{% endembed %}
