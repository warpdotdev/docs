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

If you're prompt isn't working please check out our ["Configuring and debugging your RC files"](https://docs.warp.dev/help/known-issues#configuring-and-debugging-your-rc-files) section of our Known Issues section.

### Powerlevel10K (P10K)o

We don't currently support P10K chances are we won't be able to. The tldr; it's tricky because of how we also use the prompt_command in Warp and because P10K can be installed standalone or as an Oh-My-Zsh plugin, each of which results in different problems and requires special handling.

You can also disable P10K just for Warp like so:

```sh
if [[ $TERM_PROGRAM != "WarpTerminal" ]]; then
##### WHAT YOU WANT TO DISABLE FOR WARP - BELOW

    # POWERLEVEL10K

##### WHAT YOU WANT TO DISABLE FOR WARP - ABOVE
fi
```