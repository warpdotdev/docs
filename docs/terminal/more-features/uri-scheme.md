---
description: >-
  Warps URI scheme enables you to programmatically open new windows, tabs, or
  launch configurations with ease.
---

# URI Scheme

## How to use it

There are several ways to use the URI scheme:

* Open new window `warp://action/new_window?path=<path_to_folder>`
* Open new tab `warp://action/new_tab?path=<path_to_folder>`
* Open Launch Configuration `warp://launch/<launch_configuration_path>`

{% hint style="info" %}
[Warp Preview](../../community/warp-preview-and-alpha-program.md) uri scheme begins with `warppreview://`
{% endhint %}

## How it works

Example of Warp [URIs in use in Warp + Raycast Extension](https://github.com/raycast/extensions/blob/74521b70b62355004b0958393a64f9417b1ff3a6/extensions/warp/src/uri.ts).

{% embed url="https://twitter.com/i/status/1678432353461637121" %}
Warp + Raycast Extension Demo made using URIs
{% endembed %}
