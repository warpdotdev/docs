---
description: An overview of Warp's approach to privacy
---

# Privacy

## Our Philosophy

{% hint style="info" %}
If you have any questions about any of this, please don’t hesitate to reach out at [privacy@warp.dev](mailto:privacy@warp.dev).
{% endhint %}

Our philosophy is complete transparency and control of any data leaving your machine. This means you can:

* View a list of [all the telemetry events](privacy.md#exhaustive-telemetry-table) that get sent
* Monitor telemetry in real-time with our native [Network Log](../features/network-log.md)
* [Opt-out](privacy.md#how-to-disable-telemetry) of telemetry at any time

Telemetry and crash reporting are used to improve the product and to debug any issues that may arise. Terminal sessions contain sensitive information, and we want the absolute minimum sent to our servers necessary in order to provide you with the best possible experience.

Telemetry data **never includes console input or output** and usage of this data will never be part of our business model.

You can view our [full privacy policy here](https://assets-global.website-files.com/60352b1db5736ada4741b380/60b7f8d410ec2b9fc2a45af9\_privacy-notice.pdf).

## How to disable telemetry and crash reporting

### Opt-out during signup

1. Click on "Privacy Settings"
2.  Click the toggles of the items you want on/off (if it's blue, it's "on")\


    <figure><img src="../.gitbook/assets/opt-out-signup-modal.png" alt=""><figcaption><p>Privacy Settings During Signup</p></figcaption></figure>

### Opt-out after signup

1. Open the command-palette and search for privacy
2.  Toggle the items you want on/off (if it's blue, it's "on")\


    <figure><img src="../.gitbook/assets/privacy-telem-opt-out.png" alt=""><figcaption><p>Privacy Settings After Signup</p></figcaption></figure>

### Login is still required, why?

The primary reason is that login allows us to build cloud-oriented features that make the terminal have a concept of “your stuff” and “your team’s stuff” – for example [Block Sharing](https://docs.warp.dev/features/blocks/block-sharing). This is the same reason other collaborative apps like Figma and Github require login – identity is the basis of building cloud-native apps.

That said, we understand the desire to try Warp before logging in, and are exploring product experiences that will allow users to preview Warp before signup.

{% hint style="info" %}
If you have any feedback about our login policy, please send it to this [Typeform.](https://zachlloyd.typeform.com/to/UnZu0akR#question=login\_required?utm\_source=docs)
{% endhint %}

## What telemetry data do we collect and why?

We collect usage data (only metadata **never console input or output**) to measure feature usage, discover product issues, and to help guide what we prioritize. Selling usage data will never be part of our business model, it is used solely to improve the end-user experience.

We use [Sentry](https://sentry.io/about/) for crash reporting and [Segment](https://segment.com/docs/guides/) for telemetry.

### Exhaustive Telemetry Table

| Event Name                                                 | Description                                                                                                              |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `Accept Natural Language Search Result`                    | Accepted AI Command Search result                                                                                        |
| `App Startup`                                              | App is launched                                                                                                          |
| `Approve Domains`                                          | under team management in settings, domain is approved for users with corresponding email domain to join the team         |
| `Auth Common Question Clicked in App`                      | Clicked on "Common Question" when logging in                                                                             |
| `Auth: Toggle Common Questions`                            | Toggled FAQ Page when logging in                                                                                         |
| `Autosuggestion Inserted`                                  | Accepted autosuggestion                                                                                                  |
| `BaselineCommand Latency`                                  | Command execution time                                                                                                   |
| `Block Creation`                                           | Created Block                                                                                                            |
| `Block Finished to Precmd Delay`                           | Latency between command finished and the precmd hook                                                                     |
| `Block Selection`                                          | Selected Block                                                                                                           |
| `Bootstrapping Slow`                                       | Slow bootstrap on session startup                                                                                        |
| `Bootstrapping Succeeded`                                  | Successful bootstrap for session                                                                                         |
| `Changed invite view option`                               | Toggled between link and invite for invite                                                                               |
| `Changed view option`                                      | view is changed between workflows and notebooks in the team page                                                         |
| `Clicked on another way to login`                          | Clicked on "another way to login"                                                                                        |
| `Clicked on have trouble logging in`                       | Clicked on "have trouble logging in"                                                                                     |
| `Command Correction Event`                                 | Accepted command correction                                                                                              |
| `Command Search Filter Changed`                            | Changed command search filter                                                                                            |
| `Command Search Opened`                                    | opened command search (universal search panel to search                                                                  |
| `Command Search Result Accepted`                           | Accepted command search result                                                                                           |
| `Complete Welcome Tip`                                     | Completed all welcome tips items                                                                                         |
| `Confirm Suggestion`                                       | Accepted tab completion suggestion                                                                                       |
| `Context Menu Copy`                                        | Clicked "Copy" in context menu                                                                                           |
| `Context Menu Copy Prompt Clicked`                         | "copy prompt" in context menu                                                                                            |
| `Context Menu Copy Selected Text`                          | Clicked "copy selected text" in context menu                                                                             |
| `Context Menu Insert Selected Text into Input`             | Clicked "insert into input" in context menu                                                                              |
| `Context Menu Toggle Git Prompt Dirty Indicator`           | Toggled indicator of dirty git prompt                                                                                    |
| `Context Menu Toggle PS1`                                  | Clicked "user default prompt" in context menu                                                                            |
| `Context Menu: Find Within Blocks`                         | Clicked "find within blocks" in context menu                                                                             |
| `Context Menu: Initiate Block Sharing`                     | Clicked "create permalink..." in context menu                                                                            |
| `Context Menu: Reinput Commands`                           | Clicked "reinput commands" in context menu                                                                               |
| `Copy Block Sharing Link`                                  | Clicked "Copy Link" on Block Sharing Modal                                                                               |
| `Copy Invite Link`                                         | Clicked "Copy Link" on Referral Modal                                                                                    |
| `Daily App Focus Duration (seconds)`                       | Cumulative duration of daily focus time on app in seconds                                                                |
| `Database Read Error`                                      | database read error when trying to get app state for session restoration                                                 |
| `Database Startup Error`                                   | failed to initialize sqlite upon startup                                                                                 |
| `Deleted Notebook`                                         | Deleted a notebook                                                                                                       |
| `Deleted Workflow`                                         | Workflow is deleted on the teams page                                                                                    |
| `Dismiss Welcome Tips`                                     | Dismissed Welcome tips                                                                                                   |
| `Draw Frame Latency`                                       | Recorded time to draw a frame in app (in ms)                                                                             |
| `Draw Frame Latency Histogram Overflow`                    | could not summarize histogram of draw frame latency                                                                      |
| `Edited Input Before Precmd`                               | Input edited before precmd hook completes                                                                                |
| `Expensive Frame`                                          | frame took long time to draw (past a certain threshold)                                                                  |
| `Features Page Action`                                     | changed settings in Features Page                                                                                        |
| `Find Option Toggled`                                      | changed settings in Find Toggle                                                                                          |
| `Finish Onboarding Survey`                                 | onboarding survey finished                                                                                               |
| `Generate Block Sharing Link`                              | Generated block sharing link                                                                                             |
| `Generate Natural Language Search`                         | Requested AI Command Search generation                                                                                   |
| `Initiate Natural Language Search`                         | Opened AI Command Search panel                                                                                           |
| `Jumped to Bookmark Block`                                 | Jumped to bookmarked block                                                                                               |
| `Jumped to Previous Command`                               | Jumped to a previous command                                                                                             |
| `Keybinding Changed`                                       | Edited a custom keybinding                                                                                               |
| `Keybinding Reset to Default`                              | Reset a custom keybinding to its default                                                                                 |
| `Log In Button Clicked in App`                             | Clicked on "Log in" button                                                                                               |
| `Logged in to native app`                                  | Login is successful                                                                                                      |
| `Move Active Tab`                                          | move active tab left or right                                                                                            |
| `Move Tab`                                                 | move tab left or right                                                                                                   |
| `Natural Language Search Request Failed`                   | Request AI Command Search generation failed                                                                              |
| `New Session From Directory`                               | dragged a file, folder, etc. into Warp to start a session                                                                |
| `Notebook Created`                                         | Created a new notebook                                                                                                   |
| `Notebook Opened`                                          | Opened a notebook                                                                                                        |
| `Notification Clicked`                                     | clicked desktop notification sent from Warp                                                                              |
| `Notification Failed to Send`                              | failed to send desktop notification                                                                                      |
| `Notification Permissions Requested`                       | requested permission for desktop notification permissions                                                                |
| `Notification Request Permissions Outcome`                 | recorded outcome of attempting to request desktop notification permissions                                               |
| `Notification Sent`                                        | sent desktop notification                                                                                                |
| `Notifications Discovery Banner Action`                    | showed banner introducing the notifications feature                                                                      |
| `Notifications Error Banner Action`                        | showed error banner for notifications feature                                                                            |
| `Open Command Palette`                                     | opened command palette                                                                                                   |
| `Open Context Menu`                                        | opened context menu (such as right clicking, clicking on ellipses in the top right of a block, etc.)                     |
| `Open Launch Config`                                       | opened launch config for a session                                                                                       |
| `Open Launch Config File`                                  | opened the launch config YAML file from modal once saved successfully                                                    |
| `Open Palette`                                             |                                                                                                                          |
| `Open Quake Mode Window`                                   | toggled quake mode window when previously hidden or closed                                                               |
| `Open Suggestions Menu`                                    | opened a suggestion menus, such as with up arrow or tab                                                                  |
| `Open Team from URI`                                       | showed settings view of their newly joined team within the app                                                           |
| `Open Theme Chooser`                                       | opened theme chooser (list of different themes and visualizations of those themes)                                       |
| `Open Welcome Tips`                                        | opened welcome tips in app                                                                                               |
| `Open Workflows Search`                                    | opened workflows search in command search pane                                                                           |
| `Opened Link`                                              | opened a highlighted link within input or output                                                                         |
| `Pass Through Onboarding Question: attribution`            | attribution question in onboarding flow                                                                                  |
| `Pass Through Onboarding Question: attribution:friend`     | tracked "friend" as attribution in onboarding survey flow                                                                |
| `Pass Through Onboarding Question: attribution:internet`   | tracked "internet" as attritbution in onboarding survey flow                                                             |
| `Pass Through Onboarding Question: attribution:teammate`   | tracked "teammate" as attribution in onboarding survey flow                                                              |
| `Pass Through Onboarding Question: company`                | company question in onboarding survey flow                                                                               |
| `Pass Through Onboarding Question: engineering_experience` | engineering experience question in onboarding survey flow                                                                |
| `Pass Through Onboarding Question: purpose`                | purpose of using warp question in onboarding survey flow                                                                 |
| `Pass Through Onboarding Question: role`                   | role question in onboarding survey flow                                                                                  |
| `Quit Natural Language Search`                             | quit natural language search                                                                                             |
| `Removed user from team`                                   | removed user from team                                                                                                   |
| `Resource Center Opened`                                   | opened Resource Center pane                                                                                              |
| `Resource Center Tips Skipped`                             | skipped welcome tips for new users                                                                                       |
| `SSH Bootstrap Attempt`                                    | attempted boostrapping for an SSH session                                                                                |
| `Save Launch Config`                                       | saved current launch configuration of windows, tabs, and panes                                                           |
| `Select Command Palette Option`                            | selected option from command palette (i.e. CMD+P)                                                                        |
| `Select Navigation Palette Item`                           | selected session from the Session Navigation Palette (search across panes, tabs, and windows)                            |
| `Select Theme`                                             | selected theme                                                                                                           |
| `Sent email invites`                                       | sent an email invite to join team                                                                                        |
| `Session Abandoned Before Bootstrap`                       | abandoned session before the boostrapping completes                                                                      |
| `Set Line Height`                                          | set line height through Settings -> Appearance                                                                           |
| `ShowNotificationsDiscoveryBanner`                         | showed discovery banner for notifications (notify user when long running commands finish)                                |
| `ShowNotificationsErrorBanner`                             | showed error banner for notifications (i.e. permissions issue)                                                           |
| `Sign Up Button Clicked in App`                            | "Sign Up" button clicked                                                                                                 |
| `Skip Onboarding Survey`                                   | skipped onboarding survey as a whole                                                                                     |
| `Split Pane`                                               | split tab into multiple panes                                                                                            |
| `Start Onboarding Survey`                                  | started onboarding survey                                                                                                |
| `Tab Creation`                                             | created a tab                                                                                                            |
| `Tab Operations`                                           | took operation on a tab: change color, close tab, close adjacent tabs, etc.                                              |
| `Tab Renamed`                                              | changed tab title                                                                                                        |
| `Tab Single Result Autocompletion`                         | accepted tab completion and inserted into text editor                                                                    |
| `Team Created`                                             | created team in settings                                                                                                 |
| `Team Left`                                                | member left team                                                                                                         |
| `Team Link Copied`                                         | Clicked on "Copy Link"                                                                                                   |
| `Thin Strokes Setting Changed`                             | changed thin strokes setting in settings -> appearance                                                                   |
| `Toggle Approvals Modal`                                   | opened or closed teams modal                                                                                             |
| `Toggle Restore Session`                                   | toggled session restoration ("Restore windows, tabs, panes, on startup")                                                 |
| `Toggled Bookmark Block`                                   | bookmarked or unbookmarked block                                                                                         |
| `Tried to Execute Before Precmd`                           | attempted to execute command before precmd, a shell stage which has metadata on a command such as ssh, prompt info, etc. |
| `Triggered Command XRay`                                   | triggered command x-ray (hovering over a command for explanation)                                                        |
| `Unable to Update To New Version`                          | update available but not authorized to install                                                                           |
| `Unhandled Editor Modifier Key`                            | used modifier keybinding keystroke which is not currently supported                                                      |
| `Workflow Executed`                                        | executed workflow                                                                                                        |
| `Workflow Selected`                                        | selected workflow and populated into the text editor                                                                     |
