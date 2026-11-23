import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { STRIPPED_PARAMS } from '../src/lib/tracking-redirect.js';

// Run after `npm run build`: every stripped parameter must have its own routing
// entry before the filesystem handler, or Vercel serves the copy without redirecting.
const config = JSON.parse(await readFile(new URL('../.vercel/output/config.json', import.meta.url), 'utf8'));
const filesystem = config.routes.findIndex((route) => route.handle === 'filesystem');
for (const key of STRIPPED_PARAMS) {
	const index = config.routes.findIndex((route) => route.middlewarePath === 'tracking-redirect'
		&& route.has?.length === 1 && route.has[0].type === 'query' && route.has[0].key === key);
	assert.ok(index !== -1, `no tracking-redirect route for ?${key}`);
	assert.ok(filesystem === -1 || index < filesystem, `?${key} route runs after the filesystem handler`);
}
console.log(`tracking-redirect routes OK: ${STRIPPED_PARAMS.join(', ')}`);
