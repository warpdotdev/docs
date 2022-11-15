# Text Editor Input

## What is it

Unlike other terminals, Warp’s input editor operates out-of-the-box like a modern IDE and the text editors we’re used to.

{% hint style="info" %}
Text Editor Input also works for [SSH sessions](../ssh.md).
{% endhint %}

### Soft Wrapping

Warp supports soft wrapping in the input editor. If there is an auto suggestion that goes off-screen, the input editor will be horizontally scrollable to make it visible. _Note:"_ Some operations treat soft wrapped lines like a logical line (`TRIPLE-CLICK`, `OPTION-LEFT` / `OPTION-RIGHT`) while other operations treat soft wrapped lines like visible different lines (`UP` / `DOWN`, `SHIFT-UP` / `SHIFT-DOWN`).

![Soft Wrapping](../../.gitbook/assets/soft-wrapping.png)

## How to use it

| Keyboard binding                                     | Shortcut description                                                                                       |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `escape`                                             | Closes the input suggestions or history menu                                                               |
| `ctrl-l`                                             | Clears the terminal                                                                                        |
| `ctrl-h`                                             | Backspace                                                                                                  |
| `ctrl-c`                                             | Clear the entire editor buffer                                                                             |
| `ctrl-u` `cmd-shift-K`                               | Clear the current line                                                                                     |
| `cmd-c` `ctrl-y`, `cmd-x`, `cmd-v`                   | Copy, cut, paste                                                                                           |
| `ctrl-w` / `option-d`                                | Cut the word to the left / right of the cursor                                                             |
| `option-backspace` / `option-d`                      | Delete the word to the left / right of the cursor                                                          |
| `ctrl-k cmd-delete`                                  | Delete everything to the right of the cursor                                                               |
| `option-left` / `option-right`                       | Move to the beginning of the previous / next word                                                          |
| `cmd-left` `ctrl-a`/ `ctrl-e` `cmd-down` `cmd-right` | Move the cursor to the start / end of the line                                                             |
| `cmd-up`                                             | Move the cursor to the beginning of the editor buffer. If it's already there, select the most recent block |
| `shift-left` / `shift-right`                         | Select the character to the left / right of the cursor                                                     |
| `option-shift-left` / `option-shift-right`           | Select the word to the left / right of the cursor                                                          |
| `cmd-shift-left` / `cmd-shift-right`                 | Select everything to the left / right of the cursor                                                        |
| `shift-up` / `shift-down`                            | Select everything above / below the cursor                                                                 |
| `cmd-a`                                              | Select the entire editor buffer                                                                            |
| `shift-enter` `ctrl-enter` `option-enter`            | Insert newline                                                                                             |
| `ctrl-r`                                             | [Command History](../command-history.md)                                                                   |
| `cmd-d`                                              | Split pane                                                                                                 |

## How it Works

Refer to the demo below.

{% embed url="https://loom.com/share/1517049fefc34227bf1abaf19cc7e6ea?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" %}
Text Editor Input Demo
{% endembed %}
