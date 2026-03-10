import { defineRouteMiddleware } from '@astrojs/starlight/route-data';
import { getMarkdownPathFromHtmlPath } from './lib/docs-markdown.js';

export const onRequest = defineRouteMiddleware((context) => {
	context.locals.starlightRoute.head.push({
		tag: 'link',
		attrs: {
			rel: 'alternate',
			type: 'text/markdown',
			href: getMarkdownPathFromHtmlPath(context.url.pathname),
		},
	});
});
