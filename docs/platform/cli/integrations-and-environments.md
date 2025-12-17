---
description: >-
  Learn how to set up environments and integrations so you can trigger Warp
  agents from external tools.
---

# Integrations and Environments

This article describes the environment and integration setup that is required before you can trigger Warp agents from external tools, like Slack or Linear. You will learn how to:

* Create and configure the environment needed to run agents
* Connect that environment to your team
* Trigger Warp agents using Slack or Linear

{% hint style="info" %}
**You only need to complete this setup once per Warp team**. After an integration exists, anyone on the team can use it. For example, the first time a teammate triggers an agent from Slack or Linear, they’ll be prompted to authorize GitHub with their own account in order for the agent to write back to repos.
{% endhint %}

{% hint style="info" %}
For a quick start guide to Warp integrations, please see[integrations-overview.md](../../integrations/integrations-overview.md "mention").
{% endhint %}

## How integrations and environments work

Warp integrations connect external tools, like Slack or Linear, to agents that run your code in the background.

There are three main components to know:

* **Triggers** provide the context that tells Warp _what_ to run. A trigger could be a Slack message where you tag @Warp, or a Linear issue or comment.
* [**Integrations**](/broken/pages/yZxJAcV9IjTMmnS0tGpd) are what connect the trigger surface (Slack, Linear) to Warp. An integration links the trigger to your [Warp team](../../knowledge-and-collaboration/teams.md) and handles posting results to the original tool, for example, replying in Slack.
* **Environments** define how and where agents run your code. When an agent is triggered, Warp uses the environment to spin up a container, clone repositories, and execute the agent's workflow.

{% code title="Diagram of Warp integration components" %}
```
Slack or Linear
   (trigger)
        →
Warp Integration
   (connects tools to Warp)
        →
Environment
   (Docker image + repos + setup)
        →
Warp Agent
   (runs workflow, opens PRs, posts results)
```
{% endcode %}

Setting up an integration consists of three steps.

1. **Create an environment** for the agent to run your code.
2. **Authorize GitHub** so Warp can clone repositories, write code, debug issues, open pull requests, and more.
3. **Configure** the Warp app with an integration.

***

## Step 1: Creating an environment

Before you can trigger agents from Slack or Linear, you need an environment. The environment defines how and where Warp runs your code.

At a minimum, an environment includes:

* A Docker image
* One or more GitHub repositories
* Optional setup commands

Typically, you'll create **one environment per codebase** (or closely related set of repos) and reuse it across integrations.

You can create environments using a guided Agent flow, or directly through the CLI.

#### Before you begin

Make sure you have:

* A GitHub repository (or repositories) that the agent can work in.
* A publicly-accessible Docker image that can build and run your code. Official images like `node`, `python`, or `rust` work for many projects.

{% hint style="info" %}
You only need to create an environment once. It can be reused across Slack, Linear, and terminal triggers.
{% endhint %}

### Option 1: Guided environment setup (recommended)

The fastest way to get started is to use the guided environment setup. Use the `/create-environment` [slash command](../../agents/slash-commands.md) if you want Warp to analyze your repos and suggest an environment configuration.&#x20;

You can run the command inside a git repo directory with no argument, or with one or more repo paths or URLs. For example, from Warp:

```bash
# File paths
/create-environment ./warp-internal ./warp-server

# owner/repo
/create-environment warpdotdev/warp-internal warpdotdev/warp-server

# GitHub URLs
/create-environment https://github.com/warpdotdev/warp-internal.git
```

The guided flow will:

1. Detect the repositories you want the agent to work with and identify languages, frameworks, and tools
2. Look for an existing Dockerfile, recommend an official base image, or help build a custom image (if needed)
3. Suggest setup commands based on your scripts and package managers
4. Create the environment through the CLI and return an environment ID

This produces a ready-to-use environment that can immediately be connected to [Slack](../../integrations/slack.md) or [Linear](../../integrations/linear.md).

### Option 2: Create an environment with the CLI

If you already know how you want to configure your environment, you can create it directly with the CLI.

**Use this approach when:**

* You already have a custom Docker image
* You want full control over repos and setup commands
* You’re scripting or automating environment creation

From Warp:

```sh
warp environment create \
  --name <name> \
  --docker-image <image> \
  --repo <owner/repo> \
  --repo <owner/repo> \
  --setup-command "<command1>" \
  --setup-command "<command2>"
```

Key flags:

* `--name` – human-readable label for the environment.
* `--docker-image` – image name on Docker Hub.
* `--repo` – can be repeated for each repo.
* `--setup-command` – can be repeated; commands run in the order provided.

You can inspect existing environments with `warp environment list` .

For more details about environment configuration, see the [Slack](../../integrations/slack.md) and [Linear](../../integrations/linear.md) articles.

#### Example environments

<table><thead><tr><th width="168.47265625">Project type</th><th width="185.828125">Docker image</th><th>Repos</th><th>Example setup commands</th></tr></thead><tbody><tr><td>Web dev project</td><td><code>node:20-bullseye</code></td><td>your-org/frontend-react<br><br>your-org/backend-api</td><td><p><code>npm install -g pnpm</code></p><p><br><code>cd frontend-react &#x26;&#x26; pnpm install</code></p><p><br><code>cd backend-api &#x26;&#x26; pnpm install</code></p></td></tr><tr><td>Python project</td><td>Custom image based on <code>python:3.11</code></td><td>your-org/cool_python_project</td><td><code>cd cool_python_project &#x26;&#x26; pip install -r requirements.txt</code></td></tr></tbody></table>

***

## Step 2: Authorizing GitHub

Warp needs GitHub access so agents can clone your repositories and, when permitted, write code and open pull requests.

#### How GitHub Authorization works

When you create an environment or integration, Warp will prompt you to:

* Install or update the Warp GitHub app
* Grant access to the repositories in your environment

This authorization enables agents to clone repositories into the environment, create branches and commits, and open pull requests.

**Public vs private repos**

* **Public repos:** Agents can read code without authorization, but cannot write or open PRs.
* **Private repos:** The Warp GitHub App must have access and the triggering user must have write permissions.&#x20;

#### Ongoing permissions

Depending on how the GitHub app is installed in your organization:

* You may need to grant access to new repositories over time
* An organization admin may need to update the app’s permissions

You typically only need to handle this once per team, unless your repo access changes.

***

## Step 3: Setting up an integration

Once you have set up at least one environment, you can create integrations that connect it to Slack or Linear. For example, run the following command where `<ENV_ID>` is your environment ID:

```bash
warp integration create slack --environment <ENV_ID>
# or
warp integration create linear --environment <ENV_ID>
```

{% hint style="info" %}
If you omit `--environment`, the CLI will show a list of environments and prompt you to choose one.
{% endhint %}

The CLI then:

1. Links the integration to your Warp team and environment.
2. Opens a browser flow to install the Warp app into your Slack workspace or Linear workspace.
3. Generates an **integration ID** you can later list or delete.

Optionally, you can attach a custom prompt that is applied to all runs for that integration:

```bash
warp integration create slack \
  --environment <ENV_ID> \
  --prompt "Always prefix PR titles with [WARP-AGENT] and add detailed test steps."
```

{% hint style="info" %}
For more details, see the dedicated pages for [slack.md](../../integrations/slack.md "mention") and [linear.md](../../integrations/linear.md "mention")integrations.
{% endhint %}

## How are environments used at runtime?

When you trigger an agent from Slack or Linear, Warp follows a consistent, repeatable execution process using your environment.

At a high level, each run works like this:

1. **Warp receives the trigger**\
   Warp captures the message content (for example, a Slack thread or Linear issue), along with any linked context.
2. **Warp creates an execution container**\
   Warp spins up a fresh container from the Docker image defined in your environment.
3. **Repositories are cloned**\
   The GitHub repositories associated with the environment are cloned into the container.
4. **Setup commands are run**\
   Any setup commands you configured, like installing dependencies, are executed.
5. **The agent workflow runs**\
   The agent executes the task using the provided context, tools, and permissions.
6. **Results are posted back**\
   Progress updates, summaries, and results are posted back to Slack or Linear.
7. **The container is destroyed**\
   After the run completes, the container is torn down. Each run starts from a clean, isolated environment.

## Next steps

You now have everything needed to trigger Warp agents from your team’s tools. From here, you might want to:

* Add or adjust setup commands
* Switch to a custom Docker image
* Include additional repositories
* Add custom prompts for consistent agent behavior
* Create separate environments for different workflows or teams

**Additional reading**

* [Broken link](/broken/pages/rVCLQETZqLlr5BBHYy2y "mention")
* [warp-platform.md](../warp-platform.md "mention")
* [slack.md](../../integrations/slack.md "mention"), [linear.md](../../integrations/linear.md "mention"), and [github-actions.md](../../integrations/github-actions.md "mention") integrations
* [troubleshooting.md](troubleshooting.md "mention")
