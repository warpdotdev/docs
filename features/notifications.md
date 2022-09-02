# Notifications

## What is it?

Have you ever ran a program on the terminal and started doing something else, only to find out a long time later that the program was waiting for a password to continue? No longer! Warp can send you desktop notifications when you are away from the app and something meaningful happens in your terminal sessions, like when a command completes or when you're prompted to enter a password.

## How to access it

1. Notifications can be toggled through `Settings > Features`.
2. Once enabled, you can configure notifications triggers for long running commands or password prompts.
3. You can also toggle Notifications via the Command Palette `CMD-P`.

_Note:_ The first time you enable notifications in Warp, a MacOS request for permissions will appear. You will want to **Allow** or **Accept** the request so that Warp can send you desktop notifications. If you accidentally denied it or would like to enable notifications later, check the troubleshooting guide below.

## How it works

![Notifications Demo](../.gitbook/assets/notifications-demo.gif)

## Troubleshooting Warp Notifications

If you have Notifications enabled in Warp but you still aren't receiving desktop notifications, try the following:
* Make sure that you are navigated away from Warp when you expect to receive the notification.
* Make sure 'Do not Disturb' mode is turned off.
* Go to `System Preferences > Notifications` and select Warp in the list. Make sure either banner style or alert style notifications are selected, then quit and restart Warp.

Please reach out to us on [Discord](https://warp.dev/discord) or [GitHub](https://github.com/warpdotdev/Warp/issues) if any other issue.
