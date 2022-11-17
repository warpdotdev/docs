# Updating Warp

Warp automatically checks for updates on startup. A notification will appear in the top right corner of the Warp window when a new update is available.

![Update Available](../.gitbook/assets/updating\_warp-available.png)

To check for updates, simply click on the same update menu -> Check for Update

![Update Check Manually](../.gitbook/assets/updating\_warp-check.gif)

If nothing happens, it means you already have the latest stable build.

## Auto-Update Issues

Warp cannot auto-update if it does not have correct permissions to replace the running version of Warp If this is the case, a banner will prompt you to manually update Warp.

![Update Available](<../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png>)

There are 2 main causes of this:

1. You opened Warp directly from the mounted volume and instead of dragging it into your Applications directory. If this is the case, the easiest fix is to quit Warp, drag the application into /Applications, and restart Warp.
2. You are a non-Admin user. This can happen if you use a computer with multiple profiles. If you have admin access on the computer, opening the app with the admin user should fix the auto-update issues.

Note (Nov 2021): We will work on a fix for this in the future so that multiple profiles can use Warp.

Note (Oct 2022): There is a known issue with [auto-update on MacOS Ventura](known-issues.md#auto-update-on-macos-ventura).
