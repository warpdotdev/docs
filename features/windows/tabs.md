# Tabs

## What is it

The Tabs feature allows you to organize a window into multiple terminal sessions. Tabs can be customized with a title and/or an ANSI color to help identify them. _Note:_ New Tabs will default to the active Tabs’ current working directory and the actual color values will be automatically derived from your Warp theme.

## How to use it

* Open a new Tab with `CMD-T` or by clicking on the `+` in the top bar.
* Close the current Tab with `CMD-W` or by clicking on the `x` on hover over a Tab.
* Activate the Previous or Next Tab with `SHIFT-CMD-{` or `SHIFT-CMD-}`.
* Move a Tab to the Left or Right with `CTRL-SHIFT-LEFT` or `CTRL-SHIFT-LEFT`.
* Right-clicking on a Tab reveals more options, like ‘Rename Tab’ and the color picker, or explore even more Tab actions within the Command Palette `CMD-P`

{% hint style="info" %}
**Terminal Tip**\
Using your .zshrc or .bashrc files, you can set a new Tab name:

{% code overflow="wrap" %}
```bash
# Set name, where MyTabName would be whatever you want to see in the Tab ( either a fixed string, $PWD, or something else )
function set_name () {​echo -ne "\033]0;MyTabName\007" }
# Add the function to the environment variable in either Zsh or Bash
if [ -n "$ZSH_VERSION" ]; then
  precmd_functions+=(set_name)
elif [ -n "$BASH_VERSION" ]; then
  PROMPT_COMMAND='set_name'
fi
```
{% endcode %}

Learn more about Tab names [here](https://learn.microsoft.com/en-us/windows/terminal/tutorials/tab-title#set-the-shells-title) and the Working directory for Tabs [here](../working-directory.md).
{% endhint %}

## How it works

{% embed url="https://www.loom.com/share/84d15cc7eb5a4a668bb86be9e827f261?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" %}
Tabs Demo
{% endembed %}
