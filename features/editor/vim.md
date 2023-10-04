---
description: Use Vim keybindings to edit text in Warp's text editor.
---

# Vim keybindings (Beta)

The Vi family of programs (including Vim and Neovim) are modal text editors
that allow for keyboard-driven text editing.
Several shells, including `bash` and `zsh` implement vi-style keybindings. 
Warp's input editor was built natively to support more modern text editing experiences, 
which means it replaces the shell's editor capabilities, 
so we implemented Vim keybindings ourselves.

> Please note: this feature is in Beta.

## Enabling Vim Keybindings

To enable Vim keybindings in Warp's command editor,
open the Command Palette with `CMD-P` and type `Vim Keybindings`.
This setting is also available in the Settings modal,
under `Features` → `Editor` → `Edit commands with Vim keybindings`.

Just as in `bash` and `zsh`'s vi mode implementations, the editor starts in insert mode.

## Customizing Keybindings

At the moment, we only support default Vim keybindings.

One exception is the keyboard shortcut for exiting insert mode, which can be rebound
through the Settings page, under `Keyboard Shortcuts` → `Exit Vim Insert Mode`,
or through the Command Palette with `CMD-P` and searching for `Exit Vim Insert Mode`.

# Supported Keybindings

Below is a list of the vim functionality we've implemented in Warp so far.

## Movement

See [Vim docs: motion](https://vimdoc.sourceforge.net/htmldoc/motion.html)
for more information.

### Basic

| Command(s) | Description |
| --- | --- |
| `h`, `j`, `k`, `l` | single-char movement |
| `w`, `W`, `b`, `B`, `e`, `E` | word movement |
| `ge`, `gE` | end of previous word |
| `$` | end of line |
| `0` | beginning of line |
| `^` | first non-whitespace character of line |
| `%` | jump to matching bracket |
| `[`, `]` | prev/next unmatched bracket |

### Multi-line-related

| Command(s) | Description |
| --- | --- |
| `gg`, `G `| jump to first/last line |

## Editing

| Command(s) | Description |
| --- | --- |
| `r` | replace character under cursor |
| `d`, `D` | delete a range or object |
| `c`, `C` | change a range or object (delete, then go to insert mode) |
| `s`, `S` | substitute (like change, but can only delete at the cursor) |
| `x`, `X` | delete under cursor |
| `y`, `Y` | yank (copy) into the clipboard |
| `p`, `P` | paste from the clipboard |
| `u`, `⌃r` | undo, redo |
| `~` | toggle upper/lowercase under cursor |
| `.` | repeat last edit |

See [Vim docs: editing](https://vimdoc.sourceforge.net/htmldoc/editing.html)
for more information.

## Search

### Character Search

| Command(s) | Description |
| --- | --- |
| `t`, `T`, `f`, `F` | find next/prev matching character on line |
| `;` | repeat last character search in the same direction |
| `,` | repeat last character search in the opposite direction |

See [Vim docs: left-right motions](https://vimdoc.sourceforge.net/htmldoc/motion.html#f)
for more information.

### General Search

Unlike Vim, general search commands don't search within the buffer.
Instead, they open Warp's native command search.

| Command(s) | Description |
| --- | --- |
| `/`, `?`, `*`, `#` | open Warp command search |

## Mode Switching

| Command(s) | Description |
| --- | --- |
| `i` | insert text before the cursor |
| `I` | insert text before the first non-whitespace character in the line |
| `a` | append text after the cursor |
| `A` | append text at the end of the line |
| `o` | begin new line below the cursor and insert text |
| `O` | begin new line above the cursor and insert text |
| `v` | visual character mode |
| `V` | visual line mode |

See [Vim docs: insert](https://vimdoc.sourceforge.net/htmldoc/insert.html#insert)
and [Vim docs: Visual mode](https://vimdoc.sourceforge.net/htmldoc/visual.html#visual-mode)
for more information.

## Registers

| Command(s) | Description |
| --- | --- |
| `"` | register prefix |

We currently support the following registers:
| Register name | Description |
| --- | --- |
| `a`–`z`, `A`–`Z` | named registers |
| `+` | system clipboard |
| `*` | system clipboard |
| `"` | unnamed register, containing the text of the last delete or yank |

See [Vim docs: registers](https://vimdoc.sourceforge.net/htmldoc/change.html#registers)
for more information.


# Feedback

This feature is still in Beta. We'd love to hear your feedback!
The best way to report bugs and request features is through our
[GitHub Issues](https://github.com/warpdotdev/Warp/issues) page.
Please upvote (:thumbsup:) existing issues to help us prioritize them.
