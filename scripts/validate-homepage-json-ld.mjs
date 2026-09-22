#!/usr/bin/env node
import assert from 'node:assert/strict';
import { dev } from 'astro';
import { parseHTML } from 'linkedom';

const DOCS_ORIGIN = 'https://docs.warp.dev';
const WARP_ORIGIN = 'https://www.warp.dev';
const ORGANIZATION_ID = `${WARP_ORIGIN}/#organization`;
const WEBSITE_ID = `${DOCS_ORIGIN}/#website`;
const HOMEPAGE_URL = 'http://127.0.0.1:4321/';

function parseJsonLd(html) {
	const { document } = parseHTML(html);
	return Array.from(document.querySelectorAll('script[type="application/ld+json"]'), (script) =>
		JSON.parse(script.textContent),
	);
}

async function fetchHomepage() {
	let lastError;
	for (let attempt = 0; attempt < 40; attempt += 1) {
		try {
			return await fetch(HOMEPAGE_URL);
		} catch (error) {
			lastError = error;
			await new Promise((resolve) => setTimeout(resolve, 250));
		}
	}
	throw new Error(`Docs homepage did not become available at ${HOMEPAGE_URL}`, {
		cause: lastError,
	});
}

const server = await dev({
	root: new URL('../', import.meta.url),
	host: '127.0.0.1',
	port: 4321,
	logLevel: 'error',
	vite: {
		optimizeDeps: {
			noDiscovery: true,
		},
	},
});

try {
	const response = await fetchHomepage();
	assert.equal(response.status, 200, 'Docs homepage should render successfully');

	const payloads = parseJsonLd(await response.text());
	const organizations = payloads.filter((payload) => payload['@type'] === 'Organization');
	const websites = payloads.filter((payload) => payload['@type'] === 'WebSite');

	assert.equal(organizations.length, 1, 'Expected exactly one Organization JSON-LD node');
	assert.equal(websites.length, 1, 'Expected exactly one WebSite JSON-LD node');

	assert.equal(organizations[0]['@id'], ORGANIZATION_ID);
	assert.equal(organizations[0].url, WARP_ORIGIN);
	assert.equal(websites[0]['@id'], WEBSITE_ID);
	assert.equal(websites[0].url, DOCS_ORIGIN);
	assert.deepEqual(websites[0].publisher, { '@id': ORGANIZATION_ID });

	console.log('Homepage JSON-LD validation passed.');
} finally {
	await server.stop();
}
