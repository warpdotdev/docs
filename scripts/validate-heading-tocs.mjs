#!/usr/bin/env node
import assert from 'node:assert/strict';
import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseHTML } from 'linkedom';

async function collectFiles(directory, extensions) {
	const files = [];
	for (const entry of await readdir(directory, { withFileTypes: true })) {
		const entryPath = path.join(directory, entry.name);
		if (entry.isDirectory()) {
			files.push(...(await collectFiles(entryPath, extensions)));
		} else if (extensions.some((extension) => entry.name.endsWith(extension))) {
			files.push(entryPath);
		}
	}
	return files;
}

const sourceDirectory = fileURLToPath(new URL('../src/content/docs/', import.meta.url));
const sourceFiles = await collectFiles(sourceDirectory, ['.md', '.mdx']);
const sourceHasFixture = (
	await Promise.all(sourceFiles.map((file) => readFile(file, 'utf8')))
).some((source) =>
	/^\[heading-vars-e2e-fixture\]: #\r?\n(?:\s*\r?\n)*#{1,6} .*\{VARS\.[A-Z0-9_]+\}.*$/m.test(
		source,
	),
);
assert(
	sourceHasFixture,
	'Keep `[heading-vars-e2e-fixture]: #` before a variable-backed heading under src/content/docs/; it provides end-to-end coverage for src/plugins/heading-vars.ts',
);

const htmlDirectory = fileURLToPath(new URL('../.vercel/output/static/', import.meta.url));
const htmlFiles = await collectFiles(htmlDirectory, ['.html']);
let headingCount = 0;
for (const file of htmlFiles) {
	const html = await readFile(file, 'utf8');
	const { document } = parseHTML(html);
	const tocLinks = [...document.querySelectorAll('starlight-toc a')];
	const allHeadings = [...document.querySelectorAll('main :is(h1, h2, h3, h4, h5, h6)')];

	for (const heading of allHeadings) {
		assert.doesNotMatch(
			heading.textContent,
			/\bVARS\./,
			`${file} heading #${heading.id} contains an unresolved content variable`,
		);
	}

	const tocHeadings = [...document.querySelectorAll('main h2, main h3')];
	for (const heading of tocHeadings) {
		if (!heading.id) continue;
		// Pages with TOCs disabled still need the unresolved-variable check above.
		// Keep this guard after that check rather than skipping the page.
		if (tocLinks.length === 0) continue;
		headingCount += 1;
		const link = tocLinks.find(
			(candidate) => candidate.getAttribute('href') === `#${heading.id}`,
		);
		assert(link, `Missing TOC entry for ${file}#${heading.id}`);
		assert.doesNotMatch(
			link.textContent,
			/\bVARS\./,
			`${file} TOC entry for #${heading.id} contains an unresolved content variable`,
		);
		assert.equal(
			link.textContent.trim(),
			heading.textContent.trim(),
			`TOC label does not match ${file}#${heading.id}`,
		);
	}
}

assert(headingCount > 0, 'Generated docs have no anchored H2 or H3 headings with TOC entries');
console.log(
	`Validated ${headingCount} anchored headings across ${htmlFiles.length} generated HTML files.`,
);
