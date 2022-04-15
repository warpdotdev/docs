# Privacy

Our general philosophy is complete transparency and control of any data leaving your machine.
This means that in general any data sharing is opt-in and under the control of the user, and you should be able to remove or export that data from our servers at any time.

Terminal sessions obviously contain a bunch of potentially sensitive information and we want the absolute minimum sent to our servers necessary in order to provide you with the best possible experience.

See our [privacy page](https://www.warp.dev/privacy) for an explanation (in layman’s terms) or read our [full privacy policy.](https://warp.dev/terms-of-service)

If you have any questions about any of this, please don’t hesitate to reach out at [privacy@warp.dev](mailto:privacy@warp.dev)

## Why is login required for a terminal app?

Login serves two functions now. One is that we think there are features that require login in order to create a better user experience. The other is to improve our product during beta.

We believe that the terminal is more powerful when you can share commands with teammates, generate commands using Open AI Codex, or run shared wikis directly in the terminal. These are not possible if users do not have an account with us. We've already begun building team features and we want to be able to ship them to our users without friction.

For our public beta, we do send telemetry and we do associate it with the logged in user because it makes it much easier to reach out and get feedback when something goes wrong. But we only track metadata, never console output.

## Telemetry

When Warp comes out of beta and enters General Availability, telemetry will be opt-in and anonymous.

We use [Sentry](https://sentry.io/about/) for crash reporting and [Segment](https://segment.com/docs/guides/) for telemetry.

## Exhaustive Telemetry Table

* Account logged in
* Account signed up
* App focus duration
* App focused
* App active usage
* Autosuggestion Inserted
* BaselineCommand Latency
* Block copied
* Block created
* Block selected
  * Cardinality (One, Many)
  * Any modifiers used (`CMD`/`SHIFT`)
* Block sharing link generated
* Block sharing link copied
* Bootstrapping failed
* Bootstrapping slow
* Bootstrapping succeeded
* Confirm Suggestion
* Context menu copy
* Context menu copy selected text
* Context menu find within block
* Context menu insert selected text into input
* Context menu initiate block sharing
* Context menu reinput command(s)
* Complete Welcome Tip
* Database Startup Error
* Dismiss Welcome Tips
* Features Page Action
* Invite received
* Invite requested more
* Jumped to previous command
* Keybinding Changed
* Keybinding Reset to Default
* Loaded a page
* Natural Language Search Generated
* Natural Language Search Initiated
* Natural Language Search Request Failed
* Natural Language Search Result Accepted
* Natural Language Search Quit
* Onboarding survey finished
* Onboarding survey skipped
* Onboarding survey question completed
  * Company
  * Engineering
  * Purpose
  * Role
* Opened channel download
* Opened invite-only download with invalid code
* Opened invite-only download with valid code
* Opened Quake Mode Window
* Opened Suggestions Menu
* Opened Theme Chooser
* Opened Welcome Tips
* Sessions tab created
* Session Abandoned Before Bootstrap
* Split Pane
* SSH Bootstrap Attempt
* Suggestions autosuggestion inserted
* Suggestions single autosuggestion inserted
* Suggestion confirmed / completed
* Suggestions menu opened
* Tab Created
* Tab Single Result Autocompletion
* Theme selected
* Unable to Update To New Version
* Unhandled editor modifier key
* Viewed login page
* Viewed share view
* Workflow Executed
* Workflow Selected