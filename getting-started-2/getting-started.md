# Getting Started

As of June, 2021:

**A note on accessing Warp**: currently our product is in closed beta mode—we’ve invited only a select group of users to help us test out Warp.

[Join the waitlist here](https://form.typeform.com/to/yrwMkgtj?typeform-medium=embed-snippet)! We’ll be letting people off the waitlist every week.

## Compatibility

For now, there are a few known limitations that we are actively working on:

* Mac-only
* Locally, the terminal integrates with only Bash and Zsh (fish support is coming soon).
  * We do not support `PROMPT_COMMAND` in Bash right now (working on this!).
* Via SSH, we start a Bash shell on the remote host. If your default shell is zsh, your aliases typically do not transfer over. Other shells are unsupported for now.
* You’ll need a Github account to [log in](getting-started.md#logging-into-warp).
* When you open a subshell (a shell within a shell), we do not set it up for Warp - instead it works like a normal terminal session. &#x20;

## Logging into Warp

When we publicly launch Warp, no login will be required.

However, during our closed beta, we require a login so we can interact with our users, get their feedback and focus on improving the app. After installing Warp for the first time, you will be prompted to log in using your Github account (we only get access to the associated email address - [read our approach to privacy](https://www.warp.dev/privacy)).&#x20;

Opening the app is the only time you need an active Internet connection. Otherwise, Warp is a fully-native, local app and runs fine with no internet connection whatsoever (although you will lose some of our cooler features).

### Onboarding survey

As part of our beta, we ask a few questions within the app after you sign up. The survey is completely optional—you can skip all questions if you’d like.

Why are we asking these? Understanding you helps us make the product better for you and prioritize the right features in our roadmap. For example, we might find that backend engineers spend more time with multiple terminal tabs open, less experienced developers copy and paste from the terminal more often, or engineers at large companies spend more time using CLIs. That information helps us make Warp better for you!

As a reminder, these questions are completely optional. Thanks for joining our beta and helping us improve the product before we release it to the public!

