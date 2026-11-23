import { copyFile, mkdir, readFile, writeFile } from 'node:fs/promises';
import { STRIPPED_PARAMS } from '../src/lib/tracking-redirect.js';

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
	[new URL('../src/lib/docs-markdown.js', import.meta.url)],
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
