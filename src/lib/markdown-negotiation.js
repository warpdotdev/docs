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

export default function markdownNegotiation(request) {
	const url = new URL(request.url);

	if (!isEligibleDocHtmlPath(url.pathname) || !shouldServeMarkdownProduction(request)) {
		return new Response(null, { headers: { 'x-middleware-next': '1' } });
	}

	const rewritten = new URL(request.url);
	rewritten.pathname = getMarkdownPathFromHtmlPath(url.pathname);
	return new Response(null, {
		headers: { 'x-middleware-rewrite': rewritten.toString() },
	});
}
