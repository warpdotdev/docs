// @ts-check
import { defineConfig, envField } from 'astro/config';
import remarkGfm from 'remark-gfm';
import react from '@astrojs/react';
import sitemap from '@astrojs/sitemap';
import starlight from '@astrojs/starlight';
import starlightLlmsTxt from 'starlight-llms-txt';
import starlightSidebarTopics from 'starlight-sidebar-topics';
import pageTitleOverride from './src/plugins/page-title-override.ts';
import { varsTransformPlugin } from './src/plugins/vars-transform.ts';
import vercel from '@astrojs/vercel';
import { sidebarTopics } from './src/sidebar.ts';
import docsMarkdownIntegration from './src/integrations/docs-markdown-integration.js';

// https://astro.build/config
export default defineConfig({
	site: 'https://docs.warp.dev',
	// Explicitly register remark-gfm so GitHub-Flavored Markdown (notably
	// pipe tables) is reliably applied to .mdx content. Astro enables gfm by
	// default, but the @astrojs/mdx 5.x + @astrojs/markdown-remark 7.2.0
	// version pairing stopped auto-applying it, which made markdown tables
	// render as raw `| ... |` text. Registering the plugin here restores it.
	markdown: { remarkPlugins: [remarkGfm] },
	env: {
		schema: {
			PUBLIC_KAPA_INTEGRATION_ID: envField.string({
				context: 'client',
				access: 'public',
				optional: true,
			}),
			PUBLIC_KAPA_PROJECT_ID: envField.string({
				context: 'client',
				access: 'public',
				optional: true,
			}),
			PUBLIC_RUDDERSTACK_WRITE_KEY: envField.string({
				context: 'client',
				access: 'public',
				optional: true,
			}),
			// IMPORTANT: If this host ever changes (e.g. switching from the
			// app.warp.dev proxy to a direct *.dataplane.rudderstack.com URL),
			// the `connect-src` directive in vercel.json must be updated to
			// match. A mismatch causes the browser to silently block all
			// analytics events with no visible error.
			PUBLIC_RUDDERSTACK_DATA_PLANE_URL: envField.string({
				context: 'client',
				access: 'public',
				optional: true,
			}),
			SUPPORT_HANDOFF_ENDPOINT_URL: envField.string({
				context: 'server',
				access: 'secret',
				optional: true,
			}),
			SUPPORT_HANDOFF_SHARED_SECRET: envField.string({
				context: 'server',
				access: 'secret',
				optional: true,
			}),
		},
	},
	integrations: [
		react(),
		sitemap(),
		starlight({
			// Site title kept as 'Warp' to match the suffix used by the legacy
			// GitBook docs (e.g. `<title>Page | Warp</title>` and og:site_name).
			title: 'Warp',
			logo: {
				light: './src/assets/warp-logo-light.svg',
				dark: './src/assets/warp-logo-dark.svg',
				replacesTitle: true,
			},
			editLink: {
				baseUrl: 'https://github.com/warpdotdev/docs/edit/main/',
			},
			lastUpdated: true,
			// Keep long lines unwrapped so code blocks use horizontal scrolling.
			// This aligns docs behavior with the side chat renderer and preserves
			// exact line shape for commands and snippets.
			expressiveCode: {
				defaultProps: {
					wrap: false,
				},
				// IMPORTANT: Expressive Code's Vite plugin rewrites Shiki's bundled
				// theme registry (shiki/dist/themes.mjs) and strips every theme not
				// listed as a *string* in its `themes` config. Starlight passes its
				// themes as objects, so the registry is emptied for the entire Vite
				// module graph — including the Kapa side-chat island, whose runtime
				// createHighlighter(['github-light', 'github-dark']) then throws
				// "theme is not included in this bundle" and falls back to plaintext.
				// Keeping the registry intact restores chat code block highlighting.
				// Only the requested themes are ever fetched at runtime (lazy chunks),
				// so this does not bloat the pages served to visitors.
				removeUnusedThemes: false,
				// Map languages Shiki doesn't bundle to a safe fallback. PromQL
				// blocks live in platform/self-hosting/monitoring.mdx;
				// without this alias every build emits noisy "language could not be
				// found" warnings while still falling back to plaintext.
				shiki: {
					langAlias: {
						promql: 'text',
					},
				},
			},
			head: [
				// SEO + PWA parity with the legacy GitBook docs. These were emitted
				// on every page on docs.warp.dev today; Starlight does not produce
				// them by default. Per-page OG/Twitter tags (image, branded title,
				// twitter:title/description) live in src/components/CustomHead.astro.
				{
					tag: 'meta',
					attrs: { name: 'robots', content: 'index, follow' },
				},
				{
					tag: 'meta',
					attrs: { name: 'mobile-web-app-capable', content: 'yes' },
				},
				{
					tag: 'meta',
					attrs: { name: 'apple-mobile-web-app-capable', content: 'yes' },
				},
				{
					tag: 'meta',
					attrs: { name: 'apple-mobile-web-app-title', content: 'Warp' },
				},
				{
					tag: 'meta',
					attrs: { name: 'apple-mobile-web-app-status-bar-style', content: 'black' },
				},
				{
					tag: 'link',
					attrs: { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' },
				},
			],
			customCss: ['./src/styles/custom.css', './src/styles/warp-components.css', './src/styles/kapa.css'],
			components: {
				Head: './src/components/CustomHead.astro',
				// Header drops the middle Search slot (Scalar-style: search lives
				// inside the sidebar, see CustomSidebar.astro) and adds the Kapa
				// "Ask AI" launcher to the right group.
				Header: './src/components/CustomHeader.astro',
				// Sidebar prepends Starlight's built-in <Search /> as a Scalar-style
				// pill at the top, then re-renders the topic tabs and default
				// sidebar nav (replacing starlight-sidebar-topics' own override).
				Sidebar: './src/components/CustomSidebar.astro',
				Footer: './src/components/FeedbackFooter.astro',
				PageTitle: './src/components/CustomPageTitle.astro',
				PageSidebar: './src/components/CustomPageSidebar.astro',
				// Inline-SVG SiteTitle override to eliminate logo flicker on full
				// document navigations (View Transitions are intentionally disabled
				// — see CustomHead.astro). The override inlines the logo SVGs in
				// HTML so the logo paints in the same frame as the rest of the
				// header, instead of arriving a few frames late as an <img> decode.
				SiteTitle: './src/components/CustomSiteTitle.astro',
			},
			routeMiddleware: './src/routeData.ts',
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/warpdotdev' },
			],
			plugins: [
				starlightSidebarTopics(sidebarTopics),
				pageTitleOverride(),
				// Generates /llms.txt, /llms-full.txt, /llms-small.txt at build time.
				// Restores parity with the legacy GitBook docs which served
				// /llms.txt and /llms-full.txt; /llms-full.txt alone had ~310k
				// impressions / 115 clicks in GSC over the last 90 days and is
				// widely consumed by AI agents.
				starlightLlmsTxt({
					projectName: 'Warp',
					optionalLinks: [
						{
							label: 'Oz Agent API (OpenAPI spec, YAML)',
							url: 'https://docs.warp.dev/openapi.yaml',
							description: 'Machine-readable OpenAPI 3.0 specification for the Oz Agent API.',
						},
						{
							label: 'Oz Agent API (OpenAPI spec, JSON)',
							url: 'https://docs.warp.dev/openapi.json',
							description: 'Machine-readable OpenAPI 3.0 specification (JSON format) for the Oz Agent API.',
						},
					],
				// Excludes pages that cause a stack overflow in hast-util-to-text
				// due to their size. The upstream plugin only applies `exclude` to
				// llms-small.txt; our patch (patches/starlight-llms-txt+0.8.1.patch)
				// extends it to llms-full.txt and custom sets as well.
				exclude: ['support-and-community/community/open-source-licenses'],
					description:
						'Documentation for Warp, the agentic development environment. Covers Warp Terminal, Warp Agents, and the Oz platform for cloud agents and orchestration at scale.',
					customSets: [
						{ label: 'Terminal', description: 'Warp Terminal features and configuration.', paths: ['terminal/**'] },
						{ label: 'Agents', description: 'Warp\'s agents: capabilities, local agents, and CLI agents.', paths: ['agents/**'] },
						{ label: 'Warp Agent CLI', description: 'The Warp Agent CLI: agent conversations, shell commands, permissions, and configuration in any terminal.', paths: ['agents/cli/**'] },
						{ label: 'Oz Platform', description: 'Warp\'s Oz platform: cloud agents, orchestration, triggers, integrations, environments, harnesses, and self-hosting.', paths: ['platform/**'] },
						{ label: 'Code', description: 'Code editor, code review, and Git worktrees.', paths: ['code/**'] },
						{ label: 'Enterprise', description: 'Enterprise features, SSO, team management, and security.', paths: ['enterprise/**'] },
						{ label: 'Getting Started', description: 'Installation, quickstart, and migration guides.', paths: ['index', 'quickstart', 'getting-started/**'] },
						{ label: 'Knowledge and Collaboration', description: 'Warp Drive, teams, and the Admin Panel.', paths: ['knowledge-and-collaboration/**'] },
						{ label: 'Reference', description: 'CLI and API reference.', paths: ['reference/**'] },
						// All support-and-community/ pages. open-source-licenses.mdx is excluded
						// globally above (stack overflow in hast-util-to-text); the patch ensures
						// it's excluded from this custom set as well.
						{ label: 'Support', description: 'Troubleshooting, billing, and privacy.', paths: ['support-and-community/**'] },
						{ label: 'Guides', description: 'Task-oriented walkthroughs and tutorials.', paths: ['guides/**'] },
						{ label: 'Changelog', description: 'Warp release notes by year.', paths: ['changelog/**'] },
					],
				}),
			],
		}),
		docsMarkdownIntegration(),
	],
	adapter: vercel(),
	vite: {
		plugins: [varsTransformPlugin()],
	},
});
