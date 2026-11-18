// Adds Markdown content negotiation to the Vercel build output. Runs from
// `postbuild`, after `astro build` writes .vercel/output/config.json and the
// docs-markdown integration writes the Markdown twins.
//
// A twin is `<path>.md` (`index.md` for the homepage) whose HTML page,
// `<path>/index.html`, advertises it with
// `<link rel="alternate" type="text/markdown" href="/<path>.md">`. Only those
// pages get negotiation routes. Routes go before the filesystem phase so they
// run before the static `index.html` is matched. See
// src/lib/markdown-negotiation-routes.js.
import { readdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
	buildMarkdownNegotiationRoutes,
	isNegotiationRoute,
} from '../src/lib/markdown-negotiation-routes.js';

const output = fileURLToPath(new URL('../.vercel/output/', import.meta.url));
const staticDir = path.join(output, 'static');
const configPath = path.join(output, 'config.json');

/** @param {string} dir */
async function* markdownFiles(dir) {
	for (const entry of await readdir(dir, { withFileTypes: true })) {
		const entryPath = path.join(dir, entry.name);
		if (entry.isDirectory()) yield* markdownFiles(entryPath);
		else if (entry.isFile() && entry.name.endsWith('.md')) yield entryPath;
	}
}

const twinPaths = [];
for await (const file of markdownFiles(staticDir)) {
	const twinPath = path.relative(staticDir, file).split(path.sep).join('/').slice(0, -'.md'.length);
	const htmlFile = twinPath === 'index'
		? path.join(staticDir, 'index.html')
		: path.join(staticDir, twinPath, 'index.html');
	let html;
	try {
		html = await readFile(htmlFile, 'utf8');
	} catch {
		continue;
	}
	if (html.includes(`<link rel="alternate" type="text/markdown" href="/${twinPath}.md"`)) {
		twinPaths.push(twinPath);
	}
}
if (!twinPaths.includes('index')) {
	console.error('build-markdown-negotiation-routes: no homepage Markdown twin (/index.md) found');
	process.exit(1);
}

const config = JSON.parse(await readFile(configPath, 'utf8'));
// Drop routes from an earlier run so rerunning the script does not duplicate them.
const routes = config.routes.filter((route) => !isNegotiationRoute(route));
const filesystemIndex = routes.findIndex((route) => route.handle === 'filesystem');
const negotiationRoutes = buildMarkdownNegotiationRoutes(twinPaths);
routes.splice(filesystemIndex === -1 ? routes.length : filesystemIndex, 0, ...negotiationRoutes);
config.routes = routes;
await writeFile(configPath, JSON.stringify(config, null, 2));
console.log(
	`build-markdown-negotiation-routes: ${twinPaths.length} twins, ${negotiationRoutes.length} routes`,
);
