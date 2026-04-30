import { defineMiddleware } from 'astro:middleware';
import {
	getMarkdownPathFromHtmlPath,
	isEligibleDocHtmlPath,
	shouldServeMarkdown,
} from './lib/docs-markdown.js';

export const onRequest = defineMiddleware((context, next) => {
	if (!['GET', 'HEAD'].includes(context.request.method)) {
		return next();
	}

	if (!isEligibleDocHtmlPath(context.url.pathname)) {
		return next();
	}

	// Content negotiation for AI agents — only needed at runtime.
	// Skip during prerendering (both dev and build) to avoid
	// Astro.request.headers warnings on every static page.
	if (context.isPrerendered || !shouldServeMarkdown(context.request)) {
		return next();
	}

	const markdownUrl = new URL(getMarkdownPathFromHtmlPath(context.url.pathname), context.url);
	return next(markdownUrl);
});
