import assert from 'node:assert/strict';
import test from 'node:test';
import { buildWebMcpTools, registerWebMcpTools } from './webmcp-tools.js';

const origin = 'https://docs.warp.dev';

function mockProperty(t, object, key, value) {
	const descriptor = Object.getOwnPropertyDescriptor(object, key);
	Object.defineProperty(object, key, { configurable: true, value });
	t.after(() => {
		if (descriptor) Object.defineProperty(object, key, descriptor);
		else delete object[key];
	});
}

test('builds documented, read-only tools and limits hydrated Pagefind results to eight', async () => {
	let hydrated = 0;
	let loaded = 0;
	const tools = buildWebMcpTools({
		origin,
		fetch: async () => {
			throw new Error('Search must use Pagefind, not a retrieval endpoint.');
		},
		loadPagefind: async () => {
			loaded++;
			return {
				async search(query) {
					assert.equal(query, 'skills');
					return {
						results: Array.from({ length: 10 }, (_, i) => ({
							async data() {
								hydrated++;
								return {
									meta: { title: `Skills ${i}` },
									url: `/skills-${i}/`,
									excerpt: 'Find <mark>skills</mark>.',
								};
							},
						})),
					};
				},
			};
		},
	});
	assert.equal(loaded, 0);
	assert.deepEqual(tools.map((tool) => tool.name), ['search_docs_pages', 'get_page_markdown']);
	for (const tool of tools) {
		assert.ok(tool.description);
		assert.deepEqual(tool.annotations, { readOnlyHint: true });
		assert.equal(tool.inputSchema.type, 'object');
		assert.equal(tool.inputSchema.additionalProperties, false);
		assert.deepEqual(tool.inputSchema.required, Object.keys(tool.inputSchema.properties));
		for (const parameter of Object.values(tool.inputSchema.properties)) {
			assert.equal(parameter.type, 'string');
			assert.ok(parameter.description);
		}
	}
	const { pages } = await tools[0].execute({ query: ' skills ' });
	assert.equal(pages.length, 8);
	assert.equal(hydrated, 8);
	assert.deepEqual(pages[0], {
		title: 'Skills 0',
		url: `${origin}/skills-0/`,
		excerpt: 'Find <mark>skills</mark>.',
	});
	await assert.rejects(tools[0].execute({ query: ' ' }), /non-empty/);
});

test('returns empty search results and propagates index failures', async () => {
	const [search] = buildWebMcpTools({
		origin,
		loadPagefind: async () => ({ search: async () => ({ results: [] }) }),
	});
	assert.deepEqual(await search.execute({ query: 'not-found' }), { pages: [] });
	const [unavailable] = buildWebMcpTools({
		origin,
		loadPagefind: async () => { throw new Error('Index unavailable'); },
	});
	await assert.rejects(unavailable.execute({ query: 'skills' }), /Index unavailable/);
});

test('fetches Markdown twins, normalizes trailing slashes, and handles the homepage', async () => {
	const calls = [];
	const [, markdown] = buildWebMcpTools({
		origin,
		fetch: async (url, options) => {
			calls.push({ url, options });
			return { ok: true, text: async () => '# Warp docs' };
		},
	});
	for (const [path, twin] of [
		['/', '/index.md'],
		['/agents/capabilities/skills/', '/agents/capabilities/skills.md'],
		['/agents/capabilities/skills', '/agents/capabilities/skills.md'],
		['/agents///', '/agents.md'],
	]) {
		assert.deepEqual(await markdown.execute({ path }), {
			url: `${origin}${twin}`,
			markdown: '# Warp docs',
		});
	}
	assert.ok(calls.every(({ options }) =>
		options.redirect === 'error' && options.credentials === 'omit'));
});

test('rejects absolute or unsafe paths before fetching and reports HTTP failures', async () => {
	let calls = 0;
	const [, markdown] = buildWebMcpTools({
		origin,
		fetch: async () => { calls++; return { ok: false, status: 404 }; },
	});
	for (const path of [
		'https://evil.example/page', `${origin}/agents/`, '//evil.example/page',
		'/\\evil.example/page', 'agents/', '', '/page?q=1', '/page#heading',
		'/page\n', '/%2f%2fevil.example', '/%5cevil.example',
	]) {
		await assert.rejects(markdown.execute({ path }), /root-relative/);
	}
	assert.equal(calls, 0);
	await assert.rejects(markdown.execute({ path: '/missing/' }), /\(404\)/);
	assert.equal(calls, 1);
});

test('registers with document first, executes with mocked fetch, and cleans up only our tools', async (t) => {
	const registered = [];
	const removed = [];
	t.mock.method(globalThis, 'fetch', async (url) => {
		assert.equal(url, `${origin}/index.md`);
		return { ok: true, text: async () => '# Home' };
	});
	mockProperty(t, globalThis, 'location', { origin });
	mockProperty(t, globalThis, 'document', {
		modelContext: {
			registerTool(tool, options) { registered.push({ tool, options }); },
			unregisterTool(name) { removed.push(name); },
		},
	});
	mockProperty(t, globalThis.navigator, 'modelContext', {
		registerTool() { assert.fail('document.modelContext takes precedence'); },
	});
	const cleanup = registerWebMcpTools();
	assert.equal(registered.length, 2);
	assert.deepEqual(await registered[1].tool.execute({ path: '/' }), {
		url: `${origin}/index.md`, markdown: '# Home',
	});
	cleanup();
	cleanup();
	assert.deepEqual(removed, ['search_docs_pages', 'get_page_markdown']);
	assert.ok(registered.every(({ options }) => options.signal.aborted));
});

test('falls back to navigator and no-ops when the API is unavailable', (t) => {
	mockProperty(t, globalThis, 'document', {});
	mockProperty(t, globalThis, 'location', { origin });
	const names = [];
	mockProperty(t, globalThis.navigator, 'modelContext', {
		registerTool(tool) { names.push(tool.name); },
	});
	registerWebMcpTools()();
	assert.deepEqual(names, ['search_docs_pages', 'get_page_markdown']);
	Object.defineProperty(globalThis.navigator, 'modelContext', { configurable: true, value: undefined });
	assert.doesNotThrow(() => registerWebMcpTools()());
});
