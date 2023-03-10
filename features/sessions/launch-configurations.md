# Launch Configurations

## What is it

Launch Configurations enables you to save your configuration of windows, tab, and panes, so that you can reopen the same set of windows, tab, and panes per project quickly. You can save this via the app, or by adding a yaml file.

## How it works

1. Set up the configuration of windows, tabs, and panes you would like to save.
2. From the Command Palette `CMD-P`, enter `#` to open the Launch Configuration Palette, then click plus **+**.
3. Name the configuration file. N_ote: The name field cannot be empty._
4. Click the save configuration button.
5. Then, toggle the Launch Configuration Palette like in step 2 from above, with the keyboard shortcut `CTRL-CMD-L`, or from the Mac Menu: `File > Launch Configurations`, where you can search through and open your saved configurations.

{% hint style="info" %}
**Terminal Tip**\
You can open saved Launch Configurations via [Alfred](https://www.alfredapp.com/) Workflow or [Raycast](https://www.raycast.com/) Extension. Please learn more about installation and implementation [here](https://blog.joe.codes/open-warp-launch-configurations-from-raycast-and-alfred). Credit to [@joetannenbaum](https://twitter.com/joetannenbaum/status/1633538768866009115)
{% endhint %}

{% embed url="https://www.loom.com/share/daa2a9e55c27458c8bbf722d90078880?hideEmbedTopBar=true&hide_owner=true&hide_share=true&hide_title=true" %}
Launch Configuration Demo
{% endembed %}

## YAML Format

All yaml files are stored in `~/.warp/launch_configurations/`.

{% hint style="warning" %}
The `cwd:` value in the yaml code must contain an absolute path or `""`. Note that `~` or empty paths will result in the file not being visible on the list of options for Launch Configurations.
{% endhint %}

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

Use the `commands` field to define a set of commands to run when a configuration is launched.

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
