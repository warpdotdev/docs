---
description: Instructions on how to troubleshoot login issues
---

# Troubleshooting Login Issues

## Nothing happens when I click "Sign Up"

Clicking it should open a login pop-up. If signing up does not work after trying the steps below, fill out [this Typeform](https://zachlloyd.typeform.com/to/UnZu0akR#&question=sign_up?utm_source=docs) and our team will reach out to you. If clicking the signup buttons opens a blank pop-up window, try using a proxy. It is possible that your ISP or Firewall is blocking the app's call to `*.googleapis.com` or `*.segment.io`.

### All browsers

This error could occur if you installed an ad blocker and the ad blocker blocks all pop-ups, including our Firebase auth pop-up. **To fix it:**

1. Disable your ad blocker just for app.warp.dev
2. Refresh and try again

### Safari

You are on Safari and you might notice in your console that you get the following messages:

1. `Unable to access localStorage`
2. And every time you click the "Sign Up" button, you get `Unhandled Promise Rejection: Error: This operation is not supported in the environment the application is running on. "location.protocol" must be http, https, or chrome-extension and web storage must be enabled.`&#x20;

This error occurs likely because you are blocking all cookies in Safari's security settings, but Firebase Auth requires the cookie to record whether the user is logged in. **To fix it:**

1. Go to Safari Preferences > Privacy
2. Uncheck the "Block all cookies" checkbox

## Nothing happens when I click "Take me to Warp"

If this happens to you, use the link provided on the web logged-in page (https://app.warp.dev/logged_in) to copy the authentication token, then paste it into the app as shown below.

![Copy and Pasting an Authentication Token](../.gitbook/assets/auth-token-flow.png)

If "Take me to Warp" is still not working, please fill out [this Typeform](https://zachlloyd.typeform.com/to/UnZu0akR#&question=take_me_to_warp?utm_source=docs) and our team will reach out to you.
