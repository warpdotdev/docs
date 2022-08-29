# Prompt

Warp has a built in prompt that shows your current working directory (cwd) and also git branch information when in a git directory.

## Custom prompts

Enable custom prompt support by navigating to Settings > Features and toggling on "Honor user's custom prompt (PS1) setting."

![Honor PS1](../.gitbook/assets/prompt-custom_prompt.gif)

## PS1 Compatibility Table

| Shell    | Tool            | Does it work? |
| -------- | --------------  | -------------- |
| Bash/zsh | PS1             |  Working       |
| Bash     | SBP             |  Coming soon   |
| Bash/zsh | Starship        |  Working       |
| zsh      | oh-my-zsh       |  Working       |
| zsh      | prezto          |  Working       |
| zsh      | powerlvel10k    |  Not supported |
| zsh      | zplug           |  Not supported |
| Bash/zsh | powerline-shell |  Coming soon   |
| SSH      |                 |  Working       |

## Prompt not working?

We don’t currently support multi-line or right sided prompts. The Input Editor is a separate UI element from the Prompt; this is actually what enables a modern text editor experience. Improving the native Prompt is on the roadmap.

If you’re having issues with prompts, please see our [Known Issues](../help/known-issues.md#configuring-and-debugging-your-rc-files) for more information on supported tools and troubleshooting steps.

### iTerm2

The iTerm2 shell integration breaks Warp and you're custom prompt will not be able to be visible with this on. If you're coming from iTerm please check your dotfiles for it. We advice disabling the integration just for Warp like so:

```sh
if [[ $TERM_PROGRAM != "WarpTerminal" ]]; then
##### WHAT YOU WANT TO DISABLE FOR WARP - BELOW

test -e "${HOME}/.iterm2_shell_integration.zsh" && source "${HOME}/.iterm2_shell_integration.zsh"

##### WHAT YOU WANT TO DISABLE FOR WARP - ABOVE
fi
```

### Powerlevel10K (P10K)

We don't currently support P10K chances are we won't be able to. The tldr; it's tricky because of how we also use the prompt_command in Warp and because P10K can be installed standalone or as an Oh-My-Zsh plugin, each of which results in different problems and requires special handling.

You can also disable P10K just for Warp like so:

```sh
if [[ $TERM_PROGRAM != "WarpTerminal" ]]; then
##### WHAT YOU WANT TO DISABLE FOR WARP - BELOW

    # POWERLEVEL10K

##### WHAT YOU WANT TO DISABLE FOR WARP - ABOVE
fi
```

### Context Chips

Context Chips is an idea we have for how the future of terminal prompts could like, i.e. prompts that support dynamic refreshing, mouse interactions, and extends customizability via an open spec that developers can build on. Learn more via our Twitter thread, where we also shared some Figma mocks.
