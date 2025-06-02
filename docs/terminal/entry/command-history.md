---
description: Command History helps you quickly find previously run commands.
---

# Command History

## What is it

While running, Warp isolates the history of each shell session e.g. if you have two Split Panes open, commands created in one pane do not populate the history of the other. Warp combines the history upon closing.

Command History also provides rich information like exit code, directory, thread, time to finish running, last run, etc.

<figure><img src="../../.gitbook/assets/command-history-rich.png" alt=""><figcaption><p>Command History rich information</p></figcaption></figure>

## How to access it

* Hitting `UP` in the [Input Editor](https://github.com/warpdotdev/docs/blob/main/features/entry/editor/README.md) brings up your history and performs a prefix search based on input.
* Pressing `CTRL-R` opens the [Command Search](broken-reference) panel and initiates a search of your Command History. To navigate the Command Search panel:
  * Start typing and Warp will automatically filter using fuzzy search. Warp bolds matching text when filtering with fuzzy search.

## How it works

{% embed url="https://www.loom.com/share/8119beca8d794b06859c5dea1b1377bb?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" %}
Command History Demo
{% endembed %}
