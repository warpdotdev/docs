/**
 * Vercel routing middleware that rewrites eligible doc HTML paths to their
 * pre-rendered `.md` variant when the client asks for markdown (Accept header
 * or known agent user-agent).
 *
 * Must run before the filesystem handler — Astro/Vercel otherwise serve the
 * static HTML file and never evaluate vercel.json rewrites or Astro middleware.
 */
import {
	getMarkdownPathFromHtmlPath,
	isEligibleDocHtmlPath,
	shouldServeMarkdown,
} from './docs-markdown.js';

export default function markdownNegotiation(request) {
	const url = new URL(request.url);

	if (!isEligibleDocHtmlPath(url.pathname) || !shouldServeMarkdown(request)) {
		return new Response(null, { headers: { 'x-middleware-next': '1' } });
	}

	const rewritten = new URL(request.url);
	rewritten.pathname = getMarkdownPathFromHtmlPath(url.pathname);
	return new Response(null, {
		headers: { 'x-middleware-rewrite': rewritten.toString() },
	});
}
