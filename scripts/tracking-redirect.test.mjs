import assert from 'node:assert/strict';
import { test } from 'node:test';
import trackingRedirect from '../src/lib/tracking-redirect.js';

function redirect(query, path = 'factories/how-factories-work') {
	return trackingRedirect(new Request(`https://docs.warp.dev/${path}?${query}`));
}

test('permanently redirects LinkedIn variants to the clean path', () => {
	for (const query of ['trk=article-ssr-frontend-pulse_little-text-block', 'trk=', 'trk=a&trk=b']) {
		const response = redirect(query);
		assert.equal(response.status, 301);
		assert.equal(response.headers.get('location'), 'https://docs.warp.dev/factories/how-factories-work');
	}
});

test('redirects the homepage without losing its root path', () => {
	assert.equal(redirect('trk=post', '').headers.get('location'), 'https://docs.warp.dev/');
});

test('preserves other parameters and does not loop', () => {
	const response = redirect('utm_source=linkedin&trk=post&q=a%26b&q=c', 'factories');
	const url = new URL(response.headers.get('location'));
	assert.deepEqual([...url.searchParams], [['utm_source', 'linkedin'], ['q', 'a&b'], ['q', 'c']]);
	assert.equal(redirect(url.search.slice(1), 'factories').headers.get('x-middleware-next'), '1');
});

test('does not change URLs without trk', () => {
	const response = redirect('utm_source=linkedin');
	assert.equal(response.headers.has('location'), false);
	assert.equal(response.headers.get('x-middleware-next'), '1');
});
