# Changelog

These are our release changelogs. We try to release an update every week on Thursdays!
Submit bugs and feature request on our [GitHub board!](https://github.com/warpdotdev/Warp/issues/new/choose)

### 2022.08.18 (v0.2022.08.16.10.16)

**New features**

- Launch Configurations - Save a configuration of windows, tabs, and panes to open later with `CTRL-CMD-L`
- Session Navigation - Navigate to any session in Warp with `CTRL-CMD-P`
- Added exclusive theme for users who joined Warp through a referral

**Bug fixes**

- Prompt now shows Git SHA instead of HEAD when you’re not on a branch
- Filepath completions now include current directory ('.') and parent directory ('..')
- Support `SHIFT-HOME` and `SHIFT-END` keybindings to select text to line start and end.
- Items in the Command Palette now highlight when you hover over them with your mouse
- Improved how Warp cleans up the warptmp directory for Zsh SSH sessions
- Already open dropdown menus are now properly closed when clicked
- Warp no longer crashes when dragging a window that’s running htop
- Warp no longer crashes when the find bar is open

### 2022.08.10 (v0.2022.08.08.09.21)

**New features**

- Can now Middle-click a tab to close it
- Added additional tab reordering options (Close: tab, other tabs, and tabs to the right) via the Mac Menu, the Command Palette, and a tab’s context menu (right click)

**Bug fixes**

- Added a toggle to the Mac Menu for maximizing panes
- Can now switch panes using keyboard shortcuts even when a pane is maximized
- Add support for opening file paths with RubyMine, PhpStorm, and WebStorm
- Fixed crash when highlighting links
- Fixed issue where the HISTCONTROL environment variable was ignored in bash
- Pressing `CTRL-R` to open history search no longer crashes Warp when you have multiple cursors

### 2022.08.03 (v0.2022.08.01.09.12)

**New features**

- Updated Mac menus to make Warp actions more discoverable - [101](https://github.com/warpdotdev/warp/issues/101)
- Warp now supports opening file links and urls via CMD-CLICK! - [177](https://github.com/warpdotdev/warp/issues/177)

**Bug fixes**

- Various CLI tools no longer hang e.g. Bazel and Maven
- Command Inspector hover no longer crashes with UTF-8 encoded strings
- Opening the find / search bar (`CMD-F`) now automatically selects the text
- Tab titles are no longer reset when changing panes

### 2022.07.27 (v0.2022.07.25.09.05)

**Bug fixes**

- Closing and re-opening the Command Palette now resets the selected item
- The cursor’s position is now restored after exiting the Command History Search (`CTRL-R`) menu.
- Shorthand and longhand flags are now correctly surfaced (based on the number of dashes) in tab completions
- Added voiceover support for `BACKSPACE` and `DELETE` keystrokes within the Input Editor

### 2022.07.20 (v0.2022.07.18.09.06)

**New features**

- Command Inspector - hover over any piece of a command in Warp’s Input Editor to surface documentation or press `CMD+I` to inspect at the cursor’s current location
- Improved ordering in the tab completions menu

**Bug fixes**

- Font color for links in light mode (themes) now set correctly
- Moving forward by a word no longer moves farther than expected
- Warp no longer hangs when passing an invalid file path
- Fixed issues with persisting the selected theme when “Sync with OS” is enabled and the theme picker is launched from the Command Palette (or a keyboard shortcut)
- Fixed issues with text input after clearing Blocks (`CMD-K`) while in a REPL environment.
- Fixed shortcut for select-left-by-word (`SHIFT-CMD-B`), select-right-by-word (`SHIFT-CMD-F`), select-line-to-end (`SHIFT-CTRL-E`), and select-line-to-start (`SHIFT-CTRL-A`)

### 2022.07.13 (v0.2022.07.11.09.11)

**Bug fixes**

- Improved startup time for Fish shells
- Find Bar no longer crashes on selected text
- Scrollbar now supports jumping to where you click
- Fixed a bug with the referral link for sharing Warp not loading

### 2022.07.07 (v0.2022.07.04.09.08)

**New features**

- Bookmark a Block (or multiple) for quick access via the scroll-bar
- Added a referral counter to the Settings > Account screen and the referral screen
- Added support for rendering text with a lower visual weight; enable the thin strokes option in Settings > Appearance (enabled by default for low-DPI displays)
- Togglable settings, overflow menu items, and settings pages are now accessible through the Command Palette
- CLI options are now surfaced by default without needing to type '-'
- Press SHIFT-CMD-C while in VSCode (Visual Studio Code) to open a new Warp session

**Bug fixes**

- Fixed referal links and share by email
- Fixed a hang that would sometimes occur when connecting with SSH
- Now support requesting media permissions (camera, audio, etc)
- Correctly parse Git commit SHAs in completion menus
- Improved tab completion support for command line arguments that are behind flags

### 2022.06.29 (v0.2022.06.27.09.14)

**Bug fixes**

- Cursor changes when hovering over clickable UI elements and the Input Editor
- Dim colors now render correctly

### 2022.06.27 (v0.2022.06.20.09.15)

**New features**

- Improved auto-focus behavior when closing panes by keeping track of history when navigating or clicking around panes
- Performance improvements when executing Blocks: Warp no longer flashes on every command!

**Bug fixes**

- Input Editor re-focuses after renaming a tab
- Reduced visual weight of the active tab title to improve legibility.
- Improved blending along the inside edge of rounded corners
- Global Hotkey Windows (Quake Mode) now correctly respect the active screen setting
- Completions for flag arguments now support absolute and relative file paths (when applicable)
- Git checkout <`TAB`> now also completes branches with the remote prefixed.
- Pressing Arrow-up (`UP`) when the Input Editor is non-empty opens the command history with prefix filtering
- Button to copy app version moved to main settings page

### 2022.06.17 (v0.2022.06.13.09.15)

**New features**

- Added keyboard shortcuts to reorder tabs (CTRL-SHIFT-LEFT and CTRL-SHIFT-RIGHT)

**Bug fixes**

- Warp no longer crashes on MacOS 13 (Ventura)
- Global Hotkey Window (Quake Mode) no longer overlaps Spotlight, Raycast, Alfred, and the Mac Dock
- Now correctly display the user and hostname in the Prompt after exiting an SSH session
- Fixed a memory leak on window close.

### 2022.06.08 (v0.2022.06.06.09.05)

**New features**

- Now support renaming tabs (right click on your tab title!)
- Now support enabling custom prompt from prompt context menu (right-click on prompt)
- Now support splitting panes (left and right) from the context menu (right click) and through the Command Palette
- Now support CTRL-Click as an alternative to right-clicking

**Bug fixes**

- Improved completions support for arguments nested under options (e.g. git branch -D <branch_name...>)
- Modified files are now included (in addition to commit SHAs) for `git diff`

### 2022.06.01 (v0.2022.05.30.09.10)

**New features**

- Added information about rewards to the referral screen
- Added a button that toggles regex search in the Find Bar
- Added completion support for shell functions

**Bug fixes**

- Hotfix - a regression that caused Warp to stall when using nano
- Improved kerning (font rendering) throughout the app
- Added a hyperlink (to our changelog history) in the Changelog modal
- Multiline commands that don't have any output are no longer cut off

### 2022.05.26 (v0.2022.05.23.09.07)

**New features**

- Warp can now send you desktop notifications for long-running commands and password prompts - [628](https://github.com/warpdotdev/warp/issues/628)
- Added keybinding to toggle fullscreen mode

**Bug fixes**

- Stopped prepending \ before ~ in tab titles for older versions of Bash
- Added support for CMD-G and SHIFT-CMD-G to tab between results in the Find Bar

### 2022.05.18 (v0.2022.05.16.09.01)

**New features**

- Added exclusive theme available to anyone who has referred someone to Warp. (Open Theme Picker > Warp Referral to use it)

**Bug fixes**

- Improved rendering of rounded corners throughout the app
- Fixed cell dimension computation for some fonts
- Fixed labels rendering incorrectly in the font selector dropdown in settings
- Fixed Bash remote sessions missing tab titles
- Reduced UI flickering after executing commands
- Fixed errors when sshing into remote machines which do not have xxd available
- Fixed some anti-aliased glyphs getting clipped during rasterization
- Fixed search bar stealing focus after command execution

### 2022.05.11 (v0.2022.05.09.09.06)

**New features**

- Filepath completions without needing to cd
- Support for any font (not just monospaced)

**Bug fixes**

- Tab completions (cd) with international characters are now properly escaped (edited)
- Improve rendering performance when many tabs are open (fixes non-responsiveness when searching history)
- Fixed a race condition with autoupdate a11y announcements and other a11y messaging
- Fixed a regression that would cut off the output of some long-running Blocks

### 2022.05.04 (v0.2022.05.02.09.00)

**New features**

- Added default tab titles for Bash
- Improved default tab title in Zsh
- Maximize a split pane
- Support rcfiles that check PS1 to determine if it's an interactive shell; this may explain missing aliases or commands in Warp!

**Bug fixes**

- History now correctly shows results after hitting ESC when a Block is focused
- Fixed crash when quitting AI Command Search while a command was being generated
- Global keybindings with function keys and numeric keys are now properly registered
- Warp no longer jumps up and down for single-line commands that take more than 50ms

### 2022.05.02 (v0.2022.04.25.09.59)

**New features**

- Added a Quake Mode setting that configures whether Warp should automatically hide when losing focus - [107](https://github.com/warpdotdev/warp/issues/107)7
- Added a Quake Mode setting that configures which screen to pin Warp on - [862](https://github.com/warpdotdev/warp/issues/862)
- Expanded the keybindings supported by Quake Mode / Global Hotkey Window - [856](https://github.com/warpdotdev/warp/issues/856)

**Bug fixes**

- Commands prepended with space are now stored in history if hist_ignore_space option is not set
- Now support dotfile configurations with non-English quotation marks
- Continued improving the reliability of login and auth within the app
- Improved performance for commands with large outputs
- Improved performance for long running commands
- Improved text alignment within inline banners

### 2022.04.20 (v0.2022.04.18.09.08)

**New features**

- Support logging into Warp by pasting the auth url when "Take me to Warp" fails in browser

**Bug fixes**

- Improved reliability of login and auth within the app
- Buttons within the find bar are now properly shaded for gradient themes
- Workflows with default values are now registered by Warp
- Fixed bootstrapping bug that affected Fish versions older than 3.2.0
- Fixed a memory leak that occurred when new tabs were opened or panes were split

### 2022.04.15 (v0.2022.04.11.09.09)

**Bug fixes**

- Support parsing PS1’s exit codes (Bash’s $?) and improved PS1 parsing for newer Bash versions (4.4+)
- Fixed prompt showing up as exit in Bash - [793](https://github.com/warpdotdev/warp/issues/793)
- Improved parsing of Zsh default prompts
- Opening the find bar will automatically select any existing text - [831](https://github.com/warpdotdev/warp/issues/831)

### 2022.04.08 (v0.2022.04.04.09.07)

**Bug fixes**

- Block sharing dialog now scrolls properly

### 2022.04.01 (v0.2022.04.01.01.37)

**New features**

- Warm welcome!
- A.I. Command Search

**Bug fixes**

- Warp now properly registers `SPACE` and `SHIFT` modifier keys for Global Hotkey Windows
- Page Up and Page Down keys now work correctly in vim and other fullscreen apps - [560](https://github.com/warpdotdev/warp/issues/560)
- SSH now supports bootstrapping if bash-preexec is included in a Debian VM’s system rcfiles (eg by default at Google) - [578](https://github.com/warpdotdev/warp/issues/578)
- Corrected keyboard shortcut for split pane in context menu

### 2022.03.30 (v0.2022.03.29.02.23)

**New features**

- Workflows: an easier way to share, parameterize, and execute commands - [625](https://github.com/warpdotdev/warp/issues/625)
- Quake mode / Focus Warp with a Global Hotkey - [091](https://github.com/warpdotdev/warp/issues/091)

**Bug fixes**

- Magnet, Swish and ALT-Tab window managers now work with Warp - [776](https://github.com/warpdotdev/warp/issues/776)
- SSH now handles control master connection errors - [578](https://github.com/warpdotdev/warp/issues/578)
- SSH now handles verbose mode, no longer leaks into the Input Editor as a typeahead - [578](https://github.com/warpdotdev/warp/issues/578)
- SSH now boots normally for POSIX shells that aren’t supported by Warp’s wrapper - [578](https://github.com/warpdotdev/warp/issues/578)

### 2022.03.24 (v0.2022.03.23.22.10)

**New features**

- Fish support - [190](https://github.com/warpdotdev/warp/issues/190)
- Basic screenreader support (Voiceover) - Warp is now an accessible terminal!
- Added a toggle in the settings to disable the SSH wrapper - [821](https://github.com/warpdotdev/warp/issues/821)

**Bug fixes**

- Hitting tab with a text selection shows tab completions instead of indenting
- SSH no longer hangs when /tmp is not writable for Zsh - [578](https://github.com/warpdotdev/warp/issues/578)
- SSH no longer bootstrap the shell if it’s not meant to be an interactive session (e.g. if -T or a command is passed) - [578](https://github.com/warpdotdev/warp/issues/578)
- SSH now supports Starship and Zsh's $PROMPT variable - [803](https://github.com/warpdotdev/warp/issues/803)
- Also import themes in subdirectories e.g. `~/.warp/themes/subdirectory/theme.yaml`

### 2022.03.16 (v0.2022.03.14.08.49)

**New features**

- Multi-block selections and corresponding actions - [146](https://github.com/warpdotdev/warp/issues/146)
- Case-sensitive search

**Bug fixes**

- SSH no longer returns 0~ and 1~ after executing commands for Zsh 5.0.8 or older - [578](https://github.com/warpdotdev/warp/issues/578)
- SSH now supports LocalCommand / RemoteCommand - [578](https://github.com/warpdotdev/warp/issues/578)
- SSH over Zsh no longer depends on configuring locales on the remote machine - [578](https://github.com/warpdotdev/warp/issues/578)
- SSH sources /etc/bash.bashrc which is an extra rcfile in Debian and other Linux distributions - [578](https://github.com/warpdotdev/warp/issues/578)
- Improved completions stability when there are multiple panes on the same remote machine
- Vim and other alt-screen apps properly expand to take up the full window - [552](https://github.com/warpdotdev/warp/issues/552)
- Clicking into Warp from other foreground window focuses the clicked pane - [739](https://github.com/warpdotdev/warp/issues/739)
- Warp now respects ignore-space history options for Zsh and Bash - [044](https://github.com/warpdotdev/warp/issues/044)
- Warp now creates a ~/.warp folder to persist custom keybindings - [801](https://github.com/warpdotdev/warp/issues/801)

### 2022.03.09 (v0.2022.03.07.08.51)

**Bug fixes**

- Added missing actions to Command Palette
- Option is meta is now in the settings menu
- Fix for SSH hanging when Zsh is the remote login shell
- Fix for SSH with Zsh that would break with certain rcfiles because of incorrectly set ZDOTDIR

### 2022.03.02 (v0.2022.02.28.08.45)

**New features**

- Can now edit the keybindings for arrow navigation (Up/Down/Left/Right)
- Can now edit the keybindings for activating specific tabs (by number CMD-1, CMD-2, …)

**Bug fixes**

- Crash in theme chooser
- Fix for tab completion sometimes deleting characters

### 2022.02.23 (v0.2022.02.21.08.55)

**New features**

- Zsh support over SSH
- Partially complete autosuggestion (by word) using CTRL-RIGHT and ALT-RIGHT - [488](https://github.com/warpdotdev/warp/issues/488)
- Added a Copy URL menu item after right-clicking a URL - [154](https://github.com/warpdotdev/warp/issues/154)
- Indicator for conflicting keybindings in keyboard customization UI

**Bug fixes**

- Able to fill-in longest common prefix after filtering tab completions - [618](https://github.com/warpdotdev/warp/issues/618)
- Block completion causes Input Editor to steal focus from find bar - [452](https://github.com/warpdotdev/warp/issues/452)
- UP-arrow in history menu sometimes scrolls more than one item
- CMD-F opens a no-op find bar in alt screen

### 2022.02.16 (v0.2022.02.14.08.44)

**New features**

- Customizable key bindings (accessible via the settings menu) - [579](https://github.com/warpdotdev/warp/issues/579)
- Users can opt in to use their shell’s prompt rather than Warp’s default (select the Honor PS1 toggle under the settings menu) - [580](https://github.com/warpdotdev/warp/issues/580)
- Added a timestamp showing Block runtime duration; hover to see start and end date + time - [178](https://github.com/warpdotdev/warp/issues/178)
- CTRL-F now accepts autosuggestions - [403](https://github.com/warpdotdev/warp/issues/403)
- CTRL-E and CMD-RIGHT accept autosuggestions when at the end of the buffer - [403](https://github.com/warpdotdev/warp/issues/403)
- Allow input height to expand to half the pane height - [621](https://github.com/warpdotdev/warp/issues/621)

**Bug fixes**

- Arrow key presses now (up and down now) cycle themes in the theme picker - [294](https://github.com/warpdotdev/warp/issues/294)
- ESC keypress now exits the theme picker
- CMD-Down when on most recent block to focus input now clears Block selection
- Fixed a bug where resizing a pane while a command was running made it impossible to scroll to the bottom of the pane
- Fixed a bug where resizing a pane could cause Warp to show a blank screen
- Parentheses, quotes, and brackets now also auto-close after typing an alphanumeric character
- Remapped multi-cursor key bindings to CTRL-SHIFT-UP and CTRL-SHIFT-DOWN - [374](https://github.com/warpdotdev/warp/issues/374)
- Restored OPT-CMD-UP and OPT-CMD-DOWN for switching panes up and down - [730](https://github.com/warpdotdev/warp/issues/730) 

### 2022.01.26 (v0.2022.01.31.09.03)

**New features**

- Multi-cursor keybindings for adding cursors above and below current selections with OPT-CMD-UP/DOWN - [374](https://github.com/warpdotdev/warp/issues/374)

**Bug fixes**

- Double clicking the top of the window maximizes the app - [097](https://github.com/warpdotdev/warp/issues/097)
- Icon, cursor and selection contrast fixes
- Scrolling performance improvements with bg image themes
- Changelog visual glitch
- Resize bug - losing scroll position when viewing blocks with long output

### 2022.01.26 (v0.2022.01.24.08.55)

**New features**

- Auto-close symbols (parentheses, quotes, and brackets) like VSCode

**Bug fixes**

- Block sharing link no longer cuts off - [660](https://github.com/warpdotdev/warp/issues/660)
- Right clicking a Block now focuses that Block
- Mouse dragging in vim
- Restoring history bug on session restore
- Automatically focus the last active window on session restore

### 2022.01.19 (v0.2022.01.17.08.48)

**New features**

- Restore block contents
- The longest common prefix in the completions menu auto-fills the Input Editor - [479](https://github.com/warpdotdev/warp/issues/479)
- Add description for paths in completion results - [103](https://github.com/warpdotdev/warp/issues/103)
- Can right click the prompt and copy: git branch, prompt, cwd - [346](https://github.com/warpdotdev/warp/issues/346)

**Bug fixes**

- Fixed bug where venv was inserted into input editor - [599](https://github.com/warpdotdev/warp/issues/599)
- Improved url detection

### 2022.01.12 (v0.2022.01.10.17.24)

**New features**

- Added a Changelog page to our documentation

**Bug fixes**

- Double clicking text in a url now highlights the word instead of the whole url - [508](https://github.com/warpdotdev/warp/issues/508)
- Double clicking a string with underscores now selects the whole string and not just the subword
- Selection updates correctly when a block hit its max line length
- Can now also close the Command Palette using CMD-P - [184](https://github.com/warpdotdev/warp/issues/184)
- Moved check for update button to settings dialog - [070](https://github.com/warpdotdev/warp/issues/070)
- Fixes tabs not opening in new windows when autoupdate is pending
- Fix regression with input box not being focused on app relaunch

### 2022.01.05 (v0.2022.01.03.09.07)

**New features**

- Native undo and redo in the text editor using CMD-Z - [113](https://github.com/warpdotdev/warp/issues/113)
- Added CMD-M to minimize the Window - [107](https://github.com/warpdotdev/warp/issues/107)
- Added our open source licenses to the Warp Documentation
- Split pane focus indicator - a triangle in the top left corner of the pane in focus

**Bug fixes**

- CTRL-SPACE is now properly passed to Emacs and other terminal apps - [499](https://github.com/warpdotdev/warp/issues/499)
- Copy on select setting persists across sessions and does not reset after updates

### 2021.12.29 (v0.2021.12.27.09.04)

**New features**

- Find in block (+ other find improvements)

### 2021.12.22 (v0.2021.12.20.09.04)

**New features**

- Windows, tabs, and panes are restored whenever you reopen Warp. Restoring block content is on its way!
- Warp now supports completions for over 300 commands and more information about existing commands by using Fig’s completion specs
- Git aliases are now included in completions menu - [210](https://github.com/warpdotdev/warp/issues/210)
- Switch to next pane and previous pane with CMD-[ and CMD-] - [392](https://github.com/warpdotdev/warp/issues/392)
- Scrolling the Block list with PG-UP and PG-DOWN - [370](https://github.com/warpdotdev/warp/issues/370)
- Copy and paste the file directory into Warp from Finder - [514](https://github.com/warpdotdev/warp/issues/514)
- When the last Block is selected, can re-focus the input editor using CMD-DOWN key
- Arrow down scrolls to bottom of last block

**Bug fixes**

- Copying selected text to clipboard creates a new entry for each selected character - [504](https://github.com/warpdotdev/warp/issues/504)
- Needed an extra backspace to escape CTRL-R / history menu - [427](https://github.com/warpdotdev/warp/issues/427)
- VIM performance improvements - we’ve made progress but would love more sample cases of slowness

**Updates to Mac Menu Bar (Window)**

- Zoom
- Minimize
- Tile Window to Left of Screen (Default)
- Tile Window to Right of Screen (Default)
- Move to X screen (Default)
- Enter Full Screen (Default)
- Bring All to Front

### 2021.12.15 (v0.2021.12.13.08.40)

**New features**

- Fuzzy search in CTRL-R and Command Palette
- When you share a link to a block, up to 5 recipients may now download Warp’s beta via the link

**Bug fixes**

- Fix bug where opening file:// urls would not include query params like '?foo=bar' - [426](https://github.com/warpdotdev/warp/issues/426)
- More prominent highlights in CTRL-R, Command Palette, tab completion
- Vim bug fixes and performance improvements - please let us know what else you see

### 2021.12.08 (v0.2021.12.06.19.09)

**New features**

- Added a send invite button in account section of the settings dialog
- You can now request more invites in the invite modal

**Bug fixes**

- Copy on select persistence bug
- UI Bug when trying to un-share a block - [439](https://github.com/warpdotdev/warp/issues/439)

### 2021.12.01 (v0.2021.11.29.18.59)

**New features**

- Added 15 extra invites for everyone!
- Copy on select (highlighting text will automatically copy to clipboard). This can be turned off in the settings dialog - [077](https://github.com/warpdotdev/warp/issues/077)
- CTRL-L shortcut to clear the screen - [049](https://github.com/warpdotdev/warp/issues/049)

**Bug fixes**

- Can now highlight and copy sections of a URL without it automatically opening - [138](https://github.com/warpdotdev/warp/issues/138)

### 2021.11.24 (v0.2021.11.23.17.55)

**New features**

- Background images + gradients in themes: You can now set a background image or gradient as your theme background. Warp ships with a few of these already or you can create your own via a yaml file. - [032](https://github.com/warpdotdev/warp/issues/032)
- Changelog dialog
- Emoji rendering: 😂, 😃, 🌍, 🍞, 🚗, 📞, 🎉, ❤️ - [075](https://github.com/warpdotdev/warp/issues/075)
- Improved settings dialog
- Theme search - [237](https://github.com/warpdotdev/warp/issues/237) 

**Bug fixes**

- Properly escapes whitespace when you drag and drop files

### 2021.11.17 (v0.2021.11.16.20.05)

**New features**

- Drag and drop files & directories from finder - [069](https://github.com/warpdotdev/warp/issues/069)

### 2021.11.10 (v0.2021.11.09.19.46)

**New features**

- Autosuggestions: Warp now suggests commands as you type, similar to Fish or Gmail - [052](https://github.com/warpdotdev/warp/issues/052)
- Button to copy the app/version - [106](https://github.com/warpdotdev/warp/issues/106)
- Conda context to the prompt - [235](https://github.com/warpdotdev/warp/issues/235)

**Bug fixes**

- Conda info (prompt) locking input editor
- CTRL-D now deletes forward one character
- History now preserved across sessions - [337](https://github.com/warpdotdev/warp/issues/337)
- Enter (numpad) was inputting as CTRL-C - [330](https://github.com/warpdotdev/warp/issues/330)

### 2021.11.03 (v0.2021.11.02.00.38)

**New features**

- CJK (Chinese, Japanese, and Korean) character support - [327](https://github.com/warpdotdev/warp/issues/327)
- Autocompletions for missing tar commands
- Enforcement of minimum contrasts in grid - [249](https://github.com/warpdotdev/warp/issues/249)

**Bug fixes**

- Runaway memory usage (from font loading on initial run) - [232](https://github.com/warpdotdev/warp/issues/232)
- Directories with non-english filenames not rendering on screen - [309](https://github.com/warpdotdev/warp/issues/309)
- App crashes from missing current working directory
- Pure Prompt being inserted as a typehead into editor - [242](https://github.com/warpdotdev/warp/issues/242)

### 2021.10.27 (v0.2021.10.25.22.47)

**New features**

- Ability to unshare blocks in settings modal
- Link to the documentation in kebab menu (three dots in top right corner)

**Bug fixes**

- Double character entry after input editor loses focus

### 2021.10.20 (v0.2021.10.19.21.38)

**New features**

- Switch theme based on OS appearance - [068](https://github.com/warpdotdev/warp/issues/068)
- Toggles instead of buttons in the setttings!
- Link to Custom themes documentation in the settings

**Bug fixes**

- IME support (non-English keyboards are now better supported in input box!)
- Show a banner instead of a popup when app startup takes longer than expected
- git log (and similar commands) no longer treated as a failed block

### 2021.10.13 (v0.2021.10.12.19.34)

**Bug fixes**

- Shell Bootstrapping should be a lot faster
- Support 3-char color representation for hex colors in theme
- Fix crashes relating to reading history files
- Prevent block completion from stealing focus
- Fix broken click handling for showing and hiding overflow menu

### 2021.10.06 (v0.2021.10.05.20.07)

**Bug fixes**

- Split pane navigation when 'Left / Right Option is Meta' settings are enabled
- Crash when opening a new window

### 2021.09.29 (v0.2021.09.29.13.26)

**New features**

- Split panes: create multiple panes in the same tab via shortcuts (CMD-E/SHIFT-CMD-E), the Command Palette, or by right clicking in any pane.
- Custom themes via files.  You can now define your own theme as a yaml file in ~/.warp/themes. For more information on the file format and to see ~100 of the most popular themes already implemented in this format, see https://github.com/warpdotdev/themes. The ability to add and share themes directly within Warp is coming soon!

**Bug fixes**

- Add better messaging when Warp does not have permission to autoupdate
- Crash if a tab completion result was accepted after the cursor was moved to the beginning of the editor

### 2021.09.22 (v0.2021.09.21.20.54)

**New features**

- Theme picker available from the Command Palette

**Bug fixes**

- Occasional crash when opening a new Warp window
- Font selection dropdown didn't respect theme choice
- Issues with padding and hover detection when toggling Compact Mode on or off

### 2021.09.15 (v0.2021.09.14.21.25)

**Bug fixes**

- Crash when closing full-screen window
- Executables in path were not appearing for completions in Bash
- Completions menu overlaps theme picker

### 2021.09.09 (v0.2021.09.09.0.0)

**New features**

- New themes for Warp!!! (Access them via Settings on the overflow menu. We have Dracula, Solarized, & Gruvbox)
- CMD-, opens the Settings menu

**Bug fixes**

- Fixed crash when we fail to load a font or when we scroll through fonts
- Fixed visual artifacts around windows and modals jumping
- Fixed crash that occurs when you CMD-F while selecting an already selected text

### 2021.08.31 (v0.2021.08.31.0.0)

**New features**

- Support emacs bindings in input box
- History up menu performs a prefix search based on input

**Bug fixes**

- Warp not rendering after executing long-running command
- Stop powerlevel10k instant prompt from hanging on bootstrap
- Changing “font-size” via CTRL-- and CTRL-0 should stay in sync with font size in settings menu
- Bracketed paste mode bug: 0~ ~1 on every command when ssh-ing
- Crash when tab completing with multibyte characters
- Download page doesn’t render correctly on safari
- Login is broken for some users using Chrome
- Make it more prominent in onboarding that we are collecting telemetry during the beta

### 2021.08.25 (v0.2021.08.25.0.0)

**New features**

- Custom fonts
- Completions for aliases and environment variables

**Bug fixes**

- Completions loose ends, including completions for path names with spaces and if commands are separated by &&
- Function key support within running programs (such as htop)
- Editor text respects zoom level
- Regression that caused URLs to not be highlighted
- Opening a new window required Internet connection

### 2021.08.18 (v0.2021.08.18.0.0)

**New features**

- Re-run with sudo

**Bug fixes**

- Crash caused by pressing CMD-K
- Completion not working when cursor is mid-line
- Re-input of multi-line commands
- [084](https://github.com/warpdotdev/warp/issues/084) - Rendering of colors correctly in diffs
- Selection showing after closing and re-opening alt-screen

### 2021.08.09 (v0.2021.08.09.0.0)

**New features**

- New settings modal (accessible from the top right overflow button) to set font size, toggle between light mode and dark mode, compact mode and normal mode
- CTRL-U and CTRL-K now cut to clipboard
- Typeahead: characters you type in a long-running command will now show up in the input box when the command completes

**Bug fixes**

- Handle arrow keys with modifiers (option and command) in CLIs and full-screen apps (Previously, users were unable to navigate with option and command keys in - Postgres CLI)
- Straightening the text baseline
- Translucent colors (e.g. for diff-so-fancy) are now correct (We now support the full range of opacity)
- Dotfile path completions + Completions improvements for more commands
- Artifacts when rendering svgs, especially on low res monitors. Overflow menu looks a lot better now!

### 2021.07.28 (v0.2021.07.28.0.0)

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

### 2021.07.21 (v0.2021.07.21.0.0)

**New features**

- Support for numpad ENTER
- More npm & yarn completions

**Bug fixes**

- Down arrow sends unrecognized escape sequence to Github CLI
- Can’t use UP arrow if item in history is multiple lines
- Crash when closing a tab when there are multiple tabs
- File-only completion signatures should also show directories

### 2021.07.13 (v0.2021.07.13.0.0)

**New features**

- New invite system to add users to Warp. To invite new users, click the overflow menu at the top right and click 'invite users'. For now we ask that you please don't post these invites on social media!
- URLs in the terminal screen are auto-linkified
- Double clicking the title bar maximizes/minimizes the window

**Bug fixes**

- Various Command Palette bugs
- Find box is populated with the user's text selection
- 3 second latency when changing the prompt upon first SSHing

### 2021.07.07 (v0.2021.07.07.0.0)

**New features**

- Command Palette for most keyboard shortcuts (CMD-P)
- Previously, tab completion descriptions were cut off. Now we display them in a floating box
- You can now switch tabs using CTRL-TAB and CTRL-SHIFT-TAB

**Bug fixes**

- Intermittent crashes with Zsh sessions and switching tabs
- Always fall back to path suggestions for completions
- Various bugs related to completions

### 2021.06.29 (v0.2021.06.29.0.0)

**New features**

- Multiple window support
- New completions UI and in-line documentation for commands and flags
- Horizontal scrolling of input box to support long commands

**Bug fixes**

- Crash when exiting from logout or exit when there’s a background process
- Crash when bootstrapping from detecting incorrect shell name
- Various bugs related to completions

### 2021.06.15 (v0.2021.06.15.19.04)

**New features**

- Mac File and Edit menus, along with Mac standard menu items (although New Window not yet working)

**Bug fixes**

- Crash when closing last window
- CMD-F: when there are no matches, display 0/0
- CMD-F should not scroll away if navigating to a match on the same row
- CMD-F: render the yellow rectangle at the layer of rendering the cell
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

### 2021.06.09 (v0.2021.06.09.15.14)

**New features**

- SSH support (Warp now works the same when you SSH as it does locally!)
- Improved completions: we’ve built out new completions support that are snappier and have more intelligent suggestions for options and arguments for some of the most used commands
- Find: Pressing CMD-F now brings up a find view to search for text in the terminal

**Bug fixes**

- Text rendering was faded on certain monitors
