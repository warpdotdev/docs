---
description: >-
  To see a complete list of issues and feature requests, please visit our GitHub
  issues page.
---

# Known Issues

* We do not support `PROMPT_COMMAND` in Bash right now (working on this!).
* When you [SSH](../features/ssh.md), we start a Bash shell on the remote host. We built a wrapper around SSH to make Warp features possible.
* If your default shell is zsh, your aliases typically do not transfer over. Other shells are unsupported for now.
* When you open a subshell (a shell within a shell), we do not set it up for Warp - instead it works like a normal terminal session.

Links to popular GitHub issues:

* [Vi / Vim / NeoVim](https://github.com/warpdotdev/warp/discussions/451)
* [tmux](https://github.com/warpdotdev/warp/discussions/501)
* [Oh-My-Zsh Prompts](https://github.com/warpdotdev/Warp/issues/936)

## SSH

To enable Blocks over SSH, Warp uses an SSH Wrapper function; navigate to settings > features if you need to disable it.

Note: You'll need to start a new session before a change is reflected or try invoking the SSH binary directly: `/usr/bin/ssh`

## Auto-Update on macOS Ventura

Warp may have an error opening after auto-update on macOS Ventura. This issue has been resolved for current and future releases of Warp. To avoid the issue, [update Warp](updating-warp.md) _before_ you upgrade to macOS Ventura.\
\
If you experience an error opening Warp, please try the following:

* Go to the macOS Applications folder, right-click on Warp, choose Open, then the '"Warp" is damaged' dialog will have the option to click the Open button.

<figure><img src="https://lh3.googleusercontent.com/YD_m_5N8dnKwomnPZZFs4_s3gydEzk00rXsexoZ1Po1rdhu_BT7s0zQwqGRief6XnA1q7B5J6omrT64oV2Vcq3vJBTvFj9B5YwqhNaGcUGsi5pnOipfN1Tz7NVbJlyM57E5DReZ9vQbn9urFlTGU8fk_L8bXluatW8Npd3_XEYPqA6HpK6TYI7_gWg" alt=""><figcaption></figcaption></figure>

* If the above doesn't work, [uninstall Warp](uninstalling-warp.md), then [re-install Warp](../getting-started/getting-started-with-warp.md).

## English-only UI

Nov 2021: We have added character support for Chinese, Korean, and Japanese, but our UI currently only supports English.

## Fish shell `read` command

There is an issue in Fish shell version 3.4.0 and below that causes the `read` built-in command to break Warp's integration with Fish. This means that using `read` directly or any Fish scripts that call `read` will not work as expected in Warp. That issue is resolved in the Fish repository and so should be fixed in the next release of Fish itself.

## Configuring and debugging your RC files

In order to support Blocks ([custom hooks](https://blog.warp.dev/how-warp-works/#implementing-blocks)), a native Input Editor experience, etc. we have to build custom support for a subset of shell functionality (decouple functionality from the shell and move to the terminal). Unfortunately, this leads to Warp being incompatible with various tools and plugins e.g. Powerlevel10k.

You can however, **disable the conflicting settings for just Warp** using this flag: `$TERM_PROGRAM != "WarpTerminal"`, see below for a full example.

We currently don't have support for multi-line prompts, unlike typical terminals which are essentially continuous character grids, each section of Warp is its own (separate) UI element. The native Prompt does not support multi-line at this time and does not support right sided prompts. Improving the native Prompt is on the roadmap, however. Please see our [Prompt](broken-reference) page for more information on custom prompts.

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
# Bash and Zsh
if [[ $TERM_PROGRAM != "WarpTerminal" ]]; then
##### WHAT YOU WANT TO DISABLE FOR WARP - BELOW

    # POWERLEVEL10K

##### WHAT YOU WANT TO DISABLE FOR WARP - ABOVE
fi
```

```
# Fish
if test "$TERM_PROGRAM" != "WarpTerminal"
    # Existing bootstrap script here
end
```

### List of incompatible tools

* iterm shell integration
  * usually looks like `test -e "${HOME}/.iterm2_shell_integration.zsh" && source "${HOME}/.iterm2_shell_integration.zsh" || true`
* Powerlevel10K
* Spaceship
* OH-MY-ZSH-THEMES
  * e.g. avit, spaceship, maybe more ...
* OH-MY-ZSH-PLUGINS
* Oh-My-Tmux
* zsh4h (ZSH for Humans)
* FZF
* BIND keys like:
  * bindkey "^j" down-line-or-beginning-search
* \[\[ -r "/usr/local/etc/profile.d/bash\_completion.sh" ]] && "/usr/local/etc/profile.d/bash\_completion.sh"
* eval "$(rbenv init -)"
* grml-zsh-config
* FIG, z, other completion plugins

## Some settings from Starship

```toml
[custom]
disabled = true
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

### Fish and Fig

Some older installations of Fig (most notably prior to September 2021) include startup scripts that are incompatible with Warp's bootstrap process. As described above in [Configuring and debugging your RC files](known-issues.md#configuring-and-debugging-your-rc-files), those scripts should be gated on a check of the `TERM_PROGRAM` environment variable. The two important files in this case are:

* `~/.config/fish/conf.d/00_fig_pre.fish`
* `~/.config/fish/conf.d/99_fig_post.fish`
