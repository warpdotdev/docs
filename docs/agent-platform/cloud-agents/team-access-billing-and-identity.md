# Access, Billing, and Identity Permissions

This page explains how access to cloud agents works for both individual users and teams, how billing and credits apply, and how Warp maps user identities across integrations.

***

## Overview: Individual vs Team Access

Cloud agents can be used in two ways:

**Individual users** (without a team):
* Can run cloud agents via CLI or API
* Can use normal Warp credits, [Cloud Agent Credits](https://docs.warp.dev/support-and-community/plans-and-billing/credits#cloud-agent-credits), or a Build plan with available credits
* Agents run on Warp-hosted infrastructure
* Cannot use integrations (Slack, Linear) or self-hosted agents

**Teams** (users who are part of a [Warp team](https://docs.warp.dev/warp/knowledge-and-collaboration/teams)):
* All individual capabilities, plus:
* Can use integrations (Slack, Linear) to trigger agents
* Can self-host agents on their own infrastructure (Enterprise only)
* Share team-level configuration (environments, secrets, integrations)
* Team must be on Build, Max, or Business plan with at least 20 credits (any type) for cloud agents and integrations

***

## Individual Access

Individual users can run cloud agents via the CLI or API without being part of a team.

**How it works:**

* Run agents using `oz agent run-cloud` or the Oz Agent API
* Credits are drawn from your normal Warp credits, Cloud Agent Credits (if available), or Build plan credits
* Agents execute on Warp-hosted infrastructure

**What you can do:**

* Run cloud agents from CI/CD pipelines
* Trigger agents programmatically via API
* Use personal secrets for authentication

**What requires a team:**

* Integrations (Slack, Linear)
* Self-hosted agent execution
* Team secrets and shared configuration

***

## Team Access

A [Warp team](https://docs.warp.dev/knowledge-and-collaboration/teams) is a group of users who share configuration and collaborate on cloud agents. Teams can be created on any plan, including Free.

**What teams enable:**

* **Integrations** - Create Slack and Linear integrations that all team members can use
* **Shared configuration** - Team-level environments, secrets, and settings
* **Self-hosting** - Run agents on your own infrastructure (Enterprise only)
* **Team visibility** - Shared observability into agent runs and history

Integrations are created at the team level, not per-user. Once a Slack or Linear integration is installed, everyone on your Warp team can use **@Oz** in the connected workspace. The integration behaves the same way for all teammates, and everyone shares the same underlying environment configuration.

When someone triggers a cloud agent for the first time, Warp may prompt them to grant GitHub authorization so the agent can open pull requests or push branches under their identity. This allows each run to use the correct permissions without requiring additional setup from an admin.

#### Requirements for integrations

Integrations and [cloud agents](cloud-agents-overview.md) run inside Warp's cloud, which means usage is billed based on [credits](https://docs.warp.dev/support-and-community/plans-and-billing/credits).

Your team must meet the following requirements to run integrations:

* You must be on a plan that supports **[Reload Credits (add-on credits)](https://docs.warp.dev/support-and-community/plans-and-billing/add-on-credits)**.
  * Supported: **Build, Max, Business**
  * Not supported: Pro, Turbo, Lightspeed, legacy Business.
* Your team needs at least **20 credits** available to run cloud agents and integrations (any type of Warp credits work)

When a user triggers an agent through an integration (like Slack or Linear), the run draws from credits in a specific order. It starts with any [Cloud Agent Credits](https://docs.warp.dev/support-and-community/plans-and-billing/credits#cloud-agent-credits) the user has, then moves to the user's base credits, followed by the team's Reload Credits, and finally the user's own Reload Credits. Enterprises may have different payment options and credit plans that affect this flow. If all applicable credit sources are exhausted, integrations and cloud agents will not work until credits are added.

{% hint style="info" %}
If you're on an Enterprise plan, please reach out to [warp.dev/contact-sales](https://warp.dev/contact-sales) with any billing questions related to integrations.
{% endhint %}

### Identity mapping

Warp needs a reliable way to know which person a cloud agent run is acting for, across Warp, Slack, Linear, and GitHub.

* Slack uses a dedicated account-linking flow to map a Slack user to their Warp account. This is the recommended path for Slack-triggered agents, since it doesn’t rely on email matching.
* Linear currently maps identities using email address matching. Your Linear email must match your Warp account email for Warp to correctly attribute and scope agent runs.
* Each teammate must authorize GitHub before an agent can write PRs or push branches on their behalf
* Agents always operate using the GitHub permissions of the triggering user

This ensures runs are scoped to what the user is allowed to see and modify, and that ownership of PRs remains clear across teams and repositories.

***

## Data & permissions

#### Slack / Linear

Installing the Warp app gives Warp access to the Slack channels or Linear teams where the app is installed. Access cannot be narrowed to individual issues or threads.

**When a run is triggered, Warp receives:**

* The content of the tagged thread or issue
* Relevant surrounding context used to build the agent prompt

Warp stores only the content required for the agent to complete its task. You can message @Oz directly, mention it in channels, or tag it on specific issues depending on the integration.

#### GitHub

Warp’s behavior in GitHub is defined by two layers of control:

1. **The Warp GitHub App installation scope**
   * Determines which organizations and repositories Warp can read and write to
   * Can be edited at any time in GitHub settings
2. **Permissions of the triggering user**
   * Agents inherit the user’s read/write privileges
   * Agents cannot elevate permissions, see additional repos, or write to repos the user cannot access

**In practice, agents can only operate on repositories that:**

* Are included in the environment configuration
* Are accessible to both the GitHub app and the triggering user

***

## Additional Notes: How cloud agents use credits

Cloud agents can run automatically in the background when activated by a trigger such as a Slack mention, a Linear update, or a scheduled task. These runs require compute and model usage, which translates to credit consumption.

#### How credit usage works

How credits are consumed depends on how the agent run is triggered and authenticated:

**User-triggered runs** (CLI with personal API key, Slack, Linear, or the Warp app):

* Runs are tied to the triggering user's identity
* Credits are consumed starting with any credit grants specifically allocated for cloud agent usage, then the user's base credits, followed by the team's Reload Credits, and finally the user's own Reload Credits

**Team API key runs** (fully automated or headless workflows):

* Runs are not tied to any individual user
* Only the team's Reload Credit pool is used—no individual base credits are available
* Ideal for CI/CD pipelines, scheduled tasks, and other automated workflows

For more details on creating and using API keys, see [API Keys](https://docs.warp.dev/reference/cli/api-keys).

{% hint style="info" %}
When a user triggers an agent via Slack or Linear, the run follows the standard credit precedence, starting with any credit grants specifically allocated for cloud agent usage. This applies even for integrations—as long as the triggering user's identity can be mapped to their Warp account.
{% endhint %}

#### Who configures triggers and workflows

All triggers and instructions used by cloud agents are defined and controlled by your team’s authorized users.

* Admins or other authorized users decide which triggers exist, when they fire, and what the agent should do in response.
* Trigger behavior and the agent’s instructions (system prompts, workflow steps, repo access, etc.) are fully managed by your admins or other designated users.

#### Staying aware of usage

Because triggers and instructions are configured by your team, any credits used when an agent runs are billed to your team's Reload Credit balance.

* It’s the team’s responsibility to manage triggers, confirm they behave as intended, and monitor usage.
* Reviewing triggers, prompts, and agent behavior periodically helps ensure that credit usage aligns with expectations.
