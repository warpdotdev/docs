# Changelog

These are our release changelogs. We try to release an update every week on Warp Wednesday!

### 2022-01-05 (v0.2022.01.03.09.07)

**New features**

- [113](https://github.com/warpdotdev/warp/issues/113) - Native undo and redo in the text editor using CMD-Z
- [107](https://github.com/warpdotdev/warp/issues/107) - Added Cmd-M to minimize the Window
- Added our open source licenses to the Warp Documentation
- Split pane focus indicator - a triangle in the top left corner of the pane in focus

**Bug fixes**

- [499](https://github.com/warpdotdev/warp/issues/499) - Ctrl-Space is now properly passed to Emacs and other terminal apps
- Copy on select setting persists across sessions and does not reset after updates

**Coming soon**

- Customizable key bindings
- Session restoration - block contents

### 2021-12-29 (v0.2021.12.27.09.04)

**New features**

- Find in block (+ other find improvements)

**Coming soon**

- Customizable key bindings
- Session restoration - block contents

### 2021-12-22 (v0.2021.12.20.09.04)

**New features**

- Windows, tabs, and panes are restored whenever you reopen Warp. Restoring block content is on its way!
- Warp now supports completions for over 300 commands and more information about existing commands by using Fig’s completion specs
- [210](https://github.com/warpdotdev/warp/issues/210) - Git aliases are now included in completions menu
- [392](https://github.com/warpdotdev/warp/issues/392) - Switch to next pane and previous pane with CMD-[ and CMD-]
- [370](https://github.com/warpdotdev/warp/issues/370) - Scrolling the Block list with PG-UP and PG-DOWN
- [514](https://github.com/warpdotdev/warp/issues/514) - Copy and paste the file directory into Warp from Finder
- When the last Block is selected, can re-focus the input editor using CMD-DOWN key
- Arrow down scrolls to bottom of last block

**Bug fixes**

- [504](https://github.com/warpdotdev/warp/issues/504) - Copying selected text to clipboard creates a new entry for each selected character
- [427](https://github.com/warpdotdev/warp/issues/427) - Needed an extra backspace to escape CTRL-r / history menu
- VIM performance improvements - we’ve made progress but would love more sample cases of slowness

**Coming soon**

- Customizable key bindings
- Session restoration - block contents
- Find in block
- Undo / redo in editor

**Updates to Mac Menu Bar (Window)**

- Zoom
- Minimize
- Tile Window to Left of Screen (Default)
- Tile Window to Right of Screen (Default)
- Move to X screen (Default)
- Enter Full Screen (Default)
- Bring All to Front

### 2021-12-15 (v0.2021.12.13.08.40)

**New features**

- Fuzzy search in ctrl-r and command palette
- When you share a link to a block, up to 5 recipients may now download Warp’s beta via the link

**Bug fixes**

- [426](https://github.com/warpdotdev/warp/issues/426) - Fix bug where opening file:// urls would not include query params like '?foo=bar'
- More prominent highlights in ctrl-r, command palette, tab completion
- Vim bug fixes and performance improvements - please let us know what else you see

**Coming soon**

- Customizable key-bindings
- Session restoration
- Improved completions coverage

### 2021-12-08 (v0.2021.12.06.19.09)

**New features**

- Added a send invite button in account section of the settings dialog.
- You can now request more invites in the invite modal.

**Bug fixes**

- Copy on select persistence bug
- [439](https://github.com/warpdotdev/warp/issues/439) - UI Bug when trying to un-share a block

**Coming soon**

- Customizable key-bindings
- Session restoration
- Improved completions coverage

### 2021-12-01 (v0.2021.11.29.18.59)

**New features**

- Added 15 extra invites for everyone!
- [077](https://github.com/warpdotdev/warp/issues/077) - Copy on select (highlighting text will automatically copy to clipboard). This can be turned off in the settings dialog.
- [049](https://github.com/warpdotdev/warp/issues/049) - CTRL-l shortcut to clear the screen

**Bug fixes**

- [138](https://github.com/warpdotdev/warp/issues/138) - Can now highlight and copy sections of a URL without it automatically opening

**Coming soon**

- Customizable key-bindings
- Session restoration
- Improved completions coverage

### 2021-11-24 (v0.2021.11.23.17.55)

**New features**

- [032](https://github.com/warpdotdev/warp/issues/032) - Background images + gradients in themes: You can now set a background image or gradient as your theme background. Warp ships with a few of these already or you can create your own via a yaml file.
- Changelog dialog
- [075](https://github.com/warpdotdev/warp/issues/075) - Emoji rendering: 😂, 😃, 🌍, 🍞, 🚗, 📞, 🎉, ❤️
- Improved settings dialog
- [237](https://github.com/warpdotdev/warp/issues/237) - Theme search

**Bug fixes**

- Properly escapes whitespace when you drag and drop files.

**Coming soon**

- Customizable key-bindings
- Session restoration
- Improved completions coverage

### 2021-11-17 (v0.2021.11.16.20.05)

**New features**

- [069](https://github.com/warpdotdev/warp/issues/069) - Drag and drop files & directories from finder

**Coming soon**

- Background images in themes
- Customizable key bindings
- Adding a changelog dialog
- Settings UI V2
- Session restoration

### 2021-11-10 (v0.2021.11.09.19.46)

**New features**

- [052](https://github.com/warpdotdev/warp/issues/052) - Autosuggestions: Warp now suggests commands as you type, similar to Fish or Gmail
- [106](https://github.com/warpdotdev/warp/issues/106) - Button to copy the app/version
- [235](https://github.com/warpdotdev/warp/issues/235) - Conda context to the prompt

**Bug fixes**

- Conda info (prompt) locking input editor
- CTRL+D now deletes forward one character
- [337](https://github.com/warpdotdev/warp/issues/337) - History now preserved across sessions
- [330](https://github.com/warpdotdev/warp/issues/330) - Enter (numpad) was inputting as CTRL+C

**Coming soon**

- Background images in themes
- Customizable key bindings
- Drag and Drop directories from finder

### 2021-11-03 (v0.2021.11.02.00.38)

**New features**

- [327](https://github.com/warpdotdev/warp/issues/327) - CJK (Chinese, Japanese, and Korean) character support
- Autocompletions for missing tar commands
- [249](https://github.com/warpdotdev/warp/issues/249) - Enforcement of minimum contrasts in grid

**Bug fixes**

- [232](https://github.com/warpdotdev/warp/issues/232) - Runaway memory usage (from font loading on initial run)
- [309](https://github.com/warpdotdev/warp/issues/309) - Directories with non-english filenames not rendering on screen
- App crashes from missing current working directory
- [242](https://github.com/warpdotdev/warp/issues/242) - Pure Prompt being inserted as a typehead into editor

**Coming soon**

- Autosuggestions preview (ghosting / text shadow) in input editor
- Session restoration
- Customizable key bindings
- Image support in themes

### 2021-10-27 (v0.2021.10.25.22.47)

**New features**

- Ability to unshare blocks in settings modal
- Link to the documentation in kebab menu (three dots in top right corner)

**Bug fixes**

- Double character entry after input editor loses focus

**Coming soon**

- [124](https://github.com/warpdotdev/warp/issues/124) - Autosuggestions preview (ghosting / text shadow) in input editor
- Supporting non-English characters within blocks
- Session restoration
- Custom keybindings

### 2021-10-20 (v0.2021.10.19.21.38)

**New features**

- [068](https://github.com/warpdotdev/warp/issues/068) - Switch theme based on OS appearance
- Toggles instead of buttons in the setttings!
- Link to Custom themes documentation in the settings

**Bug fixes**

- IME support (non-English keyboards are now better supported in input box!)
- Show a banner instead of a popup when app startup takes longer than expected
- git log (and similar commands) no longer treated as a failed block

**Coming soon**

- Gradients & images in themes
- Session restoration
- Long running commands notification
- Supporting non-English characters within blocks

### 2021-10-13 (v0.2021.10.12.19.34)

**Bug fixes**

- Shell Bootstrapping should be a lot faster
- Support 3-char color representation for hex colors in theme
- Fix crashes relating to reading history files
- Prevent block completion from stealing focus
- Fix broken click handling for showing and hiding overflow menu

**Coming soon**

- International keyboard support
- Desktop notifications for long-running commands
- Session restoration

### 2021-10-06 (v0.2021.10.05.20.07)

**Bug fixes**

- Split pane navigation when 'Left / Right Option is Meta' settings are enabled
- Crash when opening a new window

**Coming soon**

- Better support for international keyboard layouts
- Desktop notifications for long-running commands
- Session restoration

### 2021-09-29 (v0.2021.09.29.13.26)

**New features**

- Split pane. Create multiple panes in the same tab via shortcuts (cmd-e/cmd-shift-e), the command palette, or by right clicking in any pane.
- Custom themes via files.  You can now define your own theme as a yaml file in ~/.warp/themes. For more information on the file format and to see ~100 of the most popular themes already implemented in this format, see https://github.com/warpdotdev/themes. The ability to add and share themes directly within Warp is coming soon!

**Bug fixes**

- Add better messaging when Warp does not have permission to autoupdate
- Crash if a tab completion result was accepted after the cursor was moved to the beginning of the editor

**Coming soon**

- Desktop notifications for long-running commands
- Session restoration

### 2021-09-22 (v0.2021.09.21.20.54)

**New features**

- Theme picker available from the command palette

**Bug fixes**

- Occasional crash when opening a new Warp window
- Font selection dropdown didn't respect theme choice
- Issues with padding and hover detection when toggling Compact Mode on or off

**Coming soon**

- Custom themes
- Split panes
- Session restoration
- Desktop notifications for long-running blocks

### 2021-09-15 (v0.2021.09.14.21.25)

**Bug fixes**

- Crash when closing fullscreen window
- Executables in path were not appearing for completions in Bash
- Completions menu overlaps theme picker

**Coming soon**

- Custom themes
- Split pane
- Collapsed blocks
- Desktop notifications for long-running commands
- Session restoration

### 2021-09-09 (v0.2021.09.09.0.0)

**New features**

- New themes for Warp!!! (Access them via Settings on the overflow menu. We have Dracula, Solarized, & Gruvbox)
- Cmd comma opens the Settings menu

**Bug fixes**

- Fixed crash when we fail to load a font or when we scroll through fonts
- Fixed visual artifacts around windows and modals jumping
- Fixed crash that occurs when you Cmd-F while selecting an already selected text

**Coming soon**

- Split screens
- Desktop notifications for long-running commands
- Background images and transparency for themes

### 2021-08-31 (v0.2021.08.31.0.0)

**New features**

- Support emacs bindings in input box
- History up menu performs a prefix search based on input

**Bug fixes**

- Warp not rendering after executing long-running command
- Stop powerlevel10k instant prompt from hanging on bootstrap
- Changing “font-size” via ctrl-[- + 0] should stay in sync with font size in settings menu
- Bracketed paste mode bug: 0~ ~1 on every command when ssh-ing
- Crash when tab completing with multibyte characters
- Download page doesn’t render correctly on safari
- Login is broken for some users using Chrome
- Make it more prominent in onboarding that we are collecting telemetry during the beta

**Coming soon**

- Custom themes
- Split panes
- Desktop notifications for long-running commands

### 2021-08-25 (v0.2021.08.25.0.0)

**New features**

- Custom fonts
- Completions for aliases and environment variables

**Bug fixes**

- Completions loose ends, including completions for path names with spaces and if commands are separated by &&
- Function key support within running programs (such as htop)
- Editor text respects zoom level
- Regression that caused URLs to not be highlighted
- Opening a new window required Internet connection

**Coming soon**

- Custom themes
- Split panes
- Collapsed blocks
- Desktop notifications for long-running commands

### 2021-08-18 (v0.2021.08.18.0.0)

**New features**

- Re-run with sudo

**Bug fixes**

- Crash caused by pressing Cmd-K
- Completion not working when cursor is mid-line
- Re-input of multi-line commands
- [084](https://github.com/warpdotdev/warp/issues/084) - Rendering of colors correctly in diffs
- Selection showing after closing and re-opening alt-screen

**Coming soon**

- Environment variable completions and other completion loose ends
- Custom themes and fonts
- Split panes
- Collapsed blocks
- Desktop notifications for long-running commands

### 2021-08-09 (v0.2021.08.09.0.0)

**New features**

- New settings modal (accessible from the top right overflow button) to set font size, toggle between light mode and dark mode, compact mode and normal mode
- Ctrl + U/K now cuts to clipboard
- Typeahead: characters you type in a long-running command will now show up in the input box when the command completes

**Bug fixes**

- Handle arrow keys with modifiers (option and command) in CLIs and full-screen apps (Previously, users were unable to navigate with option and command keys in - Postgres CLI)
- Straightening the text baseline
- Translucent colors (e.g. for diff-so-fancy)are now correct (We now support the full range of opacity)
- Dotfile path completions + Completions improvements for more commands
- Artifacts when rendering svgs, especially on low res monitors. Overflow menu looks a lot better now!

**Coming soon**

- Environment variable completions
- Custom themes and fonts
- Collapsed blocks
- Desktop notifications for long-running commands
- Alias completions

### 2021-07-28 (v0.2021.07.28.0.0)

**New features**

- Compact Mode (see GIF below)
- Support for mouse events in Vim and other programs that can handle mouse input
- Completions for npm / yarn scripts

**Bug fixes**

- Major improvements to the consistency of completions, especially for commands that can take multiple arguments (e.g. rm -rf)
- Proper path completions for absolute paths
- Hang when PROMPT_COMMAND is set for the shell
- Context Menu not closing when clicking outside of the menu
- Crashes after executing multi-line commands and on older versions of macOS

**Coming soon**

- Further improvements to Completions
- Fish-like Autosuggestions
- Notifications for long-running commands
- Themes / Custom Colors

### 2021-07-21 (v0.2021.07.21.0.0)

**New features**

- Support for numpad enter
- More npm & yarn completions

**Bug fixes**

- Down arrow sends unrecognized escape sequence to Github CLI
- Can’t use up arrow if item in history is multiple lines
- Crash when closing a tab when there are multiple tabs
- File-only completion signatures should also show directories

**Coming soon**

- Url highlighting is rendered with a white background for a failed block
- Declutter shortcuts screen
- Crashes related to multiline input
- More work on completions
- Fish-like autosuggestions
- Notifications for long-running commands
- Compact Mode

### 2021-07-13 (v0.2021.07.13.0.0)

**New features**

- New invite system to add users to Warp. To invite new users, click the overflow menu at the top right and click 'invite users'. For now we ask that you please don't post these invites on social media!
- URLs in the terminal screen are auto-linkified
- Double clicking the title bar maximizes/minimizes the window

**Bug fixes**

- Various command palette bugs
- Find box is populated with the user's text selection
- 3 second latency when changing the prompt upon first SSHing

**Coming soon**

- Autosuggestions
- Fish support
- Desktop notifications for long-running commands that complete

### 2021-07-07 (v0.2021.07.07.0.0)

**New features**

- Command Palette for most keyboard shortcuts (Cmd-P)
- Previously, tab completion descriptions were cut off. Now we display them in a floating box
- You can now switch tabs using ctrl-tab and ctrl-shift-tab

**Bug fixes**

- Intermittent crashes with zsh sessions and switching tabs
- Always fall back to path suggestions for completions
- Various bugs related to completions

**Coming soon**

- Fish support
- Desktop notifications for long-running commands that complete
- Cmd-Click to open URLs

### 2021-06-29 (v0.2021.06.29.0.0)

**New features**

- Multiple window support
- New completions UI and in-line documentation for commands and flags
- Horizontal scrolling of input box to support long commands

**Bug fixes**

- Crash when exiting from logout or exit when there’s a background process
- Crash when bootstrapping from detecting incorrect shell name
- Various bugs related to completions

**Coming soon**

- Fish support
- Command palette
- Expanded completions UI for longer descriptions
- Notifications

### 2021-06-15 (v0.2021.06.15.19.04)

**New features**

- Mac File and Edit menus, along with Mac standard menu items (although New Window not yet working)

**Bug fixes**

- Crash when closing last window
- Cmd-f: when there are no matches, display 0/0
- Cmd-f should not scroll away if navigating to a match on the same row
- Cmd-f: render the yellow rectangle at the layer of rendering the cell
- Unable to move cursor upwards on multi-line previous command
- Warp bootstrap commands showing up in history over ssh
- Accept input via input box before terminal has bootstrapped
- New tab button should have hover and click state
- Output stops midway through session on iMac running Mojave 10.14.6
- Backspace doesn’t work while holding shift
- Clipping issue in share dialog
- Input suggestions closes if you click on the scrollbar
- Hitting up/down while input suggestions are open causes menu to move
- Paste is not working for full screen apps
- Underline does not render with Hack font

**Coming soon**

- Multiple window support
- In-line documentation for commands and flags
- Fish support

### 2021-06-09 (v0.2021.06.09.15.14)

**New features**

- SSH support (Warp now works the same when you SSH as it does locally!)
- Improved completions: we’ve built out new completions support that are snappier and have more intelligent suggestions for options and arguments for some of the most used commands.
- Find: Pressing cmd-f now brings up a find view to search for text in the terminal

**Bug fixes**

- Text rendering was faded on certain monitors

**Coming soon**

- Improved menu bars

