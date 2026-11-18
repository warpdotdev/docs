import { defineMiddleware } from 'astro:middleware';
import {
	shouldServeMarkdown,
	isEligibleDocHtmlPath,
	getMarkdownPathFromHtmlPath,
} from './lib/docs-markdown.js';

/**
 * Content negotiation middleware (dev / SSR only).
 *
 * When an agent sends `Accept: text/markdown` (or falls back via `text/plain` /
 * known agent user-agent), rewrite to the pre-rendered `.md` variant. This lets
 * local tools get clean markdown without discovering the `.md` URL first.
 *
 * Production static hosting cannot rely on this file: Vercel serves prerendered
 * HTML before Astro middleware. `scripts/build-tracking-middleware.mjs` installs
 * Build Output API middleware that rewrites only on explicit `Accept:
 * text/markdown` (see `shouldServeMarkdownProduction`). Direct `*.md` URLs work
 * in production without negotiation.
 */
export const onRequest = defineMiddleware(async (context, next) => {
	// Content negotiation only applies to on-demand (SSR) requests. During the
	// static prerender pass there is no real request, and reading
	// `request.headers` warns ("not available on prerendered pages") once per
	// route, which floods the build log. Skip it when the route is prerendered.
	if (context.isPrerendered) {
		return next();
	}

	const { request, url } = context;

	if (!isEligibleDocHtmlPath(url.pathname)) {
		return next();
	}

	if (!shouldServeMarkdown(request)) {
		return next();
	}

	const mdPath = getMarkdownPathFromHtmlPath(url.pathname);
	return context.rewrite(mdPath);
});
