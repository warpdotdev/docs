---
description: >-
  The Tabs feature allows you to organize a window into multiple terminal
  sessions. Tabs can be customized with a title and/or an ANSI color to help
  identify them.
---

# Tabs

{% hint style="info" %}
New Tabs will default to the active Tabs’ current [Working Directory](../working-directory.md) and the actual color values will be automatically derived from your Warp [Theme](../../appearance/themes.md).
{% endhint %}

## How to use Tabs

{% tabs %}
{% tab title="macOS" %}
* Right-click on the new Tab button `+` to make a new tab, restore closed tab, or run a saved [Launch Configuration](../sessions/launch-configurations.md).
* Open a new Tab with `CMD-T` or by clicking on the `+` in the top bar.
* Close the current Tab with `CMD-W` or by clicking on the `X` on hover over a Tab.
* Reopen closed tabs with `SHIFT-CMD-T`.
* Move a Tab to the Left / Right with `CTRL-SHIFT-LEFT` / `CTRL-SHIFT-RIGHT` or by clicking and dragging a Tab.
* Activate the Previous / Next Tab with `SHIFT-CMD-{` / `SHIFT-CMD-}` or by clicking a Tab.
* Activate the first through eighth Tabs with `CMD-1` thru `CMD-8`.
* Switch to the last Tab with `CMD-9`.
* Double-click a Tab to rename it.
* Right-clicking on a Tab reveals more options you can explore within the [Command Palette](../command-palette.md) or [Keyboard Shortcuts](../keyboard-shortcuts.md#fundamentals).
{% endtab %}

{% tab title="Windows" %}
* Right-click on the new Tab button `+` to make a new tab, restore closed tab, or run a saved [Launch Configuration](../sessions/launch-configurations.md).
* Open a new Tab with `CTRL-SHIFT-T` or by clicking on the `+` in the top bar.
* Close the current Tab with `CTRL-SHIFT-W` or by clicking on the `x` on hover over a Tab.
* Reopen closed tabs with `CTRL-ALT-T`.
* Move a Tab to the Left / Right with `CTRL-SHIFT-LEFT` / `CTRL-SHIFT-RIGHT` or by clicking and dragging a Tab.
* Activate the Previous / Next Tab with `CTRL-PGUP` / `CTRL-PGDN` or by clicking a Tab.
* Activate the first through eighth Tabs with `CTRL-1` thru `CTRL-8`.
* Switch to the last Tab with `CTRL-9`.
* Double-click a Tab to rename it.
* Right-clicking on a Tab reveals more options you can explore within the [Command Palette](../command-palette.md) or [Keyboard Shortcuts](../keyboard-shortcuts.md#fundamentals).
{% endtab %}

{% tab title="Linux" %}
* Right-click on the new Tab button `+` to make a new tab, restore closed tab, or run a saved [Launch Configuration](../sessions/launch-configurations.md).
* Open a new Tab with `CTRL-SHIFT-T` or by clicking on the `+` in the top bar.
* Close the current Tab with `CTRL-SHIFT-W` or by clicking on the `x` on hover over a Tab.
* Reopen closed tabs with `CTRL-ALT-T`.
* Move a Tab to the Left / Right with `CTRL-SHIFT-LEFT` / `CTRL-SHIFT-RIGHT` or by clicking and dragging a Tab.
* Activate the Previous / Next Tab with `CTRL-PGUP` / `CTRL-PGDN` or by clicking a Tab.
* Activate the first through eighth Tabs with `CTRL-1` thru `CTRL-8`.
* Switch to the last Tab with `CTRL-9`.
* Double-click a Tab to rename it.
* Right-clicking on a Tab reveals more options you can explore within the [Command Palette](../command-palette.md) or [Keyboard Shortcuts](../keyboard-shortcuts.md#fundamentals).
{% endtab %}
{% endtabs %}

{% hint style="success" %}
**Terminal Tip**\
Using your `.zshrc` or `.bashrc` files on macOS or Linux, you can set a new Tab name:

{% code overflow="wrap" %}
```bash
# Set name, where MyTabName would be whatever you want to see in the Tab ( either a fixed string, $PWD, or something else )
function set_name () {
  echo -ne "\033]0;MyTabName\007"
}
# Add the function to the environment variable in either Zsh or Bash
if [ -n "$ZSH_VERSION" ]; then
  precmd_functions+=(set_name)
elif [ -n "$BASH_VERSION" ]; then
  PROMPT_COMMAND='set_name'
fi
```
{% endcode %}

Learn more about Tab names [here](https://learn.microsoft.com/en-us/windows/terminal/tutorials/tab-title#set-the-shells-title).
{% endhint %}

### Tab Restoration

Tab Restoration enables you to reopen recently closed tabs for up to 60 seconds. Configure this feature in `Settings > Features > Session > Enable reopening of closed sessions`

### CTRL-TAB Behavior

`CTRL-TAB` shortcut defaults to activate the previous / next Tab. You can configure the shortcut to cycle the most recent session, including any [Split Panes](split-panes.md), in `Settings > Features > Keys > Ctrl-Tab behavior`

### Tabs Behavior

Please see our [Appearance > Tabs Behavior](../../appearance/tabs-behavior.md) docs for more Tab related settings.&#x20;

### How Tabs work

{% embed url="https://www.loom.com/share/84d15cc7eb5a4a668bb86be9e827f261?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" %}
Tabs Demo
{% endembed %}
