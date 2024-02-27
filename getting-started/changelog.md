# Changelog

Warp autoupdates whenever a new release comes out. We try to ship an update every week usually on Thursday! Submit bugs and feature request on our [GitHub board!](https://github.com/warpdotdev/Warp/issues/new/choose)

### 2024.02.26 (v0.2024.02.20.08.01.stable_02)

**New features**

* Warp is now available for Linux! [Read the blog](https://www.warp.dev/blog/warp-for-linux) to learn more and download.

**Improvements**

* Completions for apt-get, aptitude, and pacman
* You can now type to search in the font picker in Settings > Appearance

### 2024.02.20 (v0.2024.02.20.08.01.stable_01)

**Improvements**

* Completions for apt-get, aptitude, and pacman.

### 2024.02.16 (v0.2024.02.16.17.24)

**New features**

* Warp on Linux (Private Beta): Added support for the Input Mode Editor (IME).

### 2024.02.14 (v0.2024.02.14.15.46)

**New features**

* Warp on Linux (Private Beta): Added support for the Input Mode Editor (IME).

### 2023.02.08 (v0.2024.02.13.08.02)

**Bug fixes**

* Fix the inputted command sometimes overlapping rprompt (right-sided prompt)

### 2023.02.01 (v0.2024.01.30.16.52)

**Improvements**

* Improved UX for pasting an auth token to complete the sign-in flow
* Subversion (svn) information is now available in Warp's prompt

### 2023.01.18 (v0.2024.01.16.16.31)

**New features**

* Warp on Linux (Private Beta): System fonts now load as expected

**Bug fixes**

* Warp on Linux (Private Beta): `ALT-TAB` no longer incorrectly inserts 4 spaces into the Input Editor

### 2023.01.11 (v0.2024.01.09.08.02)

**New features**

* New workflow metadata for shared workflows in Warp Drive! Hover over any workflow to learn how recently the workflow has been executed, who edited it last, and when it was last edited.

### 2023.12.21 (v0.2024.01.02.08.02)

**Improvements**

* The toolbelt displayed when hovering over background Blocks now has a solid background

**Bug fixes**

* The Markdown Viewer now respects the start number of ordered lists
* Completing a path that includes the tilde (`~`) character now works as expected
* Fixed an issue where Warp could quit before saving changes to Warp Drive
* Fix Warp hanging when using the 'Insert into Input' context menu action

### 2023.12.14 (v0.2023.12.12.08.02)

**New features**

* Editing with Vim keybindings is now out of beta and generally available! Warp will detect vi mode in shell settings and suggest Vim keybindings.

**Improvements**

* You can now use `CMD-F` to search text in the Markdown Viewer

**Bug fixes**

* Block hover buttons now have a solid background when they overlap with your prompt
* The Block filter editor now has a clear button
* `J` and `K` (Vim Mode) can be used for navigation within a multi-line command
* Fixed the left alignment of the tab bar when in full-screen mode on Mac
* Fixed triple-click selection (selecting a line) when filtering a Block
* Fixed potential crash when using the find bar
* Fixed potential crash when retrieving accessibility contents
* Fix bug where "R" is erroneously inserted into the input in zsh sessions

### 2023.12.07 (v0.2023.12.05.08.02)

**Improvements**

* Markdown file links can now be configured to open with the default external editor or Warp's built-in markdown viewer
* Warp Drive folders now keep their opened/closed state through app restarts

**Bug fixes**

* The Input Editor now refocuses correctly after pasting terminal contents and running a command
* Fixed issue with missing toolbelt buttons when using fish wih Vim Mode

### 2023.11.30 (v0.2023.11.28.08.02)

**Improvements**

* Warp’s custom prompt builder now includes a context chip for Kubernetes context
* Improved completions for kubectl, including suggestions for resource, global options, and namespaces

**Bug fixes**

* Fixed a UI bug in the workflows editor where the editor for arguments was overflowing
* Search bar focuses as expected when you open Launch Configurations with the Command Palette

### 2023.11.16 (v0.2023.11.14.08.02)

**Bug fixes**

* The informational block that shows workflow metadata now resizes with your Warp window
* The scrolling speed is now standardized across Warp

### 2023.11.09 (v0.2023.11.07.08.02)

**New features**

* New Markdown Viewer: You can now open .md files in Warp and run the shell commands within these files
* Block Filtering: You can now filter block output (SHIFT-OPT-F) to quickly find matching lines based on a query.

**Improvements**

* Removed the workflow button from the toolbelt section (top-right buttons) of a block. It is still accessible through the right-click menu (see “Save as Workflow”) and its default keybinding CMD-S.
* Improved performance of Warp Drive team and state syncing

### 2023.11.02 (v0.2023.10.31.08.03)

**Improvements**

* You can now invite new team members to your shared Warp Drive by email address and revoke invitations

### 2023.10.23 (v0.2023.10.17.08.03)

**Improvements**

* Indicators appear in the tab bar when the current pane is maximized (a full-screen icon) and when a command exits with an error
* The Git context chip in Warp’s prompt now shows the commit hash instead of “HEAD” when in a detached state
* Easier to add and remove allowlisted domains when inviting teammates to Warp Drive
* Added a menu option for copying a workflow command (into the clipboard)

### 2023.10.19 (v0.2023.10.17.08.03)

**Improvements**

* Indicators appear in the tab bar when the current pane is maximized (a full-screen icon) and when a command exits with an error
* The Git context chip in Warp’s prompt now shows the commit hash instead of “HEAD” when in a detached state
* Easier to add and remove allowlisted domains when inviting teammates to Warp Drive
* Added a menu option for copying a workflow command (into the clipboard)

### 2023.10.12 (v0.2023.10.10.08.06)

**Improvements**

* Warp can now support MacOS's proxy settings
* You can now toggle whether to render Warp using the integrated GPU for dual GPU Macs
* Warp now escapes the file path of an executable loaded from Finder

**Bug fixes**

* Fixed a crash on startup for some users on MacOS Sonoma
* The workflow info box now refreshes when edited

### 2023.10.05 (v0.2023.10.03.08.03)

**New features**

* Now you can use Vim keybindings to edit text on the command line in Warp. Navigate to Settings > Feature > Editor and enable "Edit commands with Vim keybindings." This feature is currently in beta and available to try today.

**Improvements**

* Admins can now control whether the team invite link is accessible for other team members to copy and share. Admins can also reset the URL token if needed.
* You can now add a 24-hour timestamp to your Warp prompt with context chips in the prompt editor.
* The free preview for Warp AI and Warp Drive for teams has been extended. [Learn More](https://www.warp.dev/blog/free-preview-extended)

### 2023.09.28 (v0.2023.09.26.08.09)

**New features**

* If you have Cursor installed, you can now set this as your default code editor under Settings > Features > General.

**Improvements**

* Enhanced user accessibility by adding a tab bar button as a new entry point for the command palette.
* Improved user guidance by displaying a warning when attempting to run a workflow while another command is already in progress.

**Bug fixes**

* Resolved an issue where autosuggestions were not being inserted when bound to certain keybindings.
* Fixed a bug affecting Input Method Editor functionality on non-English keyboards, which caused incorrect positioning and prevented text input after opening a new window.

### 2023.09.14 (v0.2023.09.19.08.04)

**New features**

* You can now edit keybindings to scroll up and down by one line.

**Improvements**

* The input editor remains visible in inactive panes when using split panes.

**Bug fixes**

* Resolved a regression where the filled bookmark icon didn’t display on bookmarked blocks unless hovered on.
* Fixed the `TAB` key not cycling through fields in the Workflow editor under certain circumstances.
* Restored functionality of the keybinding for “New Tab” to work even when no windows are open.

### 2023.09.07 (v0.2023.09.06.18.09)

**Improvements**

* The new tab keyboard shortcut (`CMD-T` by default) can now be re-mapped.
* Warp Drive now shows a loading indicator when syncing.

**Bug fixes**

* The command timestamp tooltip is no longer hidden when the Input Editor is pinned to the top.

### 2023.08.31 (v0.2023.08.29.08.04)

**Improvements**

* You can now delete custom themes from the Warp UI
* You can now scroll to the top or bottom of a selected block from the Command Palette.

**Bug fixes**

* Fixed an issue where CPU was being used up by git processes ([3563](https://github.com/warpdotdev/warp/issues/3563))
* Fixed a Zsh bug where `set sh_word_split` could break Warp's bootstrapping

### 2023.08.24 (v0.2023.08.22.08.03)

**New features**

* Secret Redaction - Warp can now automatically redact secrets and sensitive information in terminal output, including passwords, IP addresses, API keys, and PII. Enable Secret Redaction from the Command Palette or Settings > Privacy > Secret Redaction

**Improvements**

* Special keys used in conjunction with `META` e.g. `META-DELETE` should now work within the alt-screen
* The line height for the text within the Input Editor should now actually change when the custom height in `Settings > Appearance > Text > Line Height` is updated
* Alias Abbreviations in fish should no longer show a red error underline within the Input Editor
* Reduced the bottom padding within the Input Editor when Warp is in Compact Mode

### 2023.08.17 (v0.2023.08.15.08.03)

**New features**

* Warp now displays richer metadata for each command in history, including exit code, working directory, git branch, and whether the command is part of a workflow.
* Warp's native prompt is now customizable directly within the app with drag-and-drop Context Chips (`Settings > Appearance > Prompt`)

**Improvements**

* Warp now supports xterm's escape codes (sequences) for focus reporting
* The Command Palette now supports searching for workflows with their Warp Drive folder name, in addition to the Workflow's name and description.
* Auto-generating custom themes from starting images now work even with a missing `~/.warp/themes` directory
* The "New Workflow" modal now supports more text for longer commands

### 2023.08.10 (v0.2023.08.08.08.04)

**New features**

* Automatically create new themes based on a background image! Click the `+` button in the theme picker (`Settings -> Appearance -> Current Theme`) or search `Open Theme Picker` within the Command Palette

**Improvements**

* Workflows and folders in Warp Drive can now be sorted alphabetically and by last updated
* Multiple JetBrains IDEs are now supported as external editors (e.g. WebStorm, PhpStorm, GoLand)
* The Command Palette now shows which folders a Workflow is in (breadcrumbs)
* Aliases like `...` and `....` no longer incorrectly have an error underline

### 2023.08.03 (v0.2023.08.01.08.05)

**New features**

* Reopen closed tabs with `SHIFT-CMD-T` for up to one minute; configure or disable this feature in `Settings > Features > Enable reopening of closed sessions`
* Autogenerate descriptions for Workflows in Warp Drive using Warp AI

**Improvements**

* Nested folders in Warp Drive can now be collapsed all at once
* Fixed issue where fish abbreviation expansion would include comments
* Fixed a regression with fish history becoming inaccessible

### 2023.07.27 (v0.2023.07.25.08.03)

**Improvements**

* Fixed an issue where $PATH could be overwritten in Bash subshells
* Fixed an issue where completions for file-paths broke when using Named Flags e.g. `ls --color=auto`
* Fixed an issue where Warp Drive objects could get stuck in a sync state
* The down arrow `DOWN` now correctly moves the cursor within Warp AI's text editor

### 2023.07.20 (v0.2023.07.18.08.03)

**New features**

* Can now configure whether `TAB` accepts autosuggestions or opens the completions menu; switch between the configurations via `Settings > Features > Editor`
* Improved completions behavior by improving common prefix detection, and supporting case sensitivity
* Can now natively draw some Unicode block element characters instead of using font glyphs--improves alignment and reduces fuzziness
* Warp's Resource Center now displays new features and improvements

**Improvements**

* Increased the maximum blur radius from 18 to 64

### 2023.07.13 (v0.2023.07.11.08.03)

**New features**

* Warp Drive items that failed to sync can now be retried
* Workflows in Warp Drive drive can now be edited with the workflow execution modal

**Improvements**

* Fixed a bug where git information could sometimes be missing from the prompt
* Adjusted some colors throughout Warp--replaced gradients with solid colors.

### 2023.07.06 (v0.2023.07.04.08.03)

**New features**

* A new AI Command Search experience that allows you to translate natural language to shell commands and integrates directly with workflows! Type '#' in the input to try it out!

**Improvements**

* Fixed a bug where Warp was not recognizing some single character commands and aliases.
* Fixed a bug where command output would sometimes be cut off after finishing (most notably in Gradle).
* Fixed a bug where two prompts could appear for remote Bash sessions

### 2023.06.29 (v0.2023.06.27.19.34)

**New features**

* App links of the form Warp://launch/<launch_configuration_name> directly open a launch configuration
* Added a new setting for creating new windows with a specific size in terms of rows and columns.

**Improvements**

* Fix rendering of multiple ANSI styles on the same character. This fixes rendering issues commonly encountered in Vim and emacs.
* Fix tabs (indentations) sometimes being inserted into the Input Editor when the completion menu should open.
* Added tooltip for “New tab” button
* The “Launch Configurations” sub-menu (under the Mac File menu) now updates dynamically as launch configurations are added and removed.
* Find bar is able to match double-width unicode characters, including CJK and emojis.
* Fixed a crash that could occur when pasting a command in the workflow editor

### 2023.06.20 (v0.2023.06.20.08.04)

**New features**

* You can now bring the power of your Powerlevel10k (P10K) prompt to Warp! For best results, you’ll need the latest version of P10K; see their GitHub page for upgrade instructions
* Right-side prompts are now supported in Zsh and fish!
* Warp AI commands can now be executed as workflows.

**Bug fixes**

* Clicking on an inactive Warp window now focuses the underlying pane correctly.

### 2023.06.08 (v0.2023.06.13.08.03)

**New features**

* Added a settings page for our upgraded referral system--we’ve added new swag options.
* Right-click a highlighted file path to open a context menu that now supports showing the file in Finder
* The Command Palette can now search through Warp sessions, actions and launch configurations

**Bug fixes**

* The completions menu now supports fish abbreviations
* Fixed an issue where certain aliases would be incorrect after expansion.
* Fixed command search to ignore the extra whitespace before and after the search query
* Restored background Blocks no longer create blank history entries
* Fixed an issue where enabling the “Open completions as you type” setting could sometimes break path completions
* Fixed an issue where Zsh could fail to bootstrap when `$PATH` is an a bad state
* Fixed issue where Warp’s bootstrap logic could leak into Zsh’s history
* Fix issue with properly underlining when hyperlinks are in lists or span across multiple lines

### 2023.06.01 (v0.2023.05.30.08.03)

**New features**

* Right-clicking the New Tab (`+`) button opens a context menu to select saved Launch Configurations
* Use Page Up (`PG-UP`) and Page Down (`PG-DOWN`) in the Command Palette for faster navigation
* Added support for Zed as a default code editor
* Referral counts have been updated to only include referrals who’ve onboarded onto (actually tried) Warp

**Bug fixes**

* Warp’s hotkey window (Quake Mode) now properly retains its size
* Fixed issue where command output would temporarily cutoff when resizing Warp.
* Fixed the Sticky Command Header covering content for pager commands.
* Fixed tabs showing stale text when being renamed.
* Clicking a Mac menu bar item that has a sub-menu no longer incorrectly closes the menu
* Warp now automatically focuses the shortcut search bar when the keyboard shortcuts pane is opened (`CMD-/`)
* Fixed regression where Warp’s native prompt no longer showed the virtual environment

### 2023.05.25 (v0.2023.05.23.08.05)

**Bug fixes**

* Improved shell startup performance after a system restarts for users with Xcode installed
* Fixed issue with Warpifying a pipenv shell subshell from zsh
* Fixed issue with updating the git status prompt indicator in remote subshells

### 2023.05.18 (v0.2023.05.18.01.08)

**New features**

* Warp now supports subshells in Zsh, Bash, and fish for a better experience with Docker, GCP, Poetry, and more. Configure which commands you’d like to “Warpify” under Settings > Subshells

**Bug fixes**

* Fixed an issue with Warp's completions when using flags that start with a single dash e.g. `-namespace`
* Fixed an issue with Synchronized Inputs where switching from alt-screens focused on the incorrect terminal session
* Fixed an issue where command history suggestions could cause Synchronized Inputs to get out of sync

### 2023.05.11 (v0.2023.05.09.08.03)

**New features**

* Warp now sends the output of background shell processes into new (distinct) Blocks--separate from user generated Blocks.
* Synchronize (broadcast) input across multiple panes in a single tab or multiple tabs (`Mac Menu > Edit > Synchronize Inputs` or `Synchronize` within the Command Palette)
* Added option to enable (disabled by default) an audible terminal bell (`Settings > Features > Terminal` or  “Enable/Disable Audible Terminal Bell” within the Command Palette)
* Now opens new windows with the same position and size of the most recently closed window (if there is one)
* Fish aliases are now supported in the completions menu

**Bug fixes**

* Support for `SHIFT-UP` and `SHIFT-DOWN` within alt-screen editors
* Fixed incorrect alt-screen scrolling behavior when scroll reporting is enabled
* `SHIFT-TAB` now (correctly) sends the ANSI (backward-tab) escape sequence (for Vim and NeoVim)
* SSH wrapper now also loads your /etc/profile and supports login-like prompts and interactions like printing the message of the day (MOTD)

### 2023.05.04 (v0.2023.05.02.08.03)

**New features**

* Indicate when Warp is downloading an update in Settings > Account > About Warp
* Support alias expansion for bash/zsh aliases

### 2023.04.27 (v0.2023.04.25.08.05)

**New features**

* Support for Fish abbreviations
* Right-click within the Input Editor to open a context menu where you can split panes, etc.

**Bug fixes**

* Starting a command with whitespace in the Workflow creation dialog no longer breaks its argument parser
* Fixed a bug when commands were aliased to `comm` because of a naming clash with Warp's wrapper
* `Cut word left` (`CTRL-W`) and `Cut word right` (`OPT-D`) now use the shell clipboard instead of the system clipboard

### 2023.04.13 (v0.2023.04.11.08.03)

**New features**

* Navigation by subword within the Input Editor with `CTRL-OPT-LEFT` and `CTRL-OPT-RIGHT`
* View prior Warp AI questions using the `UP` arrow even after the transcript is cleared

**Bug fixes**

* Fixed a bug in proxied SSH while not on the default shell
* Background blur now also applies to windows that are opened via drag-and-drop from Finder
* The Sticky Command Header no longer cuts off text for pagers

### 2023.04.06 (v0.2023.04.04.08.03)

**New features**

* The position of the input and direction of the terminal output are now configurable. You can start the input at the top and have it move down as new commands are run (to clear the screen and reset the position press `CTRL-L`, `CMD-K` or type `clear`). Or you can keep the input pinned to the top of the pane and have terminal outputs flow in reverse order. Settings are available under `Settings > Appearance > Input Position`
* Added a button for “jumping to the bottom” of the currently hovered Block to make it easy to get to the bottom of an output. Configurable with a setting under `Settings > Appearance > Blocks`
* Warp AI transcripts can now be navigated via keyboard (`UP` / `DOWN` arrows)
* Added a right-click context menu in the alt-screen (that still respects mouse reporting and SGR_MOUSE)
* Warp AI's past prompts can be accessed via `UP` (arrow)
* `CMD-ENTER` within Warp AI now inputs the selected command into the Input Editor

**Bug fixes**

* Workflows can now be searched by their description in Command Search
* Consolidated “Ask Warp AI” keybindings into one
* Fixed an issue causing “Move cursor by word” and “Select left/right by word” to not work if “Left/Right Option key is Meta” is enabled
* Can now unset cursor navigation bindings within an executing command

### 2023.03.30 (v0.2023.03.28.08.03)

**New features**

* Warning if a known-incompatible custom prompt is detected
* Keybindings for cursor navigation in REPLs and subshells, e.g. ⌥←, ⌥→, ⌥⌫, ⌘←, ⌘→, ⌘⌫, ⌘fn⌫

**Bug fixes**

* Fixed an issue where an input suggestion tooltip could overflow outside the visible window
* Fixed keybinding conflict with Warp AI
* Fixed completion and syntax highlighting when local paths contain separators, not in the prefix

### 2023.03.23 (v0.2023.03.21.08.02)

**New features**

* Added VSCode Insiders as a supported code editor
* Added completions for pnpm.

**Bug fixes**

* Fixed an issue where AI command results with multiple commands would all render on the same line
* The configurable width of Universal Search is now persistent (doesn’t reset to default in new sessions).
* “Copy Prompt” now correctly respects your PS1 prompt, if enabled
* Fixed automatic command corrections for cargo.

### 2023.03.20 (v0.2023.03.14.08.03)

**New features**

* Added support to configure which shell Warp should use when starting a terminal session. Configurable under Settings -> Features -> Session.
* Tabs can now be renamed via mouse double-click.

**Bug fixes**

* Launch configuration templates now support use of `~` in the `cwd` field.
* Double-clicking a button/tab in the title bar no longer resizes the whole window.
* Context menus in the blocklist are now more pronounced and easier to dismiss by clicking.
* Increased the clickable area of small search boxes.
* A keyboard shortcut can now be registered to clear all blocks.
* Fixed some locale-related issues due to use of `LC_ALL` environment variable.
* Xterm escape code OSC 4 (“change color”) no longer crashes the app when it appears in PS1.
* Fixed a crash that occurs when resizing windows after dismissing a notification banner.
* Fixed crash that occurs if you unset the keybinding for the keyboard shortcuts side panel.
* Added Warp AI to resource center.

### 2023.03.16 (v0.2023.03.07.08.02)

**New features**

* Introducing Warp AI ⚡ Get explanations for errors and outputs, ask for help with complicated workflows and scripts, easily execute suggested commands, all without leaving Warp!

### 2023.03.09 (v0.2023.03.07.08.02)

**New features**

* Added support for clearing a keybinding for an action [2300](https://github.com/warpdotdev/warp/issues/2300).
* Added support for showing/hiding Warp windows with a system-wide Activation hotkey [2585](https://github.com/warpdotdev/warp/issues/2585).
* Improved scroll speed for Sidebar menu 'Warp Essentials'/'Keyboard Shortcuts' [2673](https://github.com/warpdotdev/warp/issues/2673).
* Users may now set a custom keybinding to open the completions menu.
* Enabling/disabling mouse reporting is no longer bound to CMD-R by default.
* Toggling mouse reporting enabled shows a banner.

**Bug fixes**

* Fixed SSH wrapper hanging forever when SSH host is Arch Linux with the latest bash package [2636](https://github.com/warpdotdev/warp/issues/2636).
* Fixed Bash commands having escape codes in the last 20 characters producing incorrect output.
* Fixed a bug with bash prompt expansion on recent macOS versions.

### 2023.02.28 (v0.2023.02.28.08.03)

**New features**

* Warp now suggests a URL for creating a GitHub PR on `git push`.
* Command Search and Workflow menus are now horizontally resizable.

**Bug fixes**

* Fixed a bug where Warp doesn’t correctly Auto-Raise.
* Fixed issue where formatting is lost when pasting into nano.
* Fixed issue where Warp doesn’t detect process termination when exiting `info`.
* Fixed a bug with bash prompt expansion not working on v4.4 or earlier.
* Fixed a bug where profile pictures don’t show in the Account menu.
* Fixed Syntax Highlighting and Error Underlining’s handling of multi-byte characters.
* Fixed issue where 'Checking for Update’ doesn’t reflect the current status.

### 2023.02.23 (v0.2023.02.21.08.03)

**New features**

* Support for configuring the initial working directory for new sessions. New tabs/windows/split panes can have separate configurations, or you can set one value for all new sessions.

**Bug fixes**

* Warp now supports syntax highlighting and error underlining for multi-line inputs with multibyte characters
* Fixed a bug where the update status in Warp’s `About Section` was incorrect.
* Improved GPU memory consumption when multiple windows are open.

### 2023.02.16 (v0.2023.02.14.08.05)

**New features**

* Improved double-click selection. Double-clicking text now smart selects patterns like file paths, URLs, email addresses, etc.  - [659](https://github.com/warpdotdev/warp/issues/659)
* Warp can now be opened from Finder - [102](https://github.com/warpdotdev/warp/issues/102)

**Bug fixes**

* Warp no longer hangs after exiting the alt-screen--having searched for text using Find.
* The Block-list now scrolls to the correct position after returning from the alt-screen.
* Clicking above the scroll-bar no longer (incorrectly) changes its scroll position.
* The terminal cell dimensions now update immediately after modifying the Font size.
* Hyperlinks no longer incorrectly highlight on hover when Warp is not focused.
* The Input Method Editor (non-English keyboards) is now positioned correctly in the alt-screen and in running Blocks
* When there are no windows open, clicking `New Tab` from the Mac menu will create a new window

### 2023.02.09 (v0.2023.02.07.08.03)

**Bug fixes**

* Warp now sets the Mac window title; right-clicking on the dock icon will show the name of the active tab.
* Fixed a bug where navigating the theme picker with the arrow keys would lead to a crash when no theme matches the search.
* The Input Editor now refocuses correctly after clicking hyperlinks.
* Custom keybindings incorporating the `SPACE` key now persist after closing Warp.
* The Input Method Editor (non-English keyboards) now positions itself within the Input Editor

### 2023.02.02 (v0.2023.01.31.08.08)

### 2023.01.26 (v0.2023.01.24.08.03)

**New features**

* Warp can now dim inactive terminal panes, navigate to `Settings > Appearance > Panes > Dim inactive panes`

**Bug fixes**

* Fixed crash when selecting multiple occurrences of multi-byte characters using `CTRL-G`

### 2023.01.19 (v0.2023.01.17.08.03)

**New features**

* The current Git branch can now be copied using the Command Palette (`CMD-P`)

**Bug fixes**

* Fixed bug where some keybinding actions would be applied to the wrong terminal pane.
* Warp now checks the input values for font size and line height and ignores them if they are too small or large
* The `missing update permissions banner`, can now be dismissed
* Fixed a rare crash when closing panes created by a launch configuration

### 2023.01.12 (v0.2023.01.10.08.02)

**New features**

* Support setting window background transparency and blur radius, via sliders under `Settings > Appearance`
* Revamped resource center! Click the Warp icon in the top right to see keyboard shortcuts and learn how to best use Warp
* Quit modal: Quitting or closing Warp while a session is running triggers a warning prompt–that also lets you view which sessions are running
* Added a toggle to disable cursor blinking

**Bug fixes**

* Can now support completions that have escaped paths
* Can now support background images with paths that start with ~
* Can now properly restore a Warp window’s position when using multiple monitors
* Commands from restored sessions run on the local machine no longer appear in the SSH server’s history
* Fixed issues SSHing into RHEL/Fedora machines with PackageKit-command-not-found installed
* Fixed incorrect handling of `->` as the user's prompt
* Fixed ls completions when using the --color option

### 2023.01.05 (v0.2023.01.03.08.03)

**Bug fixes**

* Trailing periods are no longer considered part of a URL.
* Fixed regression where the "autocomplete symbols" setting was not being respected.

### 2022.12.15 (v0.2022.12.13.08.04)

**New features**

* You can now reorder and drag tabs around with your mouse!

**Bug fixes**

* The welcome Block now also works when using Fish shell.
* AI Command Search no longer crashes from multi-byte characters when opened via the `#` prefix
* Warp no longer crashes when starting a new session in a deleted or inaccessible directory
* Resolved rendering bugs and hangs in full-screen applications like 'k9s' and 'less'.
* Added a login failure notification.

### 2022.12.06 (v0.2022.12.06.08.03)

**New features**

* Users may now opt out of telemetry (app analytics and crash reporting)
* Added 'Tail Warp network log' workflow for viewing logs of all app network activity.

**Bug fixes**

* Full-screen CLI commands like mitmproxy now correctly span the entire view.
* Improved styling and organization of Features page in settings.
* Completions While Typing menu closes while generating new results.
* Added a hidden completion result for root dir.
* Warp now consumes less memory when a session has many blocks.
* Fixed an issue over SSH where logs were being inserted into input.

### 2022.12.02 (v0.2022.11.29.08.03)

**New features**

* Users may now opt out of telemetry (app analytics and crash reporting)
* Added 'Tail Warp network log' workflow for viewing logs of all app network activity.

**Bug fixes**

* Mitigated an issue where running a command over SSH would emit spurious output (specifically, 'channel: open failed' statements) in a block.

### 2022.12.01 (v0.2022.11.29.08.03)

**New features**

* Warp now supports using the find bar within the alt-screen! `CMD-F` now opens find within vim, less, and other alt-screen apps!

**Bug fixes**

* Respect symlinks in Warp configuration directories (for themes and workflows).
* Fixed unwanted text appearing in the Input Editor when RPROMPT is set
* Fixed the emoji composer not working properly.
* Fixed a crash that could occur when using the Unicode Hex Input keyboard.
* Fixed escape binding not closing the resource center
* Move Backward/Forward One Word bindings can now be overridden.
* Fixed crash when hovering over multiple byte text within the Input Editor
* Fixed “command not found: sed” and “command not found: tr” issues with the SSH wrapper.
* Fixed issue where tab completions and command search could be visible at the same time.

### 2022.11.15 (v0.2022.11.14.14.55)

**New features**

* Command Search: Ctrl-R opens a panel where you can search your history, workflows, and other command execution-related items, all in one place.
* Sticky command header: Warp now pins the prompt/command section of a Block to the top of the screen; click it to scroll to the top of the Block. Can be toggled via Settings > Features > Show Sticky Command Header
* Warp’s Input Editor now supports soft wrapping; long commands are now fully visible!

**Bug fixes**

* Warp now sets the TERM_PROGRAM environment variable correctly in wrapped SSH sessions.

### 2022.11.10 (v0.2022.11.08.08.07)

**New features**

* Warp now offers Command Corrections! Warp will suggest corrections for errors in previous console commands
* Warp now also detects invalid file paths -- they are underlined red when error underlining is enabled
* Added a toggle in `Settings > Appearance` to configure whether and how Warp enforces minimum contrast

**Bug fixes**

* Fixed an issue where toggling the default prompt would not update it immediately
* Improved positioning of the `TAB` completions menu when using split panes

### 2022.11.03 (v0.2022.11.01.08.03)

**New features**

* Warp's prompt now shows the number of modified files on your local git branch! Search "changed file count" in the Command Palette or right-click the Prompt to toggle.

**Bug fixes**

* Dim-styled colors are now restored properly.

### 2022.10.27 (v0.2022.10.25.08.06)

**Bug fixes**

* Fixed a bug when hovering over hover icons

### 2022.10.20 (v0.2022.10.18.08.10)

**Bug fixes**

* Modifying the mouse and scroll reporting settings now applies immediately
* Fixed cursor not blinking when starting a shell instance
* Fixed temporarily flashing the wrong prompt while Warp is still bootstrapping
* Removed duplicate entry for toggling error underlining and syntax highlighting within the Command Palette

### 2022.10.13 (v0.2022.10.11.08.13)

**New features**

* Warp’s Input Editor now has Syntax Highlighting and Error Underlining, with no configuration!
* Warp now uses a pointer cursor when hovering over links

**Bug fixes**

* Git branches in the completions menu now bold correctly
* Warp no longer crashes when `/bin/bash` is missing

### 2022.10.06 (v0.2022.10.04.08.05)

**New features**

* Drag and drop a folder or file onto the Warp dock icon to open a new tab in this directory
* Added dividers between Blocks in compact mode
* Shell keywords are now supported for completions and Command Inspector

**Bug fixes**

* Accessibility support for context menu keybinding
* Keystrokes typed while a command is still executing no longer gets dropped
* Link recognition no longer includes trailing quotes
* Find search results will continue to be highlighted after clearing the screen during a long running command
* Fixed completions for commands prefixed with environment variables
* Warp’s resource center is now center aligned

### 2022.09.29 (v0.2022.09.27.08.11)

**New features**

* Extend the currently selected text (within Blocks) with `SHIFT-LEFT`, `SHIFT-RIGHT`, `SHIFT-UP`, and `SHIFT-DOWN`
* Double-click and drag to select text in the Input Editor
* Insert the last word of the previous command with `META-.`
* Added a toggle to enable mouse and scroll reporting to the settings dialog (`Settings > Features`)

**Bug fixes**

* The `clear` command no longer appears in the snackbar at the top of the window
* Warp’s completions now support executables in remote sessions (no longer just bash)
* Fixed subcommand completions for commands with proper prefixes of each other (e.g. `npm r` and `npm run`)
* The completion spec for `lsd` now supports files

### 2022.09.22 (v0.2022.09.20.08.08)

**New features**

* After selecting a Block press `CTRL-M` to open its context menu
* Commands in the tab completions menu and history menu can now be executed directly with `CMD-ENTER`
* Completions now support shell builtins, git aliases, and also npm aliases

**Bug fixes**

* Command Palette now includes the most useful features at the top
* Improved flag completions for cargo

### 2022.09.15 (v0.2022.09.13.08.15)

**New features**

* Warp Resource Center - explore Warp features and documentation by clicking the `?` icon or pressing `SHIFT-CTRL-?`
* New icons in the completion menu denoting flags, folders, branches, etc.

**Bug fixes**

* Press `CMD-ENTER` within the history menu (`CTRL-R`) to directly execute the highlighted command
* Fixed crash when opening many tabs (due to MacOS’s default open file descriptor limits)
* Fixed crash when laying out RTL text

### 2022.09.08 (v0.2022.09.07.14.56)

**New features**

* Global hotkey window can now float above full-screen apps
* Tabs can now have their color customized (via right-clicking on a tab)
* Terminal line height is now configurable (via Settings > Appearance)

### 2022.09.01 (v0.2022.08.31.18.11)

**New features**

* Tab completions now support fuzzy string matching
* Improve completions for over 450 commands, including docker, kubernetes, cargo, node, and git

**Bug fixes**

* Properly send C0 control codes for <ctrl-[2-8]> keystrokes
* Session restoration now also persists bold, underline, italic, and strikethrough formatting
* Inspect mode now works for the changelog modal
* Fixed a crash when highlighting a link
* Fixed Find occasionally returning only partial results
* Fixed occasional crash when loading images
* Fixed display issue in the Mac Menu for keyboard shortcuts with special keys

### 2022.08.25 (v0.2022.08.23.08.06)

**New features**

* Experimental feature: support for always-on completions — the completions menu can now open automatically while typing (enable via Settings -> Features)

**Bug fixes**

* Custom tab titles no longer get overwritten when using multiple panes
* A Block’s execution duration is now formatted in hours, minutes, and seconds
* Improved rendering of the ‘Current session’ text in the Navigation Palette
* Warp properly hides the cursor when a CLI sends the respective escape sequence
* Warp stays focused (keyboard-interactive) after closing the Share Block menu and the context menu
* Warp no longer lags when the Ctrl-R menu is opened
* Confirming a tab suggestion appends a space to the buffer

### 2022.08.18 (v0.2022.08.16.10.16)

**New features**

* Launch Configurations - Save a configuration of windows, tabs, and panes to open later with `CTRL-CMD-L`
* Session Navigation - Navigate to any session in Warp with `SHIFT-CMD-P`
* Added exclusive theme for users who joined Warp through a referral

**Bug fixes**

* Prompt now shows Git SHA instead of HEAD when you’re not on a branch
* Filepath completions now include current directory ('.') and parent directory ('..')
* Support `SHIFT-HOME` and `SHIFT-END` keybindings to select text to line start and end.
* Items in the Command Palette now highlight when you hover over them with your mouse
* Improved how Warp cleans up the warptmp directory for Zsh SSH sessions
* Already open dropdown menus are now properly closed when clicked
* Warp no longer crashes when dragging a window that’s running htop
* Warp no longer crashes when the find bar is open

### 2022.08.10 (v0.2022.08.08.09.21)

**New features**

* Can now Middle-click a tab to close it
* Added additional tab reordering options (Close: tab, other tabs, and tabs to the right) via the Mac Menu, the Command Palette, and a tab’s context menu (right click)

**Bug fixes**

* Added a toggle to the Mac Menu for maximizing panes
* Can now switch panes using keyboard shortcuts even when a pane is maximized
* Add support for opening file paths with RubyMine, PhpStorm, and WebStorm
* Fixed crash when highlighting links
* Fixed issue where the HISTCONTROL environment variable was ignored in bash
* Pressing `CTRL-R` to open history search no longer crashes Warp when you have multiple cursors

### 2022.08.03 (v0.2022.08.01.09.12)

**New features**

* Updated Mac menus to make Warp actions more discoverable - [101](https://github.com/warpdotdev/warp/issues/101)
* Warp now supports opening file links and urls via CMD-CLICK! - [177](https://github.com/warpdotdev/warp/issues/177)

**Bug fixes**

* Various CLI tools no longer hang e.g. Bazel and Maven
* Command Inspector hover no longer crashes with UTF-8 encoded strings
* Opening the find / search bar (`CMD-F`) now automatically selects the text
* Tab titles are no longer reset when changing panes

### 2022.07.27 (v0.2022.07.25.09.05)

**Bug fixes**

* Closing and re-opening the Command Palette now resets the selected item
* The cursor’s position is now restored after exiting the Command History Search (`CTRL-R`) menu.
* Shorthand and longhand flags are now correctly surfaced (based on the number of dashes) in tab completions
* Added voiceover support for `BACKSPACE` and `DELETE` keystrokes within the Input Editor

### 2022.07.20 (v0.2022.07.18.09.06)

**New features**

* Command Inspector - hover over any piece of a command in Warp’s Input Editor to surface documentation or press `CMD+I` to inspect at the cursor’s current location
* Improved ordering in the tab completions menu

**Bug fixes**

* Font color for links in light mode (themes) now set correctly
* Moving forward by a word no longer moves farther than expected
* Warp no longer hangs when passing an invalid file path
* Fixed issues with persisting the selected theme when “Sync with OS” is enabled and the theme picker is launched from the Command Palette (or a keyboard shortcut)
* Fixed issues with text input after clearing Blocks (`CMD-K`) while in a REPL environment.
* Fixed shortcut for select-left-by-word (`SHIFT-CMD-B`), select-right-by-word (`SHIFT-CMD-F`), select-line-to-end (`SHIFT-CTRL-E`), and select-line-to-start (`SHIFT-CTRL-A`)

### 2022.07.13 (v0.2022.07.11.09.11)

**Bug fixes**

* Improved startup time for Fish shells
* Find Bar no longer crashes on selected text
* Scrollbar now supports jumping to where you click
* Fixed a bug with the referral link for sharing Warp not loading

### 2022.07.07 (v0.2022.07.04.09.08)

**New features**

* Bookmark a Block (or multiple) for quick access via the scroll-bar
* Added a referral counter to the Settings > Account screen and the referral screen
* Added support for rendering text with a lower visual weight; enable the thin strokes option in Settings > Appearance (enabled by default for low-DPI displays)
* Togglable settings, overflow menu items, and settings pages are now accessible through the Command Palette
* CLI options are now surfaced by default without needing to type '-'
* Press SHIFT-CMD-C while in VSCode (Visual Studio Code) to open a new Warp session

**Bug fixes**

* Fixed referal links and share by email
* Fixed a hang that would sometimes occur when connecting with SSH
* Now support requesting media permissions (camera, audio, etc)
* Correctly parse Git commit SHAs in completion menus
* Improved tab completion support for command line arguments that are behind flags

### 2022.07.06 (v0.2022.07.04.09.08)

**New features**

* Bookmark a Block (or multiple) for quick access via the scroll-bar
* Added a referral counter to the Settings > Account screen and the referral screen
* Added support for rendering text with a lower visual weight; enable the thin strokes option in Settings > Appearance (enabled by default for low-DPI displays)
* Togglable settings, overflow menu items, and settings pages are now accessible through the Command Palette
* CLI options are now surfaced by default without needing to type '-'
* Press SHIFT-CMD-C while in VSCode (Visual Studio Code) to open a new Warp session

**Bug fixes**

* Fixed a hang that would sometimes occur when connecting with SSH
* Now support requesting media permissions (camera, audio, etc)
* Correctly parse Git commit SHAs in completion menus
* Improved tab completion support for command line arguments that are behind flags

### 2022.06.29 (v0.2022.06.27.09.14)

**Bug fixes**

* Cursor changes when hovering over clickable UI elements and the Input Editor
* Dim colors now render correctly

### 2022.06.27 (v0.2022.06.20.09.15)

**New features**

* Improved auto-focus behavior when closing panes by keeping track of history when navigating or clicking around panes
* Performance improvements when executing Blocks: Warp no longer flashes on every command!

**Bug fixes**

* Input Editor re-focuses after renaming a tab
* Reduced visual weight of the active tab title to improve legibility.
* Improved blending along the inside edge of rounded corners
* Global Hotkey Windows (Quake Mode) now correctly respect the active screen setting
* Completions for flag arguments now support absolute and relative file paths (when applicable)
* Git checkout <`TAB`> now also completes branches with the remote prefixed.
* Pressing Arrow-up (`UP`) when the Input Editor is non-empty opens the command history with prefix filtering
* Button to copy app version moved to main settings page

### 2022.06.22 (v0.2022.06.20.09.15)

**New features**

* Improved auto-focus behavior when closing panes by keeping track of history when navigating or clicking around panes
* Performance improvements when executing Blocks: Warp no longer flashes on every command!

**Bug fixes**

* Input Editor re-focuses after renaming a tab
* Reduced visual weight of the active tab title to improve legibility.
* Improved blending along the inside edge of rounded corners
* Global Hotkey Windows (Quake Mode) now correctly respect the active screen setting
* Completions for flag arguments now support absolute and relative file paths (when applicable)
* Git checkout <`TAB`> now also completes branches with the remote prefixed.
* Pressing Arrow-up (`UP`) when the Input Editor is non-empty opens the command history with prefix filtering
* Button to copy app version moved to main settings page

### 2022.06.17 (v0.2022.06.13.09.15)

**New features**

* Added keyboard shortcuts to reorder tabs (CTRL-SHIFT-LEFT and CTRL-SHIFT-RIGHT)

**Bug fixes**

* Warp no longer crashes on MacOS 13 (Ventura)
* Global Hotkey Window (Quake Mode) no longer overlaps Spotlight, Raycast, Alfred, and the Mac Dock
* Now correctly display the user and hostname in the Prompt after exiting an SSH session
* Fixed a memory leak on window close.

### 2022.06.15 (v0.2022.06.13.09.15)

**New features**

* Added keyboard shortcuts to reorder tabs (CTRL-SHIFT-LEFT and CTRL-SHIFT-RIGHT)

**Bug fixes**

* Global Hotkey Window (Quake Mode) no longer overlaps Spotlight, Raycast, Alfred, and the Mac Dock
* Now correctly display the user and hostname in the Prompt after exiting an SSH session
* Fixed a memory leak on window close.

### 2022.06.08 (v0.2022.06.06.09.05)

**New features**

* Now support renaming tabs (right click on your tab title!)
* Now support enabling custom prompt from prompt context menu (right-click on prompt)
* Now support splitting panes (left and right) from the context menu (right click) and through the Command Palette
* Now support CTRL-Click as an alternative to right-clicking

**Bug fixes**

* Improved completions support for arguments nested under options (e.g. git branch -D <branch_name...>)
* Modified files are now included (in addition to commit SHAs) for `git diff`

### 2022.06.01 (v0.2022.05.30.09.10)

**New features**

* Added information about rewards to the referral screen
* Added a button that toggles regex search in the Find Bar
* Added completion support for shell functions

**Bug fixes**

* Hotfix - a regression that caused Warp to stall when using nano
* Improved kerning (font rendering) throughout the app
* Added a hyperlink (to our changelog history) in the Changelog modal
* Multiline commands that don't have any output are no longer cut off

### 2022.05.26 (v0.2022.05.23.09.07)

**New features**

* Warp can now send you desktop notifications for long-running commands and password prompts - [628](https://github.com/warpdotdev/warp/issues/628)
* Added keybinding to toggle fullscreen mode

**Bug fixes**

* Stopped prepending \ before ~ in tab titles for older versions of Bash
* Added support for CMD-G and SHIFT-CMD-G to tab between results in the Find Bar

### 2022.05.18 (v0.2022.05.16.09.01)

**New features**

* Added exclusive theme available to anyone who has referred someone to Warp. (Open Theme Picker > Warp Referral to use it)

**Bug fixes**

* Improved rendering of rounded corners throughout the app
* Fixed cell dimension computation for some fonts
* Fixed labels rendering incorrectly in the font selector dropdown in settings
* Fixed Bash remote sessions missing tab titles
* Reduced UI flickering after executing commands
* Fixed errors when sshing into remote machines which do not have xxd available
* Fixed some anti-aliased glyphs getting clipped during rasterization
* Fixed search bar stealing focus after command execution

### 2022.05.11 (v0.2022.05.09.09.06)

**New features**

* Filepath completions without needing to cd
* Support for any font (not just monospaced)

**Bug fixes**

* Tab completions (cd) with international characters are now properly escaped (edited)
* Improve rendering performance when many tabs are open (fixes non-responsiveness when searching history)
* Fixed a race condition with autoupdate a11y announcements and other a11y messaging
* Fixed a regression that would cut off the output of some long-running Blocks

### 2022.05.04 (v0.2022.05.02.09.00)

**New features**

* Added default tab titles for Bash
* Improved default tab title in Zsh
* Maximize a split pane
* Support rcfiles that check PS1 to determine if it's an interactive shell; this may explain missing aliases or commands in Warp!

**Bug fixes**

* History now correctly shows results after hitting ESC when a Block is focused
* Fixed crash when quitting AI Command Search while a command was being generated
* Global keybindings with function keys and numeric keys are now properly registered
* Warp no longer jumps up and down for single-line commands that take more than 50ms

### 2022.05.02 (v0.2022.04.25.09.59)

**New features**

* Added a Quake Mode setting that configures whether Warp should automatically hide when losing focus - [1077](https://github.com/warpdotdev/warp/issues/1077)
* Added a Quake Mode setting that configures which screen to pin Warp on - [862](https://github.com/warpdotdev/warp/issues/862)
* Expanded the keybindings supported by Quake Mode / Global Hotkey Window - [856](https://github.com/warpdotdev/warp/issues/856)

**Bug fixes**

* Commands prepended with space are now stored in history if hist_ignore_space option is not set
* Now support dotfile configurations with non-English quotation marks
* Continued improving the reliability of login and auth within the app
* Improved performance for commands with large outputs
* Improved performance for long running commands
* Improved text alignment within inline banners

### 2022.04.27 (v0.2022.04.25.09.59)

**New features**

* Added a Quake Mode setting that configures whether Warp should automatically hide when losing focus - [1077](https://github.com/warpdotdev/warp/issues/1077)
* Added a Quake Mode setting that configures which screen to pin Warp on - [862](https://github.com/warpdotdev/warp/issues/862)
* Expanded the keybindings supported by Quake Mode / Global Hotkey Window - [856](https://github.com/warpdotdev/warp/issues/856)

**Bug fixes**

* Commands prepended with space are now stored in history if hist_ignore_space option is not set
* Now support dotfile configurations with non-English quotation marks
* Continued improving the reliability of login and auth within the app
* Improved performance for commands with large outputs
* Improved performance for long running commands
* Improved line height computation for some fonts
* Improved text alignment within inline banners

### 2022.04.20 (v0.2022.04.18.09.08)

**New features**

* Support logging into Warp by pasting the auth url when "Take me to Warp" fails in browser

**Bug fixes**

* Improved reliability of login and auth within the app
* Buttons within the find bar are now properly shaded for gradient themes
* Workflows with default values are now registered by Warp
* Fixed bootstrapping bug that affected Fish versions older than 3.2.0
* Fixed a memory leak that occurred when new tabs were opened or panes were split

### 2022.04.15 (v0.2022.04.11.09.09)

**Bug fixes**

* Support parsing PS1’s exit codes (Bash’s $?) and improved PS1 parsing for newer Bash versions (4.4+)
* Fixed prompt showing up as exit in Bash - [793](https://github.com/warpdotdev/warp/issues/793)
* Improved parsing of Zsh default prompts
* Opening the find bar will automatically select any existing text - [831](https://github.com/warpdotdev/warp/issues/831)

### 2022.04.13 (v0.2022.04.11.09.09)

**Bug fixes**

* Support parsing PS1’s exit codes (Bash’s $?) and improved PS1 parsing for newer Bash versions (4.4+)
* Fixed prompt showing up as exit in Bash - [793](https://github.com/warpdotdev/warp/issues/793)
* Improved parsing of Zsh default prompts
* Opening the find bar will automatically select any existing text - [831](https://github.com/warpdotdev/warp/issues/831)

### 2022.04.08 (v0.2022.04.04.09.07)

**Bug fixes**

* Block sharing dialog now scrolls properly

### 2022.04.01 (v0.2022.04.01.01.37)

**New features**

* Warm welcome!
* A.I. Command Search

**Bug fixes**

* Warp now properly registers `SPACE` and `SHIFT` modifier keys for Global Hotkey Windows
* Page Up and Page Down keys now work correctly in vim and other fullscreen apps - [560](https://github.com/warpdotdev/warp/issues/560)
* SSH now supports bootstrapping if bash-preexec is included in a Debian VM’s system rcfiles (eg by default at Google) - [578](https://github.com/warpdotdev/warp/issues/578)
* Corrected keyboard shortcut for split pane in context menu

### 2022.03.30 (v0.2022.03.29.02.23)

**New features**

* Workflows: an easier way to share, parameterize, and execute commands - [625](https://github.com/warpdotdev/warp/issues/625)
* Quake mode / Focus Warp with a Global Hotkey - [091](https://github.com/warpdotdev/warp/issues/091)

**Bug fixes**

* Magnet, Swish and ALT-Tab window managers now work with Warp - [776](https://github.com/warpdotdev/warp/issues/776)
* SSH now handles control master connection errors - [578](https://github.com/warpdotdev/warp/issues/578)
* SSH now handles verbose mode, no longer leaks into the Input Editor as a typeahead - [578](https://github.com/warpdotdev/warp/issues/578)
* SSH now boots normally for POSIX shells that aren’t supported by Warp’s wrapper - [578](https://github.com/warpdotdev/warp/issues/578)

### 2022.03.24 (v0.2022.03.23.22.10)

**New features**

* Fish support - [190](https://github.com/warpdotdev/warp/issues/190)
* Basic screenreader support (Voiceover) - Warp is now an accessible terminal!
* Added a toggle in the settings to disable the SSH wrapper - [821](https://github.com/warpdotdev/warp/issues/821)

**Bug fixes**

* Hitting tab with a text selection shows tab completions instead of indenting
* SSH no longer hangs when /tmp is not writable for Zsh - [578](https://github.com/warpdotdev/warp/issues/578)
* SSH no longer bootstrap the shell if it’s not meant to be an interactive session (e.g. if -T or a command is passed) - [578](https://github.com/warpdotdev/warp/issues/578)
* SSH now supports Starship and Zsh's $PROMPT variable - [803](https://github.com/warpdotdev/warp/issues/803)
* Also import themes in subdirectories e.g. `~/.warp/themes/subdirectory/theme.yaml`

### 2022.03.16 (v0.2022.03.14.08.49)

**New features**

* Multi-block selections and corresponding actions - [146](https://github.com/warpdotdev/warp/issues/146)
* Case-sensitive search

**Bug fixes**

* SSH no longer returns 0~ and 1~ after executing commands for Zsh 5.0.8 or older - [578](https://github.com/warpdotdev/warp/issues/578)
* SSH now supports LocalCommand / RemoteCommand - [578](https://github.com/warpdotdev/warp/issues/578)
* SSH over Zsh no longer depends on configuring locales on the remote machine - [578](https://github.com/warpdotdev/warp/issues/578)
* SSH sources /etc/bash.bashrc which is an extra rcfile in Debian and other Linux distributions - [578](https://github.com/warpdotdev/warp/issues/578)
* Improved completions stability when there are multiple panes on the same remote machine
* Vim and other alt-screen apps properly expand to take up the full window - [552](https://github.com/warpdotdev/warp/issues/552)
* Clicking into Warp from other foreground window focuses the clicked pane - [739](https://github.com/warpdotdev/warp/issues/739)
* Warp now respects ignore-space history options for Zsh and Bash - [044](https://github.com/warpdotdev/warp/issues/044)
* Warp now creates a ~/.warp folder to persist custom keybindings - [801](https://github.com/warpdotdev/warp/issues/801)

### 2022.03.09 (v0.2022.03.07.08.51)

**Bug fixes**

* Added missing actions to Command Palette
* Option is meta is now in the settings menu
* Fix for SSH hanging when Zsh is the remote login shell
* Fix for SSH with Zsh that would break with certain rcfiles because of incorrectly set ZDOTDIR

### 2022.03.02 (v0.2022.02.28.08.45)

**New features**

* Can now edit the keybindings for arrow navigation (Up/Down/Left/Right)
* Can now edit the keybindings for activating specific tabs (by number CMD-1, CMD-2, …)

**Bug fixes**

* Crash in theme chooser
* Fix for tab completion sometimes deleting characters

### 2022.02.23 (v0.2022.02.21.08.55)

**New features**

* Zsh support over SSH
* Partially complete autosuggestion (by word) using CTRL-RIGHT and ALT-RIGHT - [488](https://github.com/warpdotdev/warp/issues/488)
* Added a Copy URL menu item after right-clicking a URL - [154](https://github.com/warpdotdev/warp/issues/154)
* Indicator for conflicting keybindings in keyboard customization UI

**Bug fixes**

* Able to fill-in longest common prefix after filtering tab completions - [618](https://github.com/warpdotdev/warp/issues/618)
* Block completion causes Input Editor to steal focus from find bar - [452](https://github.com/warpdotdev/warp/issues/452)
* UP-arrow in history menu sometimes scrolls more than one item
* CMD-F opens a no-op find bar in alt screen

### 2022.02.16 (v0.2022.02.14.08.44)

**New features**

* Customizable key bindings (accessible via the settings menu) - [579](https://github.com/warpdotdev/warp/issues/579)
* Users can opt in to use their shell’s prompt rather than Warp’s default (select the Honor PS1 toggle under the settings menu) - [580](https://github.com/warpdotdev/warp/issues/580)
* Added a timestamp showing Block runtime duration; hover to see start and end date + time - [178](https://github.com/warpdotdev/warp/issues/178)
* CTRL-F now accepts autosuggestions - [403](https://github.com/warpdotdev/warp/issues/403)
* CTRL-E and CMD-RIGHT accept autosuggestions when at the end of the buffer - [403](https://github.com/warpdotdev/warp/issues/403)
* Allow input height to expand to half the pane height - [621](https://github.com/warpdotdev/warp/issues/621)

**Bug fixes**

* Arrow key presses now (up and down now) cycle themes in the theme picker - [294](https://github.com/warpdotdev/warp/issues/294)
* ESC keypress now exits the theme picker
* CMD-Down when on most recent block to focus input now clears Block selection
* Fixed a bug where resizing a pane while a command was running made it impossible to scroll to the bottom of the pane
* Fixed a bug where resizing a pane could cause Warp to show a blank screen
* Parentheses, quotes, and brackets now also auto-close after typing an alphanumeric character
* Remapped multi-cursor key bindings to CTRL-SHIFT-UP and CTRL-SHIFT-DOWN - [374](https://github.com/warpdotdev/warp/issues/374)
* Restored OPT-CMD-UP and OPT-CMD-DOWN for switching panes up and down - [730](https://github.com/warpdotdev/warp/issues/730) 

### 2022.02.02 (v0.2022.01.31.09.03)

**New features**

* Multi-cursor keybindings for adding cursors above and below current selections with OPT-CMD-UP/DOWN - [374](https://github.com/warpdotdev/warp/issues/374)

**Bug fixes**

* Double clicking the top of the window maximizes the app - [097](https://github.com/warpdotdev/warp/issues/097)
* Icon, cursor and selection contrast fixes
* Scrolling performance improvements with bg image themes
* Changelog visual glitch
* Resize bug - losing scroll position when viewing blocks with long output

### 2022.01.26 (v0.2022.01.24.08.55)

**New features**

* Auto-close symbols (parentheses, quotes, and brackets) like VSCode

**Bug fixes**

* Block sharing link no longer cuts off - [660](https://github.com/warpdotdev/warp/issues/660)
* Right clicking a Block now focuses that Block
* Mouse dragging in vim
* Restoring history bug on session restore
* Automatically focus the last active window on session restore

### 2022.01.19 (v0.2022.01.17.08.48)

**New features**

* Restore block contents
* The longest common prefix in the completions menu auto-fills the Input Editor - [479](https://github.com/warpdotdev/warp/issues/479)
* Add description for paths in completion results - [103](https://github.com/warpdotdev/warp/issues/103)
* Can right click the prompt and copy: git branch, prompt, cwd - [346](https://github.com/warpdotdev/warp/issues/346)

**Bug fixes**

* Fixed bug where venv was inserted into input editor - [599](https://github.com/warpdotdev/warp/issues/599)
* Improved url detection

### 2022.01.12 (v0.2022.01.10.17.24)

**New features**

* Added a Changelog page to our documentation

**Bug fixes**

* Double clicking text in a url now highlights the word instead of the whole url - [508](https://github.com/warpdotdev/warp/issues/508)
* Double clicking a string with underscores now selects the whole string and not just the subword
* Selection updates correctly when a block hit its max line length
* Can now also close the Command Palette using CMD-P - [184](https://github.com/warpdotdev/warp/issues/184)
* Moved check for update button to settings dialog - [070](https://github.com/warpdotdev/warp/issues/070)
* Fixes tabs not opening in new windows when autoupdate is pending
* Fix regression with input box not being focused on app relaunch

### 2022.01.05 (v0.2022.01.03.09.07)

**New features**

* Native undo and redo in the text editor using CMD-Z - [113](https://github.com/warpdotdev/warp/issues/113)
* Added CMD-M to minimize the Window - [107](https://github.com/warpdotdev/warp/issues/107)
* Added our open source licenses to the Warp Documentation
* Split pane focus indicator - a triangle in the top left corner of the pane in focus

**Bug fixes**

* CTRL-SPACE is now properly passed to Emacs and other terminal apps - [499](https://github.com/warpdotdev/warp/issues/499)
* Copy on select setting persists across sessions and does not reset after updates

### 2021.12.29 (v0.2021.12.27.09.04)

**New features**

* Find in block (+ other find improvements)

### 2021.12.22 (v0.2021.12.20.09.04)

**New features**

* Windows, tabs, and panes are restored whenever you reopen Warp. Restoring block content is on its way!
* Warp now supports completions for over 300 commands and more information about existing commands by using Fig’s completion specs
* Git aliases are now included in completions menu - [210](https://github.com/warpdotdev/warp/issues/210)
* Switch to next pane and previous pane with CMD-[ and CMD-] - [392](https://github.com/warpdotdev/warp/issues/392)
* Scrolling the Block list with PG-UP and PG-DOWN - [370](https://github.com/warpdotdev/warp/issues/370)
* Copy and paste the file directory into Warp from Finder - [514](https://github.com/warpdotdev/warp/issues/514)
* When the last Block is selected, can re-focus the input editor using CMD-DOWN key
* Arrow down scrolls to bottom of last block

**Bug fixes**

* Copying selected text to clipboard creates a new entry for each selected character - [504](https://github.com/warpdotdev/warp/issues/504)
* Needed an extra backspace to escape CTRL-R / history menu - [427](https://github.com/warpdotdev/warp/issues/427)
* VIM performance improvements - we’ve made progress but would love more sample cases of slowness

**Updates to Mac Menu Bar (Window)**

* Zoom
* Minimize
* Tile Window to Left of Screen (Default)
* Tile Window to Right of Screen (Default)
* Move to X screen (Default)
* Enter Full Screen (Default)
* Bring All to Front

### 2021.12.15 (v0.2021.12.13.08.40)

**New features**

* Fuzzy search in CTRL-R and Command Palette
* When you share a link to a block, up to 5 recipients may now download Warp’s beta via the link

**Bug fixes**

* Fix bug where opening file:// urls would not include query params like '?foo=bar' - [426](https://github.com/warpdotdev/warp/issues/426)
* More prominent highlights in CTRL-R, Command Palette, tab completion
* Vim bug fixes and performance improvements - please let us know what else you see

### 2021.12.08 (v0.2021.12.06.19.09)

**New features**

* Added a send invite button in account section of the settings dialog
* You can now request more invites in the invite modal

**Bug fixes**

* Copy on select persistence bug
* UI Bug when trying to un-share a block - [439](https://github.com/warpdotdev/warp/issues/439)

### 2021.12.01 (v0.2021.11.29.18.59)

**New features**

* Added 15 extra invites for everyone!
* Copy on select (highlighting text will automatically copy to clipboard). This can be turned off in the settings dialog - [077](https://github.com/warpdotdev/warp/issues/077)
* CTRL-L shortcut to clear the screen - [049](https://github.com/warpdotdev/warp/issues/049)

**Bug fixes**

* Can now highlight and copy sections of a URL without it automatically opening - [138](https://github.com/warpdotdev/warp/issues/138)

### 2021.11.24 (v0.2021.11.23.17.55)

**New features**

* Background images + gradients in themes: You can now set a background image or gradient as your theme background. Warp ships with a few of these already or you can create your own via a yaml file. - [032](https://github.com/warpdotdev/warp/issues/032)
* Changelog dialog
* Emoji rendering: 😂, 😃, 🌍, 🍞, 🚗, 📞, 🎉, ❤️ - [075](https://github.com/warpdotdev/warp/issues/075)
* Improved settings dialog
* Theme search - [237](https://github.com/warpdotdev/warp/issues/237) 

**Bug fixes**

* Properly escapes whitespace when you drag and drop files

### 2021.11.17 (v0.2021.11.16.20.05)

**New features**

* Drag and drop files & directories from finder - [069](https://github.com/warpdotdev/warp/issues/069)

### 2021.11.10 (v0.2021.11.09.19.46)

**New features**

* Autosuggestions: Warp now suggests commands as you type, similar to Fish or Gmail - [052](https://github.com/warpdotdev/warp/issues/052)
* Button to copy the app/version - [106](https://github.com/warpdotdev/warp/issues/106)
* Conda context to the prompt - [235](https://github.com/warpdotdev/warp/issues/235)

**Bug fixes**

* Conda info (prompt) locking input editor
* CTRL-D now deletes forward one character
* History now preserved across sessions - [337](https://github.com/warpdotdev/warp/issues/337)
* Enter (numpad) was inputting as CTRL-C - [330](https://github.com/warpdotdev/warp/issues/330)

### 2021.11.03 (v0.2021.11.02.00.38)

**New features**

* CJK (Chinese, Japanese, and Korean) character support - [327](https://github.com/warpdotdev/warp/issues/327)
* Autocompletions for missing tar commands
* Enforcement of minimum contrasts in grid - [249](https://github.com/warpdotdev/warp/issues/249)

**Bug fixes**

* Runaway memory usage (from font loading on initial run) - [232](https://github.com/warpdotdev/warp/issues/232)
* Directories with non-english filenames not rendering on screen - [309](https://github.com/warpdotdev/warp/issues/309)
* App crashes from missing current working directory
* Pure Prompt being inserted as a typehead into editor - [242](https://github.com/warpdotdev/warp/issues/242)

### 2021.10.27 (v0.2021.10.25.22.47)

**New features**

* Ability to unshare blocks in settings modal
* Link to the documentation in kebab menu (three dots in top right corner)

**Bug fixes**

* Double character entry after input editor loses focus

### 2021.10.20 (v0.2021.10.19.21.38)

**New features**

* Switch theme based on OS appearance - [068](https://github.com/warpdotdev/warp/issues/068)
* Toggles instead of buttons in the setttings!
* Link to Custom themes documentation in the settings

**Bug fixes**

* IME support (non-English keyboards are now better supported in input box!)
* Show a banner instead of a popup when app startup takes longer than expected
* git log (and similar commands) no longer treated as a failed block

### 2021.10.13 (v0.2021.10.12.19.34)

**Bug fixes**

* Shell Bootstrapping should be a lot faster
* Support 3-char color representation for hex colors in theme
* Fix crashes relating to reading history files
* Prevent block completion from stealing focus
* Fix broken click handling for showing and hiding overflow menu

### 2021.10.06 (v0.2021.10.05.20.07)

**Bug fixes**

* Split pane navigation when 'Left / Right Option is Meta' settings are enabled
* Crash when opening a new window

### 2021.09.29 (v0.2021.09.29.13.26)

**New features**

* Split panes: create multiple panes in the same tab via shortcuts (CMD-E/SHIFT-CMD-E), the Command Palette, or by right clicking in any pane.
* Custom themes via files.  You can now define your own theme as a yaml file in ~/.warp/themes. For more information on the file format and to see ~100 of the most popular themes already implemented in this format, see https://github.com/warpdotdev/themes. The ability to add and share themes directly within Warp is coming soon!

**Bug fixes**

* Add better messaging when Warp does not have permission to autoupdate
* Crash if a tab completion result was accepted after the cursor was moved to the beginning of the editor

### 2021.09.22 (v0.2021.09.21.20.54)

**New features**

* Theme picker available from the Command Palette

**Bug fixes**

* Occasional crash when opening a new Warp window
* Font selection dropdown didn't respect theme choice
* Issues with padding and hover detection when toggling Compact Mode on or off

### 2021.09.15 (v0.2021.09.14.21.25)

**Bug fixes**

* Crash when closing full-screen window
* Executables in path were not appearing for completions in Bash
* Completions menu overlaps theme picker

### 2021.09.09 (v0.2021.09.09.0.0)

**New features**

* New themes for Warp!!! (Access them via Settings on the overflow menu. We have Dracula, Solarized, & Gruvbox)
* CMD-, opens the Settings menu

**Bug fixes**

* Fixed crash when we fail to load a font or when we scroll through fonts
* Fixed visual artifacts around windows and modals jumping
* Fixed crash that occurs when you CMD-F while selecting an already selected text

### 2021.08.31 (v0.2021.08.31.0.0)

**New features**

* Support emacs bindings in input box
* History up menu performs a prefix search based on input

**Bug fixes**

* Warp not rendering after executing long-running command
* Stop powerlevel10k instant prompt from hanging on bootstrap
* Changing “font-size” via CTRL-- and CTRL-0 should stay in sync with font size in settings menu
* Bracketed paste mode bug: 0~ ~1 on every command when ssh-ing
* Crash when tab completing with multibyte characters
* Download page doesn’t render correctly on safari
* Login is broken for some users using Chrome
* Make it more prominent in onboarding that we are collecting telemetry during the beta

### 2021.08.25 (v0.2021.08.25.0.0)

**New features**

* Custom fonts
* Completions for aliases and environment variables

**Bug fixes**

* Completions loose ends, including completions for path names with spaces and if commands are separated by &&
* Function key support within running programs (such as htop)
* Editor text respects zoom level
* Regression that caused URLs to not be highlighted
* Opening a new window required Internet connection

### 2021.08.18 (v0.2021.08.18.0.0)

**New features**

* Re-run with sudo

**Bug fixes**

* Crash caused by pressing CMD-K
* Completion not working when cursor is mid-line
* Re-input of multi-line commands
* [084](https://github.com/warpdotdev/warp/issues/084) - Rendering of colors correctly in diffs
* Selection showing after closing and re-opening alt-screen

### 2021.08.09 (v0.2021.08.09.0.0)

**New features**

* New settings modal (accessible from the top right overflow button) to set font size, toggle between light mode and dark mode, compact mode and normal mode
* CTRL-U and CTRL-K now cut to clipboard
* Typeahead: characters you type in a long-running command will now show up in the input box when the command completes

**Bug fixes**

* Handle arrow keys with modifiers (option and command) in CLIs and full-screen apps (Previously, users were unable to navigate with option and command keys in - Postgres CLI)
* Straightening the text baseline
* Translucent colors (e.g. for diff-so-fancy) are now correct (We now support the full range of opacity)
* Dotfile path completions + Completions improvements for more commands
* Artifacts when rendering svgs, especially on low res monitors. Overflow menu looks a lot better now!

### 2021.07.28 (v0.2021.07.28.0.0)

**New features**

* Compact Mode (see GIF below)
* Support for mouse events in Vim and other programs that can handle mouse input
* Completions for npm / yarn scripts

**Bug fixes**

* Major improvements to the consistency of completions, especially for commands that can take multiple arguments (e.g. rm -rf)
* Proper path completions for absolute paths
* Hang when PROMPT_COMMAND is set for the shell
* Context Menu not closing when clicking outside of the menu
* Crashes after executing multi-line commands and on older versions of macOS

### 2021.07.21 (v0.2021.07.21.0.0)

**New features**

* Support for numpad ENTER
* More npm & yarn completions

**Bug fixes**

* Down arrow sends unrecognized escape sequence to Github CLI
* Can’t use UP arrow if item in history is multiple lines
* Crash when closing a tab when there are multiple tabs
* File-only completion signatures should also show directories

### 2021.07.13 (v0.2021.07.13.0.0)

**New features**

* New invite system to add users to Warp. To invite new users, click the overflow menu at the top right and click 'invite users'. For now we ask that you please don't post these invites on social media!
* URLs in the terminal screen are auto-linkified
* Double clicking the title bar maximizes/minimizes the window

**Bug fixes**

* Various Command Palette bugs
* Find box is populated with the user's text selection
* 3 second latency when changing the prompt upon first SSHing

### 2021.07.07 (v0.2021.07.07.0.0)

**New features**

* Command Palette for most keyboard shortcuts (CMD-P)
* Previously, tab completion descriptions were cut off. Now we display them in a floating box
* You can now switch tabs using CTRL-TAB and CTRL-SHIFT-TAB

**Bug fixes**

* Intermittent crashes with Zsh sessions and switching tabs
* Always fall back to path suggestions for completions
* Various bugs related to completions

### 2021.06.29 (v0.2021.06.29.0.0)

**New features**

* Multiple window support
* New completions UI and in-line documentation for commands and flags
* Horizontal scrolling of input box to support long commands

**Bug fixes**

* Crash when exiting from logout or exit when there’s a background process
* Crash when bootstrapping from detecting incorrect shell name
* Various bugs related to completions

### 2021.06.15 (v0.2021.06.15.19.04)

**New features**

* Mac File and Edit menus, along with Mac standard menu items (although New Window not yet working)

**Bug fixes**

* Crash when closing last window
* CMD-F: when there are no matches, display 0/0
* CMD-F should not scroll away if navigating to a match on the same row
* CMD-F: render the yellow rectangle at the layer of rendering the cell
* Unable to move cursor upwards on multi-line previous command
* Warp bootstrap commands showing up in history over ssh
* Accept input via input box before terminal has bootstrapped
* New tab button should have hover and click state
* Output stops midway through session on iMac running Mojave 10.14.6
* Backspace doesn’t work while holding shift
* Clipping issue in share dialog
* Input suggestions closes if you click on the scrollbar
* Hitting up/down while input suggestions are open causes menu to move
* Paste is not working for full screen apps
* Underline does not render with Hack font

### 2021.06.09 (v0.2021.06.09.15.14)

**New features**

* SSH support (Warp now works the same when you SSH as it does locally!)
* Improved completions: we’ve built out new completions support that are snappier and have more intelligent suggestions for options and arguments for some of the most used commands
* Find: Pressing CMD-F now brings up a find view to search for text in the terminal

**Bug fixes**

* Text rendering was faded on certain monitors

