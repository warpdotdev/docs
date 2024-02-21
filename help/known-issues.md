---
description: >-
  To see a complete list of issues and feature requests, please visit our GitHub
  issues page.
---

# Known Issues

* Warp doesn't support `PROMPT_COMMAND` in bash right now, to set a custom prompt use `PS1`.
* When you [SSH](../features/ssh.md), we start a bash shell on the remote host. We built a wrapper around SSH to make Warp features possible.
* If your default shell is zsh, your aliases typically do not transfer over. Other shells are unsupported for now.
* When you open a [non-shell-based subshell (REPL)](https://github.com/warpdotdev/Warp/issues/4082), we do not set it up for Warp - instead, it works like a normal terminal session.
* Warp may become unresponsive if it doesn't have permission to access the folders.

Links to popular GitHub issues:

* [Vi / Vim / NeoVim](https://github.com/warpdotdev/warp/discussions/451)
* [tmux](https://github.com/warpdotdev/warp/discussions/501)
* [oh-my-zsh Prompts](https://github.com/warpdotdev/Warp/issues/936)

## SSH

To enable Blocks over SSH, Warp uses an SSH Wrapper function; navigate to settings > features if you need to disable it.

Note: You'll need to start a new session before a change is reflected or try invoking the SSH binary directly: `command ssh`.

There is also a known issue with the [SSH Wrapper not working in Windows SSH sessions](https://github.com/warpdotdev/Warp/issues/2413). You can workaround this by [installing Cygwin](https://www.cygwin.com/) on the Windows machine you'd like to connect to.

## Online features don't work

There is a known issue that can occur that causes online features to break ([Warp AI](../features/warp-ai/), [AI Command Suggestions](../features/warp-ai/ai-command-suggestions.md), [Block Sharing](../features/blocks/block-sharing.md), [Refe](../getting-started/refer-a-friend.md)[r a Friend](../getting-started/refer-a-friend.md), etc. ). This is due to the login token going stale, typically due to a password change, and can be resolved by the following steps:

{% tabs %}
{% tab title="macOS" %}
1. Remove Warp user login with `sudo security delete-generic-password -l "dev.warp.Warp-Stable" $HOME/Library/Keychains/login.keychain`
2. [Login to Warp](../getting-started/getting-started-with-warp.md#logging-into-warp)
{% endtab %}

{% tab title="Linux" %}
1. Remove Warp user login with your keychain manager (gnome-keyring, kwallet, etc.). Search for `dev.warp.Warp` and delete the `User` password/secret.
2. Remove any user files with the following command:
   ```sh
   rm -f ${XDG_STATE_HOME:-$HOME/.local/state}/warp-terminal/*-User
   ```
3. [Login to Warp](../getting-started/getting-started-with-warp.md#logging-into-warp)
{% endtab %}
{% endtabs %}

## English-only UI

Nov 2021: We have added character support for Chinese, Korean, and Japanese, but our UI currently only supports English.

### Abnormal rendering of Chinese characters

If you notice issues with the terminal rendering Chinese characters (i.e. [#3366](https://github.com/warpdotdev/Warp/issues/3366)). Please try adding the following lines to your rc file.

```
export LC_ALL=zh_CN.UTF-8
export LANG=zh_CN.UTF-8
```

## fish shell `read` command

There is an issue in fish shell version 3.6 and below that causes the `read` built-in command to break Warp's integration with fish. This means that using `read` directly or any fish scripts that call `read` will not work as expected in Warp. That issue is resolved in the fish repository and so should be fixed in the next release of fish itself. We recommend upgrading fish to the most recent version to resolve this issue.

### List of incompatible tools

* [iterm shell integration](https://iterm2.com/documentation-shell-integration.html)
  * usually looks like `test -e "${HOME}/.iterm2_shell_integration.zsh" && source "${HOME}/.iterm2_shell_integration.zsh" || true`
* FIG, `z`, `zsh-autocomplete`, `compdef`, `compinit`, or other [shell-based completion](https://github.com/warpdotdev/Warp/discussions/434) plugins or definitions.
* OH-MY-ZSH-THEMES
  * e.g. avit, spaceship, maybe more ...
* OH-MY-ZSH-PLUGINS
* Oh-My-Tmux
* zsh4h (ZSH for Humans)
* znap
* FZF
* fubectl
  * `[ -f ${HOME}/bin/fubectl.source ] && source ${HOME}/bin/fubectl.source`
* [BIND keys](https://github.com/warpdotdev/Warp/issues/537) like:
  * `bindkey '^j' down-line-or-beginning-search`, which causes users to have to hit ENTER twice to run a command.
  * `bindkey 'tab' autosuggest-accept`, which causes incorrect behavior with autocompletion.
* \[\[ -r "/usr/local/etc/profile.d/bash\_completion.sh" ]] && "/usr/local/etc/profile.d/bash\_completion.sh"
* eval "$(rbenv init -)"
* grml-zsh-config
* Python virtual environment PS1 [settings](https://github.com/warpdotdev/Warp/issues/2713#issuecomment-1447129449)
* [Starship settings](../appearance/prompt.md#starship-settings)

## Configuring and debugging your RC files

To support Blocks ([custom hooks](https://blog.warp.dev/how-warp-works/#implementing-blocks)), a native Input Editor experience, etc. we have to build custom support for a subset of shell functionality (decouple functionality from the shell and move to the terminal). This leads to Warp being incompatible with various tools and plugins.

You can **disable the conflicting settings for Warp** using this flag: `$TERM_PROGRAM != "WarpTerminal"`, see below for a full example.

We currently don't have support for multi-line custom prompts in bash, only zsh and fish. Unlike typical terminals which are essentially continuous character grids, each section of Warp is its own (separate) UI element. Warps default prompt does not support multi-line or right-sided prompts at this time. Improving the native Prompt is on the roadmap, however. Please see our [Prompt](../appearance/prompt.md) page for more information on custom prompts.

### Debugging

If Warp is not working with your dotfile configuration,

You can quickly set up clean configs by putting `ZDOTDIR=/` in a `~/.zshenv` file. This forces zsh to run with zero configs.

Zsh loads your configuration settings in this [order](https://zsh.sourceforge.io/Intro/intro\_3.html):

```
$ZDOTDIR/.zshenv
$ZDOTDIR/.zprofile
$ZDOTDIR/.zshrc
$ZDOTDIR/.zlogin
$ZDOTDIR/.zlogout
```

If Warp starts working correctly then Warp is incompatible with something in the current dotfiles. We can isolate what is incompatible by iteratively disabling sections of our dotfiles with the `WarpTerminal` flag until we find the culprit. If you find an incompatible tool please email us at [feedback@warp.dev](mailto:feedback@warp.dev)

```
# bash and zsh
if [[ $TERM_PROGRAM != "WarpTerminal" ]]; then
##### WHAT YOU WANT TO DISABLE FOR WARP - BELOW

    # Unsupported plugin/prompt code here

##### WHAT YOU WANT TO DISABLE FOR WARP - ABOVE
fi
```

```
# fish
if test "$TERM_PROGRAM" != "WarpTerminal"
    # Unsupported plugin/prompt code here
end
```

## Fig

### Bash and Fig

A recent version of Fig (happens as of 1.0.56 - and may also happen on earlier versions) updated the bash rcfiles in a way that prevents Warp from bootstrapping.

In order to work around this, you can disable this logic for Warp. Note that you might have to do this for `.bash_profile` _and_ `.bashrc`.

Also, Fig has a tendency to re-write these lines in these files when it updates - so you might have to do this multiple times if you are using Fig actively.

.bash\_profile

```
# Fig post block. Keep at the bottom of this file.
if [[ $TERM_PROGRAM != "WarpTerminal" ]]; then
    . "$HOME/.fig/shell/bash_profile.post.bash"
fi
```

.bashrc

```
# Fig post block. Keep at the bottom of this file.
if [[ $TERM_PROGRAM != "WarpTerminal" ]]; then
    . "$HOME/.fig/shell/bashrc.post.bash"
fi
```

### fish and Fig

Some older installations of Fig (most notably prior to September 2021) include startup scripts that are incompatible with Warp's bootstrap process. As described above in [Configuring and debugging your RC files](known-issues.md#configuring-and-debugging-your-rc-files), those scripts should be gated on a check of the `TERM_PROGRAM` environment variable. The two important files in this case are:

* `~/.config/fish/conf.d/00_fig_pre.fish`
* `~/.config/fish/conf.d/99_fig_post.fish`

## macOS

### Auto-Update on macOS Ventura

Warp may have an error opening after auto-update on macOS Ventura. This issue has been resolved for current and future releases of Warp. To avoid the issue, [update Warp](updating-warp.md) _before_ you upgrade to macOS Ventura.\
\
If you experience an error opening Warp, please try the following:

* Go to the macOS Applications folder, right-click on Warp, choose Open, then the '"Warp" is damaged' dialog will have the option to click the Open button.

<figure><img src="https://lh3.googleusercontent.com/YD_m_5N8dnKwomnPZZFs4_s3gydEzk00rXsexoZ1Po1rdhu_BT7s0zQwqGRief6XnA1q7B5J6omrT64oV2Vcq3vJBTvFj9B5YwqhNaGcUGsi5pnOipfN1Tz7NVbJlyM57E5DReZ9vQbn9urFlTGU8fk_L8bXluatW8Npd3_XEYPqA6HpK6TYI7_gWg" alt=""><figcaption></figcaption></figure>

* If the above doesn't work, [uninstall Warp](uninstalling-warp.md), then [re-install Warp](../getting-started/getting-started-with-warp.md).

### Running x86 commands with macOS Rosetta

In some cases, [CLI applications only work on x86](https://discord.com/channels/851854972600451112/1204829324847358002) so you can run Warp with Rosetta on macOS to be able to use them by doing the following.

* Go to `Finder > Applications` and search for Warp.
* Right-Click and select Get Info.
* Then check the box on Open with Rosetta.
