# Synchronized Inputs

## What it is

Synchronized Inputs allows you to sync your commands from one session to multiple similar panes as you’re typing, so you can easily run the same command in multiple sessions at the same time.

## How it works

There are two modes available to scope how input is synchronized and one to stop any synchronization:

* Synchronize All Panes in All Tabs
* Synchronize All Panes in Current Tab (`OPT-CMD-I`)
* Stop Synchronizing Any Panes (`OPT-CMD-I`)

When inputs are synchronized, you can start typing in one input editor and that same input will be entered into all of the input editors for all panes in your current tab or all tabs, depending on the scope you selected.

If you are working in an alternative editor mode (like vim), synchronized inputs will only apply to all tabs with that same editor type running.

When you get done, you can select “Stop Synchronizing Any Panes” or use `OPT-CMD-I` to end synchronization.

## How to access it

There are three ways to access controls to synchronize inputs:&#x20;

* Command Palette in Warp: Search for “synchronize”&#x20;
* Mac menus for the Warp app: Edit > Synchronize Input&#x20;
* Keyboard shortcuts: `OPT-CMD-I` to sync / unsync all panes in your current tab

### Synchronized inputs vs. broadcast input

Synchronized inputs in Warp works similarly to “broadcast input” settings in other terminals, but there are some differences.

With Warp’s synchronized inputs, whatever command you enter in one session will sync to the other sessions in its entirety. Whereas, "broadcast input" typically allows you to "broadcast" individual keystrokes, which may be more suitable for editing parts of commands.\
