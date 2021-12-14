# Keyboard Shortcuts

Warp opens with a shortcut screen showing some of the most commonly used keyboard shortcuts. You can opt to hide this shortcut screen by clicking the menu button below it. This setting is sticky.

These are all the shortcuts Warp currently supports:

## Input Editor Shortcuts

| Keyboard binding                                     | Shortcut description                                                                                       |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `escape`                                             | Closes the input suggestions or history menu                                                               |
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
| `ctrl-r`                                             | [Command History](command-history.md)                                              |
| `cmd-d`                                              | Select all occurrences of the word(s) that has a cursor in it                                              |

## Block Shortcuts

| Keyboard binding                   | Shortcut description                                                     |
| ---------------------------------- | ------------------------------------------------------------------------ |
| `cmd-up`                           | If the cursor is at the start of the input, select the most recent block |
| `up` `cmd-up`/ `cmd-d`o`wn` `down` | If a block is selected, select the previous / next block                 |
| `cmd-shift-c`                      | If a block is selected, copy its input command to clipboard              |
| `cmd-shift-option-c`               | If a block is selected, copy its output to clipboard                     |
| `cmd-c`                            | If a block is selected, copy both its input and output to clipboard      |
| `cmd-shift-s`                      | If a block is selected, share it                                         |
| `cmd-i`                            | Reinput the command of the selected block                                |
| `escape`                           | If a block is selected, deselect it                                      |
| Typing `clear` into the editor     | Inserts an empty block that spans the length of the terminal window      |

## Terminal Shortcuts

| Keyboard binding | Shortcut description      |
| ---------------- | ------------------------- |
| `cmd-l`          | Focus on the input editor |
| `cmd-f`          | [Find](find.md)           |
| `cmd-t`          | Open a new tab            |
| `cmd-w`          | Close current tab         |
| `cmd-k`          | Clears the terminal       |

Want us to support a keyboard shortcut? [File a feature request here](../help/sending-us-feedback.md)!
