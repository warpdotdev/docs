# Session Restoration

When Warp opens, it restores your session history, specifically windows, tabs, panes, and also the last few Blocks in each pane.

![](../.gitbook/assets/sessions-block\_restoration.gif)

Warp saves data to a sqlite database on your computer. You can open the database directly and inspect its full contents like so:

```
sqlite3 "$HOME/Library/Application Support/dev.warp.Warp-Stable/warp.sqlite"
```

Press `CMD-K` for Clear Lines (also in the Mac menu under Edit), to clear the database, which deletes the Blocks in the focused pane. You can also clear the database by deleting the sqlite file. Note that this might interfere with the running session’s ability to save content.

Toggle Block content restoration from the Settings dialog under the Features section (`Restore windows, tabs, and panes on startup`). Toggling it off will not clear the sqlite databse; however, Warp will stop recording new output.
