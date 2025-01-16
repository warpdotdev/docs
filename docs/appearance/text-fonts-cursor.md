---
description: >-
  Warp supports customizing the font and how text is displayed. This can help
  improve readability and usability. Warp also supports disabling the blinking
  cursor.
---

# Text, Fonts, & Cursor

{% hint style="info" %}
Once a new font is installed in your system, you need to restart Warp for it to show on the list of options. You may also need to check "View all available system fonts" to see the new font.
{% endhint %}

## How to use it

### Text and Fonts

To access it, go to `Settings > Appearance > Text`

From there you can customize:

* Font type
* Font size
* Line height
* Use thin strokes
  * The default setting prevents text from being blurry on low-DPI displays.

{% hint style="warning" %}
On Linux, Warp does not support the "Use thin stroke" feature.
{% endhint %}

* Enforce minimum contrast
  * The default setting tweaks named colors to meet accessibility standards.
* Show ligatures in terminal

{% hint style="info" %}
Enabling ligatures can reduce performance. Warps default font, Hack, doesn't yet have ligature support. We recommend font that supports ligatures (e.g. [Fira Code](https://github.com/tonsky/FiraCode)) as a stopgap.
{% endhint %}

### Cursor

To access it, go to `Settings > Appearance > Cursor`

From there you can customize:

* Select the Cursor type to Bar, Block, or Underline.
* Toggle the Blinking cursor or from the [Command Palette](../features/command-palette.md), type "Cursor blink" and toggle the setting.

{% hint style="info" %}
Cursor type preference is disabled while [Vim keybindings](../features/editor/vim.md) (vim mode) is active.
{% endhint %}

## How it works

{% embed url="https://www.loom.com/share/be2fa6ab10a3494a8c57a5431966905b?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" %}
Text and Fonts Demo
{% endembed %}

{% embed url="https://www.loom.com/share/6ce3218472894763bb80a26b6c632c4d?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" %}
Cursor Demo
{% endembed %}
