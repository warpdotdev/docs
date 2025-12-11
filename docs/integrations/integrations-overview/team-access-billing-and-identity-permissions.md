# Team Access, Billing, and Identity Permissions

This page explains how access to integrations and Ambient Agents work across your Warp team, how billing and credits apply, and how Warp maps user identities across Slack, Linear, and GitHub.

***

## Team Access

Integrations are created at the team level, not per-user. Once a Slack or Linear integration is installed, everyone on your Warp team can use **@Warp** in the connected workspace. The integration behaves the same way for all teammates, and everyone shares the same underlying environment configuration.

When someone triggers an ambient agent for the first time, Warp may prompt them to grant GitHub authorization so the agent can open pull requests or push branches under their identity. This allows each run to use the correct permissions without requiring additional setup from an admin.

#### Team and billing requirements

Integrations and ambient agents run inside Warp’s cloud, which means usage is billed based on [AI credits](../../support-and-billing/plans-and-pricing/ai-credits.md). Credits are shared at the team level.

Your team must meet the following requirements to run integrations:

* You must be on a plan that supports **add-on credits** ([add-on-credits.md](../../support-and-billing/plans-and-pricing/add-on-credits.md "mention"))&#x20;
  * Supported: **Build, Business**
  * Not supported: Pro, Turbo, Lightspeed, legacy Business.
* Your team needs at least **20 add-on credits** available to run an integration
* All integration usage is billed to the team’s add-on credit balance

Integrations do not draw from personal monthly base credits. If the team’s balance reaches zero, integrations and ambient agents will pause until credits are added.

{% hint style="info" %}
If you’re on an enterprise plan, please reach out to your dedicated Warp representative with any billing questions related to integrations.
{% endhint %}

### Identity mapping

Warp maps your identity across systems using the email address on your account.

* Your Slack or Linear email must match your Warp account email
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

Warp stores only the content required for the agent to complete its task. You can message @Warp directly, mention it in channels, or tag it on specific issues depending on the integration.

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

## Additional Notes: How Ambient Agents Use Credits

Ambient agents can run automatically in the background when activated by a trigger such as a Slack mention, a Linear update, or a scheduled task. These runs require compute and model usage, which translates to AI credit consumption.

#### How credit usage works

Ambient agents and integrations draw from your team’s add-on credit balance.

* When a trigger activates, the agent starts a run and consumes credits until the workflow completes.
* Depending on the integration and implementation of Ambient Agents, these runs may not require anyone to be present unless your workflow is designed to ask for input.

#### Who configures triggers and workflows

All triggers and instructions used by ambient agents are defined and controlled by your team’s authorized users.

* Admins or other authorized users decide which triggers exist, when they fire, and what the agent should do in response.
* Trigger behavior and the agent’s instructions (system prompts, workflow steps, repo access, etc.) are fully managed by your admins or other designated users.

#### Staying aware of usage

Because triggers and instructions are configured by your team, any AI credits used when an agent runs are billed to your team’s add-on credit balance.

* It’s the team’s responsibility to manage triggers, confirm they behave as intended, and monitor usage.
* Reviewing triggers, prompts, and agent behavior periodically helps ensure that credit usage aligns with expectations.

***
