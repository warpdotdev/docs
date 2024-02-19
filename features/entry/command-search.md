---
description: >-
  The Command Search panel allows you to search across Command History,
  Workflows, Notebooks, and Warp AI all at once. Warp supports fuzzy search and
  tries to rank more relevant results.
---

# Command Search

{% hint style="info" %}
Tailor your [Command Search](command-search.md) experience by toggling off "Show Global Workflows" in `Settings > Features`. When disabled, your search will exclusively encompass YAML and Warp Drive Workflows.
{% endhint %}

## How to use it

* Press `CTRL-R` to open the Command Search Panel. You’ll be greeted with a landing page, where you can click through different filters to get started.

![Command Search Panel](../../.gitbook/assets/command-search.png)

* Type into the input box what your search query is. The results will be a mix of command history, saved workflows, and AI Command Suggestions.
  * $\_ Dollar Sign-Underscore signifies that the result is a [Workflow](yaml-workflows.md).
  * <img src="../../.gitbook/assets/history.png" alt="rewind time clock" data-size="line">  Rewind Time Clock icon signifies that the result is a [Command History](command-history.md).
  * <img src="../../.gitbook/assets/notebook.png" alt="earmarked page" data-size="line"> Earmarked Page icon signifies that the result is a [Notebook](../warp-drive/notebooks.md).
  * ⚡ Lightning Bolt icon signifies piping that search query into [AI Command Suggestions](../warp-ai/ai-command-suggestions.md).
* Activate a specific filter, by prepending your search term with:
  * `workflows:` will activate the workflow filter. You can also use the shortcuts `w:` or `W+TAB`.
  * `history:` will activate the history filter. You can also use the shortcuts `h:` or `H+TAB`.
  * `#:` will activate the AI Command Suggestions filter. Once the filter is activated, it will be bolded and italicized.
* Once the result shows up, press `ENTER` to input the command directly into Warp's Input Editor.
* You can also expand the menu horizontally with the mouse by dragging it on the right edge.

## How it works

{% embed url="https://www.loom.com/share/21a6f58a33754ee7913edbff6d33d8d1?hideEmbedTopBar=true&hide_owner=true&hide_share=true&hide_title=true" %}
Command Search Demo
{% endembed %}
