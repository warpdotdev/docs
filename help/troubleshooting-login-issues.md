---
description: Instructions on how to troubleshoot login issues
---

# Troubleshooting Login Issues

## Nothing happens when I click "Sign Up with GitHub" on Safari

You are on Safari and you might notice in your console that you get the following messages:

1. `Unable to access localStorage`
2. And every time you click the "Sign Up" button, you get `Unhandled Promise Rejection: Error: This operation is not supported in the environment the application is running on. "location.protocol" must be http, https, or chrome-extension and web storage must be enabled.`&#x20;

This error occurs likely because you are blocking all cookies in Safari's security settings, but Firebase Auth requires the cookie to record whether the user is logged in. **To fix it:**

1. Go to Safari Preferences > Privacy
2. Uncheck the "Block all cookies" checkbox

