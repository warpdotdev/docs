import { access, copyFile, mkdir, readdir, readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { STRIPPED_PARAMS } from '../src/lib/tracking-redirect.js';
import { isEligibleDocHtmlPath } from '../src/lib/docs-markdown.js';

// Astro's Vercel adapter serves prerendered pages before its own middleware.
// Emit native routing middleware before the filesystem phase instead:
// https://vercel.com/docs/build-output-api/features#routing-middleware
const output = new URL('../.vercel/output/', import.meta.url);
const configPath = new URL('config.json', output);
const config = JSON.parse(await readFile(configPath, 'utf8'));

async function installEdgeMiddleware(name, entryUrl, extraFiles = []) {
	const functionPath = new URL(`functions/${name}.func/`, output);
	await mkdir(functionPath, { recursive: true });
	await copyFile(entryUrl, new URL('index.js', functionPath));
	for (const fileUrl of extraFiles) {
		const fileName = fileUrl.pathname.split('/').at(-1);
		await copyFile(fileUrl, new URL(fileName, functionPath));
	}
	await writeFile(
		new URL('.vc-config.json', functionPath),
		JSON.stringify({
			runtime: 'edge',
			entrypoint: 'index.js',
		}),
	);
}

await installEdgeMiddleware(
	'tracking-redirect',
	new URL('../src/lib/tracking-redirect.js', import.meta.url),
);
await installEdgeMiddleware(
	'markdown-negotiation',
	new URL('../src/lib/markdown-negotiation.js', import.meta.url),
	[
		new URL('../src/lib/docs-markdown.js', import.meta.url),
		new URL('../src/lib/markdown-negotiation.js', import.meta.url),
	],
);

// Use deployed files, not URL guesses: aliases, unknown paths, and HTML-only
// pages must reach normal redirects or the filesystem instead of a missing .md.
const staticDir = new URL('static/', output);
const canonicalPages = [];
for (const entry of await readdir(staticDir, { recursive: true, withFileTypes: true })) {
	if (!entry.isFile() || !entry.name.endsWith('.md')) continue;
	const file = pathToFileURL(join(entry.parentPath, entry.name));
	const relative = file.pathname.slice(staticDir.pathname.length);
	const page = relative === 'index.md' ? '/' : `/${relative.slice(0, -3)}/`;
	if (!isEligibleDocHtmlPath(page)) continue;
	try {
		await access(new URL(`${page.slice(1)}index.html`, staticDir));
	} catch (error) {
		if (error.code === 'ENOENT') continue;
		throw error;
	}
	canonicalPages.push(page);
}
if (!canonicalPages.includes('/')) throw new Error('No homepage Markdown twin found');
await writeFile(
	new URL('functions/markdown-negotiation.func/index.js', output),
	`import negotiate from './markdown-negotiation.js';\n`
	+ `const pages = new Set(${JSON.stringify(canonicalPages.sort())});\n`
	+ `export default (request) => negotiate(request, pages);\n`,
);

// Entries in `has` are AND-ed, so each stripped parameter gets its own route.
// Install markdown negotiation first, then tracking on top so tracking runs
// earlier and can 301 away dirty query params before a markdown rewrite.
config.routes.unshift({
	src: '/(.*)',
	middlewarePath: 'markdown-negotiation',
	continue: true,
});
config.routes.unshift(
	...STRIPPED_PARAMS.map((key) => ({
		src: '/(.*)',
		has: [{ type: 'query', key }],
		middlewarePath: 'tracking-redirect',
		continue: true,
	})),
);
await writeFile(configPath, JSON.stringify(config, null, 2));
