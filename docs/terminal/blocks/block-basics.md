---
description: The basics of creating, selecting, and navigating between Blocks.
---

# Block Basics

## The Basics

* Blocks group your command and command output
* The Input Editor can pin to the bottom, pin to the top, or start at the top.
* Blocks grow from the bottom to the top.
* Blocks are color-coded. Blocks that quit with a non-zero exit code have a red background and red sidebar.

{% hint style="info" %}
Try it yourself!\
Type `xyz` (or some other command that doesn’t exist) and hit `ENTER`
{% endhint %}

## Create A Block

1. Execute a command (type `ls` and hit `ENTER`) in the Input Editor at the bottom of the screen.
2. Your command and output are grouped into a Block.
3. Try executing a different command (type `echo hello` and hit `ENTER`).
4. Warp adds your newly created Block to the bottom (directly above the input editor).

{% embed url="https://www.loom.com/share/4b435c78344d4dc0bb92af5d1da5e219?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" %}
Create a Block
{% endembed %}

## Select a Single Block

{% tabs %}
{% tab title="macOS" %}
* Using your mouse: click on a Block.
* Or using your keyboard: hit `CMD-UP` (or `CMD-DOWN` if input as pinned up top) to select the most recently executed Block and use the `UP ↑` and `DOWN ↓` arrow keys to navigate to the desired Block.
* For long Blocks:
  * You can click "Jump to the bottom of this block".
  * You can press `SHIFT-CMD-UP`/`SHIFT-CMD-DOWN` to Scroll to the top/bottom of the selected block.
  * From the [Command Palette](broken-reference), you can also "Scroll to the top/bottom of selected block".
{% endtab %}

{% tab title="Windows" %}
* Using your mouse: Click on a Block.
* Or using your keyboard: hit `CTRL-UP` (or `CTRL-DOWN` if input as pinned up top) to select the most recently executed Block and use the `UP ↑` and `DOWN ↓` arrow keys to navigate to the desired Block.
* For long Blocks:
  * You can click "Jump to the bottom of this block".
  * You can press `CTRL-SHIFT-UP`/`CTRL-SHIFT-DOWN` to Scroll to the top/bottom of the selected block.
  * From the [Command Palette](broken-reference), you can also "Scroll to the top/bottom of selected block".
{% endtab %}

{% tab title="Linux" %}
* Using your mouse: Click on a Block.
* Or using your keyboard: hit `CTRL-UP` (or `CTRL-DOWN` if input as pinned up top) to select the most recently executed Block and use the `UP ↑` and `DOWN ↓` arrow keys to navigate to the desired Block.
* For long Blocks:
  * You can click "Jump to the bottom of this block".
  * You can press `CTRL-SHIFT-UP`/`CTRL-SHIFT-DOWN` to Scroll to the top/bottom of the selected block.
  * From the [Command Palette](broken-reference), you can also "Scroll to the top/bottom of selected block".
{% endtab %}
{% endtabs %}

{% embed url="https://www.loom.com/share/1cf8546daad548fbbe056c35edb23cdc?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" %}
Select a Single Block
{% endembed %}

## Select Multiple Blocks

{% tabs %}
{% tab title="macOS" %}
* Click another Block while holding `CMD` to toggle the selection of that Block, or
* Click another Block while holding `SHIFT` to select a range of Block, or
* Use `SHIFT-UP ↑` or `SHIFT-DOWN ↓` to expand the active selection (the Block with the thicker border) up or down, respectively.
{% endtab %}

{% tab title="Windows" %}
* Click another Block while holding `CTRL-SHIFT` to toggle the selection of that Block, or
* Click another Block while holding `SHIFT` to select a range of Block, or
* Use `SHIFT-UP ↑` or `SHIFT-DOWN ↓` to expand the active selection (the Block with the thicker border) up or down, respectively.
{% endtab %}

{% tab title="Linux" %}
* Click another Block while holding `CTRL-SHIFT` to toggle the selection of that Block, or
* Click another Block while holding `SHIFT` to select a range of Block, or
* Use `SHIFT-UP ↑` or `SHIFT-DOWN ↓` to expand the active selection (the Block with the thicker border) up or down, respectively.
{% endtab %}
{% endtabs %}

{% embed url="https://www.loom.com/share/5058ab0dc3d244d4a2ce576331440821?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" %}
Select Multiple Blocks
{% endembed %}

## Navigate Blocks

* Either scroll using your mouse or the scrollbar or select a Block and use the `UP ↑` and `DOWN ↓` arrow keys.
* "Scroll Terminal output up/down one line" is also a way to navigate block output, and can be configured with a keyboard shortcut or accessed from the [Command Palette](broken-reference).
* When the output of a command is cut off, Warp keeps the [Sticky Command Header](sticky-command-header.md) pinned at the top that displays the command the Block corresponds to. Clicking the header will scroll the screen to the start of the Block.

{% embed url="https://www.loom.com/share/21ebb0a79c1248a98846cba12a4b7020?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" %}
Navigate between Blocks
{% endembed %}
