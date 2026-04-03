---
description: >-
  Connect Oz cloud agents to your AWS and GCP services.
---

# Cloud Providers (Preview)

Oz cloud agents can securely access cloud providers using short-lived OpenID Connect credentials.

This page explains how to configure a cloud agent environment to automatically authenticate to your
cloud provider. Oz has built-in support for AWS and GCP, and can work with any provider that
supports OIDC tokens.

***

## Prerequisites

* A Warp account ([create an account at oz.warp.dev](https://oz.warp.dev))
* A cloud provider account

Follow the section for your cloud provider.

***

## AWS

### Step 1: Create an OIDC identity provider

The first step is to configure your AWS account to trust OIDC tokens produced by Oz.

1. Open the AWS IAM console at <https://console.aws.amazon.com/iam>.
2. Click **Identity Providers**, then click **Add provider**.
3. Set the provider type to **OpenID Connect**.
4. Set the **Provider URL** to `https://app.warp.dev`.
5. Set the **Audience** to `sts.amazonaws.com`.
6. Copy the ARN of the new identity provider, which will look like: `arn:aws:iam::<account-id>:oidc-provider/app.warp.dev`.

{% hint style="info" %}
Verify that the provider was created correctly by:
1. Clicking on the `app.warp.dev` link in the list of identity providers.
2. Clicking on **Endpoint verification**
3. Checking that the thumbprint is `08745487e891c19e3078c1f2a07e452950ef36f6`
{% endhint %}

***

### Step 2: Configure an IAM role

Next, you will need to set up an AWS IAM role with a trust policy that links it to the OIDC provider.

1. Open the AWS IAM console at <https://console.aws.amazon.com/iam>.
2. Click **Roles**, then click **Create role**.
3. Select **Custom trust policy**, and fill in the following JSON trust policy:

```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "AllowOzFederation",
			"Effect": "Allow",
			"Principal": {
				"Federated": "<oidc-provider-arn>"
			},
			"Action": "sts:AssumeRoleWithWebIdentity",
			"Condition": {
				"StringEquals": {
					"app.warp.dev:aud": "sts.amazonaws.com",
                    "app.warp.dev:sub": "<subject>"
				}
			}
		}
	]
}
```

You will need to replace:
* `<oidc-provider-arn>` with the ARN of the OIDC provider added in Step 1.
* `<subject-prefix>` with the specific Warp user or service account ID. See [the subject claim](#subject-sub) for details.

To allow multiple users, you must use a list in the subject condition:

```json
...
"Condition": {
    "StringEquals": {
        "app.warp.dev:sub": [
            "user:<uid-1>",
            "user:<uid-2>",
            "service_account:<uid-3>"
        ]
    }
}
...
```

{% hint style="info" %}
AWS trust policies currently cannot match on custom OIDC claims, such as the `teams` claim.
Support for custom subject claim formatting as a workaround is coming soon.
{% endhint %}

4. Click **Next** and add permissions policies. These policies determine what Oz agents can access
   in your AWS account.
5. Click **Next** and enter a role name and optional description.
6. Click **Create role**, then open the role and note down the role ARN. This will be of the form `arn:aws:iam::<account-id>:role/<role-name>`.

***

### Step 3: Enable AWS federation in your cloud agent environment

Finally, configure the Oz cloud agent environment to use your new AWS role.

1. Open the Oz web app at <https://oz.warp.dev>.
2. Create or edit an environment. See [Environments](../oz-web-app.md#environments) for instructions.
3. Expand the **AWS** section and enter the AWS role ARN from Step 2.
4. Save the environment.

{% hint style="warning" %}
Currently, AWS federation can only be configured in the Oz web app, not the CLI.
{% endhint %}

Oz agents running in this environment will now automatically assume the configured role when using
the `aws` CLI or a compatible SDK.

{% hint style="info" %}
Oz uses the [**Assume role with web identity**](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html#cli-configure-role-oidc)
AWS authentication mechanism. The following environment variables are set while the agent is running:
* `AWS_ROLE_ARN`: the ARN of the role configured above
* `AWS_WEB_IDENTITY_TOKEN_FILE`: the path to a temporary file containing the agent's Oz OIDC token
* `AWS_ROLE_SESSION_NAME`: a derived session name, of the form `Oz_Run_<run-id>`.
{% endhint %}

***

## GCP

### Step 1: Create a Workload Identity Pool and Provider

The Oz GCP integration uses [Workload Identity Federation](https://docs.cloud.google.com/iam/docs/workload-identity-federation).
You will need to configure a pool and provider to trust OIDC tokens produced by Oz.

These instructions use the `gcloud` tool. You may also follow the OIDC instructions in
[Configure Workload Identity Federation with other identity providers](https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-other-providers)
to use the GCP console or Terraform.

1. Create a Workload Identity Pool using the `gcloud` CLI:

```bash
gcloud iam workload-identity-pools create "<pool-id>" --location=global
```

Replace `<pool-id>` with the desired identifier for your pool, such as `oz-agent-pool`.

2. Create a Provider within the pool:

```bash
gcloud iam workload-identity-pool-providers create-oidc \
    "<provider-id>" \
    --location=global \
    "--workload-identity-pool=<pool-id>" \
    --issuer-uri="https://app.warp.dev" \
    "--attribute-mapping=google.subject=assertion.sub,google.groups=assertion.teams,attribute.environment=assertion.environment" \
    "--attribute-condition='<team-uid>' in assertion.teams"
```

Replace `<pool-id>` with the ID you used above, and `<provider-id>` with the desired identifier
for your provider, such as `oz-oidc-provider`.

Replace `<team-uid>` with the UID of your Warp team. This is the last component of your
[Admin Panel](../../../enterprise/team-management/admin-panel.md) URL. For example, if the admin
panel URL is `https://app.warp.dev/admin/abc123def456`, your team UID would be `abc123def456`.

{% hint style="warning" %}
If you do not set an attribute condition, then _any_ Oz agent will be able to use your Workload
Identity Federation provider, even if they do not belong to your team.
{% endhint %}

### Step 2: Configure IAM policies

You will need to configure IAM policies in GCP that allow Oz agents in the Workload Identity
Federation pool access to resources.

To give all Oz agents on your team read-only access to all Compute Engine resources in a project,
for example, you would run:

```bash
gcloud projects add-iam-policy-binding <project-id> \
    --member "principalSet://iam.googleapis.com/projects/<project-number>/locations/global/workloadIdentityPools/<pool-id>/attribute.teams/<team-id>" \
    --role "roles/compute.viewer"
```

See [Workload Identity Federation principal types](https://docs.cloud.google.com/iam/docs/workload-identity-federation#principal-types)
for the full syntax supported.

### Step 3: Enable Workload Identity Federation in your cloud agent environment

Finally, configure the Oz cloud agent environment to use your Workload Identity Federation provider.

1. Open the Oz web app at <https://oz.warp.dev>.
2. Create or edit an environment. See [Environments](../oz-web-app.md#environments) for instructions.
3. Expand the **GCP** section and enter the project number, pool ID, and provider ID from Step 1.
4. Save the environment.

{% hint style="warning" %}
Currently, Workload Identity Federation can only be configured in the Oz web app, not the CLI.
{% endhint %}

Oz agents running in this environment will now automatically configure
[Application Default Credentials](https://docs.cloud.google.com/docs/authentication/application-default-credentials)
to use the configured pool. Both the `GOOGLE_APPLICATION_CREDENTIALS` and `CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE`
environment variables are set, so both the `gcloud` CLI and official Google SDKs will use the Oz
federated credentials. Oz uses
[**executable-sourced credentials**](https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-other-providers#create-credential-config)
to configure ADC for automatic token rotation.

## Other Providers

To authenticate from Oz to another provider that supports OIDC federation, you can issue tokens
directly.

Within the agent environment, use the `oz federate issue-token` command to produce an OIDC token
with your provider as the audience:

```bash
oz federate issue-token --audience your-provider.com --output-format json
```

Optionally, add `--duration <duration>` to customize the token validity. This cannot exceed the
maximum runtime of an Oz agent.

You may then exchange this token for provider-specific credentials.

## OIDC Token Claims

All Oz OIDC tokens include standard claims like `iss` (issuer) and `iat` (issued at).

### Audience

The `aud` claim will reflect the default for your cloud provider. For AWS, this is always
`sts.amazonaws.com`. For GCP, it is derived from the Workload Identity Federation provider,
such as `https://iam.googleapis.com/projects/<project-number>/locations/global/workloadIdentityPools/<pool-id>/providers/<provider-id>`.

### Subject (`sub`)

The `sub` claim is set to the identity that the Oz agent is executing as. This will either be a
Warp user ID or an autogenerated account ID for team-scoped agent runs.

In addition, user OIDC tokens include an `email` claim with the user's email address.

To get possible user ID values, use the Oz API:

```bash
curl https://app.warp.dev/api/v1/agent/runs -H "Authorization: Bearer $WARP_API_KEY"
{
    "runs": [
        {
            ...
            "creator": {
                "type": "user",
                "uid": "<user-id>",
                "display_name": "User Name",
                "email": "user@warp.dev"
            }
        }
    ]
}
```

### Team

Every token includes a `teams` claim. The value will be a list with your team UID - currently, this
list only ever contains a single value.

### Oz Run

The following claims are derived from the Oz agent run:

* `run_id`: the unique identifier for the individual run. This is not suitable for configuring
  access, but is useful to log for debugging.
* `environment`: the unique identifier for the agent's [Environment](../environments.md).
* `agent_name`: the name of the [Skill](../skills-as-agents.md) that the agent was invoked with.
* `skill_spec`: the canonical identifier for the skill, such as `github-org/github-repo:.warp/skills/skill-name/SKILL.md`.
* `host`: the execution host. This will either be `warp`, for Warp-hosted agents, or the worker ID if [self-hosting](../self-hosting.md).

### Example Token

The following OIDC token references an Oz agent running as a specific Warp user:

```json
// JWT Header
{
    "typ": "JWT",
    "alg": "ES256",
    "kid": "<example-key-id>"
}
// JWT Payload
{
    "aud": ["sts.amazonaws.com"],
    "sub": "user:<example-user-id>",
    "email": "user@warp.dev",
    "teams": ["<example-team-id>"],
    "run_id": "<example-id>",
    "environment": "<example-id>",
    "agent_name": "<example-name>",
    "skill_spec": "<example-spec>",
    "host": "warp",
    "iss": "https://app.warp.dev",
    "jti": "<example-id>",
    "exp": 1775210175,
    "iat": 1775206575,
    "nbf": 1775206575
}
