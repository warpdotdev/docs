#!/usr/bin/env node
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { parseHTML } from 'linkedom';

const html = await readFile(new URL('../.vercel/output/static/index.html', import.meta.url), 'utf8');
const source = await readFile(new URL('../src/content/docs/index.mdx', import.meta.url), 'utf8');
const { document } = parseHTML(html);
const tocLinks = [...document.querySelectorAll('starlight-toc a')];
const headings = [...document.querySelectorAll('main h2')];
// The homepage is a deliberate build canary for variable-backed heading metadata.
assert.match(
	source,
	/^## .*\{VARS\.[A-Z0-9_]+\}.*$/m,
	'Keep a variable-backed H2 on the homepage or move this canary to another stable page',
);
assert(headings.length > 0, 'Homepage has no rendered H2 headings');

for (const heading of headings) {
	assert.doesNotMatch(
		heading.textContent,
		/\bVARS\./,
		`Homepage H2 #${heading.id} contains an unresolved content variable`,
	);
	const link = tocLinks.find((candidate) => candidate.getAttribute('href') === `#${heading.id}`);
	assert(link, `Missing homepage TOC entry for #${heading.id}`);
	assert.doesNotMatch(
		link.textContent,
		/\bVARS\./,
		`Homepage TOC entry for #${heading.id} contains an unresolved content variable`,
	);
	assert.equal(
		link.textContent.trim(),
		heading.textContent.trim(),
		`Homepage TOC label does not match #${heading.id}`,
	);
}

console.log('Homepage table of contents matches rendered H2 headings.');
