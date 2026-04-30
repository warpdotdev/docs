import { defineRouteMiddleware } from '@astrojs/starlight/route-data';
import config from 'virtual:starlight/user-config';
import { getMarkdownPathFromHtmlPath } from './lib/docs-markdown.js';

/**
 * Per-page head augmentation.
 *
 * - Always exposes the page's Markdown source via `<link rel="alternate">`
 *   (matches what GitBook serves today and what AI agents look for).
 * - Pushes branded OG and Twitter tags so social previews include the site
 *   name ("Page Title | Warp") and a real preview image. Starlight's
 *   `getHead()` runs before this middleware and seeds `route.head` with its
 *   defaults; we strip its bare `og:title` first so we don't end up with
 *   duplicate tags, then push the branded replacement.
 */
export const onRequest = defineRouteMiddleware((context) => {
	const route = context.locals.starlightRoute;
	const head = route.head;

	head.push({
		tag: 'link',
		attrs: {
			rel: 'alternate',
			type: 'text/markdown',
			href: getMarkdownPathFromHtmlPath(context.url.pathname),
		},
	});

	const siteTitle =
		(typeof config.title === 'string' ? config.title : config.title?.en) ?? 'Warp';
	const pageTitle = route.entry?.data?.title ?? siteTitle;
	const pageDescription = route.entry?.data?.description ?? config.description;
	const brandedTitle = `${pageTitle} ${config.titleDelimiter} ${siteTitle}`;
	const site = context.site ?? new URL('https://docs.warp.dev');
	const ogImageUrl = new URL('/og-image.png', site).href;

	// Drop Starlight's bare og:title before adding the branded one. Inline
	// rather than a helper so we keep the exact `route.head` element type
	// (Starlight types `attrs` values as `string | boolean | undefined`,
	// which a separate function signature would have to restate).
	for (let i = head.length - 1; i >= 0; i--) {
		const entry = head[i];
		if (entry.tag === 'meta' && entry.attrs?.property === 'og:title') {
			head.splice(i, 1);
		}
	}

	head.push(
		{ tag: 'meta', attrs: { property: 'og:title', content: brandedTitle } },
		{ tag: 'meta', attrs: { property: 'og:image', content: ogImageUrl } },
		{ tag: 'meta', attrs: { property: 'og:image:secure_url', content: ogImageUrl } },
		{ tag: 'meta', attrs: { property: 'og:image:type', content: 'image/png' } },
		{ tag: 'meta', attrs: { property: 'og:image:width', content: '1200' } },
		{ tag: 'meta', attrs: { property: 'og:image:height', content: '630' } },
		{ tag: 'meta', attrs: { property: 'og:image:alt', content: `${siteTitle} — ${pageTitle}` } },
		{ tag: 'meta', attrs: { name: 'twitter:title', content: brandedTitle } },
		{ tag: 'meta', attrs: { name: 'twitter:image', content: ogImageUrl } },
	);
	if (pageDescription) {
		head.push({
			tag: 'meta',
			attrs: { name: 'twitter:description', content: pageDescription },
		});
	}
});
