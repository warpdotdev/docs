# Privacy

Our general philosophy is complete transparency and control of any data leaving your machine.
This means that in general any data sharing is opt-in and under the control of the user, and you should be able to remove or export that data from our servers at any time.

Terminal sessions obviously contain a bunch of potentially sensitive information and we want the absolute minimum sent to our servers necessary in order to provide you with the best possible experience.

See our [privacy page](https://www.warp.dev/privacy) for an explanation (in layman’s terms) or read our [full privacy policy.](https://warp.dev/terms-of-service)

If you have any questions about any of this, please don’t hesitate to reach out at [privacy@warp.dev](mailto:privacy@warp.dev)

## Telemetry

When we do launch publicly, telemetry will be opt-in and anonymous.

But for our closed beta, we do send telemetry by default and we do associate it with the logged in user because it makes it much easier to reach out and get feedback when something goes wrong.

We use [Sentry](https://sentry.io/about/) for crash reporting and [Segment](https://segment.com/docs/guides/) for telemetry.

We do not store any data from the command input or output itself as part of our telemetry.

## Exhaustive Telemetry Table

* Account logged in
* Account signed up
* App focus duration
* App active usage
* Block copied
* Block created
* Block selected
  - Cardinality (One, Many)
  - Any modifiers used (`CMD`/`SHIFT`)
* Block sharing link generated
* Block sharing link copied
* Bootstrapping failed
* Bootstrapping slow
* Bootstrapping succeeded
* Context menu copy
* Context menu copy selected text
* Context menu find within block
* Context menu insert selected text into input
* Context menu initiate block sharing
* Context menu reinput command
* Invite received
* Invite requested more
* Jumped to previous command
* Loaded a page
* Onboarding survey finished
* Onboarding survey skipped
* Onboarding survey question completed
  - Company
  - Engineering
  - Purpose
  - Role
* Opened channel download
* Opened invite-only download with invalid code
* Opened invite-only download with valid code
* Sessions tab created
* Suggestions autosuggestion inserted
* Suggestions single autosuggestion inserted
* Suggestion confirmed / completed
* Suggestions menu opened
* Theme selected
* Unhandled editor modifier key
* Viewed login page
* Viewed share view
