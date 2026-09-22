#!/usr/bin/env node
import assert from 'node:assert/strict';
import { dev } from 'astro';

const DOCS_ORIGIN = 'https://docs.warp.dev';
const WARP_ORIGIN = 'https://www.warp.dev';
const ORGANIZATION_ID = `${WARP_ORIGIN}/#organization`;
const WEBSITE_ID = `${DOCS_ORIGIN}/#website`;

function parseJsonLd(html) {
	const payloads = [];
	const scriptPattern = /<script\b([^>]*)>([\s\S]*?)<\/script\s*>/gi;

	for (const match of html.matchAll(scriptPattern)) {
		if (!/\btype=["']application\/ld\+json["']/i.test(match[1])) continue;
		payloads.push(JSON.parse(match[2]));
	}

	return payloads;
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
	const response = await fetch('http://127.0.0.1:4321/');
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
