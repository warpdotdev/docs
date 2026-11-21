import sitemap from '@astrojs/sitemap';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { parseHTML } from 'linkedom';

export default function sitemapLastmod() {
	let outputRoot;
	const integration = sitemap({
		serialize: async (item) => {
			const pathname = decodeURIComponent(new URL(item.url).pathname);
			const htmlPath = path.join(outputRoot, pathname, 'index.html');
			try {
				return withLastmod(item, await readFile(htmlPath, 'utf8'));
			} catch (error) {
				// Routes without generated HTML have no Starlight git date.
				if (error.code === 'ENOENT' || error.code === 'ENOTDIR') return item;
				throw error;
			}
		},
	});
	return {
		...integration,
		hooks: {
			...integration.hooks,
			// Runs before @astrojs/sitemap's build:done serialization, while
			// the adapter still exposes the generated HTML directory.
			'astro:build:generated': ({ dir }) => {
				outputRoot = fileURLToPath(dir);
			},
		},
	};
}

export function withLastmod(item, html) {
	const { document } = parseHTML(html);
	const value = document.querySelector('meta[property="article:modified_time"]')?.getAttribute('content');
	if (!value || !Number.isFinite(Date.parse(value))) return item;
	return { ...item, lastmod: new Date(value).toISOString() };
}
