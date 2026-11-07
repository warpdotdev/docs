import assert from 'node:assert/strict';
import { access, readdir, readFile } from 'node:fs/promises';
import { DOCS_ORIGIN } from '../src/lib/site.js';

// Validate the actual plugin and route outputs, not just their configuration.
// Run after `npm run build`.
const output = new URL('../.vercel/output/static/', import.meta.url);
const errorHtml = await readFile(new URL('404.html', output), 'utf8');
assert.match(errorHtml, /Page not found/, 'The HTML error page must remain available');
for (const path of ['404.md', '404.md.html', '404/index.md']) {
	await assert.rejects(
		access(new URL(path, output)),
		{ code: 'ENOENT' },
		`${path} must not be generated as documentation`,
	);
}

const homepageMarkdown = await readFile(new URL('index.md', output), 'utf8');
assert.ok(
	homepageMarkdown.includes(`[llms.txt](${DOCS_ORIGIN}/llms.txt)`),
	'Normal documentation must still receive cleaned Markdown',
);

const index = await readFile(new URL('llms.txt', output), 'utf8');
for (const file of ['llms-small.txt', 'llms-full.txt']) {
	assert.ok(
		index.includes(`${DOCS_ORIGIN}/${file}`),
		`The root agent index must still link to ${file}`,
	);
}

const customSets = (await readdir(new URL('_llms-txt/', output)))
	.filter((file) => file.endsWith('.txt'));
assert.ok(customSets.length > 0, 'Custom documentation sets must still be generated');
const aggregates = [
	'llms-small.txt',
	'llms-full.txt',
	...customSets.map((file) => `_llms-txt/${file}`),
];
for (const file of aggregates) {
	const content = await readFile(new URL(file, output), 'utf8');
	const canonicalUrls = [...content.matchAll(/^Canonical page: \[[^\]]+\]\(([^)]+)\)$/gm)]
		.map((match) => new URL(match[1]));
	assert.ok(canonicalUrls.length > 0, `${file} must still contain canonical documentation links`);
	for (const url of canonicalUrls) {
		assert.notEqual(
			url.pathname.replace(/\/$/, ''),
			'/404',
			`${file} must not advertise the error page as documentation`,
		);
	}
}

console.log(`Validated ${aggregates.length} agent documentation sets; HTML 404 preserved and error-page Markdown excluded.`);
