// @ts-check
import { defineConfig, envField } from 'astro/config';
import react from '@astrojs/react';
import sitemap from '@astrojs/sitemap';
import starlight from '@astrojs/starlight';
import starlightLlmsTxt from 'starlight-llms-txt';
import starlightSidebarTopics from 'starlight-sidebar-topics';
import pageTitleOverride from './src/plugins/page-title-override.ts';
import vercel from '@astrojs/vercel';
import { sidebarTopics } from './src/sidebar.ts';
import docsMarkdownIntegration from './src/integrations/docs-markdown-integration.js';

// https://astro.build/config
export default defineConfig({
	site: 'https://docs.warp.dev',
	env: {
		schema: {
			PUBLIC_KAPA_INTEGRATION_ID: envField.string({
				context: 'client',
				access: 'public',
				optional: true,
			}),
			PUBLIC_PUSHFEEDBACK_PROJECT_ID: envField.string({
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
			// Soft-wrap long lines by default. Expressive Code defaults to
			// `overflow-x: auto` for `<pre>`, which combined with macOS's
			// auto-hidden scrollbars made wide lines silently truncate.
			// `wrap: true` adds the `.wrap` class so EC's `white-space: pre-wrap`
			// kicks in; leading indents are preserved via its `span.indent` rule.
			expressiveCode: {
				defaultProps: {
					wrap: true,
				},
			},
			head: [
				// SEO + PWA parity with the legacy GitBook docs. These were emitted
				// on every page on docs.warp.dev today; Starlight does not produce
				// them by default. Per-page OG/Twitter tags (image, branded title,
				// twitter:title/description) live in src/components/CustomHead.astro.
				//
				// PushFeedback CSS + JS used to live here, but they were render-
				// blocking on every page even though the widget itself only sits
				// at the bottom of the page in `FeedbackFooter.astro`. The lazy
				// loader now lives inside `FeedbackButtons.astro` and pulls the
				// assets in `requestIdleCallback` time — off the critical path.
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
					description:
						'Documentation for Warp, the agentic development environment, and Oz, Warp\'s programmable agent for running and coordinating agents at scale.',
					customSets: [
						{ label: 'Terminal', description: 'Warp Terminal features and configuration.', paths: ['terminal/**'] },
						{ label: 'Agent Platform', description: 'Warp\'s Agent Platform: capabilities, local agents, CLI agents, cloud agents.', paths: ['agent-platform/**'] },
						{ label: 'Code', description: 'Code editor, code review, and Git worktrees.', paths: ['code/**'] },
						{ label: 'Enterprise', description: 'Enterprise features, SSO, team management, and security.', paths: ['enterprise/**'] },
						{ label: 'Getting Started', description: 'Installation, quickstart, and migration guides.', paths: ['getting-started/**'] },
						{ label: 'Knowledge and Collaboration', description: 'Warp Drive, teams, and the Admin Panel.', paths: ['knowledge-and-collaboration/**'] },
						{ label: 'Reference', description: 'CLI and API reference.', paths: ['reference/**'] },
						{ label: 'Support', description: 'Troubleshooting, billing, and privacy.', paths: ['support-and-community/**'] },
						{ label: 'Guides (Warp University)', description: 'Task-oriented walkthroughs.', paths: ['university/**'] },
					],
				}),
			],
		}),
		docsMarkdownIntegration(),
	],
	adapter: vercel(),
});
