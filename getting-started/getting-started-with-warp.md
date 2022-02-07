# Getting Started with Warp

A note on accessing Warp (June 2021):

Currently, our product is in closed beta mode—we’ve invited only a select group of users to help us test out Warp.

[Request access here.](https://form.typeform.com/to/yrwMkgtj)

We have been granting access to people every week. You can also join our [Discord](https://www.warp.dev/discord)—we drop invites every week in the `#invite-codes` channel.

## Compatibility

For now, there are a few known limitations that we are actively working on:

* Mac-only
* Locally, the terminal integrates with only Bash and Zsh (fish support is coming soon).
  * We do not support `PROMPT_COMMAND` in Bash right now (working on this!).
* When you [SSH](https://docs.warp.dev/features/ssh), we start a Bash shell on the remote host.
  * We built a [wrapper](https://docs.warp.dev/features/ssh#how-it-works) around SSH to make Warp features possible.

If your default shell is zsh, your aliases typically do not transfer over. Other shells are unsupported for now.

* When you open a subshell (a shell within a shell), we do not set it up for Warp - instead it works like a normal terminal session.
* You’ll need a Github account to log in.

Our [known issues](https://docs.warp.dev/help/known-issues) section elaborates how to set up common tools:\
[Vi / Vim / NeoVim](https://github.com/warpdotdev/warp/discussions/451), [tmux](https://github.com/warpdotdev/warp/discussions/501), and Oh-My-Zsh.

## Logging into Warp

During our closed beta, we require a login so we can interact with you, get your feedback, and focus on improving the app. After installing Warp for the first time, you will be prompted to log in using your GitHub account (we only get access to the associated email address - [read our approach to privacy](https://www.warp.dev/privacy)).

Opening the app is the only time you need an active Internet connection. Otherwise, Warp is a fully-native, local app and runs fine with no internet connection whatsoever (although you will lose access to some of our cooler features).

### Onboarding survey

As part of our beta, we ask a few questions within the app after you sign up. The survey is completely optional—you can skip all questions if you’d like.

Why do we ask these? Understanding how you use the terminal helps us improve the product and prioritize the right features. For example, we might find that backend engineers spend more time with multiple terminal tabs open, less experienced developers copy output from blocks more often, or engineers at large companies spend more time using CLIs.

Thanks for joining our beta and helping us improve Warp!
