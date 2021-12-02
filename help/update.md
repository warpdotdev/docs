# Updating Warp

When there is an update available, you will notice a notification in the top-right corner of Warp.

![An update is available for Warp](../.gitbook/assets/9\_update\_available.png)

To check for updates, simply click on the same update menu -> Check for Update…

If nothing happens, it means you already have the latest stable build.

![Check for updates in Warp](../.gitbook/assets/9\_check\_for\_updates.png)



## Autoupdate Issues

Warp cannot autoupdate if it does not have correct permissions to replace the the running version of Warp. If this is the case, a large banner will show prompting you to manually update Warp.

![](<../.gitbook/assets/image (2).png>)

There are 2 main causes of this:

1. You opened Warp directly from the mounted volume and instead of dragging it into your `Applications` directory. If this is the case, the easiest fix is to quit Warp, drag the application into `/Applications` , and restart Warp.
2. You are a non-Admin user. This can happen if you use a computer with multiple profiles. If you have admin access on the computer, opening the app with the admin user should fix the autoupdate issues.

