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
).some((source) => /^#{1,6} .*\{\s*VARS\.[A-Z0-9_]+\s*\}.*$/m.test(source));
assert(
	sourceHasFixture,
	'Keep the variable-backed heading in src/content/docs/index.mdx to provide end-to-end coverage for src/plugins/heading-vars.ts',
);

const htmlDirectory = fileURLToPath(new URL('../.vercel/output/static/', import.meta.url));
const htmlFiles = await collectFiles(htmlDirectory, ['.html']).catch((error) => {
	if (error?.code !== 'ENOENT') throw error;
	throw new Error(
		`No build output at ${htmlDirectory}. Run npm run build before npm run test:heading-tocs.`,
	);
});
let tocEntryCount = 0;
for (const file of htmlFiles) {
	const html = await readFile(file, 'utf8');
	const { document } = parseHTML(html);
	const tocLinks = [...document.querySelectorAll('starlight-toc a')];
	const allHeadings = [...document.querySelectorAll('main :is(h1, h2, h3, h4, h5, h6)')];
	const agentOnlyHeadings = [...document.querySelectorAll('template[data-agent-only]')].flatMap(
		(template) => [...template.content.querySelectorAll('h1, h2, h3, h4, h5, h6')],
	);

	for (const heading of [...allHeadings, ...agentOnlyHeadings]) {
		assert.doesNotMatch(
			heading.textContent,
			/\{\s*VARS\.[A-Z0-9_]+\s*\}/,
			`${file} heading #${heading.id || heading.textContent.trim()} contains an unresolved content variable`,
		);
	}

	const headingsById = new Map(
		[...allHeadings, ...agentOnlyHeadings]
			.filter((heading) => heading.id)
			.map((heading) => [heading.id, heading]),
	);
	const visibleHeadingIds = new Set(
		allHeadings.filter((heading) => heading.id).map((heading) => heading.id),
	);
	const tocHrefs = new Set();
	const tocHeadingTags = new Set();
	for (const link of tocLinks) {
		const href = link.getAttribute('href');
		if (!href?.startsWith('#') || href === '#_top') continue;
		tocEntryCount += 1;
		tocHrefs.add(href);
		assert.doesNotMatch(
			link.textContent,
			/^\s*(?:\{\s*)?VARS\.[A-Z0-9_]+(?:\s*\})?\s*$/,
			`${file} TOC entry for ${href} contains an unresolved content variable`,
		);
		const heading = headingsById.get(href.slice(1));
		assert(heading, `${file} TOC entry ${href} has no matching heading`);
		if (visibleHeadingIds.has(heading.id)) tocHeadingTags.add(heading.tagName);
		assert.equal(
			link.textContent.trim(),
			heading.textContent.trim(),
			`TOC label does not match ${file}${href}`,
		);
	}

	for (const heading of allHeadings) {
		if (!heading.id || !tocHeadingTags.has(heading.tagName)) continue;
		assert(tocHrefs.has(`#${heading.id}`), `Missing TOC entry for ${file}#${heading.id}`);
	}
}

assert(tocEntryCount > 0, 'Generated docs have no anchored table-of-contents entries');
console.log(
	`Validated ${tocEntryCount} table-of-contents entries across ${htmlFiles.length} generated HTML files.`,
);
