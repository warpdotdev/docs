# Session Management and Restoration

When Warp opens, it restores your session history, specifically windows, tabs, panes, and also the last few Blocks in each pane.

![](../.gitbook/assets/sessions-block\_restoration.gif)

Warp saves data to a sqlite database on your computer. You can open the database directly and inspect its full contents like so:

```
sqlite3 "$HOME/Library/Application Support/dev.warp.Warp-Stable/warp.sqlite"
```

To clear the database, you can press `CMD-K` for Clear Lines (also in the Mac menu under Edit), which deletes the Blocks in the focused pane. You can also manually clear the database by entirely deleting the sqlite file but note that this could interfere with a running app’s ability to save content.

You can toggle Block content restoration from the Settings dialog under the Features section. Toggling it off does not delete what is already in sqlite. Warp, however, stops recording new output.
