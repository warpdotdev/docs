# Notifications

## What is it?

Have you ever run a program on the terminal and started doing something else, only to find out a long time later that the program was waiting for a password to continue? No longer! Warp can send you customizable desktop notifications when you are away from the app and something meaningful happens in your terminal sessions. Warp can send you a notification when a command completes after a configurable number of seconds or when a running command needs you to enter a password to proceed. For either of these triggers, Warp will only send you a desktop notification if you are using a different app at the time the trigger is fired.

## How to access it

* Notifications are enabled by default and require MacOS permissions to appear. You will want to **Allow** or **Accept** the request so that Warp can send you desktop notifications. If you accidentally denied it or would like to re-enable Notifications later, check the [troubleshooting guide below](../features/notifications.md#troubleshooting-warp-notifications).
* If you've turned Notifications off before, toggle it back on by going to `Settings > Features`, or quickly toggle Notifications on or off via the Command Palette `CMD-P`. 
* Customize Notification triggers for long-running commands or password prompts by going to `Settings > Features`.

## How it works

![Notifications Demo](../.gitbook/assets/notifications-demo.gif)

## Troubleshooting Warp Notifications

Warp requires two different notifications settings in order to work. Mac system settings found in `Mac > System Preferences > Notifications & Focus > Notifications` and Warp app settings found in `Settings > Features > Notifications` must both be enabled in order for Notifications to work. If you have Notifications enabled in the system and Warp but you still aren't receiving desktop notifications, try the following:
* Make sure that you are navigated away from Warp when you expect to receive the notification.
* Make sure the **Do not Disturb** mode is turned off in `Mac > System Preferences > Notifications > Notifications & Focus > Focus`.
* Go to `Mac > System Preferences > Notifications & Focus > Notifications` and select Warp in the list. Make sure either banner style or alert style notifications are selected, then quit and restart Warp.

Please reach out to us on [Discord](https://warp.dev/discord) or [GitHub](https://github.com/warpdotdev/Warp/issues) if any other issue.
