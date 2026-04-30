import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

/**
 * Serves the raw MDX body of any doc page at `<url>.md`.
 *
 *   /                       → /index.md
 *   /quickstart/            → /quickstart.md
 *   /terminal/blocks/       → /terminal/blocks.md
 *   /terminal/command-palette/ → /terminal/command-palette.md
 *
 * In dev, Astro routes `.md` requests to this endpoint. In production
 * builds, prerendering writes the `.md` files to disk; the existing
 * `docs-markdown-integration` then overwrites them with its turndown
 * output (which produces cleaner markdown from the rendered HTML).
 */
export async function getStaticPaths() {
	const entries = await getCollection('docs');
	return entries.map((entry) => {
		let slug: string;
		if (entry.id === 'index') {
			slug = 'index';
		} else if (entry.id.endsWith('/index')) {
			slug = entry.id.slice(0, -'/index'.length);
		} else {
			slug = entry.id;
		}
		return {
			params: { slug },
			props: { entry },
		};
	});
}

export const GET: APIRoute = ({ props }) => {
	const entry = props.entry as {
		id: string;
		body?: string;
		data: { title?: string; description?: string };
	};

	const title = entry.data.title ?? '';
	const description = entry.data.description ?? '';
	const body = entry.body ?? '';

	const sections = [];
	if (title) sections.push(`# ${title}`);
	if (description) sections.push(description);
	if (body) sections.push(body);

	return new Response(`${sections.join('\n\n').trim()}\n`, {
		status: 200,
		headers: {
			'Content-Type': 'text/markdown; charset=utf-8',
			'Cache-Control': 'public, max-age=0, must-revalidate',
		},
	});
};
