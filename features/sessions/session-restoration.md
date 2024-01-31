# Session Restoration

## What is it

The Session Restoration feature enables Warp to restore your session history, specifically windows, tabs, and panes, along with the last few Blocks in each pane. This allows you to quickly pick up where you left off in your previous terminal session.

## How to access it

* Session Restoration comes enabled by default in Warp.
* You can disable Session Restoration by going to `Settings > Features`, then toggle off `Restore windows, tabs, and panes on startup`. _Note:_ Toggling off the feature will not [clear the SQLite database](session-restoration.md#session-restoration-data); however, Warp will stop recording new output.

## How it works

![Session Restoration Demo](../../.gitbook/assets/sessions-block\_restoration.gif)

#### Session Restoration database

Warp saves the data from your previous session's windows, tabs, and panes to a SQLite database on your computer, and every time you quit the app, this data is overwritten by your latest session. You can open the database directly and inspect its full contents like so:

{% tabs %}
{% tab title="macOS" %}
```
sqlite3 "$HOME/Library/Application Support/dev.warp.Warp-Stable/warp.sqlite"
```
{% endtab %}

{% tab title="Linux" %}
```
sqlite3 "${XDG_STATE_HOME:-$HOME/.local/state}/warp/warp.sqlite"
```
{% endtab %}
{% endtabs %}

**How to clear the database**

Sometimes, you may want to prevent a sensitive Block from being saved on your computer, or you may want to clear blocks from a machine entirely.

There are two ways to do this.

* Clear the blocks from your running Warp session with `CMD-K`.
* Delete the SQLite file entirely via:

{% tabs %}
{% tab title="macOS" %}
```
rm "$HOME/Library/Application Support/dev.warp.Warp-Stable/warp.sqlite"
```
{% endtab %}

{% tab title="Linux" %}
```
rm "${XDG_STATE_HOME:-$HOME/.local/state}/warp/warp.sqlite"
```
{% endtab %}
{% endtabs %}


_Note:_ This interferes with the running session's ability to save content and may require you to restart Warp.
