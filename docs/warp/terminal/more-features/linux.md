---
description: Linux specific features.
---

# Linux

## Native Wayland

Warp Wayland support can be enabled in **Settings** > **Features** > **System**. Enabling Wayland support may fix issues with blurry text if you have fractional scaling enabled in your window manager.

{% hint style="warning" %}
When native Wayland is enabled, Global Hotkey support will be disabled. Unlike X11, the Wayland protocol does not expose the configuration necessary to support this feature.
{% endhint %}

## Wayland crash recovery

When Wayland support is enabled, Warp uses a custom crash recovery process to detect any crashes that may occur when using Wayland. If there's a crash, Warp will fallback to use X11 to allow you to continue to use the application.
