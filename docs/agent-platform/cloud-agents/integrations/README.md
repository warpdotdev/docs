---
description: >-
  Configure Warp’s first-party integrations by creating environments, connecting
  GitHub, and enabling agents to run your code and automate development
  workflows.
---

# Integrations Overview

Warp integrations let your team trigger Warp agents directly from the terminal, or from first-party tools like [Slack](slack.md) and [Linear](linear.md). Once everything is set up, agents can:

* Read conversation or issue context
* Run code inside your codebase in a remote environment
* Open pull requests and perform other multi-step agent workflows on your behalf

{% hint style="info" %}
For a full walkthrough of Warp's integrations and configurable environments, please refer to [Integrations and Environments](https://docs.warp.dev/reference/cli/integrations-and-environments).
{% endhint %}

All of this is powered by the [Oz CLI](https://docs.warp.dev/reference/cli).

***

## Quickstart

The fastest way to get Warp agents running from Slack or Linear is to create an environment with the guided flow. An **environment** defines everything the agent needs to run your code remotely, including your Docker image, repos, and setup commands.

{% embed url="https://www.youtube.com/watch?v=ahFfInVD0HQ" %}

#### 1. Run /create-environment

From Warp, run the following slash command:

```
/create-environment
```

You can run it inside any repo, or point it at multiple repos:

```
/create-environment ./frontend ./backend
/create-environment your-org/repo-name
/create-environment https://github.com/your-org/api.git
```

{% hint style="info" %}
Learn more about slash commands and how to use them in the [Slash Commands](../../capabilities/slash-commands.md) documentation.
{% endhint %}

The guided flow will:

* Detect which repos you want the agent to work with
* Identify languages, frameworks, and tools
* Suggest a Docker image (or build/push one if needed)
  * The Docker image can be your own custom image, an official base image (e.g. node, python), or one of Warp's prebuilt dev images (see [repo](https://github.com/warpdotdev/oz-dev-environments)).
* Recommend setup commands
* Create the environment and return an environment ID

This produces a ready-to-use environment that Warp can use across Slack, Linear, and terminal triggers.

#### 2. Authorize GitHub

Warp will prompt you to install or update the Warp GitHub app so the agent can read and write to the repos you included. You only need to do this once. Teammates will authorize on their first run as needed.

#### 3. Create an integration

{% hint style="info" %}
For easier setup, use the [Oz web app](../oz-web-app.md) at [oz.warp.dev](https://oz.warp.dev) to configure integrations with a guided flow. The web app works on mobile devices.
{% endhint %}

Alternatively, use the CLI:

For Slack:

```
oz integration create slack --environment <ENV_ID>
```

For Linear:

```
oz integration create linear --environment <ENV_ID>
```

The CLI opens an authorization page where you install Warp into your Slack workspace or Linear team. Once installed, everyone on your Warp team can trigger agents.

#### 4. Start using agents

In Slack:

* Tag **@Oz** in a message or thread
* Or DM the bot

In Linear:

* Tag the Oz agent on an issue

Warp will read the thread/issue, spin up your environment, run the workflow in the cloud, and post progress + PRs back into the same conversation.

***

For more details on configuring integrations and environments in Warp, please refer to [Integrations and Environments](https://docs.warp.dev/reference/cli/integrations-and-environments).
