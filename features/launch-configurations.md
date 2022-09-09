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
      - title: documents
        layout:
          cwd: /Users/warp-user/Documents
        color: blue
  - tabs:
      - title: warp user
        layout:
          cwd: /Users/warp-user
        color: green

```

### Tabs

Here's a sample configuration that shows how tabs are structured.
- Use `title` field to set custom tab name
- Use `color` field to set tab color
  
  - We currently support using the terminal colors (ANSI colors): 
  
    `Red | Green | Yellow | Blue | Magenta | Cyan`
  
    The actual color values will be automatically derived from your Warp theme.

```yaml
# Warp Launch Configuration
#
# This configuration has two tabs in the same window.

---
name: Example Configuration With Two Tabs
windows:
  - tabs:
      - title: documents 
        layout:
          cwd: /Users/warp-user/Documents
        color: blue
      - title: warp user
        layout:
          cwd: /Users/warp-user
        color: green

```

You can also set the custom tab title and color:

```yaml
# Warp Launch Configuration
#
# This configuration has one tab with custom title and color

---
name: Example Configuration With One Tab
windows:
  - tabs:
      - layout:
        cwd: /Users/warp-user/Documents
        title: "Test tab title"
        color: blue

```

Note that we currently support using the terminal colors (ANSI colors) in your configuration: [black, red, green, yellow, blue, magenta, cyan, white]. 
The actual color values will be automatically derived from your Warp theme.


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
      - title: downloads and warp user
        layout:
          split_direction: vertical
          panes:
            - cwd: /Users/warp-user/Downloads
            - cwd: /Users/warp-user
        color: blue
  - tabs:
      - title: desktop, documents and warp uesr
        layout:
          split_direction: horizontal
          panes:
            - cwd: /Users/warp-user/Desktop
            - split_direction: vertical
              panes:
                - cwd: /Users/warp-user/Documents
                - cwd: /Users/warp-user
        color: green

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
      - title: documents
        layout:
          cwd: /Users/warp-user/Documents
          commands:
            - exec: ls
            - exec: code .
        color: blue
  - tabs:
      - title: downloads
        layout:
          split_direction: vertical
          panes:
            - cwd: /Users/warp-user/Downloads
              commands:
                - exec: ls -a
            - cwd: /Users/warp-user
        color: green
```
