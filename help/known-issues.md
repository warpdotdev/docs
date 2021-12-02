# Known Issues

To see a complete list of issues and to follow along, please visit our GitHub issues page: [https://github.com/warpdotdev/warp/issues](https://github.com/warpdotdev/warp/issues).

**SSHing to the same machine more than once.**

If you log in to the same machine more than once, you will notice this following message:

`ControlSocket /Users/<your-username>/.ssh/bad89d3452f63f92c2a9a56e8d78b02dfebacf1e already exists, disabling multiplexing`

This is due to our multiplexing setting, which we will be updating soon.&#x20;

**Lack of soft wrapping.**

Typing a long command into the input editor doesn’t soft wrap. The effect of this is that right now it’s very hard to work with long commands on a single line in warp. The workaround is to use `\n` to continue your command on the next line.

**No tmux, or split plane support.**

Please upvote [https://github.com/warpdotdev/warp/issues/14](https://github.com/warpdotdev/warp/issues/14) if you are interested in this feature!

**No custom prompt support.**

We will be adding this shortly.

**English-only UI.**

**Fig is not supported.**

If you have Fig installed, Warp won't start. To fix this, you need to comment out the following lines in your **\~/.zprofile , \~/.zshrc, \~/.profile, and \~/.bash\_profile**

```
### FIG ENV VARIABLES ####
[ -s ~/.fig/shell/pre.sh ] && source ~/.fig/shell/pre.sh
### END FIG ENV VARIABLES ####
```

**Powerlevel 10K Instant Prompt is not supported.**

If you are using Powerlevel10k Instant Prompt, Warp won't start. To fix this, you need to comment out the following lines in your **\~/.zshrc:**

```
# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi
```



Want Warp to support something? File an issue at [https://github.com/warpdotdev/warp/issues](https://github.com/warpdotdev/warp/issues).
