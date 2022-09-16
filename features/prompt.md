# Prompt

Warp has a built in prompt that shows your current working directory (cwd) and also git branch information when in a git directory.

## Custom prompts

Enable custom prompt support by navigating to Settings > Features and toggling on "Honor user's custom prompt (PS1) setting."

{% embed url="https://www.loom.com/share/ef24cac454024ac9be423345f15c7e27" %}
Custom Prompt Demo
{% endembed %}

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

Here we outline the underlying cause of some common pain points regarding prompts. tldr; if your prompt is not working consider disabling it just for Warp like so:

### Workaround

```sh
# Bash and Zsh
if [[ $TERM_PROGRAM != "WarpTerminal" ]]; then
    # OMZ
    # POWERLEVEL10K
    # RPS1
fi
```

See [Known Issues](./../help/known-issues.md) for more info.

### Why some custom prompts are not supported

In order to enable Blocks and other features, we've built uses custom wrappers that parse the data the shell outputs (read [How Warp Works](https://www.warp.dev/blog/how-warp-works) or our [blog post on PS1](https://www.warp.dev/blog/whats-so-special-about-ps1) for more details). Warp's prompt section is a UI element that's generated after parsing information from your prompt setup and unfortunately we're not able to parse multiline prompts or right sided prompts at this time.

Improving our native prompt by adding support for [Git status indicators](https://github.com/warpdotdev/Warp/issues/67), among other things is on our roadmap!

### Known bug: prompt appears within the Input Editor or autosuggestion

If the right-handed side of your custom prompt ends up in the Input Editor, it's because Warp does not currently support right-handed custom prompts. As a stop-gap you can disable the `RPS1` variable or your custom prompt entirely just for Warp.

## Known bug: multi-line prompt is compressed into a single line

If you have custom PS1 turned on, you might realize that the contents of the prompt have been concatenated into a single line; Warp does not currently support multiline prompts.  
As a stopgap, consider disabling your custom prompt just for Warp using the Warp conditional flag like above:
`[[ $TERM_PROGRAM != "WarpTerminal" ]];`

### iTerm2's Shell Integration

The iTerm2 shell integration breaks Warp and you're custom prompt will not be able to be visible with this on. If you're coming from iTerm please check your dotfiles for it. We advise disabling the integration just for Warp like so:

```sh
if [[ $TERM_PROGRAM != "WarpTerminal" ]]; then
test -e "${HOME}/.iterm2_shell_integration.zsh" && source "${HOME}/.iterm2_shell_integration.zsh"
fi
```

### Powerlevel (P10K and P9K)

Powerlevel prompts are also not supported; these are particulary tricky because powerlevel can be installed standalone or as an Oh-My-Zsh plugin, each of which results in different problems and requires special handling.

### Context Chips

Context Chips is an idea we have for how the future of terminal prompts could like, i.e. prompts that support dynamic refreshing, mouse interactions, and extends customizability via an open spec that developers can build on. Learn more via our Twitter thread, where we also shared some Figma mocks.
