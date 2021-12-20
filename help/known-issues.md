# Known Issues

To see a complete list of issues and feature requests, please visit our [GitHub issues page](https://github.com/warpdotdev/warp/issues).

## Vi / Vim / Neovim

Try disabling Oh-My-Tmux.

In your [vimrc](https://github.com/warpdotdev/warp/discussions/451) set:

`hi Normal guifg=#bbbbbb guibg=#333333 gui=NONE`

## Soft wrapping

Nov 2021:
Warp does not currently support soft wrapping in the input editor.
The workaround is to use `\` and `ENTER` to continue your command on the next line.

## Custom prompt support

Nov 2021:
We are working on this! See configuring and debugging your rc files.
We are also soliciting feedback on custom prompts in this [GitHub Discussion](https://github.com/warpdotdev/warp/discussions/422).

## SSH

If you log in to the same machine more than once, you will notice the following message:
`ControlSocket /Users/<your-username>/.ssh/bad89d3452f63f92c2a9a56e8d78b02dfebacf1e already exists, disabling multiplexing`

This is due to our [multiplexing setting](https://docs.warp.dev/features/ssh), which we will be updating soon.

If SSH isn’t working you can try invoking the SSH binary directly:
`usr/bin/ssh`

## English-only UI

Nov 2021:
We have added character support for Chinese, Korean, and Japanese, but our UI currently only supports English.

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

### Is this an interactive session? (bash)

To determine within a startup script whether or not Bash is running interactively, test the value of the ‘-’ special parameter.
It contains i when the shell is [interactive](https://www.gnu.org/software/bash/manual/html_node/Is-this-Shell-Interactive_003f.html).

```sh
case "$-" in
*i*) echo This shell is interactive ;;
*) echo This shell is not interactive ;;
esac
```

Alternatively, startup scripts may examine the variable PS1; it is unset in non-interactive shells, and set in interactive shells.

```sh
if [ -z "$PS1" ]; then
        echo This shell is not interactive
else
        echo This shell is interactive
fi
```
