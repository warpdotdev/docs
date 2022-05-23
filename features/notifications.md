# Notifications
Warp can send you desktop notifications when you are away from the app and something meaningful happens in your terminal sessions!

## Getting Started
To get started with notifications,
1. Go to Settings->Features in Warp and toggle Notifications on (ignore this step if you came here from the banner).
1. The first time you enable notifications in Warp, a MacOS request for permissions will appear. 
    - Depending on your MacOS version, this request will look slightly different. In any case, you will want to 'Allow'/'Accept' the request so that Warp is allowed to send you desktop notifications. 
    - If you accidentally denied it or would like to enable notifications later, check the troubleshooting guide below. 
1. Once accepted, you're ready to receive notifications! If you'd like a zero-config setup, then you're all done! But, if you'd like to manually configure *which types* of notifications you receive, keep on reading!

![Notifications Demo](../.gitbook/assets/notifications-demo.gif)

## Configuring Notifications
To configure notifications, go to Settings->Features and scroll to Notifications. Once there, you can configure the different notification triggers to your liking. 

### Notification Triggers
A notification trigger is a reason for which Warp can send you a notification. Currently, we support two different triggers:
1. **Long-running commands.** Warp can send you a notification when a command completes after a configurable number of seconds.
1. **Password prompts.** Warp can send you a notification when a running command needs you to enter a password to proceed.

For either of these triggers, Warp will only send you a desktop notification if you are using a different app at the time the trigger is fired.

## Troubleshooting Warp Notifications

### I'm not receiving notifications when I expect them!
If you have notifications enabled in Warp (under Settings->Features) but you still aren't receiving desktop notifications, try the following:
1. Make sure that you are navigated away from Warp when you expect to receive the notification.
1. Make sure 'Do not Disturb' mode is turned off.
1. Go to System Preferences->Notifications and select Warp in the list. Make sure either banner style or alert style notifications are selected.
1. Quit and restart Warp.

### I don't want to receive notifications!
The easiest way to disable notifications is within Warp itself. Go to Settings->Features and toggle off Notifications. After that, Warp won't try to send you notifications anymore! 

### I have another problem!
We're sorry that notifications aren't working the way you expect them to! Please reach out to us on [Discord](https://warp.dev/discord) or [GitHub](https://github.com/warpdotdev/Warp/issues) and we can help you debug further!
