// Usage: node scripts/verify-live-routing.mjs https://PREVIEW_HOST [--sitemap]
// GET-only, sequential, 150 ms between requests; 429 stops verification as incomplete.
import assert from 'node:assert/strict';
import { setTimeout as delay } from 'node:timers/promises';
import { routingJourneys } from './routing-journeys.mjs';

const base = new URL(process.argv[2]);
assert.ok(['https:', 'http:'].includes(base.protocol), 'Expected an HTTP(S) base URL');
const started = new Date().toISOString();
let passed = 0;
let failed = 0;

async function get(url, accept = 'text/html') {
	await delay(150);
	const response = await fetch(url, {
		redirect: 'manual',
		headers: { accept },
		signal: AbortSignal.timeout(30_000),
	});
	if (response.status === 429) {
		await response.body?.cancel();
		throw new Error(`INCOMPLETE: rate limited at ${url}`);
	}
	return response;
}

async function follow(path, accept) {
	let url = new URL(path, base);
	const chain = [];
	const seen = new Set();
	for (let i = 0; i < 7; i += 1) {
		assert.equal(url.origin, base.origin, `Unexpected cross-origin redirect: ${url}`);
		assert.ok(!seen.has(url.href), `Redirect loop: ${url}`);
		seen.add(url.href);
		const response = await get(url, accept);
		const location = response.headers.get('location');
		chain.push({ path: url.pathname + url.search, status: response.status, location });
		const type = response.headers.get('content-type')?.split(';')[0];
		await response.body?.cancel();
		if (response.status >= 300 && response.status < 400) {
			assert.ok(location, 'Redirect missing Location');
			url = new URL(location, url);
			continue;
		}
		return { chain, final: url.pathname + url.search, status: response.status, type, hops: chain.length - 1 };
	}
	throw new Error(`Too many redirects: ${path}`);
}

async function check(fixture, accept) {
	const actual = await follow(fixture.path, accept);
	try {
		assert.equal(actual.final, fixture.final, 'final destination');
		assert.equal(actual.hops, fixture.hops, 'redirect count');
		assert.equal(actual.status, fixture.status ?? 200, 'final status');
		const htmlOnly = fixture.status || fixture.final.startsWith('/api') || fixture.final.endsWith('.html');
		assert.equal(actual.type, fixture.type ?? (htmlOnly ? 'text/html' : accept), 'content type');
		for (const hop of actual.chain.slice(0, -1)) {
			assert.equal(hop.status, hop.location && fixture.path.includes('trk=') ? 301 : 308);
		}
		passed += 1;
		console.log(JSON.stringify({ result: 'PASS', request: fixture.path, accept, ...actual }));
	} catch (error) {
		failed += 1;
		console.log(JSON.stringify({ result: 'FAIL', request: fixture.path, accept, ...actual, error: error.message }));
	}
}

try {
	for (const fixture of routingJourneys) {
		for (const accept of ['text/html', 'text/markdown']) await check(fixture, accept);
	}
	// Missing q is a deterministic JSON validation response, without querying
	// the retrieval backend or depending on its credentials.
	const retrieval = await follow('/retrieve', 'application/json');
	assert.equal(retrieval.final, '/retrieve/');
	assert.equal(retrieval.hops, 1);
	assert.equal(retrieval.chain[0].status, 308);
	assert.equal(retrieval.status, 400);
	assert.equal(retrieval.type, 'application/json');
	passed += 1;
	console.log(JSON.stringify({ result: 'PASS', request: '/retrieve', ...retrieval }));

	if (process.argv.includes('--sitemap')) {
		async function locations(path) {
			const response = await get(new URL(path, base), 'application/xml');
			assert.equal(response.status, 200, `Sitemap: ${path}`);
			return [...(await response.text()).matchAll(/<loc>([^<]+)<\/loc>/g)]
				.map((match) => new URL(match[1].replaceAll('&amp;', '&')).pathname);
		}
		const sitemapPaths = await locations('/sitemap-index.xml');
		assert.ok(sitemapPaths.length > 0, 'No sitemap files found');
		const pages = [];
		for (const path of sitemapPaths) pages.push(...await locations(path));
		assert.ok(pages.length > 100, 'Sitemap unexpectedly small');
		for (const page of pages) {
			assert.ok(page.endsWith('/'), `Noncanonical sitemap URL: ${page}`);
			await check({ path: page, final: page, hops: 0 }, 'text/html');
			if (page !== '/') await check({ path: page.slice(0, -1), final: page, hops: 1 }, 'text/html');
		}
		console.log(JSON.stringify({ sitemapPages: pages.length }));
	}
	console.log(JSON.stringify({ base: base.href, started, finished: new Date().toISOString(), passed, failed }));
	process.exitCode = failed ? 1 : 0;
} catch (error) {
	console.error(JSON.stringify({ base: base.href, started, passed, failed, incomplete: true, error: error.message }));
	process.exitCode = 1;
}
