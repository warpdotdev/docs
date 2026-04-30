# Contributing to Warp Docs

Thanks for helping improve Warp's documentation. This guide explains how to propose changes, work locally, and open a pull request for review.

## TL;DR

* Fork the repository, create a branch, make your changes locally, and open a pull request.
* Open or comment on an issue before starting substantial changes. Small fixes can go straight to a pull request.
* Use an agent if it helps you draft, edit, test, or review the change.
* Run `npm run build` and `npm run typecheck` before opening a pull request. Run `npm run lint` if [Trunk](https://trunk.io/) is installed locally.
* Keep pull requests focused, accurate, and easy to review.

## How contributing works

These docs use a standard open-source contribution flow:

1. Find a docs issue, identify a missing or incorrect page, or notice a small improvement.
2. For substantial changes, open or comment on an issue to align with the docs team before drafting. Substantial changes include new pages, major rewrites, navigation changes, redirects, and content that changes how Warp features are explained.
3. Fork the repository and create a branch for your work.
4. Make the change locally. You can write the docs yourself or use an agent to help draft, edit, and validate the contribution.
5. Run the relevant checks.
6. Open a pull request from your fork.
7. Respond to review feedback from the Warp team.

Small fixes do not need an issue first. Examples include typo fixes, broken links, outdated screenshots, formatting fixes, and short clarifications.

## Set up the project

Install [Node.js](https://nodejs.org/) 20.19+, 22.12+, or 24. These versions match Astro 6's supported runtimes.

Clone your fork and install dependencies:

```bash
git clone https://github.com/YOUR_USERNAME/docs.git
cd docs
npm install
```

Start the local development server:

```bash
npm run dev
```

Open [http://localhost:4321](http://localhost:4321) to preview the docs site.

The site runs without local environment variables. To enable optional integrations like the Ask AI button and the "Was this helpful?" widget, copy `.env.example` to `.env` and fill in the public values:

```bash
cp .env.example .env
```

## Work on a change with an agent

You can use any coding agent to help with a contribution, including Warp's built-in Agent Mode, Claude Code, Codex, Gemini CLI, or another tool. A useful agent workflow is:

1. Use the repository's included AGENTS.md and related skills.
2. Ask the agent to draft the smallest change that resolves the issue or improves the page.
3. Review the draft or code change yourself for accuracy, tone, and scope.
4. Ask the agent to run available checks and fix any failures.
5. Review the final diff before opening the pull request.
6. If you use an agent to submit a PR on your behalf, ensure the agent uses the repository's pull request template.

You are responsible for the pull request you submit, even when an agent helped write it. Verify commands, links, screenshots, and product behavior before requesting review.

## Content guidelines

Read `AGENTS.md` before drafting or editing docs. It contains the style guide, terminology standards, content type guidance, repository structure, and validation commands used by the Warp docs team.

Follow these baseline expectations:

* **Be accurate** - Verify product behavior, commands, UI labels, links, and file paths before publishing.
* **Write for users** - Lead with what the reader can accomplish, then explain how to do it.
* **Use consistent terminology** - Match product names and feature names from `AGENTS.md`.
* **Keep changes scoped** - Avoid mixing unrelated rewrites, formatting changes, and content updates in one pull request.
* **Update navigation when needed** - If you add or move a page, update `astro.config.mjs`.
* **Add redirects when needed** - If you rename or move a published page, add a redirect in `vercel.json`.
* **Use the right asset location** - Put optimized PNGs in `src/assets/` and GIFs in `public/assets/`.

## Validate your work

Build the site before opening a pull request:

```bash
npm run build
```

Run typechecking:

```bash
npm run typecheck
```

Run linting if [Trunk](https://trunk.io/) is installed:

```bash
npm run lint
```

Format files if Trunk is installed:

```bash
npm run fmt
```

If a command fails, fix the issue or explain the failure in your pull request description.

## Open a pull request

Create a focused pull request from your fork using the repository's [pull request template](https://github.com/warpdotdev/docs/blob/main/.github/PULL_REQUEST_TEMPLATE.md).

If you're using Warp or Oz to prepare your pull request, the [`create_pr` skill](.warp/skills/create_pr/SKILL.md) can review the branch, format the description, and open the PR for you.

All pull requests should include a summary of what changed and why, related issues, screenshots when helpful, and known follow-ups or out-of-scope work.

Keep pull requests small enough to review confidently. If the change affects multiple areas, split it into separate pull requests when possible.

## Review process

The Warp docs team reviews pull requests for:

* **Technical accuracy** - The content matches current product behavior.
* **Reader value** - The change helps users accomplish a task or understand a concept.
* **Style consistency** - The writing follows `AGENTS.md`.
* **Site health** - The build passes, links work, assets render, and navigation is correct.
* **Scope control** - The pull request stays focused on one logical change.

Reviewers may ask for edits before merging. Respond by pushing updates to the same branch and commenting when the pull request is ready for another look.

## Code of Conduct

This project adopts the [Contributor Covenant](https://www.contributor-covenant.org/) (v2.1) as its code of conduct. All contributors and maintainers are expected to follow it in every project space. See Warp's [Code of Conduct](https://github.com/warpdotdev/.github/blob/main/CODE_OF_CONDUCT.md) for the full text, or report violations to warp-coc@warp.dev.

## Reporting security issues

See Warp's [security policy](https://github.com/warpdotdev/.github/blob/main/SECURITY.md) for our security disclosure policy and private reporting channels. **Do not open public issues for security vulnerabilities.**

## Getting help

* Browse the [Warp docs](https://docs.warp.dev/).
* Join the [Slack Community](https://go.warp.dev/join-preview) to ask questions and connect with other contributors.
* Open a [GitHub issue](https://github.com/warpdotdev/docs/issues) for docs bugs, missing coverage, or suggested improvements.
