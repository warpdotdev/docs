# Keyboard Shortcuts

Warp opens with a shortcut screen showing some of the most commonly used keyboard shortcuts. Hide
the shortcut screen by clicking the menu button below it.

## Custom Keyboard Shortcuts

Set custom keyboard shortcuts by navigating to Settings > Keyboard Shortcuts. Search through the
re-mappable actions using the search bar.

## All Available Shortcuts

### Warp Essentials

| Shortcut       | Description                  | Action                                         |
| -------------- | ---------------------------- | ---------------------------------------------- |
| `CTRL-CMD-L`   | Launch Configuration Palette | `workspace:toggle_launch_config_palette`       |
| `CTRL-``       | A.I. Command Search          | `input:toggle_natural_language_command_search` |
| `CMD-D`        | Split Pane Right             | `pane_group:add_right`                         |
| `CTRL-SHIFT-R` | Workflows                    | `input:toggle_workflows`                       |
| `CTRL-R`       | Command Search               | `workspace:show_command_search`                |
| `CTRL-CMD-T`   | Open Theme Picker            | `workspace:show_theme_chooser`                 |

### Blocks

| Shortcut          | Description                       | Action                                                 |
| ----------------- | --------------------------------- | ------------------------------------------------------ |
| `ALT-UP`          | Select the Closest Bookmark Up    | `terminal:select_bookmark_up`                          |
| `ALT-SHIFT-CMD-C` | Copy Command Output               | `terminal:copy_outputs`                                |
| `CMD-DOWN`        | Select Next Block                 | `terminal:select_next_block`                           |
| `ALT-DOWN`        | Select the Closest Bookmark Down  | `terminal:select_bookmark_down`                        |
| `SHIFT-CMD-S`     | Share Selected Block              | `terminal:open_share_modal`                            |
| `CMD-I`           | Reinput Selected Commands         | `terminal:reinput_commands`                            |
| `CMD-UP`          | Select Previous Block             | `terminal:select_previous_block`                       |
| `CMD-A`           | Select All Blocks                 | `terminal:select_all_blocks`                           |
| `SHIFT-CMD-C`     | Copy Command                      | `terminal:copy_commands`                               |
| `CMD-L`           | Focus Terminal Input              | `terminal:focus_input`                                 |
| `SHIFT-DOWN`      | Expand Selected Blocks Below      | `terminal:expand_block_selection_below`                |
| `SHIFT-CMD-I`     | Reinput Selected Commands as Root | `terminal:reinput_commands_with_sudo`                  |
| `CTRL-M`          | Open Block Context Menu           | `terminal:open_block_list_context_menu_via_keybinding` |
| `SHIFT-UP`        | Expand Selected Blocks Above      | `terminal:expand_block_selection_above`                |
| `CMD-B`           | Bookmark Selected Block           | `terminal:bookmark_selected_block`                     |

### Input Editor

| Shortcut          | Description                               | Action                                     |
| ----------------- | ----------------------------------------- | ------------------------------------------ |
| `CTRL-SHIFT-E`    | Select to End of Line                     | `editor:select_to_line_end`                |
| `CTRL-U`          | Copy and Clear Selected Lines             | `editor_view:clear_and_copy_lines`         |
| `CMD-RIGHT`       | End                                       | `editor_view:end`                          |
| `CMD-DOWN`        | Move Cursor to the Bottom                 | `editor_view:cmd_down`                     |
| `META-F`          | Move Forward One Word                     | `editor_view:move_forward_one_word`        |
| `CMD-LEFT`        | Home                                      | `editor_view:home`                         |
| `SHIFT-META-<`    | Move to the Start of the Buffer           | `editor_view:move_to_buffer_start`         |
| `META-E`          | Move to the End of the Paragraph          | `editor_view:move_to_paragraph_end`        |
| `CMD-I`           | Inspect Command                           | `editor_view:cmd_i`                        |
| `CTRL-SHIFT-A`    | Select to Start of Line                   | `editor:select_to_line_start`              |
| `SHIFT-META-B`    | Select One Word to the Left               | `editor_view:select_left_by_word`          |
| `CTRL-SHIFT-P`    | Select Up                                 | `editor_view:select_up`                    |
| `CTRL-J`          | Insert Newline                            | `editor_view:insert_newline`               |
| `META-A`          | Move to the Start of the Paragraph        | `editor_view:move_to_paragraph_start`      |
| `CTRL-G`          | Add Selection for Next Occurrence         | `editor_view:add_next_occurrence`          |
| `CTRL-H`          | Remove the Previous Character             | `editor_view:backspace`                    |
| `SHIFT-META->`    | Move to the End of the Buffer             | `editor_view:move_to_buffer_end`           |
| `SHIFT-META-F`    | Select One Word to the Right              | `editor_view:select_right_by_word`         |
| `ALT-DELETE`      | Delete Word Right                         | `editor:delete_word_right`                 |
| `CTRL-K`          | Cut All Right                             | `editor_view:cut_all_right`                |
| `META-.`          | Insert Last Word of Previous Command      | `editor:insert_last_word_previous_command` |
| `CTRL-A`          | Move to Start of Line                     | `editor_view:move_to_line_start`           |
| `ALT-CMD-F`       | Fold Selected Ranges                      | `editor_view:fold_selected_ranges`         |
| `META-D`          | Cut Word Right                            | `editor_view:cut_word_right`               |
| `SHIFT-CMD-K`     | Clear Selected Lines                      | `editor_view:clear_lines`                  |
| `CTRL-D`          | Delete                                    | `editor_view:delete`                       |
| `ALT-BACKSPACE`   | Delete Word Left                          | `editor:delete_word_left`                  |
| `CTRL-B`          | Move Cursor Left                          | `editor_view:left`                         |
| `CMD-BACKSPACE`   | Delete All Left                           | `editor_view:delete_all_left`              |
| `META-B`          | Move Backward One Word                    | `editor_view:move_backward_one_word`       |
| `CTRL-E`          | Move to End of Line                       | `editor_view:move_to_line_end`             |
| `CTRL-C`          | Clear Command Editor                      | `editor_view:clear_buffer`                 |
| `CTRL-SHIFT-F`    | Select One Character to the Right         | `editor_view:select_right`                 |
| `CMD-DELETE`      | Delete All Right                          | `editor_view:delete_all_right`             |
| `CTRL-SHIFT-N`    | Select Down                               | `editor_view:select_down`                  |
| `CMD-A`           | Select All                                | `editor_view:select_all`                   |
| `CTRL-N`          | Move Cursor Down                          | `editor_view:down`                         |
| `CTRL-SHIFT-UP`   | Add Cursor Above                          | `editor_view:add_cursor_above`             |
| `CTRL-L`          | Clear Screen                              | `input:clear_screen`                       |
| `CTRL-F`          | Move Cursor Right / Accept Autosuggestion | `editor_view:right`                        |
| `ALT-CMD-]`       | Unfold                                    | `editor_view:unfold`                       |
| `ALT-CMD-[`       | Fold                                      | `editor_view:fold`                         |
| `CTRL-W`          | Cut Word Left                             | `editor_view:cut_word_left`                |
| `CTRL-SHIFT-DOWN` | Add Cursor Below                          | `editor_view:add_cursor_below`             |
| `CTRL-P`          | Move Cursor Up                            | `editor_view:up`                           |
| `CTRL-SHIFT-B`    | Select One Character to the Left          | `editor_view:select_left`                  |

### Terminal

| Shortcut          | Description                                       | Action                                       |
| ----------------- | ------------------------------------------------- | -------------------------------------------- |
| `ALT-CMD-RIGHT`   | Switch Panes Right                                | `pane_group:navigate_right`                  |
| `CMD-P`           | Toggle Command Palette                            | `workspace:toggle_command_palette`           |
| `CTRL-CMD-LEFT`   | Resize Pane > Move Divider Left                   | `pane_group:resize_left`                     |
| `ALT-CMD-V`       | [a11y] Set Verbose Accessibility Announcements    | `workspace:set_a11y_verbose_verbosity_level` |
| `CTRL-CMD-UP`     | Resize Pane > Move Divider Up                     | `pane_group:resize_up`                       |
| `SHIFT-CMD-ENTER` | Toggle Maximize Active Pane                       | `pane_group:toggle_maximize_pane`            |
| `CMD-[`           | Activate Previous Pane                            | `pane_group:navigate_prev`                   |
| `CTRL-CMD-DOWN`   | Resize Pane > Move Divider Down                   | `pane_group:resize_down`                     |
| `CMD-G`           | Find the Next Occurrence of Your Search Query     | `find:find_next_occurrence`                  |
| `SHIFT-CMD-P`     | Toggle Navigation Palette                         | `workspace:toggle_navigation_palette`        |
| `ALT-CMD-LEFT`    | Switch Panes Left                                 | `pane_group:navigate_left`                   |
| `ALT-CMD-V`       | [a11y] Set Concise Accessibility Announcements    | `workspace:set_a11y_concise_verbosity_level` |
| `CTRL-SHIFT-?`    | Open Resource Center                              | `workspace:toggle_resource_center`           |
| `ALT-CMD-DOWN`    | Switch Panes Down                                 | `pane_group:navigate_down`                   |
| `SHIFT-CMD-D`     | Split Pane Down                                   | `pane_group:add_down`                        |
| `ALT-CMD-UP`      | Switch Panes Up                                   | `pane_group:navigate_up`                     |
| `CMD-R`           | Toggle Mouse Reporting                            | `workspace:toggle_mouse_reporting`           |
| `CTRL-CMD-K`      | Open Keybindings Editor                           | `workspace:show_keybinding_settings`         |
| `CTRL-CMD-RIGHT`  | Resize Pane > Move Divider Right                  | `pane_group:resize_right`                    |
| `SHIFT-CMD-G`     | Find the Previous Occurrence of Your Search Query | `find:find_prev_occurrence`                  |
| `CMD-,`           | Open Settings: Account                            | `workspace:show_settings_account_page`       |
| `CMD-,`           | Open Settings                                     | `workspace:show_settings_modal`              |
| `CMD-]`           | Activate Next Pane                                | `pane_group:navigate_next`                   |

### Fundamentals

| Shortcut           | Description                | Action                           |
| ------------------ | -------------------------- | -------------------------------- |
| `CMD-5`            | Switch to 5th Tab          | `workspace:activate_fifth_tab`   |
| `CMD-F`            | Find                       | `terminal:find`                  |
| `CMD-1`            | Switch to 1st Tab          | `workspace:activate_first_tab`   |
| `SHIFT-CMD-}`      | Activate Next Tab          | `workspace:activate_next_tab`    |
| `CMD-8`            | Switch to 8th Tab          | `workspace:activate_eighth_tab`  |
| `CMD-=`            | Increase Font Size         | `workspace:increase_font_size`   |
| `CMD-V`            | Paste                      | `terminal:paste`                 |
| `CMD-6`            | Switch to 6th Tab          | `workspace:activate_sixth_tab`   |
| `CMD-9`            | Switch to Last Tab         | `workspace:activate_last_tab`    |
| `CMD--`            | Decrease Font Size         | `workspace:decrease_font_size`   |
| `SHIFT-CMD-{`      | Activate Previous Tab      | `workspace:activate_prev_tab`    |
| `CMD-7`            | Switch to 7th Tab          | `workspace:activate_seventh_tab` |
| `CMD-0`            | Reset Font Size to Default | `workspace:reset_font_size`      |
| `CMD-4`            | Switch to 4th Tab          | `workspace:activate_fourth_tab`  |
| `CMD-2`            | Switch to 2nd Tab          | `workspace:activate_second_tab`  |
| `CTRL-SHIFT-RIGHT` | Move Tab Right             | `workspace:move_tab_right`       |
| `CMD-C`            | Copy                       | `terminal:copy`                  |
| `CTRL-SHIFT-LEFT`  | Move Tab Left              | `workspace:move_tab_left`        |
| `CMD-3`            | Switch to 3rd Tab          | `workspace:activate_third_tab`   |
