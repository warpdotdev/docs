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
	if (context.isPrerendered) {
		return next();
	}

	if (!isEligibleDocHtmlPath(context.url.pathname)) {
		return next();
	}

	if (!shouldServeMarkdown(context.request)) {
		return next();
	}

	const markdownUrl = new URL(getMarkdownPathFromHtmlPath(context.url.pathname), context.url);
	return next(markdownUrl);
});
