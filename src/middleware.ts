import { defineMiddleware } from 'astro:middleware';
import {
	shouldServeMarkdown,
	isEligibleDocHtmlPath,
	getMarkdownPathFromHtmlPath,
} from './lib/docs-markdown.js';

/**
 * Content negotiation middleware.
 *
 * When an agent sends `Accept: text/markdown` (or is identified by user-agent),
 * rewrite the request to the pre-rendered `.md` variant of the page. This lets
 * agents like Claude Code, Cursor, and OpenCode get clean markdown without
 * needing to discover the `.md` URL convention first.
 *
 * The `shouldServeMarkdown` helper handles both explicit Accept-header
 * negotiation and user-agent fallback detection (see `src/lib/docs-markdown.js`).
 */
export const onRequest = defineMiddleware(async (context, next) => {
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
