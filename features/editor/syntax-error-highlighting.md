# Syntax and Error Highlighting

## What is Syntax Highlighting

Warp supports Syntax Highlighting in the [Input Editor.](./) It colors each part of a command to help differentiate between sub-commands, options/flags, arguments, and variables.

### How to access Syntax Highlighting

When Syntax Highlighting is enabled, Warp's [Input Editor](./) automatically recognizes each part of the command as you type it into the Input Editor, and syntactically highlight them.

### How to enable/disable Syntax Highlighting

Syntax highlighting is enabled by default, to toggle it:

* Through the [Command Palette](../command-palette.md), search for the "Syntax Highlighting" option and click it (or press enter) to enable/disable.
* Through  `Settings > Features > Editor` , toggle "Syntax highlighting for commands"

### How Syntax Highlighting Works

{% embed url="https://www.loom.com/share/87b15de13ee9407b98a24f1a31835784?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" %}
Syntax Highlighting Demo
{% endembed %}

## What is Error Underlining

Warp highlights errors in commands that are typed within the [Input Editor](./) e.g. if the binary for the command you've typed does not exist.

{% hint style="warning" %}
Newly installed apps or newly created aliases will trigger error underlining until you open a new Warp session (new window, tab, or pane).
{% endhint %}

### How to access Error Underlining

When Error Underlining is enabled, Warp automatically underlines any invalid commands with a dashed red underline.

### How to enable/disable Error Underlining

Error underlining is enabled by default, to toggle it:

* Through the [Command Palette](../command-palette.md), search for the "Syntax Highlighting" option and click it (or press enter) to enable/disable.
* Through  `Settings > Features > Editor` , toggle "Error underlining for commands"

### How Error Underlining works

{% embed url="https://www.loom.com/share/7721e06ed4aa4e1380abae4f5827ef6f?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" %}
Error Underlining Demo
{% endembed %}
