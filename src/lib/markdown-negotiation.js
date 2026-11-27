/**
 * Vercel routing middleware that rewrites eligible doc HTML paths to their
 * pre-rendered `.md` variant when the client explicitly asks for markdown via
 * `Accept: text/markdown`.
 *
 * Must run before the filesystem handler — Astro/Vercel otherwise serve the
 * static HTML file and never evaluate vercel.json rewrites or Astro middleware.
 *
 * Production intentionally does not rewrite on `text/plain` or agent user-agent
 * tokens (those remain local/dev fallbacks in Astro middleware). Clients can
 * always request the pre-rendered `*.md` URL directly.
 */
import {
	getMarkdownPathFromHtmlPath,
	isEligibleDocHtmlPath,
	shouldServeMarkdownProduction,
} from './docs-markdown.js';

/**
 * @param {Request} request
 * @param {Set<string>} canonicalPages Pages with built HTML and Markdown twins.
 */
export default function markdownNegotiation(request, canonicalPages) {
	const url = new URL(request.url);

	// Only canonical, existing pages can negotiate. Let Vercel normalize
	// slashless URLs and migrate legacy aliases before attempting a rewrite.
	if (!isEligibleDocHtmlPath(url.pathname) || !canonicalPages.has(url.pathname)
		|| !shouldServeMarkdownProduction(request)) {
		return new Response(null, { headers: { 'x-middleware-next': '1' } });
	}

	const rewritten = new URL(request.url);
	rewritten.pathname = getMarkdownPathFromHtmlPath(url.pathname);
	return new Response(null, {
		headers: { 'x-middleware-rewrite': rewritten.toString() },
	});
}
