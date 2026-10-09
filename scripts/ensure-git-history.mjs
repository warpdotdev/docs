import { spawnSync } from 'node:child_process';
import { performance } from 'node:perf_hooks';

// A shallow boundary commit makes unchanged files look newly modified to
// Starlight. Fetch history before Astro inlines git dates for pages/sitemaps.
const shallow = spawnSync('git', ['rev-parse', '--is-shallow-repository'], { encoding: 'utf8' });
if (shallow.status === 0 && shallow.stdout.trim() === 'true') {
	const start = performance.now();
	const origin = spawnSync('git', ['remote', 'get-url', 'origin'], { encoding: 'utf8' });
	const { VERCEL_GIT_REPO_OWNER: owner, VERCEL_GIT_REPO_SLUG: slug } = process.env;
	const publicRepo = owner && slug && /^[\w.-]+$/.test(owner) && /^[\w.-]+$/.test(slug)
		? `https://github.com/${owner}/${slug}.git`
		: undefined;
	const remote = origin.status === 0 ? 'origin' : publicRepo;
	const fetch = remote
		? spawnSync('git', ['fetch', '--unshallow', '--no-tags', remote], { encoding: 'utf8', timeout: 120_000 })
		: undefined;
	if (fetch?.status === 0) {
		console.log(`Fetched full git history in ${((performance.now() - start) / 1000).toFixed(1)}s.`);
	} else {
		console.warn('Could not restore full git history; shallow-boundary page dates will be omitted.');
	}
}
