# Command History

## What is it

While running, Warp isolates the history of each shell session e.g. if you have two Split Panes open, commands created in one pane do not populate the history of the other. Warp combines the history upon closing.

## How to access it

* Hitting `↑` (UP) in the [Input Editor](editor/) brings up your history and performs a prefix search based on input.
* Pressing `CTRL-R` opens the Command History Menu and initiates a search of your command history. To navigate the Command History Menu:
  * Use the `UP` `↑` and `DOWN` `↓` arrow keys or the mouse to scroll through your command history.
  * Start typing and Warp will automatically filter using fuzzy search. Warp bolds matching text when filtering with fuzzy search.

## How it works

{% embed url="https://www.loom.com/share/8119beca8d794b06859c5dea1b1377bb?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" %}
Command History Demo
{% endembed %}
