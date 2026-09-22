#!/usr/bin/env node
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { parseHTML } from 'linkedom';

const DOCS_ORIGIN = 'https://docs.warp.dev';
const WARP_ORIGIN = 'https://www.warp.dev';
const ORGANIZATION_ID = `${WARP_ORIGIN}/#organization`;
const WEBSITE_ID = `${DOCS_ORIGIN}/#website`;

function parseJsonLd(html) {
	const { document } = parseHTML(html);
	return Array.from(document.querySelectorAll('script[type="application/ld+json"]'), (script) =>
		JSON.parse(script.textContent),
	);
}

const homepageHtml = await readFile(
	new URL('../.vercel/output/static/index.html', import.meta.url),
	'utf8',
);
const payloads = parseJsonLd(homepageHtml);
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
