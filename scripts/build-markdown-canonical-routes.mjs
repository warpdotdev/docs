// Adds canonical `Link` headers for the generated Markdown twins to the Vercel
// build output. Runs from `postbuild`, after `astro build` writes
// .vercel/output/config.json and the docs-markdown integration writes the twins.
//
// A twin is `<path>.md` (`index.md` for the homepage) whose HTML page,
// `<path>/index.html`, advertises it with
// `<link rel="alternate" type="text/markdown" href="/<path>.md">`. Only those
// paths get the header, so 404 responses for other `.md` requests do not claim
// a canonical page. Routes go before the filesystem phase, where vercel.json
// headers also run, and use `continue` so the static file is still served.
// See src/lib/markdown-canonical-routes.js.
import { readdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildMarkdownCanonicalRoutes } from '../src/lib/markdown-canonical-routes.js';

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
if (twinPaths.length === 0) {
	console.error('build-markdown-canonical-routes: no Markdown twins found in .vercel/output/static');
	process.exit(1);
}

const config = JSON.parse(await readFile(configPath, 'utf8'));
// Drop routes from an earlier run so rerunning the script does not duplicate them.
const routes = config.routes.filter(
	(route) => !(route.headers?.Link ?? '').endsWith('; rel="canonical"'),
);
const filesystemIndex = routes.findIndex((route) => route.handle === 'filesystem');
const canonicalRoutes = buildMarkdownCanonicalRoutes(twinPaths);
routes.splice(filesystemIndex === -1 ? routes.length : filesystemIndex, 0, ...canonicalRoutes);
config.routes = routes;
await writeFile(configPath, JSON.stringify(config, null, 2));
console.log(
	`build-markdown-canonical-routes: ${twinPaths.length} twins, ${canonicalRoutes.length} header routes`,
);
