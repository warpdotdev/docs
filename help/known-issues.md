# Known Issues

To see a complete list of issues and feature requests, please visit our [GitHub issues page](https://github.com/warpdotdev/warp/issues).

## SSH

To enable Blocks over SSH, Warp uses an SSH Wrapper function; navigate to settings > features if you need to disable it.

Note: You'll need to start a new session before a change is reflected) or try invoking the SSH binary directly:
`/usr/bin/ssh`

## Soft wrapping

Nov 2021:
Warp does not currently support soft wrapping in the input editor.
Press `SHIFT`-`ENTER` or use `\` and `ENTER` to continue your command on the next line.

## English-only UI

Nov 2021:
We have added character support for Chinese, Korean, and Japanese, but our UI currently only supports English.

## Fish shell `read` command

There is an issue in Fish shell version 3.4.0 and below that causes the `read` built-in command to break Warp's integration with Fish. This means that using `read` directly or any Fish scripts that call `read` will not work as expected in Warp. That issue is resolved in the Fish repository and so should be fixed in the next release of Fish itself.

## Configuring and debugging your RC files

In order to support Blocks ([custom hooks](https://blog.warp.dev/how-warp-works/#implementing-blocks)), a native Input Editor experience, etc. we have to build custom support for a subset of shell functionality (decouple functionality from the shell and move to the terminal). Unfortunately, this leads to Warp being incompatible with various tools and plugins e.g. Powerlevel10k.

You can however, **disable the conflicting settings for just Warp** using this flag: `$TERM_PROGRAM != "WarpTerminal"`, see below for a full example.

### Debugging

If Warp is not working with your dotfile configuration,

You can quickly set up clean configs by putting `ZDOTDIR=/` in a `~/.zshenv` file.
This forces zsh to run with zero configs.

Zsh loads your configuration settings in this [order](https://zsh.sourceforge.io/Intro/intro_3.html):

```sh
$ZDOTDIR/.zshenv
$ZDOTDIR/.zprofile
$ZDOTDIR/.zshrc
$ZDOTDIR/.zlogin
$ZDOTDIR/.zlogout
```

If Warp starts working correctly then Warp is incompatible with something in the current dotfiles.
We can isolate what is incompatible by iteratively disabling sections of our dotfiles with the `WarpTerminal` flag until we find the culprit. When you do find what's incompatible please let us know and we'll add it to the list below.

```sh
# Bash and Zsh
if [[ $TERM_PROGRAM != "WarpTerminal" ]]; then
##### WHAT YOU WANT TO DISABLE FOR WARP - BELOW

    # POWERLEVEL10K

##### WHAT YOU WANT TO DISABLE FOR WARP - ABOVE
fi
```

```sh
# Fish
if test "$TERM_PROGRAM" != "WarpTerminal"
    # Existing bootstrap script here
end
```

### List of incompatible tools

- iterm shell integration
  - usually looks like `test -e "${HOME}/.iterm2_shell_integration.zsh" && source "${HOME}/.iterm2_shell_integration.zsh" || true`
- Oh-My-Tmux.
- OH-MY-ZSH-THEMES
  - avit
- OH-MY-ZSH-PLUGINS
- FZF
- BIND keys like:
  - bindkey "^j" down-line-or-beginning-search
- [[ -r "/usr/local/etc/profile.d/bash_completion.sh" ]] && "/usr/local/etc/profile.d/bash_completion.sh"
- eval "$(rbenv init -)"
- grml-zsh-config
- FIG

## Fig

### Bash and Fig

A recent version of Fig (happens as of 1.0.56 - and may also happen on earlier versions) updated the bash rcfiles in a way that prevents Warp from bootstrapping.

In order to work around this, you can disable this logic for Warp. Note that you might have to do this for `.bash_profile` _and_ `.bashrc`.

Also, Fig has a tendency to re-write these lines in these files when it updates - so you might have to do this multiple times if you are using Fig actively.

.bash_profile

```sh
# Fig post block. Keep at the bottom of this file.
if [[ $TERM_PROGRAM != "WarpTerminal" ]]; then
    . "$HOME/.fig/shell/bash_profile.post.bash"
fi
```

.bashrc

```sh
# Fig post block. Keep at the bottom of this file.
if [[ $TERM_PROGRAM != "WarpTerminal" ]]; then
    . "$HOME/.fig/shell/bashrc.post.bash"
fi
```

### Fish and Fig

Some older installations of Fig (most notably prior to September 2021) include startup scripts that are incompatible with Warp's bootstrap process. As described above in [Configuring and debugging your RC files](#configuring-and-debugging-your-rc-files), those scripts should be gated on a check of the `TERM_PROGRAM` environment variable. The two important files in this case are:

- `~/.config/fish/conf.d/00_fig_pre.fish`
- `~/.config/fish/conf.d/99_fig_post.fish`
