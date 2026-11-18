import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { test } from 'node:test';
import {
	buildMarkdownNegotiationRoutes,
	isNegotiationRoute,
	resolve,
} from '../src/lib/markdown-negotiation-routes.js';

const routes = buildMarkdownNegotiationRoutes(['index', 'agents', 'terminal/blocks', 'a.b']);

test('homepage serves index.md for Accept: text/markdown, with Vary', () => {
	const r = resolve(routes, '/', 'text/markdown');
	assert.equal(r.dest, '/index.md');
	assert.equal(r.headers['Content-Type'], 'text/markdown; charset=utf-8');
	assert.equal(r.headers.Vary, 'Accept');
});

test('pages map to their twin with or without the trailing slash', () => {
	assert.equal(resolve(routes, '/agents/', 'text/markdown, text/html;q=0.5').dest, '/agents.md');
	assert.equal(resolve(routes, '/agents', 'text/markdown').dest, '/agents.md');
	assert.equal(resolve(routes, '/terminal/blocks/', 'text/markdown').dest, '/terminal/blocks.md');
});

test('HTML requests keep the HTML page and still get Vary: Accept', () => {
	for (const accept of ['text/html', 'text/html,application/xhtml+xml,*/*;q=0.8', '*/*', '']) {
		const r = resolve(routes, '/agents/', accept);
		assert.equal(r.dest, null, accept);
		assert.equal(r.headers.Vary, 'Accept');
		assert.equal(r.headers['Content-Type'], undefined);
	}
});

test('paths without a twin are untouched, and dots are escaped', () => {
	assert.deepEqual(resolve(routes, '/nope/', 'text/markdown'), { dest: null, headers: {} });
	assert.equal(resolve(routes, '/aXb/', 'text/markdown').dest, null);
	assert.equal(resolve(routes, '/a.b/', 'text/markdown').dest, '/a.b.md');
	assert.equal(resolve(routes, '/Agents/', 'text/markdown').dest, null);
});

test('large inputs are split below the per-pattern size limit', () => {
	const many = Array.from({ length: 2000 }, (_, i) => `section-${i}/page-name-${i}`);
	const big = buildMarkdownNegotiationRoutes(many);
	assert.ok(big.length > 2);
	for (const route of big) assert.ok(route.src.length < 4000);
	assert.equal(resolve(big, '/section-1999/page-name-1999/', 'text/markdown').dest, '/section-1999/page-name-1999.md');
});

test('generated routes are recognized for idempotent reruns, others are not', () => {
	assert.ok(routes.every(isNegotiationRoute));
	assert.equal(isNegotiationRoute({ src: '^/index\\.md$', headers: { Link: '<x>; rel="canonical"' }, continue: true }), false);
	assert.equal(isNegotiationRoute({ handle: 'filesystem' }), false);
});

// After `npm run build`, check the real config: routes sit before the filesystem
// phase and resolve the homepage and a sample page.
const config = new URL('../.vercel/output/config.json', import.meta.url);
test('built config.json places negotiation routes before handle: filesystem', { skip: !existsSync(config) }, () => {
	const built = JSON.parse(readFileSync(config, 'utf8')).routes;
	const fs = built.findIndex((r) => r.handle === 'filesystem');
	const ours = built.map((r, i) => (isNegotiationRoute(r) ? i : -1)).filter((i) => i >= 0);
	assert.ok(ours.length >= 2);
	assert.ok(ours.every((i) => i < fs));
	const before = built.slice(0, fs).filter((r) => r.src);
	assert.equal(resolve(before.filter(isNegotiationRoute), '/', 'text/markdown').dest, '/index.md');
	assert.equal(resolve(before.filter(isNegotiationRoute), '/agents/', 'text/markdown').dest, '/agents.md');
});
