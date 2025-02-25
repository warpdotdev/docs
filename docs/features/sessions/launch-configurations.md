---
description: >-
  Launch Configurations enables you to save your configuration of windows, tabs,
  and panes, so that you can reopen the same set of sessions per project
  quickly.
---

# Launch Configurations

## What is it

With Launch configurations you can save in the app or by adding a yaml file.

## Creating a Launch Configuration

### From the UI

1. Set up the configuration of windows, tabs, and panes you would like to save.
2. Open the [Command Palette](../command-palette.md), and type in `Save New Launch Configuration`.
3. Name the configuration file. The name field cannot be empty.
4. Click the Save configuration button.

### With a YAML File

* Launch Configurations files are generated when you create them with the UI and can also be created or modified manually.
* Please see the below for [Launch Configuration YAML file locations, format, and examples](launch-configurations.md#launch-configuration-yaml-format).

## Using a Launch Configuration

{% tabs %}
{% tab title="macOS" %}
* From the [Command Palette](../command-palette.md), enter `Launch Configuration` to open and select Launch Configuration.
* Right-clicking the new Tab **+** button to open a menu and select saved Launch Configuration.
* From the Mac Menu, `File > Launch Configurations`, where you can search through and open your saved Launch Configuration.
  * Single-window launch configs can be launched into the active window from the launch configuration palette using `CMD-ENTER` on Mac.
{% endtab %}

{% tab title="Linux" %}
* From the [Command Palette](../command-palette.md), enter `Launch Configuration` to open and select Launch Configuration.
* Right-clicking the new Tab **+** button to open a menu and select saved Launch Configuration.
  * Single-window launch configs can be launched into the active window from the launch configuration palette using `CTRL-ENTER` on Linux.
{% endtab %}
{% endtabs %}

{% hint style="info" %}
**Terminal Tip**\
You can open saved Launch Configurations via Alfred Workflow or [Raycast](../integrations-and-plugins.md#raycast) Extension. Learn more [here](https://blog.joe.codes/open-warp-launch-configurations-from-raycast-and-alfred). Credit to [@joetannenbaum](https://twitter.com/joetannenbaum/status/1633538768866009115)
{% endhint %}

## How it works

{% embed url="https://www.loom.com/share/daa2a9e55c27458c8bbf722d90078880?hideEmbedTopBar=true&hide_owner=true&hide_share=true&hide_title=true" %}
Launch Configuration Demo
{% endembed %}

## Launch Configuration YAML Format

All Launch Configuration yaml files are stored in the following location:

{% tabs %}
{% tab title="macOS" %}
```sh
$HOME/.warp/launch_configurations/
```

```sh
$HOME/.warp/launch_configurations/
```
{% endtab %}

{% tab title="Linux" %}
```
${XDG_DATA_HOME:-$HOME/.local/share}/warp-terminal/launch_configurations/
```

```
${XDG_DATA_HOME:-$HOME/.local/share}/warp-terminal/launch_configurations/
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
The `cwd:` value in the yaml code must contain an absolute path or `""`. Note that `~` or empty paths will result in the file not being visible on the list of options for Launch Configurations.
{% endhint %}

### Windows

Here's a sample configuration that shows how windows are structured in launch configuration files.

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

Here's a sample configuration that shows how tabs are structured in launch configuration files.

* Use the `title` field to set a custom tab name
* Use the `color` field to set the tab color
  *   We currently support using the terminal colors (ANSI colors):

      `Red | Green | Yellow | Blue | Magenta | Cyan`

      The actual color values will be automatically derived from your Warp theme

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

### Panes

Launch Configurations support setting split panes in each tab. Note that Warp also supports nesting split panes in launch configuration files.

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
      - title: desktop, documents, and warp user
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

Use the `commands` field to define a set of commands to run when a launch configuration in run.

```yaml
# Warp Launch Configuration
#
# This configuration has two windows.
# The first window executes two commands on start.
# The second window has a split pane that executes a command on start.

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
                - exec: curl http://example.com -o my.file
            - cwd: /Users/warp-user
              commands:
                - exec: ssh user@remote.server.com
        color: green
```
