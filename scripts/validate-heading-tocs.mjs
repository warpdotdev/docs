#!/usr/bin/env node
import assert from 'node:assert/strict';
import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseHTML } from 'linkedom';

const unresolvedHeadingVarPattern = /\bVARS\.[A-Z0-9_]+/;

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
const sourceFixtureFile = path.join(sourceDirectory, 'index.mdx');
const sourceHasFixture = /^#{1,6} .*\{\s*VARS\.[A-Z0-9_]+\s*\}.*$/m.test(
	await readFile(sourceFixtureFile, 'utf8'),
);
assert(
	sourceHasFixture,
	`${sourceFixtureFile} must contain a variable-backed heading to provide end-to-end coverage for src/plugins/heading-vars.ts`,
);

const htmlDirectory = fileURLToPath(new URL('../.vercel/output/static/', import.meta.url));
const htmlFiles = await collectFiles(htmlDirectory, ['.html']).catch((error) => {
	if (error?.code !== 'ENOENT' || error.path !== htmlDirectory) throw error;
	throw new Error(
		`No build output at ${htmlDirectory}. Run npm run build before npm run test:heading-tocs.`,
	);
});
let tocEntryCount = 0;
for (const file of htmlFiles) {
	const html = await readFile(file, 'utf8');
	const { document } = parseHTML(html);
	const toc = document.querySelector('starlight-toc');
	const tocLinks = toc ? [...toc.querySelectorAll('a')] : [];
	const allHeadings = [...document.querySelectorAll('main :is(h1, h2, h3, h4, h5, h6)')];
	const markdownHeadings = allHeadings.filter((heading) =>
		heading.closest('.sl-markdown-content'),
	);
	const agentOnlyHeadings = [...document.querySelectorAll('template[data-agent-only]')].flatMap(
		(template) => [...template.content.querySelectorAll('h1, h2, h3, h4, h5, h6')],
	);

	for (const heading of [...allHeadings, ...agentOnlyHeadings]) {
		assert.doesNotMatch(
			heading.textContent,
			unresolvedHeadingVarPattern,
			`${file} heading #${heading.id || heading.textContent.trim()} contains an unresolved content variable`,
		);
	}

	const headingsById = new Map(
		[...agentOnlyHeadings, ...allHeadings]
			.filter((heading) => heading.id)
			.map((heading) => [heading.id, heading]),
	);
	const tocHrefs = new Set();
	const expectedTocHeadingTags = new Set();
	if (toc) {
		const minHeadingLevel = Number(toc.getAttribute('data-min-h'));
		const maxHeadingLevel = Number(toc.getAttribute('data-max-h'));
		assert(
			Number.isInteger(minHeadingLevel) &&
				Number.isInteger(maxHeadingLevel) &&
				minHeadingLevel >= 1 &&
				maxHeadingLevel <= 6 &&
				minHeadingLevel <= maxHeadingLevel,
			`${file} table of contents has an invalid heading range`,
		);
		for (let level = minHeadingLevel; level <= maxHeadingLevel; level += 1) {
			expectedTocHeadingTags.add(`H${level}`);
		}
	}
	for (const link of tocLinks) {
		const href = link.getAttribute('href');
		if (!href?.startsWith('#') || href === '#_top') continue;
		tocEntryCount += 1;
		tocHrefs.add(href);
		assert.doesNotMatch(
			link.textContent,
			unresolvedHeadingVarPattern,
			`${file} TOC entry for ${href} contains an unresolved content variable`,
		);
		const heading = headingsById.get(href.slice(1));
		assert(heading, `${file} TOC entry ${href} has no matching heading`);
		assert.equal(
			link.textContent.trim(),
			heading.textContent.trim(),
			`TOC label does not match ${file}${href}`,
		);
	}

	for (const heading of markdownHeadings) {
		if (!heading.id || !expectedTocHeadingTags.has(heading.tagName)) continue;
		assert(tocHrefs.has(`#${heading.id}`), `Missing TOC entry for ${file}#${heading.id}`);
	}
}

assert(tocEntryCount > 0, 'Generated docs have no anchored table-of-contents entries');
console.log(
	`Validated ${tocEntryCount} table-of-contents entries across ${htmlFiles.length} generated HTML files.`,
);
