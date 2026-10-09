import { spawnSync } from 'node:child_process';
import { performance } from 'node:perf_hooks';

// A shallow boundary commit makes unchanged files look newly modified to
// Starlight. Fetch history before Astro inlines git dates for pages/sitemaps.
const shallow = spawnSync('git', ['rev-parse', '--is-shallow-repository'], { encoding: 'utf8' });
if (shallow.status === 0 && shallow.stdout.trim() === 'true') {
	const start = performance.now();
	const fetch = spawnSync('git', ['fetch', '--unshallow', '--no-tags', 'origin'], { stdio: 'inherit' });
	if (fetch.status !== 0) throw new Error('Full git history is required for truthful page dates.');
	console.log(`Fetched full git history in ${((performance.now() - start) / 1000).toFixed(1)}s.`);
}
