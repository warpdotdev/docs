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

| Project type    | Docker image                        | Repos                                                      | Example setup commands                                                                                                                                                            |
| --------------- | ----------------------------------- | ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Web dev project | `node:20-bullseye`                  | <p>your-org/frontend-react<br><br>your-org/backend-api</p> | <p><code>npm install -g pnpm</code></p><p><br><code>cd frontend-react &#x26;&#x26; pnpm install</code></p><p></p><p><br><code>cd backend-api &#x26;&#x26; pnpm install</code></p> |
| Python project  | Custom image based on `python:3.11` | your-org/cool\_python\_project                             | `cd cool_python_project && pip install -r requirements.txt`                                                                                                                       |

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

If you’d like Warp to analyze your repos and suggest an environment configuration, use the guided setup  [slash-commands.md](../../agents/slash-commands.md "mention"): `/create-environment`

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

***

### Team access and identity mapping

Integrations are scoped to your Warp team, not to a single user. If you create a Slack or Linear integration for your team, everyone on that team can use @Warp in the configured workspace.

#### Team and billing requirements

To use integrations:

* **Your team must be on a plan that supports add-on credits**
  * **Supported**: Build and Business (new)
  * Not supported (legacy plans): Pro, Turbo, Lightspeed, legacy Business. Learn more about these plan changes in [ai-faqs.md](../../agents/ai-faqs.md "mention").
* Your team must have **at least 20 add-on** ([reload-credits-add-on-credits.md](../../support-and-billing/plans-and-pricing/reload-credits-add-on-credits.md "mention")) **credits available**
* Integrations run entirely on usage-based pricing
  * They do not draw from an individual user’s monthly base credits
  * All usage is billed to the team’s add-on credit balance

If your team does not meet these requirements or run out of [reload-credits-add-on-credits.md](../../support-and-billing/plans-and-pricing/reload-credits-add-on-credits.md "mention"), integrations will not run.

{% hint style="info" %}
If you’re on an enterprise plan, please reach out to your dedicated Warp representative with any billing questions related to integrations.
{% endhint %}

#### Identity mapping

Warp maps identities by email address:

* The email on your Slack or Linear account must match the email on your Warp account
* Each teammate must authorize GitHub the first time they trigger an integration if they want agents to open PRs or push branches on their behalf

### Data & permissions

#### Slack / Linear

* When you install the Warp app:
  * Warp gains access to the Slack channels or Linear teams where the app is installed.
  * Access cannot currently be restricted to specific individual threads or tickets within that workspace/team.
  * For each run, Warp collects:
    * The thread or issue content you tagged (and relevant context, such as previous messages in that thread).
  * Warp only stores the content that becomes part of the agent prompt.
  * Warp does not store unrelated workspace data.

You can DM the Warp bot directly, mention it in channels, or tag it on specific issues/tickets, depending on the integration.

#### GitHub

**Warp’s GitHub behavior is constrained by two layers:**

1. Installation scope of the Warp GitHub app
   * When installing the app, you choose which orgs and repos Warp can access.
   * This can be changed later in your GitHub settings.
2. Permissions of the user who triggered the run
   * When an agent runs, it uses the GitHub permissions of the triggering user.
   * If the user only has read access, agents cannot open PRs or push branches.
   * Agents cannot escalate permissions or access repos the user cannot see.

**Practical implications:**

* Warp can only clone, read, and write to repos that:
  * Are included in the environment definition and
  * Are visible to both the Warp GitHub app and the triggering user.

***

## Troubleshooting

### Environments

#### How do I see what environment my integration is using?

List your integrations:

```
warp integration list
```

This shows each integration, its ID, and the environment it’s linked to. Use this to confirm which environment to inspect or update before making changes.

#### How do I see what’s inside that environment?

Once you know the environment ID, run:

```
warp environment get <ENV_ID>
```

This prints the full configuration, including:

* The **environment ID** (used in other commands)
* The **name**
* The **Docker image**
* Associated **repos**

This is the most reliable way to verify what the agent will see when it runs.

#### How do I add or remove repos and setup commands?

Use `warp environment` update. You can modify environments incrementally without recreating them.

**Add a repo:**

```
warp environment update <ENV_ID> --repo owner/repo
```

**Remove a repo:**

```
warp environment update <ENV_ID> --remove-repo owner/repo
```

**Add a setup command:**

```
warp environment update <ENV_ID> --setup-command "your command"
```

**Remove a setup command (must match exactly):**

```
warp environment update <ENV_ID> --remove-setup-command "exact command"
```

Notes:

* Warp may prompt you to adjust GitHub app permissions when adding repos.
* Setup commands run in the order they are defined.

#### **How do I delete an environment?**

If an environment is no longer needed:

```
warp environment delete <ID>
```

Only do this once you’ve confirmed no active integrations are relying on that environment. If an integration points to a deleted environment, requests from Slack/Linear will fail until you create a new integration with a valid environment.

### Integrations

#### **How do I figure out what environment my integration is using?**

List your integrations:

```
warp integration list
```

This shows each integration, its ID, and the environment it’s attached to. Use this when you’re unsure which environment to update or delete.

#### **I created a new environment, but don’t see it when running warp integration create**

Check:

1. Environment exists and is healthy: `warp environment list`
2. You’re on the correct Warp team. Make sure your local CLI is logged into the same team where the environment was created.
   1. If both look correct and the environment still doesn’t appear, recreate it and confirm there were no errors during creation.

### GitHub & repo access issues

#### **I’m being asked to authorize GitHub when creating/using an environment**

This happens when:

* You add a repo that Warp doesn’t have access to yet, or
* You personally haven’t granted the Warp GitHub app permissions for that repo.

Follow the GitHub popup flow to install/adjust the Warp GitHub app.

#### **The agent can’t open PRs or push changes to my repo**

Check the following:

1. **Repo is part of your environment**.&#x20;
   1. Make sure the repo is listed in: `warp environment get <id>`&#x20;
2. **Warp GitHub app has access to that repo**
   1. In GitHub’s settings, confirm the Warp app is installed and that the repo is selected.
3. **You have write access**
   1. The agent inherits your GitHub permissions. If you only have read access, Warp can’t open PRs or push branches on your behalf.

### Docker image & environment failures

#### **I see errors like “pull access denied” or “repository does not exist”**

Check:

1. The Docker image name and tag are correct.
2. The image is public on Docker Hub.
3. You can pull it locally: `docker pull <image_name>`

If local docker pull fails, fix the image visibility/name first, then recreate or update the environment with a working image.

#### **The agent can’t find tools or runtimes inside the environment**

This usually means the Docker image is missing required dependencies. Fix by either:

* Updating the Dockerfile used to build the image, then pushing a new version to Docker Hub and updating the environment with the new image, or
* Adding additional setup commands to install the missing tools: `warp environment update --setup-command "apt-get update && apt-get install -y "`
