import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';
import {
	buildMarkdownCanonicalRoutes,
	canonicalLinkValue,
	linkHeadersFor,
} from '../src/lib/markdown-canonical-routes.js';
import { DOCS_ORIGIN } from '../src/lib/site.js';

const twins = [
	'index',
	'agents',
	'factories',
	'terminal/blocks/block-basics',
	'changelog/2026',
	'factories/api-and-sdk/troubleshooting/errors/conflict',
];
const routes = buildMarkdownCanonicalRoutes(twins);

test('every generated twin points to its HTML page', () => {
	const cases = {
		'/index.md': `${DOCS_ORIGIN}/`,
		'/agents.md': `${DOCS_ORIGIN}/agents/`,
		'/factories.md': `${DOCS_ORIGIN}/factories/`,
		'/terminal/blocks/block-basics.md': `${DOCS_ORIGIN}/terminal/blocks/block-basics/`,
		'/changelog/2026.md': `${DOCS_ORIGIN}/changelog/2026/`,
		'/factories/api-and-sdk/troubleshooting/errors/conflict.md':
			`${DOCS_ORIGIN}/factories/api-and-sdk/troubleshooting/errors/conflict/`,
	};
	for (const [pathname, htmlUrl] of Object.entries(cases)) {
		assert.deepEqual(linkHeadersFor(routes, pathname), [canonicalLinkValue(htmlUrl)], pathname);
	}
});

test('paths that are not generated twins get no canonical Link header', () => {
	for (const pathname of [
		// HTML pages and other generated files
		'/', '/factories/', '/factories', '/llms.txt', '/openapi.yaml', '/sitemap-0.xml',
		// reserved and missing paths, which return 404
		'/assets/not-a-twin.md', '/_astro/not-a-twin.md', '/.well-known/not-a-twin.md',
		'/robots.md', '/not-a-twin.md', '/factories/missing.md', '/terminal/index.md',
		// near misses
		'/factories.md/', '/factories.mdx', '/factories.md.html', '/xfactories.md', '/factories-x.md',
		'/terminal/blocks.md', '/index.md/extra',
		// case variants: static files are case-sensitive, so these 404
		'/AGENTS.md', '/Factories.md', '/INDEX.md', '/factories.MD',
	]) {
		assert.deepEqual(linkHeadersFor(routes, pathname), [], pathname);
	}
});

test('large twin sets are split into bounded routes that still match exactly', () => {
	const many = Array.from({ length: 600 }, (_, index) => `section-${index}/page-with-a-long-name-${index}`);
	const manyRoutes = buildMarkdownCanonicalRoutes(many);
	assert.ok(manyRoutes.length > 1);
	for (const route of manyRoutes) {
		assert.ok(route.src.length < 4000, `src is ${route.src.length} characters`);
		assert.equal(route.caseSensitive, true);
		assert.equal(route.continue, true);
	}
	for (const twin of [many[0], many[299], many[599]]) {
		assert.deepEqual(linkHeadersFor(manyRoutes, `/${twin}.md`), [canonicalLinkValue(`${DOCS_ORIGIN}/${twin}/`)]);
	}
	assert.deepEqual(linkHeadersFor(manyRoutes, '/section-0.md'), []);
});

test('regex characters in a path are matched literally', () => {
	const special = buildMarkdownCanonicalRoutes(['guides/c++', 'a.b']);
	assert.deepEqual(linkHeadersFor(special, '/guides/c++.md'), [canonicalLinkValue(`${DOCS_ORIGIN}/guides/c++/`)]);
	assert.deepEqual(linkHeadersFor(special, '/guides/cc.md'), []);
	assert.deepEqual(linkHeadersFor(special, '/aXb.md'), []);
});

test('vercel.json adds no canonical Link header (generated routes own it)', async () => {
	const vercelConfig = JSON.parse(await readFile(new URL('../vercel.json', import.meta.url), 'utf8'));
	for (const entry of vercelConfig.headers ?? []) {
		for (const header of entry.headers) {
			assert.notEqual(header.key.toLowerCase(), 'link', entry.source);
		}
	}
});
