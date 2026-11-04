import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';
// Same converter Vercel uses to turn vercel.json `headers` into routes
// (installed through @astrojs/vercel), so the test exercises the real
// source pattern and `:path` substitution instead of a reimplementation.
import { getTransformedRoutes } from '@vercel/routing-utils';
import { DOCS_ORIGIN } from '../src/lib/site.js';

const vercelConfig = JSON.parse(await readFile(new URL('../vercel.json', import.meta.url), 'utf8'));
const { routes, error } = getTransformedRoutes({ headers: vercelConfig.headers });

/** Returns every Link header value Vercel would add to a response for `pathname`. */
function linkHeadersFor(pathname) {
	const values = [];
	for (const route of routes ?? []) {
		const key = Object.keys(route.headers ?? {}).find((name) => name.toLowerCase() === 'link');
		if (!key) continue;
		const match = pathname.match(new RegExp(route.src));
		if (!match) continue;
		values.push(route.headers[key].replace(/\$(\d+)/g, (_, index) => match[Number(index)] ?? ''));
	}
	return values;
}

const canonical = (url) => `<${url}>; rel="canonical"`;

test('vercel.json headers compile', () => {
	assert.equal(error, null);
});

test('every Markdown twin points to its HTML page with a canonical Link header', () => {
	const cases = {
		'/index.md': `${DOCS_ORIGIN}/`,
		'/factories.md': `${DOCS_ORIGIN}/factories/`,
		'/terminal/blocks/block-basics.md': `${DOCS_ORIGIN}/terminal/blocks/block-basics/`,
		'/changelog/2026.md': `${DOCS_ORIGIN}/changelog/2026/`,
	};
	for (const [pathname, htmlUrl] of Object.entries(cases)) {
		assert.deepEqual(linkHeadersFor(pathname), [canonical(htmlUrl)], pathname);
	}
});

test('HTML pages and other files get no canonical Link header', () => {
	for (const pathname of ['/', '/factories/', '/factories', '/llms.txt', '/openapi.yaml', '/sitemap-0.xml']) {
		assert.deepEqual(linkHeadersFor(pathname), [], pathname);
	}
});
