# Command Search

## What is it

Command Search panel allows you to search across Command History, Workflows, Notebooks (**Coming Soon**), and A.I. Command Suggestions all at once. Warp supports fuzzy search and tries to rank more relevant search queries.

## How to use it

* Press `CTRL-R` to open the Command Search Panel. You’ll be greeted with a landing page, where you can click through different filters to get started.

![Command Search Panel](../../.gitbook/assets/command-search.png)

* Type into the input box what your search query is. The results will be a mix of command history, saved workflows, and A.I. Command Suggestions.
  * <img src="../../.gitbook/assets/workflow.png" alt="curly brackets" data-size="line"> Curly Brackets icon signifies that the result is a [Workflow](yaml-workflows.md).
  * <img src="../../.gitbook/assets/history.png" alt="rewind time clock" data-size="line"> Rewind Time Clock icon signifies that the result is a [Command History](command-history.md).
  * <img src="../../.gitbook/assets/notebook.png" alt="earmarked page" data-size="line"> Earmarked Page icon signifies that the result is a Notebook (**Coming Soon**).
  * <img src="../../.gitbook/assets/ai-sparkle.png" alt="sparkle" data-size="line"> Sparkle icon signifies piping that search query into [A.I. Command Suggestions ](../warp-ai/ai-command-search.md)
* Activate a specific filter, by prepending your search term with:
  * `workflows:` will activate the workflows filter. You can also use the shortcuts `w:` or `W+TAB`.
  * `history:` will activate the history filter. You can also use the shortcuts `h:` or `H+TAB`.
  * `#:` will activate the A.I. Command Suggestions  filter. Once the filter is activated, it will be bolded and italicized.
* Once the result shows up, press ENTER to input the command directly into Warp's Input Editor. For history results, `CMD-ENTER` will directly execute the command.
* You can also expand the menu horizontally with the mouse by dragging it on the right edge.

## How it works

{% embed url="https://www.loom.com/share/21a6f58a33754ee7913edbff6d33d8d1?hideEmbedTopBar=true&hide_owner=true&hide_share=true&hide_title=true" %}
Command Search Demo
{% endembed %}
