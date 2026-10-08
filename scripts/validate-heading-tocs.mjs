#!/usr/bin/env node
import assert from 'node:assert/strict';
import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseHTML } from 'linkedom';

async function collectFiles(directory, extension) {
	const files = [];
	for (const entry of await readdir(directory, { withFileTypes: true })) {
		const entryPath = path.join(directory, entry.name);
		if (entry.isDirectory()) {
			files.push(...(await collectFiles(entryPath, extension)));
		} else if (entry.name.endsWith(extension)) {
			files.push(entryPath);
		}
	}
	return files;
}

const sourceDirectory = fileURLToPath(new URL('../src/content/docs/', import.meta.url));
const sourceFiles = await collectFiles(sourceDirectory, '.mdx');
const sourceHasFixture = (
	await Promise.all(sourceFiles.map((file) => readFile(file, 'utf8')))
).some((source) => /^## .*\{VARS\.[A-Z0-9_]+\}.*$/m.test(source));
assert(
	sourceHasFixture,
	'Keep a variable-backed H2 fixture shaped like `## ... {VARS.KEY} ...` under src/content/docs/ (usually index.mdx)',
);

const htmlDirectory = fileURLToPath(new URL('../.vercel/output/static/', import.meta.url));
const htmlFiles = await collectFiles(htmlDirectory, '.html');
let headingCount = 0;
for (const file of htmlFiles) {
	const html = await readFile(file, 'utf8');
	const { document } = parseHTML(html);
	const tocLinks = [...document.querySelectorAll('starlight-toc a')];
	const headings = [...document.querySelectorAll('main h2, main h3')];

	for (const heading of headings) {
		assert.doesNotMatch(
			heading.textContent,
			/\bVARS\./,
			`${file} heading #${heading.id} contains an unresolved content variable`,
		);
		if (!heading.id) continue;
		headingCount += 1;
		if (tocLinks.length === 0) continue;
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

assert(headingCount > 0, 'Generated docs have no anchored H2 or H3 headings');
console.log(
	`Validated ${headingCount} anchored headings across ${htmlFiles.length} generated pages.`,
);
