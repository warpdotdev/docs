import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { parseHTML } from 'linkedom';

const html = await readFile(new URL('../.vercel/output/static/index.html', import.meta.url), 'utf8');
const source = await readFile(new URL('../src/content/docs/index.mdx', import.meta.url), 'utf8');
const { document } = parseHTML(html);
const tocLinks = [...document.querySelectorAll('starlight-toc a')];
const headings = [...document.querySelectorAll('main h2')];

assert.match(source, /^## .*\{VARS\.[A-Z_]+\}/m, 'Homepage has no variable-backed H2 fixture');
assert(headings.length > 0, 'Homepage has no rendered H2 headings');
const automationPlatformHeading = headings.find(
	(heading) => heading.textContent.trim() === 'Automation Platform',
);
assert(automationPlatformHeading, 'Homepage has no rendered Automation Platform H2');
assert.equal(
	automationPlatformHeading.id,
	'automation-platform',
	'Automation Platform H2 has an unexpected anchor',
);

for (const heading of headings) {
	const link = tocLinks.find((candidate) => candidate.getAttribute('href') === `#${heading.id}`);
	assert(link, `Missing homepage TOC entry for #${heading.id}`);
	assert.equal(
		link.textContent.trim(),
		heading.textContent.trim(),
		`Homepage TOC label does not match #${heading.id}`,
	);
}

console.log('Homepage table of contents matches rendered H2 headings.');
