#!/usr/bin/env node
import assert from 'node:assert/strict';
import { readdir, readFile } from 'node:fs/promises';
import { parseHTML } from 'linkedom';

async function collectFiles(directory, extension) {
	const files = [];
	for (const entry of await readdir(directory, { withFileTypes: true })) {
		if (entry.isDirectory()) {
			files.push(...(await collectFiles(new URL(`${entry.name}/`, directory), extension)));
		} else if (entry.name.endsWith(extension)) {
			files.push(new URL(entry.name, directory));
		}
	}
	return files;
}

const sourceFiles = await collectFiles(new URL('../src/content/docs/', import.meta.url), '.mdx');
const sourceHasFixture = (
	await Promise.all(sourceFiles.map((file) => readFile(file, 'utf8')))
).some((source) => /^## .*\{VARS\.[A-Z0-9_]+\}.*$/m.test(source));
assert(sourceHasFixture, 'Docs have no variable-backed H2 fixture');

const htmlFiles = await collectFiles(
	new URL('../.vercel/output/static/', import.meta.url),
	'.html',
);
let headingCount = 0;
for (const file of htmlFiles) {
	const html = await readFile(file, 'utf8');
	const { document } = parseHTML(html);
	const tocLinks = [...document.querySelectorAll('starlight-toc a')];
	const headings = [...document.querySelectorAll('main h2')];
	headingCount += headings.length;

	for (const heading of headings) {
		assert.doesNotMatch(
			heading.textContent,
			/\bVARS\./,
			`${file.pathname} H2 #${heading.id} contains an unresolved content variable`,
		);
		const link = tocLinks.find(
			(candidate) => candidate.getAttribute('href') === `#${heading.id}`,
		);
		assert(link, `Missing TOC entry for ${file.pathname}#${heading.id}`);
		assert.doesNotMatch(
			link.textContent,
			/\bVARS\./,
			`${file.pathname} TOC entry for #${heading.id} contains an unresolved content variable`,
		);
		assert.equal(
			link.textContent.trim(),
			heading.textContent.trim(),
			`TOC label does not match ${file.pathname}#${heading.id}`,
		);
	}
}

assert(headingCount > 0, 'Generated docs have no H2 headings');
console.log(
	`Tables of contents match ${headingCount} rendered H2 headings across ${htmlFiles.length} generated pages.`,
);
