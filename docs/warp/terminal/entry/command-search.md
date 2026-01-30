---
description: >-
  The Command Search panel allows you to search across Command History,
  Workflows, Environment Variables, Notebooks, Prompts, and Agent Mode history
  simultaneously. Warp supports fuzzy search and tries
---

# Command Search

![Command Search Panel](../../.gitbook/assets/command-search-panel.png)

{% hint style="info" %}
Tailor your Command Search experience by toggling off "Show Global Workflows" in `Settings > Features`. When disabled, your search will exclusively encompass YAML and Warp Drive Workflows.
{% endhint %}

## Quick Start

1. Press `CTRL-R` to open the Command Search Panel
2. Type your search query in the input box
3. Press `ENTER` to input the selected command into Warp's Input Editor

## Search Filters

You can filter your search results by prepending your search term with any of the following:

<table><thead><tr><th width="215.78436279296875">Filter</th><th>Shortcuts</th></tr></thead><tbody><tr><td>Command History</td><td><code>history:</code>, <code>h:</code>, or <code>H-TAB</code></td></tr><tr><td>Prompts</td><td><code>prompts:</code>, <code>p:</code>, or <code>P-TAB</code></td></tr><tr><td>Agent Mode History</td><td><code>ai_history:</code>, <code>a:</code>, or <code>A-TAB</code></td></tr><tr><td>Workflows</td><td><code>workflows:</code>, <code>w:</code>, or <code>W-TAB</code></td></tr><tr><td>Notebooks</td><td><code>notebooks:</code>, <code>n:</code>, or <code>N-TAB</code></td></tr><tr><td>Environment Variables</td><td><code>env_vars:</code>, <code>e:</code>, or <code>E-TAB</code></td></tr><tr><td>Generate</td><td><code>#:</code></td></tr></tbody></table>

{% hint style="info" %}
When a filter is activated, it will be bolded and italicized in the search panel.
{% endhint %}

## Additional Features

* You can expand the menu horizontally by dragging the right edge
* The panel supports fuzzy search and ranks results by relevance

## How it works

{% embed url="https://www.loom.com/share/21a6f58a33754ee7913edbff6d33d8d1?hideEmbedTopBar=true&hide_owner=true&hide_share=true&hide_title=true" %}
Command Search Demo
{% endembed %}
