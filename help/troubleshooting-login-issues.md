---
description: Instructions on how to troubleshoot login issues
---

# Troubleshooting Login Issues

## Nothing happens when I click "Sign Up"

Clicking it should open a login pop-up. If clicking the signup button opens a blank pop-up window, try using a proxy. It is possible that your ISP or Firewall is blocking the app's call to `*.googleapis.com` or `*.segment.io`. In in some older Ruby development environments, `.dev` domains do not resolve properly and you may need to delete the `/etc/resolver/dev`, see more [here](https://superuser.com/questions/1374892/dev-domains-dont-resolve).

### All browsers

This error could occur if you installed an ad blocker and the ad blocker blocks all pop-ups, including our Firebase auth pop-up. **To fix it:**

1. Disable your ad blocker just for app.warp.dev
2. Refresh and try again

### Safari

You are on Safari and you might notice in your console that you get the following messages:

1. `Unable to access localStorage`
2. And every time you click the "Sign Up" button, you get `Unhandled Promise Rejection: Error: This operation is not supported in the environment the application is running on. "location.protocol" must be http, https, or chrome-extension and web storage must be enabled.`

This error occurs likely because you are blocking all cookies in Safari's security settings, but Firebase Auth requires the cookie to record whether the user is logged in. **To fix it:**

1. Go to Safari Preferences > Privacy
2. Uncheck the "Block all cookies" checkbox

If "Sign Up" does not work after trying the steps above, fill out [this Typeform](https://zachlloyd.typeform.com/to/UnZu0akR#\&question=sign\_up?utm\_source=docs) and our team will reach out to you.

## Nothing happens when I click "Take me to Warp"

If this happens to you, use the link provided on the web logged-in page (https://app.warp.dev/logged\_in) to copy the authentication token, then paste it into the app as shown below.

![Copy and Pasting an Authentication Token](../.gitbook/assets/auth-token-flow.png)

If "Take me to Warp" is still not working, please fill out [this Typeform](https://zachlloyd.typeform.com/to/UnZu0akR#\&question=take\_me\_to\_warp?utm\_source=docs) and our team will reach out to you.
