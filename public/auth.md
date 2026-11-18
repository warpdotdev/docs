# Warp Agent API Authentication

The Warp Agent API lets clients create, manage, and query Warp cloud agent runs.

## Authentication

Most operations require HTTP Bearer authentication. The token is a Warp API key or a supported Warp-issued user token. Automated clients use an API key:

```http
Authorization: Bearer YOUR_WARP_API_KEY
```

Create, rotate, and revoke keys using the [API key management guide](https://docs.warp.dev/agents/cli/oz-cli/api-keys/). Store API keys in an environment variable or secret manager rather than in source code.

Two public-artifact operations can be called without authentication when the requested artifact is public:

- `GET /agent/artifacts/{artifactUid}`
- `GET /agent/artifacts/{artifactUid}/download`

Private artifacts and all other operations require a valid API key or user token with access to the requested resource.

## Endpoints and reference

- Base URL: `https://app.warp.dev/api/v1`
- Human-readable reference: `https://docs.warp.dev/api`
- OpenAPI JSON: `https://docs.warp.dev/openapi.json`
- OpenAPI YAML: `https://docs.warp.dev/openapi.yaml`
