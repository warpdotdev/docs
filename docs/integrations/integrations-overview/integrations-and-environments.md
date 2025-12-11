# Integrations and Environments

**This page walks through the end-to-end setup:**

1. Creating an environment
2. Authorizing GitHub
3. Creating and configuring integrations (Slack / Linear)

{% hint style="info" %}
For a quickstart guide with Warp integrations, please refer to [.](./ "mention").
{% endhint %}

## How integrations work

At a high level, an **integration** wires together three things:

1. Your [Warp team](../../knowledge-and-collaboration/teams.md)
2. A remote environment that knows how to build and run your code
3. A trigger surface, like Slack or Linear, where you tag @Warp or DM the bot.
   1. Warp receives the thread/issue content.
   2. Warp spins up (or reuses) an environment based on your Docker image and setup commands.
   3. The agent clones the configured repositories, runs your setup commands, and executes the workflow.
   4. Results are posted back into Slack/Linear and reflected in your repos (i.e., in the form of PRs)

Setting up an integration consists of three high-level steps.

1. **Create an environment** for the agent to run your code inside.
2. **Authorize GitHub access** so Warp can clone repositories, write code to the correct repos, debug issues, run a cloud version of your codebase, and open pull requests.
3. **Configure** the Warp app with an integration.

{% hint style="info" %}
**You only need to do this once per Warp team**. After an integration exists, every teammate can use it. The first time a teammate triggers an agent from Slack or Linear for instance, they’ll be prompted to authorize GitHub on their own account if they want the agent to write back to repos.
{% endhint %}

## Creating an environment

#### What is an environment?

When agents run in the background or in the cloud (via Slack, Linear, etc.), they need a place to execute code. An **environment** defines that execution context.

An environment consists of:

1. A Docker image
2. A set of GitHub repositories
3. Optional setup commands

You can use one environment per codebase, or share an environment across multiple related repos (e.g. frontend + backend).

#### 1. Docker image

The Docker image is the base system where your code runs. It should include:

* Language runtimes (Node, Go, Rust, Python, etc.)
* Build tools and CLIs (e.g. cargo, npm, pip)
* Any utilities or dependencies that rarely change

**Requirements**

* The image must be **publicly accessible** on Docker Hub.
* You can validate this by running `docker pull <your-image>` locally.
* The image does not need to contain your code. Warp will handle cloning repositories into the container.

**Warp will either:**

* Use an existing official image (e.g. rust:latest, node:20-bullseye, python:3.11), or
* Help you build and push a custom image if you have a multi-language stack or more complex dependencies.

#### 2. A set of relevant Github repositories

Warp clones these into the environment each time the agent runs.

* Each environment defines the set of repos that agents can access.
  * Warp clones these repos each time an agent session starts.
  * You’ll be prompted to install the **Warp GitHub app** and grant it access to specific repos or orgs.
  * You can include **multiple repos** in a single environment, for example:
    * `your-org/frontend`
    * `your-org/backend`

**Public vs private repos**

* If you only use public repos, the agent can read them without GitHub authorization, but cannot open PRs or push changes.
* To enable write operations (PRs, branches, commits), the Warp GitHub app must have access and the triggering user must have write permissions.

#### 3. Optional setup commands

Setup commands run on every new agent session:

* They are executed after cloning repositories and before the agent starts its workflow.
* Use them for project-specific prep, such as:
  * Installing frequently changing dependencies
  * Running bootstrap scripts
  * Building artifacts or seeding test data

#### Example environments

| Project type    | Docker image                        | Repos                                                      | Example setup commands                                                                                                                                                     |
| --------------- | ----------------------------------- | ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Web dev project | `node:20-bullseye`                  | <p>your-org/frontend-react<br><br>your-org/backend-api</p> | <p><code>npm install -g pnpm</code></p><p><br><code>cd frontend-react &#x26;&#x26; pnpm install</code></p><p><br><code>cd backend-api &#x26;&#x26; pnpm install</code></p> |
| Python project  | Custom image based on `python:3.11` | your-org/cool\_python\_project                             | `cd cool_python_project && pip install -r requirements.txt`                                                                                                                |

***

### How to create an environment

You can create environments either directly through the CLI or using a guided Agent flow.

#### Option A — Create it directly via CLI

If you already know what you want:

```
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

You can inspect existing environments with: `warp environment list`

#### Option B — Use the guided setup (/create-environment)

If you’d like Warp to analyze your repos and suggest an environment configuration, use the guided setup [slash-commands.md](../../agents/slash-commands.md "mention"): `/create-environment`

You can run it:

* In a git repo directory with no arguments, or
* With one or more paths/URLs:

```
# File paths
/create-environment ./warp-internal ./warp-server

# owner/repo
/create-environment warpdotdev/warp-internal warpdotdev/warp-server

# GitHub URLs
/create-environment https://github.com/warpdotdev/warp-internal.git
```

The guided flow will:

1. Detect the repositories and their languages/toolchains.
2. Look for an existing Dockerfile or recommend an official base image.
3. If needed, generate a custom Dockerfile, build the image, and push it to **Docker Hub** (you may be prompted to log into Docker).
4. Suggest reasonable setup commands based on your scripts and package managers.
5. Create the environment through the CLI and return the environment ID.

That environment can then be reused across multiple integrations.

***

### Setting up an integration

Once you have at least one environment, you can create integrations that connect it to Slack or Linear.

```
warp integration create linear
# or
warp integration create slack
```

If you omit --environment, the CLI will show a list of environments and prompt you to choose one.

**The CLI then:**

1. Links the integration to your Warp team and environment.
2. Opens a browser flow to install the Warp app into your Slack workspace or Linear workspace.
3. Generates an **integration ID** you can later list or delete.

You can optionally attach a custom prompt that is applied to all runs for that integration:

```
warp integration create slack \
  --environment <ENV_ID> \
  --prompt "Always prefix PR titles with [WARP-AGENT] and add detailed test steps."
```

{% hint style="info" %}
For more details, see the dedicated pages for the respective integrations: [slack.md](../slack.md "mention") &[linear.md](../linear.md "mention")
{% endhint %}
