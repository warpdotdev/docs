import assert from 'node:assert/strict';
import { test } from 'node:test';
import middleware from '../middleware.js';

test('permanently redirects LinkedIn variants to the clean path', () => {
	for (const query of ['trk=article-ssr-frontend-pulse_little-text-block', 'trk=', 'trk=a&trk=b']) {
		const response = middleware(new Request(`https://docs.warp.dev/factories/how-factories-work?${query}`));
		assert.equal(response.status, 301);
		assert.equal(response.headers.get('location'), 'https://docs.warp.dev/factories/how-factories-work');
	}
});

test('preserves other parameters and does not loop', () => {
	const response = middleware(new Request('https://docs.warp.dev/factories?utm_source=linkedin&trk=post&q=a%26b&q=c'));
	const url = new URL(response.headers.get('location'));
	assert.deepEqual([...url.searchParams], [['utm_source', 'linkedin'], ['q', 'a&b'], ['q', 'c']]);
	assert.equal(middleware(new Request(url)).headers.get('x-middleware-next'), '1');
});

test('does not change URLs without trk', () => {
	const response = middleware(new Request('https://docs.warp.dev/factories?utm_source=linkedin'));
	assert.equal(response.headers.has('location'), false);
	assert.equal(response.headers.get('x-middleware-next'), '1');
});
