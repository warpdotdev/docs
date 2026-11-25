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

// Eligible paths return HTML or Markdown depending on Accept, so both variants
// say so: without `Vary: Accept` a shared cache can hand one client the other's
// variant (RFC 9110 §12.5.5).
const VARY = { vary: 'Accept' };

export default function markdownNegotiation(request) {
	const url = new URL(request.url);

	if (!isEligibleDocHtmlPath(url.pathname)) {
		return new Response(null, { headers: { 'x-middleware-next': '1' } });
	}

	if (!shouldServeMarkdownProduction(request)) {
		return new Response(null, { headers: { 'x-middleware-next': '1', ...VARY } });
	}

	const rewritten = new URL(request.url);
	rewritten.pathname = getMarkdownPathFromHtmlPath(url.pathname);
	return new Response(null, {
		headers: { 'x-middleware-rewrite': rewritten.toString(), ...VARY },
	});
}
