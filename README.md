# Warp Docs

Documentation for [Warp](https://www.warp.dev) — the Agentic Development Environment — and the [Oz](https://oz.warp.dev) agent platform.

Built with [Astro](https://astro.build) + [Starlight](https://starlight.astro.build).

## Getting started

```bash
npm install
npm run dev
```

Open [http://localhost:4321](http://localhost:4321) to preview locally.

## Kapa AI setup

The Ask AI header integration requires a public Kapa Custom Frontend integration ID.

Set these environment variables before running the site locally or deploying it:

```bash
PUBLIC_KAPA_INTEGRATION_ID=your_custom_frontend_integration_id
PUBLIC_KAPA_PROJECT_NAME="Warp Docs" # optional
PUBLIC_KAPA_WELCOME_MESSAGE="I can help answer questions about Warp and point you to the most relevant docs." # optional
```

`PUBLIC_KAPA_INTEGRATION_ID` is required by Astro's env schema, so `npm run dev` and `npm run build` will fail fast if it is missing.

## Commands

| Command          | Description                              |
| :--------------- | :--------------------------------------- |
| `npm run dev`    | Start local dev server at localhost:4321 |
| `npm run build`  | Build production site to `./dist/`       |
| `npm run preview`| Preview the production build locally     |

## Content structure

Content lives in `src/content/docs/`, organized by topic (matching GitBook spaces):

```
src/content/docs/
├── index.mdx                       # Root landing page
└── agent-platform/                 # Agent Platform topic
    ├── index.mdx                   # Topic landing page
    ├── getting-started/
    ├── capabilities/
    ├── local-agents/    (planned)
    └── cloud-agents/    (planned)
```

Each top-level directory becomes a tab in the sidebar via `starlight-sidebar-topics`. Sidebar structure is configured in `astro.config.mjs`.

### Adding pages

- Create `.mdx` files in the appropriate directory under `src/content/docs/`
- Use `index.mdx` for directory landing pages
- Add the page to the sidebar config in `astro.config.mjs`
- Images go in `src/assets/` (Astro optimizes them automatically)

### Content format

Pages use MDX with Starlight components. Key syntax (migrated from GitBook):

- **Callouts**: `:::note`, `:::tip`, `:::caution`, `:::danger`
- **Tabs**: `<Tabs>` / `<TabItem>` (import from `@astrojs/starlight/components`)
- **Code blocks**: Standard fenced code blocks with Expressive Code features (titles, line highlighting, `wrap`)

## Known issues

- **`@astrojs/sitemap` override**: `package.json` pins `@astrojs/sitemap` to 3.3.0 via npm overrides to work around a zod v3/v4 compatibility issue in newer versions. This can be removed once the upstream fix lands.
