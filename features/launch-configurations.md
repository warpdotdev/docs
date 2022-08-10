# Launch Configurations

Save your configuration of windows, tabs, and panes to a file! Open a saved configuration through the Command Palette > Toggle Launch Configuration Palette (`CTRL-CMD-L`).

## Getting Started

To get started with Launch Configurations,

1. Set up the configuration of windows, tabs and panes that you would like to save.
1. Press `CTRL-CMD-L` to open the Launch Configuration Palette and click the plus button.
1. Name the configuration file.
1. Click the save configuration button (plus sign).

Press `CTRL-CMD-L` to open the Launch Configuration Palette, where you can earch through and open your saved configurations.

![Launch Configurations Demo](../.gitbook/assets/launch-config-demo.gif)

## YAML Format

All yaml files are stored in `~/.warp/launch_configurations/`.

### Windows

Here's a sample configuration that shows how windows are structured.

```yaml
# Warp Launch Configuration
#
#
# Use this to start a certain configuration of windows, tabs, and panes.
# Open the launch configuration palette with ctrl-cmd-L to access 
# and open any launch configuration.
#
# This configuration has two windows, each with one tab in different starting directories.

---
name: Example Configuration With Two Windows
windows:
  - tabs:
      - layout:
          cwd: /Users/warp-user/Documents
  - tabs:
      - layout:
          cwd: /Users/warp-user

```

### Tabs

Here's a sample configuration that shows how tabs are structured.

```yaml
# Warp Launch Configuration
#
# This configuration has two tabs in the same window.

---
name: Example Configuration With Two Tabs
windows:
  - tabs:
      - layout:
          cwd: /Users/warp-user/Documents
      - layout:
          cwd: /Users/warp-user

```

### Panes

Launch Configurations support setting split panes in each tab. Note that Warp also supports nesting split panes.

```yaml
# Warp Launch Configuration
#
# This configuration is two windows, each with split panes.
# The first window contains a vertically split tab with two panes.
# The second window contains a horizontally split tab, 
# with a vertically split tab on the right.

---
name: Example Configuration With Split Panes
windows:
  - tabs:
      - layout:
          split_direction: vertical
          panes:
            - cwd: /Users/warp-user/Downloads
            - cwd: /Users/warp-user
  - tabs:
      - layout:
          split_direction: horizontal
          panes:
            - cwd: /Users/warp-user/Desktop
            - split_direction: vertical
              panes:
                - cwd: /Users/warp-user/Documents
                - cwd: /Users/warp-user

```

### Commands

Use the `commands` field to define a set of commands to run when a configuration is launched.

```yaml
# Warp Launch Configuration
#
# This configuration has two windows.
# The first window executes two commands on start.
# The second window has a split pane which executes a command on start.

---
name: Example Configuration With Starting Commands
windows:
  - tabs:
      - layout:
          cwd: /Users/warp-user/Documents
          commands:
            - exec: ls
            - exec: code .
  - tabs:
      - layout:
          split_direction: vertical
          panes:
            - cwd: /Users/warp-user/Downloads
              commands:
                - exec: ls -a
            - cwd: /Users/warp-user
```
