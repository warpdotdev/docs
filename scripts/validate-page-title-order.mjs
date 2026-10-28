#!/usr/bin/env node
// Validates the page-title markup in the built site (`npm run build` first).
//
// Search and answer engines anchor snippets on the H1 and the text right after
// it, so on every docs page that renders `CustomPageTitle`:
// - the page description (`p.page-subtitle`) is the H1's next element, and its
//   text matches `<meta name="description">`;
// - the text in the first 200 characters after `</h1>` starts with that
//   description (no Copy-menu labels in between);
// - the page no longer ships the hidden `page-markdown-content` template that
//   carried a second copy of the raw MDX source.
import assert from 'node:assert/strict';
import { readdir, readFile } from 'node:fs/promises';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseHTML } from 'linkedom';

const STATIC_DIR = fileURLToPath(new URL('../.vercel/output/static/', import.meta.url));
const MIN_PAGES = 100;
const WINDOW = 200;

async function* htmlFiles(dir) {
	for (const entry of await readdir(dir, { withFileTypes: true })) {
		const path = join(dir, entry.name);
		if (entry.isDirectory()) yield* htmlFiles(path);
		else if (entry.name.endsWith('.html')) yield path;
	}
}

const normalize = (text) => text.replace(/\s+/g, ' ').trim();

// Text of everything after `</h1>` in document order, skipping non-rendered
// elements, until `limit` characters are collected.
function textAfter(node, limit) {
	const skip = new Set(['SCRIPT', 'STYLE', 'TEMPLATE', 'SVG', 'svg']);
	let out = '';
	function walk(n) {
		if (out.length >= limit) return;
		// Adjacent text nodes (e.g. around an `&#39;` entity) join directly;
		// element boundaries count as whitespace.
		if (n.nodeType === 3) out += n.textContent;
		else if (n.nodeType === 1 && !skip.has(n.tagName)) {
			out += ' ';
			n.childNodes.forEach(walk);
			out += ' ';
		}
	}
	for (let cur = node; cur && out.length < limit; cur = cur.parentNode) {
		for (let sib = cur.nextSibling; sib && out.length < limit; sib = sib.nextSibling) walk(sib);
	}
	return normalize(out).slice(0, limit);
}

let checked = 0;
const failures = [];

for await (const file of htmlFiles(STATIC_DIR)) {
	const html = await readFile(file, 'utf8');
	if (!html.includes('page-title-row')) continue;
	const page = relative(STATIC_DIR, file);
	checked++;

	if (html.includes('page-markdown-content')) {
		failures.push(`${page}: still ships the page-markdown-content template`);
	}

	const { document } = parseHTML(html);
	const h1 = document.querySelector('.page-title-row h1');
	const description = normalize(
		document.querySelector('meta[name="description"]')?.getAttribute('content') ?? '',
	);
	if (!h1) {
		failures.push(`${page}: no H1 inside .page-title-row`);
		continue;
	}
	if (!description) continue;

	const next = h1.nextElementSibling;
	if (!next?.classList.contains('page-subtitle')) {
		failures.push(`${page}: H1 is followed by <${next?.tagName?.toLowerCase()}>, not p.page-subtitle`);
		continue;
	}
	if (normalize(next.textContent) !== description) {
		failures.push(`${page}: page-subtitle text does not match the meta description`);
	}
	const after = textAfter(h1, WINDOW);
	if (!after.startsWith(description.slice(0, Math.min(60, description.length)))) {
		failures.push(`${page}: first ${WINDOW} chars after </h1> are "${after.slice(0, 80)}..."`);
	}
}

assert.ok(
	checked >= MIN_PAGES,
	`Expected at least ${MIN_PAGES} pages with a page title row, found ${checked}. Run \`npm run build\` first.`,
);
assert.deepEqual(failures, [], `Page title order check failed:\n${failures.join('\n')}`);
console.log(`Page title order validation passed (${checked} pages).`);
