# Table of contents

* [Reference](README.md)

## CLI

* [Oz CLI](cli/README.md)
* [Quickstart](cli/quickstart.md)
* [API Keys](cli/api-keys.md)
* [Agent Profiles](cli/agent-profiles.md)
* [MCP Servers](cli/mcp-servers.md)
* [Skills](cli/skills.md)
* [Warp Drive Context](cli/warp-drive.md)
* [Integration Setup](cli/integration-setup.md)
* [Troubleshooting](cli/troubleshooting.md)

## API & SDK

* [Oz Agent API & SDK](api-and-sdk/README.md)
* ```yaml
  props:
    models: true
    downloadLink: false
  type: builtin:openapi
  dependencies:
    spec:
      ref:
        kind: openapi
        spec: warp-public-agent-api
  ```
* [Demo: Sentry monitoring with SDK](api-and-sdk/demo-sentry-monitoring-with-sdk.md)
* [Troubleshooting](api-and-sdk/troubleshooting/README.md)
  * [Errors](api-and-sdk/troubleshooting/errors/README.md)
    * [insufficient\_credits](api-and-sdk/troubleshooting/errors/insufficient-credits.md)
    * [feature\_not\_available](api-and-sdk/troubleshooting/errors/feature-not-available.md)
    * [external\_authentication\_required](api-and-sdk/troubleshooting/errors/external-authentication-required.md)
    * [not\_authorized](api-and-sdk/troubleshooting/errors/not-authorized.md)
    * [invalid\_request](api-and-sdk/troubleshooting/errors/invalid-request.md)
    * [resource\_not\_found](api-and-sdk/troubleshooting/errors/resource-not-found.md)
    * [budget\_exceeded](api-and-sdk/troubleshooting/errors/budget-exceeded.md)
    * [integration\_disabled](api-and-sdk/troubleshooting/errors/integration-disabled.md)
    * [integration\_not\_configured](api-and-sdk/troubleshooting/errors/integration-not-configured.md)
    * [operation\_not\_supported](api-and-sdk/troubleshooting/errors/operation-not-supported.md)
    * [environment\_setup\_failed](api-and-sdk/troubleshooting/errors/environment-setup-failed.md)
    * [content\_policy\_violation](api-and-sdk/troubleshooting/errors/content-policy-violation.md)
    * [conflict](api-and-sdk/troubleshooting/errors/conflict.md)
    * [authentication\_required](api-and-sdk/troubleshooting/errors/authentication-required.md)
    * [resource\_unavailable](api-and-sdk/troubleshooting/errors/resource-unavailable.md)
    * [internal\_error](api-and-sdk/troubleshooting/errors/internal-error.md)
