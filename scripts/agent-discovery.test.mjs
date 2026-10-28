import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';

const DOCS_ORIGIN = 'https://docs.warp.dev';
const repoFile = (path) => new URL(`../${path}`, import.meta.url);
const readJson = async (path) => JSON.parse(await readFile(repoFile(path), 'utf8'));

const catalog = await readJson('public/.well-known/ard.json');
const byId = (identifier) => catalog.entries.find((entry) => entry.identifier === identifier);

test('ARD catalog entries are valid', () => {
	assert.deepEqual(Object.keys(catalog), ['entries']);
	assert.ok(catalog.entries.length > 0);
	const identifiers = catalog.entries.map((entry) => entry.identifier);
	assert.equal(new Set(identifiers).size, identifiers.length, 'Identifiers must be unique');
	for (const entry of catalog.entries) {
		assert.match(entry.identifier, /^urn:air:warp\.dev:[a-z0-9._-]+:[a-z0-9._-]+$/);
		assert.equal(typeof entry.displayName, 'string');
		assert.equal(typeof entry.type, 'string');
		assert.equal(typeof entry.description, 'string');
		assert.notEqual('url' in entry, 'data' in entry, `${entry.identifier} needs exactly one of url or data`);
		assert.ok(entry.url.startsWith('https://'), `${entry.identifier} url must use HTTPS`);
		assert.ok(entry.representativeQueries.length >= 2 && entry.representativeQueries.length <= 5);
		for (const query of entry.representativeQueries) assert.equal(typeof query, 'string');
	}
});

test('MCP entry points to the served MCP manifest', async () => {
	const entry = byId('urn:air:warp.dev:server:documentation');
	assert.equal(entry.url, `${DOCS_ORIGIN}/.well-known/mcp.json`);
	const manifest = await readJson('public/.well-known/mcp.json');
	assert.match(manifest.url, /^https:\/\//);
});

test('OpenAPI entry media type matches the spec version', async () => {
	const entry = byId('urn:air:warp.dev:api:agent');
	assert.equal(entry.url, `${DOCS_ORIGIN}/openapi.json`);
	const spec = await readFile(repoFile('developers/agent-api-openapi.yaml'), 'utf8');
	const [, major, minor] = spec.match(/^openapi:\s*['"]?(\d+)\.(\d+)/m);
	assert.equal(entry.type, `application/vnd.oai.openapi+json;version=${major}.${minor}`);
});

test('LLM index entry points to the generated docs llms.txt', async () => {
	const entry = byId('urn:air:warp.dev:resource:docs-llms');
	assert.equal(entry.url, `${DOCS_ORIGIN}/llms.txt`);
	assert.equal(entry.type, 'text/plain');
	const astroConfig = await readFile(repoFile('astro.config.mjs'), 'utf8');
	assert.match(astroConfig, /from 'starlight-llms-txt'/, 'starlight-llms-txt generates /llms.txt');
});

test('discovery manifests do not use retired Oz wording or URLs', async () => {
	const serialized = JSON.stringify([catalog, await readJson('public/.well-known/mcp.json')]);
	assert.doesNotMatch(serialized, /\boz\b/i);
	assert.doesNotMatch(serialized, /\/oz(?:[/#?"]|$)/i);
});
