---
description: >-
  Warp can send you customizable desktop notifications when you are away from
  the app and quickly re-focus when something meaningful happens in your
  terminal sessions.
---

# Desktop Notifications

## What is it

Notifications can be sent when a command completes after a configurable number of seconds or when a running command needs you to enter a password to proceed. For either of these triggers, Warp will only send you a desktop notification if you are using a different app at the time the trigger is fired.

## Custom notification hooks (OSC 9 / OSC 777)

Warp supports pluggable notifications triggered by terminal escape sequences, so scripts and tools can raise desktop notifications without additional dependencies.

- OSC 9 (body only): sends a notification with just a body.
  - Format: `ESC ] 9 ; <body> BEL`
  - Example (bash/zsh): `printf '\033]9;Build complete\007'`
- OSC 777 (title + body): sends a notification with a title and body.
  - Format: `ESC ] 777 ; notify ; <title> ; <body> BEL`
  - Example (bash/zsh): `printf '\033]777;notify;Deploy;Success on prod\007'`

Notes:
- Works on macOS, Windows, and Linux where Warp is allowed to show notifications.
- Newlines and semicolons should be avoided or escaped in payloads.
- This feature is enabled by default in current releases of Warp.

## How to access it

### Notifications

* Notifications are enabled by default and require system permissions to appear.
* If you've turned Notifications off before, toggle it back on by going to `Settings > Features > Session`, or quickly toggle Notifications with the [Command Palette](../command-palette.md).
* Customize Notification triggers for long-running commands or password prompts by going to `Settings > Features`.

{% hint style="info" %}
On macOS, you will want to **Allow** or **Accept** the request so that Warp can send you desktop notifications. If you accidentally denied it or would like to re-enable Notifications later, check the [troubleshooting guide below](notifications.md#troubleshooting-notifications).
{% endhint %}

## How it works

{% embed url="https://www.loom.com/share/65967f43a7fa432b98cf3e94766a8e79?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" %}
Notifications Demo
{% endembed %}

## Troubleshooting Notifications

{% tabs %}
{% tab title="macOS" %}
Warp requires two distinct notification settings to work. Mac system settings found in `Mac > System Preferences > Notifications & Focus` and Warp app settings found in `Settings > Features > Session` must both be enabled for Notifications to show.\
\
If you have Notifications enabled in the system and Warp, but you still aren't receiving desktop notifications, try the following:

* Make sure that you are navigated away from Warp when you expect to receive the notification.
* Make sure the **Do Not Disturb** mode is turned off in `Mac > System Preferences > Notifications > Notifications & Focus > Focus`.
* Go to `Mac > System Preferences > Notifications & Focus > Notifications` and select Warp in the list. Make sure either banner style or alert style notifications are selected, then quit and restart Warp.
* To get the MacOS notification prompt to show again for Warp, run `defaults delete dev.warp.Warp-Stable Notifications`, then restart Warp and toggle on the `Settings > Features > Receive desktop notifications from Warp`.
* Once all of the above is done, please Restart MacOS to apply the changes and that should help with restoring notifications in Warp.
{% endtab %}

{% tab title="Windows" %}
Warp requires two distinct notification settings to work. Windows system settings found in `Settings > System > Notifications > Warp` and Warp app settings found in `Settings > Features > Session` must both be enabled for Notifications to show.

If you have Notifications enabled in the system and Warp, but you still aren't receiving desktop notifications, try the following:

* Make sure that you are navigated away from Warp when you expect to receive the notification.
* Make sure the **Do Not Disturb** mode or **Focus** is turned off.
* Go to `System > Notifications` and select Warp in the list. Make sure notifications are turned on, then quit and restart Warp.
{% endtab %}

{% tab title="Linux" %}
Warp requires two distinct notification settings to work. Linux system settings found in `Settings > Notifications > Warp` and Warp app settings found in `Settings > Features > Session` must both be enabled for Notifications to show.

If you have Notifications enabled in the system and Warp, but you still aren't receiving desktop notifications, try the following:

* Make sure that you are navigated away from Warp when you expect to receive the notification.
* Make sure the **Do Not Disturb** mode (if your distribution supports it) is turned off.
* Go to `Settings > Notifications` and select Warp in the list. Make sure notifications are turned on, then quit and restart Warp.
{% endtab %}
{% endtabs %}

Please [reach out to us](../../support-and-billing/sending-us-feedback.md#sending-warp-feedback) if any other issues.
