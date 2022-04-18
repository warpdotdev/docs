# Known Issues

To see a complete list of issues and feature requests, please visit our [GitHub issues page](https://github.com/warpdotdev/warp/issues).

## Configuring and debugging your RC files

The TLDR; is that in order to build Blocks and create an IDE-like input / text editor experience, we set up [custom hooks](https://blog.warp.dev/how-warp-works/#implementing-blocks) and intercept the prompt so we can render it natively.
Unfortunately, Warp is incompatible with some ZSH themes and plugins because of this e.g. powerlvel10k.

You can disable the conflicting settings for just Warp, by placing using this flag: `$TERM_PROGRAM != "WarpTerminal"`

An example RC File:

```sh
if [[ $TERM_PROGRAM != "WarpTerminal" ]]; then
##### WHAT YOU WANT TO DISABLE FOR WARP - BELOW

    # POWERLEVEL10K
    # OH-MY-ZSH-THEMES
    # OH-MY-ZSH-PLUGINS
    # FIG
    # FZF
    # BIND keys like:
    # bindkey "^j" down-line-or-beginning-search
    # [[ -r "/usr/local/etc/profile.d/bash_completion.sh" ]] && 
    # . "/usr/local/etc/profile.d/bash_completion.sh"
    # eval "$(rbenv init -)"

##### WHAT YOU WANT TO DISABLE FOR WARP - ABOVE
fi
```

Zsh loads your configuration settings in this [order](https://zsh.sourceforge.io/Intro/intro_3.html):

```sh
$ZDOTDIR/.zshenv
$ZDOTDIR/.zprofile
$ZDOTDIR/.zshrc
$ZDOTDIR/.zlogin
$ZDOTDIR/.zlogout
```

You can quickly set up clean configs by putting `ZDOTDIR=/` in a `~/.zshenv` file.
This forces zsh to run with zero configs.

## SSH

If SSH isn’t working you can either turn off the SSH Wrapper function in the settings (note that you'll need to start a new session before a change is reflected) or try invoking the SSH binary directly:
`/usr/bin/ssh`

## Fish shell `read` command

There is an issue in Fish shell version 3.4.0 and below that causes the `read` built-in command to break Warp's integration with Fish. This means that using `read` directly or any Fish scripts that call `read` will not work as expected in Warp. That issue is resolved in the Fish repository and so should be fixed in the next release of Fish itself.

## Fish shell and Fig

Some older installations of Fig (most notably prior to September 2021) include startup scripts that are incompatible with Warp's bootstrap process. As described above in [Configuring and debugging your RC files](#configuring-and-debugging-your-rc-files), those scripts should be gated on a check of the `TERM_PROGRAM` environment variable. The two important files in this case are:

- `~/.config/fish/conf.d/00_fig_pre.fish`
- `~/.config/fish/conf.d/99_fig_post.fish`

To allow Warp to properly bootstrap, edit those files and wrap all of the contents in a check of the environment variable:

```sh
if test "$TERM_PROGRAM" != "WarpTerminal"
    # Existing bootstrap script here
end
```

## Soft wrapping

Nov 2021:
Warp does not currently support soft wrapping in the input editor.
The workaround is to use `\` and `ENTER` to continue your command on the next line.

## English-only UI

Nov 2021:
We have added character support for Chinese, Korean, and Japanese, but our UI currently only supports English.

## Vi / Vim / Neovim

Try disabling Oh-My-Tmux.
