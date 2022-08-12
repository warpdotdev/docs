# Text Editor Input

## What is it

Unlike other terminals, Warp’s input editor operates out-of-the-box like a modern IDE and the text editors we’re used to.

{% hint style="info" %}
Text Editor Input also works for [SSH sessions](https://docs.warp.dev/features/ssh).
{% endhint %}

## How to access it

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
| `ctrl-r`                                             | [Command History](command\-history.md)                                                                     |
| `cmd-d`                                              | Select all occurrences of the word(s) that has a cursor in it                                              |

## How it Works

Refer to the demo below.

{% embed url="https://loom.com/share/1517049fefc34227bf1abaf19cc7e6ea" %}
Text Editor Input demo
{% endembed %}
