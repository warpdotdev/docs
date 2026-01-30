# Table of contents

* [Technical Reference](README.md)

## CLI

* [Warp CLI](cli/README.md)
* [Integrations and Environments](cli/integrations-and-environments.md)
* [Troubleshooting](cli/troubleshooting.md)

## API & SDK

* [Agent API & SDK](api-and-sdk/README.md)
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
