# Warp Docs

Source content for [docs.warp.dev](https://docs.warp.dev), the documentation site for [Warp](https://www.warp.dev) and the [Oz](https://oz.warp.dev) agent platform.

<p align="center">
  <a href="https://www.warp.dev">Website</a>
  ·
  <a href="https://docs.warp.dev">Docs</a>
  ·
  <a href="https://www.warp.dev/code">Code</a>
  ·
  <a href="https://www.warp.dev/agents">Agents</a>
  ·
  <a href="https://github.com/warpdotdev/warp">Warp repo</a>
  ·
  <a href="CONTRIBUTING.md">Contributing</a>
</p>

## About

Warp is an agentic development environment, born out of the terminal. This repository contains the public documentation for Warp's terminal, editor, agents, collaboration features, API, and support content.

The site is built with [Astro](https://astro.build) and [Starlight](https://starlight.astro.build). Content is written in MDX and organized under `src/content/docs/`.

## Building the project

Node.js 20.19+, 22.12+, or 24 is required. The supported versions match Astro 6's runtime requirements and are enforced in `package.json`.

Install dependencies:

```bash
npm install
```

Start the local development server:

```bash
npm run dev
```

Open [http://localhost:4321](http://localhost:4321) to preview the docs site locally.

## Environment variables

The site runs without local environment variables. To enable optional integrations like the Ask AI button and the "Was this helpful?" widget, copy `.env.example` to `.env` and fill in the public values:

```bash
cp .env.example .env
```

## Repository structure

Content lives in `src/content/docs/`, organized by product area:

* **`terminal/`** - Warp terminal features, including blocks, sessions, editor behavior, and appearance.
* **`code/`** - Code editor, code review, and Git worktree documentation.
* **`getting-started/`** - Installation, quickstarts, migration guides, and onboarding content.
* **`knowledge-and-collaboration/`** - Warp Drive, teams, and Admin Panel documentation.
* **`agent-platform/`** - Agent Platform docs, including agent capabilities, local agents, CLI agents, and cloud agents.
* **`reference/`** - CLI, API, SDK, keyboard shortcut, and technical reference docs.
* **`support-and-community/`** - Troubleshooting, billing, privacy, and support content.
* **`enterprise/`** - Enterprise features, SSO, and team management documentation.
* **`changelog/`** - Public release changelog.
* **`university/`** - Guides and tutorials.

Sidebar structure is configured in `astro.config.mjs`. Redirects are configured in `vercel.json`.

## Contributing

The Warp docs are open source, and contributions are welcome. For substantial changes, open or comment on an issue first so the docs team can align on scope. Small fixes like typo corrections, broken links, and minor clarifications can go straight to a pull request.

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the full contribution flow, local setup, style expectations, and pull request checklist.

## Agent skills

The `.warp/skills/` directory contains [Oz agent skills](https://docs.warp.dev/agent-platform/capabilities/skills) used by the Warp docs team for automated workflows, including style linting, link checking, changelog updates, and terminology syncing. The skills are included for transparency and as examples of how Oz skills can automate documentation workflows. See [`warpdotdev/oz-skills`](https://github.com/warpdotdev/oz-skills) for more examples.

Some skills depend on internal Warp repositories (`warp-internal`, `warp-server`) and won't run end-to-end without access to those codebases.

## Support and questions

* Browse the published [Warp docs](https://docs.warp.dev/).
* Join the [Slack Community](https://go.warp.dev/join-preview) to connect with other users and contributors.
* Open a [GitHub issue](https://github.com/warpdotdev/docs/issues) for docs bugs, missing coverage, or suggested improvements.

## Code of Conduct and security

This project follows Warp's [Code of Conduct](https://github.com/warpdotdev/.github/blob/main/CODE_OF_CONDUCT.md). Report security issues through the private channels described in Warp's [security policy](https://github.com/warpdotdev/.github/blob/main/SECURITY.md), not through public issues.

## License

Warp Docs is licensed under the [MIT License](LICENSE).
