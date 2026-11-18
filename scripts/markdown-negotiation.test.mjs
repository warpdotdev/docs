import assert from 'node:assert/strict';
import { test } from 'node:test';
import markdownNegotiation from '../src/lib/markdown-negotiation.js';

function request(path, headers = {}) {
	return new Request(`https://docs.warp.dev${path}`, { headers });
}

test('rewrites eligible paths when Accept prefers markdown', () => {
	const cases = [
		['/', '/index.md'],
		['/quickstart', '/quickstart.md'],
		['/quickstart/', '/quickstart.md'],
		['/support-and-community/', '/support-and-community.md'],
		['/agents/capabilities/skills', '/agents/capabilities/skills.md'],
	];

	for (const [path, expected] of cases) {
		const response = markdownNegotiation(
			request(path, { accept: 'text/markdown' }),
		);
		assert.equal(response.headers.get('x-middleware-next'), null);
		assert.equal(
			response.headers.get('x-middleware-rewrite'),
			`https://docs.warp.dev${expected}`,
		);
	}
});

test('rewrites when Accept includes text/plain or a known agent UA', () => {
	const plain = markdownNegotiation(request('/quickstart', { accept: 'text/plain' }));
	assert.equal(plain.headers.get('x-middleware-rewrite'), 'https://docs.warp.dev/quickstart.md');

	const agent = markdownNegotiation(
		request('/quickstart', { 'user-agent': 'Claude-User/1.0' }),
	);
	assert.equal(agent.headers.get('x-middleware-rewrite'), 'https://docs.warp.dev/quickstart.md');
});

test('preserves query strings on rewrite', () => {
	const response = markdownNegotiation(
		request('/quickstart?utm_source=agent', { accept: 'text/markdown' }),
	);
	assert.equal(
		response.headers.get('x-middleware-rewrite'),
		'https://docs.warp.dev/quickstart.md?utm_source=agent',
	);
});

test('continues for HTML clients, assets, APIs, retrieve, and direct .md URLs', () => {
	const skipped = [
		request('/quickstart', { accept: 'text/html' }),
		request('/quickstart.md', { accept: 'text/markdown' }),
		request('/_astro/page.js', { accept: 'text/markdown' }),
		request('/retrieve?q=hello', { accept: 'text/markdown' }),
		request('/api/support-handoff', { accept: 'text/markdown' }),
		request('/llms.txt', { accept: 'text/markdown' }),
	];

	for (const req of skipped) {
		const response = markdownNegotiation(req);
		assert.equal(response.headers.get('x-middleware-rewrite'), null);
		assert.equal(response.headers.get('x-middleware-next'), '1');
	}
});
