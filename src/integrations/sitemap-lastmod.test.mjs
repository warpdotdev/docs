import assert from 'node:assert/strict';
import test from 'node:test';
import { withLastmod } from './sitemap-lastmod.js';

test('sitemap uses the exact rendered Starlight date, not build time', () => {
	const item = { url: 'https://docs.warp.dev/factories/quickstart/' };
	for (const date of ['2026-10-08T17:42:12.000Z', '2025-03-01T09:00:00.000Z']) {
		assert.deepEqual(
			withLastmod(item, `<meta property="article:modified_time" content="${date}">`),
			{ ...item, lastmod: date },
		);
	}
});

test('pages without a valid Starlight date do not invent lastmod', () => {
	const item = { url: 'https://docs.warp.dev/api/' };
	for (const html of ['', '<time datetime="2026-10-09">A content example</time>',
		'<meta property="article:modified_time" content="invalid">']) {
		assert.equal(withLastmod(item, html), item);
	}
});
