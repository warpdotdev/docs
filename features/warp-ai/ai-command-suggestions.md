# AI Command Suggestions

## What is it

AI Command Suggestions allows you to convert natural language descriptions into shell commands that can be executed and saved as [Workflows in Warp Drive](../warp-drive/workflows.md). This feature is backed by OpenAI's APIs and is completely opt-in.

_Note_: Currently, you need to be online to use this feature. If this feature doesn't work, it is possible that your ISP or firewall is blocking the calls to `app.warp.dev`

## How to access it

1. Press `` CTRL-` `` or type `#` into the Text Input Editor to search by natural language.
2. Type in the input box what you'd like to do. For example, "replace string in file".
3. Results are generated in real time, and you can keep the current prompt or modify the prompt to generate new commands.
4. When you've found the command you want to execute, it can be run or saved as a Workflow onto Warp Drive to easily recall it in the future.

_Note:_ If you experience any issues with AI Command Suggestions, please see our known issues for [troubleshooting steps](../../help/known-issues.md#online-features-ai-command-block-sharing-referrals-etc.).

## How it works

{% embed url="https://www.loom.com/share/424a763ef0c8455e8269e541301968f2?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" %}
AI Command Suggestions Demo
{% endembed %}

## Privacy

Warp does not store any commands or prompts that users send. Any provided prompts are sent to OpenAI. [Reference OpenAI’s privacy policy](https://openai.com/policies/privacy-policy).
