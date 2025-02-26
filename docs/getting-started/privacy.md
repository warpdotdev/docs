---
description: Warp's approach to privacy and your control over your data
---

# Privacy

## Transparency and control

{% hint style="info" %}
If you have any questions about any of this, please don’t hesitate to reach out at [privacy@warp.dev](mailto:privacy@warp.dev).
{% endhint %}

Our philosophy is complete transparency and control of any data leaving your machine. This means you can:

* Read a complete list of [all the telemetry events](privacy.md#exhaustive-telemetry-table) that get sent for app analytics
* Monitor telemetry in real-time with Warp's native [Network Log](../features/network-log.md)
* [Opt out](privacy.md#how-to-disable-telemetry-and-crash-reporting) of telemetry at any time

App analytics and crash reporting are used to improve the product and to debug any issues that may arise. Terminal sessions contain sensitive information, and we want the **absolute minimum** sent to Warp's servers necessary to provide you with the best possible experience.

Telemetry data **never includes console input or output** and usage of this data will never be part of Warp's business model.

You can read our [full privacy policy](https://www.warp.dev/privacy/policy) as well as [how Warp handles security](https://www.warp.dev/security).

{% hint style="info" %}
For security-related issues or questions, please email [security@warp.dev](mailto:security@warp.dev).
{% endhint %}

## How to disable telemetry and crash reporting

1. Navigate to `Settings > Privacy`, or open the [Command Palette](../features/command-palette.md) and search for "privacy"
2. Toggle off app analytics, crash reports, or both (if it's blue, it's "on")

<figure><img src="../.gitbook/assets/privacy-settings-after-signup.png" alt=""><figcaption><p>Privacy Settings</p></figcaption></figure>

### Your data privacy and AI in Warp

Warp includes optional [AI features](../features/warp-ai/) you can choose to engage for assistance on the command line or across the Warp app. For [Agent Mode](../features/warp-ai/agent-mode.md), natural language detection happens locally, and you can choose to disable this at any time. Any AI requests are sent to the APIs through a proxy. No input or console data is collected or stored by Warp. No AI data is ever used to train public models. Zero data retention is available. [Learn more](https://docs.warp.dev/features/warp-ai/agent-mode#privacy-security-and-safety)

### Delete your data

Warp provides a convenient way for you to delete your data:

* From Warp, go to `Settings > Privacy > "Visit the data management page"`
  * Click the "Delete" button on the Data Management page to go through the data deletion flow.
* From the [Data Management](https://app.warp.dev/data_management) page, log into your Warp account, and click the "Delete" button to go through the data deletion flow.

{% hint style="info" %}
Deletion jobs run every 24 hours, so if you deleted your account and want to sign up again with the same email, you won't be able to do so until that deletion completes.
{% endhint %}

{% hint style="warning" %}
If you're a [Team](../features/teams.md) admin, the deletion flow will require that you assign a team member as the new admin.
{% endhint %}

## What telemetry data does Warp collect and why?

Warp collects high-level usage data (**never console input or output**) to discover product quality issues and guide feature prioritization. Selling usage data will never be part of Warp's business model. This data is used solely to improve the end-user experience.

Warp uses Sentry for crash reporting and Rudderstack for app analytics.

### Exhaustive Telemetry Table

| Event Name                                                 | Description                                                                                                                                                       |
| ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AI Command Search opened`                                 | Opened the modal for AI Command Search, where you can use natural language to search for commands                                                                 |
| `Add Added Subshell Command`                               | Added a command to be automatically Warpified via Warp's subshell wrapper                                                                                         |
| `Add Denylisted Subshell Command`                          | Explicitly prevent a command from being Warpified via Warp's subshell wrapper                                                                                     |
| `AgentMode.AttachedContext`                                | Attached block as context to an Agent Mode query                                                                                                                  |
| `AgentMode.ClickedEntrypoint`                              | Clicked on an Agent Mode entrypoint                                                                                                                               |
| `AgentMode.QueryAttemptAtLImit`                            | Tried to send an Agent Mode query but they already reached the query limit                                                                                        |
| `AgentMode.ToggledAskFollowUp`                             | Toggled 'ask followup' on Agent Mode query                                                                                                                        |
| `App Download Source`                                      | Whether the Warp was installed from the home page or through homebrew                                                                                             |
| `App Startup`                                              | App is launched                                                                                                                                                   |
| `Approve Domains`                                          | Under team management in settings, domain is approved for users with corresponding email domain to join the team                                                  |
| `Auth Common Question Clicked in App`                      | Clicked on "Common Question" when logging in                                                                                                                      |
| `Auth: Open Privacy Settings Overlay`                      | Privacy settings modal is open during sign-in                                                                                                                     |
| `Auth: Toggle Common Questions`                            | Toggled FAQ Page when logging in                                                                                                                                  |
| `Autosuggestion Inserted`                                  | Accepted autosuggestion                                                                                                                                           |
| `Background Block Started`                                 | Warp created a background-output Block (whenever a processes has been backgrounded and yields some output)                                                        |
| `BaselineCommand Latency`                                  | Command execution time                                                                                                                                            |
| `Block Creation`                                           | Created Block                                                                                                                                                     |
| `Block Filter Toolbelt Button Clicked`                     | Clicked the block filter icon in the top-right of a block                                                                                                         |
| `Block Selection`                                          | Selected Block                                                                                                                                                    |
| `BlocklistAI.CreatedBlock`                                 | Created an AI Block                                                                                                                                               |
| `Bootstrapping Slow`                                       | Slow bootstrap on session startup                                                                                                                                 |
| `Bootstrapping Succeeded`                                  | Successful bootstrap for session                                                                                                                                  |
| `Changed invite view option`                               | Toggled between link and invite for invite                                                                                                                        |
| `Command Correction Event`                                 | Accepted command correction                                                                                                                                       |
| `Command File Run`                                         | Opened a .cmd or unix executable file and ran it directly in Warp                                                                                                 |
| `Command Search Async Query Completed`                     | Finished searching for a command in the background                                                                                                                |
| `Command Search Filter Changed`                            | Changed command search filter                                                                                                                                     |
| `Command Search Opened`                                    | Opened command search (universal search panel to search                                                                                                           |
| `Command Search Result Accepted`                           | Accepted command search result                                                                                                                                    |
| `Complete Welcome Tip`                                     | Completed all welcome tips items                                                                                                                                  |
| `Confirm Suggestion`                                       | Accepted tab completion suggestion                                                                                                                                |
| `Context Menu Copy`                                        | Clicked "Copy" in context menu                                                                                                                                    |
| `Context Menu Copy Prompt`                                 | Clicked "Copy Prompt" in context menu                                                                                                                             |
| `Context Menu Copy Selected Text`                          | Clicked "Copy selected text" in context menu                                                                                                                      |
| `Context Menu Insert Selected Text into Input`             | Clicked "insert into input" in context menu                                                                                                                       |
| `Context Menu Toggle Git Prompt Dirty Indicator`           | Toggled indicator of dirty git prompt                                                                                                                             |
| `Context Menu Toggle PS1`                                  | Clicked "user default prompt" in context menu                                                                                                                     |
| `Context Menu: Find Within Blocks`                         | Clicked "find within blocks" in context menu                                                                                                                      |
| `Context Menu: Initiate Block Sharing`                     | Opened "Share" modal via context menu                                                                                                                             |
| `Context Menu: Reinput Commands`                           | Clicked "reinput commands" in context menu                                                                                                                        |
| `Copied Shared Session Link`                               | Copied a shared session link                                                                                                                                      |
| `Copy Block Sharing Link`                                  | Clicked "Share block..." in context menu                                                                                                                          |
| `Copy Invite Link`                                         | Clicked "Copy Link" on Referral Modal                                                                                                                             |
| `Copy Obfuscated Secret`                                   | Copied a secret's obfuscated contents to clipboard                                                                                                                |
| `Copy Object To Clipboard`                                 | Copied an object to the user's keyboard                                                                                                                           |
| `Create Custom Theme`                                      | Created a custom theme using the built-in theme creator                                                                                                           |
| `Custom Secret Regex Added`                                | Custom Secret Regex Added                                                                                                                                         |
| `Database Read Error`                                      | Database read error when trying to get app state for session restoration                                                                                          |
| `Database Startup Error`                                   | Failed to initialize sqlite upon startup                                                                                                                          |
| `Database Write Error`                                     | Database write error when trying to write app state for session restoration                                                                                       |
| `Decline Subshell Bootstrap`                               | Developer declined the Warp banner to Warpify the current session                                                                                                 |
| `Delete Custom Theme`                                      | Deleted a custom theme using the built-in theme creator                                                                                                           |
| `Deleted Notebook`                                         | Deleted notebook from Warp Drive team                                                                                                                             |
| `Deleted Workflow`                                         | Deleted workflow from Warp Drive team                                                                                                                             |
| `Disable Input Sync Inputs`                                | Disabled / turn off the Input Synchronization (across editors)                                                                                                    |
| `Dismiss Alias Expansion Banner`                           | Dismissed the banner to enable automatic alias expansion within the Input Editor                                                                                  |
| `Dismiss Welcome Tips`                                     | Dismissed Welcome tips                                                                                                                                            |
| `Don't Show Sharer Grant Modal Again`                      | When you check don't show again on the confirmation modal for granting a role                                                                                     |
| `Drag and Drop Tab`                                        | Tab dragged and dropped                                                                                                                                           |
| `Draw Frame Latency`                                       | Recorded time to draw a frame in app (in ms)                                                                                                                      |
| `Draw Frame Latency Histogram Overflow`                    | Could not summarize histogram of draw frame latency                                                                                                               |
| `Duplicate Object`                                         | Cloned a Warp Drive object                                                                                                                                        |
| `Edited Input Before Precmd`                               | Input edited before precmd hook completes                                                                                                                         |
| `Enable Alias Expansion From Banner`                       | Enabled automatic alias expansion within the Input Editor from the banner                                                                                         |
| `Expensive Frame`                                          | Frame took long time to draw (past a certain threshold)                                                                                                           |
| `Experiment Triggered`                                     | User assigned to A/B test                                                                                                                                         |
| `Export Object`                                            | Exported a Warp Drive object                                                                                                                                      |
| `Features Page Action`                                     | Changed settings in Features Page                                                                                                                                 |
| `Find Option Toggled`                                      | Changed settings in Find Toggle                                                                                                                                   |
| `Generate Block Sharing Link`                              | Generated Block sharing link                                                                                                                                      |
| `Generate Metadata For Workflow Error`                     | Failed to generate metadata for a workflow using Warp AI                                                                                                          |
| `Generate Metadata For Workflow Success`                   | Successfully generated metadata for a workflow using Warp AI                                                                                                      |
| `Get Invite`                                               | Clicked "Get Invite"                                                                                                                                              |
| `InitialWorkingDirectoryConfigurationChanged`              | Replaced the default working directory with a different path                                                                                                      |
| `Initiate Reauth`                                          | Started the flow to re-authenticate the client                                                                                                                    |
| `Input Mode Changed`                                       | Changed the Input Editor Mode (Pinned to Bottom, Pinned to Top, Classic / Waterfall Mode)                                                                         |
| `InputBoxAICommandSearch`                                  | Opened AI Command Search via the Input Editor's context menu (right clicking the buffer)                                                                          |
| `InputBoxAskWarpAI`                                        | Clicked "Ask Warp AI" from the Input Editor's context menu                                                                                                        |
| `InputBoxCommandSearch`                                    | Opened Command Search via the Input Editor's context menu (right clicking the buffer)                                                                             |
| `InputBoxCutSelectedText`                                  | Copied selected text from Input Editor                                                                                                                            |
| `InputBoxPaste`                                            | Pasted text into the Input Editor's via its context menu (right clicking the buffer)                                                                              |
| `InputBoxSelectAll`                                        | Selected all the text in the Input Editor via its context menu (right clicking the buffer)                                                                        |
| `Joined Shared Session`                                    | When you join another instance of Warp using shared sessions                                                                                                      |
| `Jumped to Bookmark Block`                                 | Jumped to bookmarked Block                                                                                                                                        |
| `Jumped to Bottom of Block Button Clicked`                 | Used the button to jump to the bottom of a Block                                                                                                                  |
| `Jumped to Previous Command`                               | Jumped to a previous command                                                                                                                                      |
| `Jumped to Shared Session Participant`                     | Clicked on a shared session participant avatar to jump to their location in the session                                                                           |
| `Keybinding Changed`                                       | Edited a custom keybinding                                                                                                                                        |
| `Keybinding Removed`                                       | Removed / cleared a keybinding                                                                                                                                    |
| `Keybinding Reset to Default`                              | Reset a custom keybinding to its default                                                                                                                          |
| `Log In Button Clicked in App`                             | Clicked on "Log in" button                                                                                                                                        |
| `Log Out`                                                  | Logged out of the Warp client                                                                                                                                     |
| `Log Out Modal Cancel Pressed`                             | Escaped the log out flow by canceling the log out modal                                                                                                           |
| `Log Out Modal Shown`                                      | When the log out modal is displayed                                                                                                                               |
| `Logged in to native app`                                  | Login is successful                                                                                                                                               |
| `Logged-out App Startup`                                   | Started Warp in the logged-out / signed-out state                                                                                                                 |
| `Manually toggle off AI autodetection`                     | Manually toggled off AI input after autodetected AI                                                                                                               |
| `Move Active Tab`                                          | Move active tab left or right                                                                                                                                     |
| `Move Tab`                                                 | Move tab left or right                                                                                                                                            |
| `Needs Reauth`                                             | User needs to re-authenticate                                                                                                                                     |
| `New Session From Directory`                               | Dragged a file, folder, etc. into Warp to start a session                                                                                                         |
| `Notification Clicked`                                     | Clicked desktop notification sent from Warp                                                                                                                       |
| `Notification Failed to Send`                              | Failed to send desktop notification                                                                                                                               |
| `Notification Permissions Requested`                       | Requested permission for desktop notification permissions                                                                                                         |
| `Notification Request Permissions Outcome`                 | Recorded outcome of attempting to request desktop notification permissions                                                                                        |
| `Notification Sent`                                        | Sent desktop notification                                                                                                                                         |
| `Notifications Discovery Banner Action`                    | Showed banner introducing the notifications feature                                                                                                               |
| `Notifications Error Banner Action`                        | Showed error banner for notifications feature                                                                                                                     |
| `Open Context Menu`                                        | Opened context menu (such as right clicking, clicking on ellipses in the top right of a Block, etc.)                                                              |
| `Open Launch Config`                                       | Opened launch config for a session                                                                                                                                |
| `Open Launch Config File`                                  | Opened the launch config YAML file from modal once saved successfully                                                                                             |
| `Open Palette`                                             | Opened the palette                                                                                                                                                |
| `Open Quake Mode Window`                                   | Toggled quake mode window when previously hidden or closed                                                                                                        |
| `Open Save Config Modal`                                   | Opened save launch configuration modal                                                                                                                            |
| `Open Suggestions Menu`                                    | Opened a suggestion menus, such as with up arrow or tab                                                                                                           |
| `Open Team from URI`                                       | Showed settings view of their newly joined team within the app                                                                                                    |
| `Open Theme Chooser`                                       | Opened theme chooser (list of different themes and visualizations of those themes)                                                                                |
| `Open Theme Creator Modal`                                 | Opened theme creator modal (modal to create a new theme)                                                                                                          |
| `Open Welcome Tips`                                        | Opened welcome tips in app                                                                                                                                        |
| `Open Workflows Search`                                    | Opened workflows search in command search pane                                                                                                                    |
| `OpenAndWarpifyDockerSubshell`                             | Warpifying a docker subshell from using the docker extension                                                                                                      |
| `OpenInputBoxContextMenu`                                  | Opened the Input Editor's context menu                                                                                                                            |
| `Opened Changelog Link`                                    | Opened the changelog link within the App                                                                                                                          |
| `Opened Link`                                              | Opened a highlighted link within input or output                                                                                                                  |
| `Opened Save As Workflow Modal`                            | Opened the modal to create a new workflow using a Block's context--command, etc.                                                                                  |
| `Opened Warp AI`                                           | Activated Warp AI                                                                                                                                                 |
| `Opened alt screen find bar`                               | Opened the Find bar in the Alt Screen                                                                                                                             |
| `Page Up/Down In Editor Pressed`                           | Pressed `PAGE-UP` or `PAGE-DOWN` within the Input Editor                                                                                                          |
| `Pane Drag Ended`                                          | Ended dragging a pane via the pane header                                                                                                                         |
| `Pane Drag Inititiated`                                    | Initiated dragging a pane via the header                                                                                                                          |
| `Prompt Edited`                                            | Edited the prompt using the built-in prompt editor                                                                                                                |
| `Prompt Editor Opened`                                     | Opened the prompt editor                                                                                                                                          |
| `Pty Spawned`                                              | Tracks the manner by which we create a new shell process (new codepath vs. old codepath). Used to ensure nothing breaks as we change parts of our infrastructure. |
| `Quit Modal Cancel Pressed`                                | `Cancel` button on the alert modal was pressed                                                                                                                    |
| `Quit Modal Disabled`                                      | The quit modal dialog has been disabled and will not popup when a user closes Warp while a session is running                                                     |
| `Quit Modal Shown`                                         | Showed an alert modal to warn the user about closing the app/window with a running process                                                                        |
| `Received Subshell RC File DCS`                            | Spawned a subshell to be automatically Warpified                                                                                                                  |
| `Remove Added Subshell Command`                            | Removed a command from the list of commands to automatically Warpify via Warp's subshell wrapper                                                                  |
| `Remove Denylisted Subshell Command`                       | Removed a command from the list of commands to IGNORE when trying to Warpify via Warp's subshell wrapper                                                          |
| `Removed user from team`                                   | Remove user from Warp Drive team                                                                                                                                  |
| `Resource Center Keybindings Page Opened`                  | Opened the keybinding page within the resource center                                                                                                             |
| `Resource Center Opened`                                   | Opened Resource Center pane                                                                                                                                       |
| `Resource Center Tips Completed`                           | Completed resource center tips                                                                                                                                    |
| `Resource Center Tips Skipped`                             | Skipped welcome tips for new users                                                                                                                                |
| `SSH Bootstrap Attempt`                                    | Attempted boostrapping for an SSH session                                                                                                                         |
| `Save Launch Config`                                       | Saved current launch configuration of windows, tabs, and panes                                                                                                    |
| `Select Command Palette Option`                            | Selected option from command palette (i.e. CMD-P)                                                                                                                 |
| `Select Navigation Palette Item`                           | Selected session from the Session Navigation Palette (search across panes, tabs, and windows)                                                                     |
| `Select Theme`                                             | Selected theme                                                                                                                                                    |
| `Sent email invites`                                       | Sent email invites for Warp Drive team                                                                                                                            |
| `Session Abandoned Before Bootstrap`                       | Abandoned session before the boostrapping completes                                                                                                               |
| `Set Line Height`                                          | Set line height through Settings -> Appearance                                                                                                                    |
| `Set New Windows at Custom Size`                           | Set new windows at custom size through Settings -> Appearance                                                                                                     |
| `Set Window Blur Radius`                                   | Changed the blur radius from the `Settings -> Appearance` dialog                                                                                                  |
| `Set Window Opacity`                                       | Changed the opacity (window transparency) from the `Settings -> Appearance` dialog                                                                                |
| `Setup Flow Completed`                                     | Finished the setup flow for new users                                                                                                                             |
| `Setup Flow Interrupted`                                   | The setup flow could not finish due to some interruption                                                                                                          |
| `Setup Flow Skipped`                                       | Skipped the setup flow for new users                                                                                                                              |
| `Setup Flow Started`                                       | Started the setup flow for new users                                                                                                                              |
| `Shared Object Limit Hit Banner View Plans Button Clicked` | Clicked the 'View Plans' button on the persistent drive banner                                                                                                    |
| `Shared Session Modal Upgrade Pressed`                     | Clicked the 'View Plans' button on the upgrade modal for shared sessions                                                                                          |
| `Shared Session Onboarding Block Shown`                    | Showed the onboarding block for session sharing                                                                                                                   |
| `Sharer Cancelled Grant Role`                              | When you cancel granting a role to a shared session participant                                                                                                   |
| `Show Alias Expansion Banner`                              | Displayed the banner asking whether Warp should automatically expand aliases within the Input Editor                                                              |
| `Show Subshell Banner`                                     | Displayed the banner asking whether Warp should Warpify the current session via Warp's subshell wrapper                                                           |
| `ShowNotificationsDiscoveryBanner`                         | Showed notifications discovery banner in the block list                                                                                                           |
| `ShowNotificationsErrorBanner`                             | Showed error banner for notifications feature                                                                                                                     |
| `Showed File in File Explorer`                             | Opened a file in Finder by using "Show in Finder"                                                                                                                 |
| `Sign Up Button Clicked in App`                            | Clicked "Sign Up" button                                                                                                                                          |
| `Skip Onboarding Survey`                                   | Skipped onboarding survey as a whole                                                                                                                              |
| `Split Pane`                                               | Split tab into multiple panes                                                                                                                                     |
| `Start Shared Session In New Tab`                          | Started a shared session in a new tab                                                                                                                             |
| `Started Shared Session In New Window`                     | Started a shared session in a new window                                                                                                                          |
| `Tab Creation`                                             | Created a tab                                                                                                                                                     |
| `Tab Operations`                                           | Took operation on a tab: change color, close tab, close adjacent tabs, etc.                                                                                       |
| `Tab Renamed`                                              | Changed tab title                                                                                                                                                 |
| `Tab Single Result Autocompletion`                         | Accepted tab completion and inserted into Input Editor                                                                                                            |
| `Team Created`                                             | Created a Warp Drive team                                                                                                                                         |
| `Team Joined`                                              | Joined a Warp Drive team                                                                                                                                          |
| `Team Left`                                                | Left a Warp Drive team                                                                                                                                            |
| `Team Link Copied`                                         | Copied a Warp Drive team link                                                                                                                                     |
| `Thin Strokes Setting Changed`                             | Changed thin strokes setting in settings -> Appearance                                                                                                            |
| `Tier Limit Hit`                                           | User hit the tier limit for a feature                                                                                                                             |
| `Toggle Approvals Modal`                                   | Opened or closed teams modal                                                                                                                                      |
| `Toggle Block Filter Case Sensitivity`                     | Toggled on/off case sensitivity within the block filter editor                                                                                                    |
| `Toggle Block Filter Invert`                               | Toggled on/off invert within the block filter editor                                                                                                              |
| `Toggle Block Filter Query`                                | Toggled on/off a block filter query                                                                                                                               |
| `Toggle Block Filter Regex`                                | Toggled on/off regex within the block filter editor                                                                                                               |
| `Toggle Dim Inactive Panes`                                | Whether the dim inactive panes feature has been toggled                                                                                                           |
| `Toggle Jump to Bottom of Block Button`                    | Enabled or disabled the Jump to Bottom of Block Button                                                                                                            |
| `Toggle New Windows at Custom Size`                        | Whether the new windows at custom size feature has been toggled                                                                                                   |
| `Toggle Obfuscate Secret`                                  | Revealed or hid a secret                                                                                                                                          |
| `Toggle Restore Session`                                   | Toggled session restoration ("Restore windows, tabs, panes, on startup")                                                                                          |
| `Toggle Same Line Prompt`                                  | Toggled same line prompt                                                                                                                                          |
| `Toggle Secret Redaction`                                  | Toggled the setting for Secret Redaction - attempts to redact secrets and sensitive information                                                                   |
| `Toggle Sticky Command Header in Active Pane`              | Expanded or collapsed the sticky command header in the active pane                                                                                                |
| `Toggle Sync Inputs Across All Panes in All Tabs`          | Enable the synchronization of the Input Editor's buffer to all the panes in all the tabs                                                                          |
| `Toggle Sync Inputs Across All Panes in Current Tab`       | Enable the synchronization of the Input Editor's buffer to all the panes in the current tab                                                                       |
| `Toggle Tab Indicators`                                    | Enabled or disabled the tab indicators (failed command, etc.)                                                                                                     |
| `Toggle Warp AI`                                           | Toggled Warp AI--an AI assistant to help you debug errors, look up forgotten commands and more                                                                    |
| `Toggled Bookmark Block`                                   | Bookmarked or unbookmarked Block                                                                                                                                  |
| `Tried to Execute Before Precmd`                           | Attempted to execute command before precmd, a shell stage that has metadata on a command such as ssh, prompt info, etc.                                           |
| `Trigger Subshell Bootstrap`                               | Attempted to Warpify the current session via Warp's subshell wrapper                                                                                              |
| `Triggered Command XRay`                                   | Triggered Command X-Ray (hovering over a command for explanation)                                                                                                 |
| `Unable to Update To New Version`                          | Update available but not authorized to install                                                                                                                    |
| `Undo Close`                                               | Re-opened a closed tab or window (undo closing a tab or window)                                                                                                   |
| `Unhandled Editor Modifier Key`                            | Used modifier keybinding keystroke which is not currently supported                                                                                               |
| `Unsupported Shell`                                        | Booted Warp with a shell that isn't supported                                                                                                                     |
| `Update Block Filter Query`                                | When a new filter is applied to a block                                                                                                                           |
| `Update Block Filter Query With Context Lines`             | When the number of context lines for a block filter query is updated                                                                                              |
| `Updated Sorting Choice`                                   | Modified the sorting scheme for Warp Drive objects                                                                                                                |
| `Used Warp AI Prepared Prompt`                             | Used one of the Warp-provided prompts, like "Show examples"                                                                                                       |
| `User Initiated Closing Something`                         | Attempted to either quit the app or close a window                                                                                                                |
| `User Initiated Log Out`                                   | Confirms a user has explicitly logged out of the application                                                                                                      |
| `Vim Keybindings Banner Dismissed`                         | Dismissed the banner to enable Vim keybindings in the Input Editor                                                                                                |
| `Vim Keybindings Banner Displayed`                         | Displayed the banner asking whether Warp should enable Vim keybindings in the Input Editor                                                                        |
| `Vim Keybindings Enabled from Banner`                      | Enabled Vim keybindings in the Input Editor from the banner                                                                                                       |
| `Warp AI Action`                                           | Executed a Warp AI action: Restart, Copy, Insert into terminal                                                                                                    |
| `Warp AI Character Limit Exceeded`                         | Attempted to ask a question longer than 1k chars to Warp AI                                                                                                       |
| `Warp AI Request Issued`                                   | Issued a question to Warp AI                                                                                                                                      |
| `Warp Drive Opened`                                        | Opened Warp Drive panel                                                                                                                                           |
| `Web session opened on desktop`                            | Shared session viewed on the web was opened on the desktop                                                                                                        |
| `Workflow Executed`                                        | Executed workflow                                                                                                                                                 |
| `Workflow Selected`                                        | Selected workflow and populated into the Input Editor                                                                                                             |
