# Session Restoration

## What is it

The Session Restoration feature enables Warp to restore the last few Blocks of your your session history, specifically windows, tabs, panes, along with the last few Blocks in each pane.

## How to access it

1. Enable Session Restoration by going to `Settings > Features`, then toggle `Restore windows, tabs, and panes on startup`. 

_Note:_ Toggling off the feature will not [clear the sqlite database](../features/session-restoration.md#session-restoration-data); however, Warp will stop recording new output.

## How it works

![Session Restoration Demo](../.gitbook/assets/sessions-block\_restoration.gif)

#### Session Restoration Database

Warp saves data to a sqlite database on your computer. You can open the database directly and inspect it's full contents like so:

```sh
sqlite3 "$HOME/Library/Application Support/dev.warp.Warp-Stable/warp.sqlite"
```
Once in the database, clear the lines with `CMD-K`, to deleted the Blocks in the focused pane. You can also clear the database by deleting the sqlite file. _Note:_ This interferes with the running session’s ability to save content and may require you restart Warp.
