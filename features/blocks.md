# Blocks

In other terminals, the atomic unit is a character. But most developers think in commands and outputs, rather than characters. In Warp the structure of the UI reflects this mental model: commands and outputs are grouped into what we call **Blocks**.&#x20;

Grouping commands into blocks makes the UI easier to use and navigate. For you as a developer, this means it’s easy to copy just a specific command or output, and to scroll directly to the start of a command.&#x20;

Blocks also allow you re-input commands, and share commands and their outputs (with all formatting intact) with a click of a button.To see how we differentiate between input and output, or how we implement blocks, check out the [How It Works](https://blog.warp.dev/how-warp-works/) page on Warp.

![Warp's Blocks](../.gitbook/assets/1\_annotated\_blocks\_v2.png)

## **The Basics: Create your first Block**

* Execute a command (type `ls` and hit `Enter`) in the input editor at the bottom of the screen
* You will notice that your command and output appear visually grouped together into a Block.

## Design: Blocks grow from bottom to the top. Input is fixed to the bottom.

* Try executing a different command (type `echo hello` and hit `Enter`).&#x20;
* You will notice that the new Block starts populating from the bottom while the input is fixed to the bottom.

## **Design: Color-coded Blocks**

We designed visual cues to help with quickly identifying what’s going on in a block.

* Blocks with long-running commands have a yellow side bar.
  * Try it: type `sleep 5` and hit `Enter`
* Blocks that quit with a non-zero exit code have a red background and red side bar.
  * Try it: type `xyz` (or some other command that doesn’t exist) and hit `Enter`

## Selecting a Block&#x20;

To select a Block:

* Using your mouse: click on a Block.
* Using your keyboard: hit `cmd-up` to select the most recently executed Block and use the up `↑` and down `↓` arrow keys to navigate to the desired Block.

## **Navigating Between Blocks**

To navigate between Blocks, you can either scroll using your mouse or the scrollbar, or you can [select a Block](blocks.md#selecting-a-block) and use the up `↑` and down `↓` arrow keys.

For any Block where its command is obscured, Warp has a “snackbar” button that scrolls you to the top of the Block.&#x20;

![Warp has a snackbar that scrolls you to the top of a Block whose command is obscured.](../.gitbook/assets/2\_snackbar.gif)

## Actions on a Block

Using your mouse: the top right corner of each Block has an expandable menu that allows you to:

* **Copy the input, output, or both contents in a Block**. The content is copied to your clipboard; you are free to paste it anywhere.
* **Re-run that Block’s input command**. The command is automatically re-entered into the input editor at the bottom of the screen. All you have to do is hit Enter.
* **Share the Block**, retaining all of its formatting. We create a web permalink to this block (only if you choose to!) which you can share with your coworkers. For now, this link is viewable to anyone who has it. In the future, you will be able to restrict viewing permissions to specific Warp users or email domains. [Here’s an example of a shared block.](https://app.warp.dev/kKadm5)

Using your keyboard: [select a Block](blocks.md#selecting-a-block) with your keyboard and press `⌘` `C` (`cmd-c`) to copy its input command to your clipboard. Keyboard shortcuts for the rest of the Block actions will soon be supported.&#x20;

