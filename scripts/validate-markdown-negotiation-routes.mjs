import assert from 'node:assert/strict';
import { access, readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import routingUtils from '@vercel/routing-utils';
import { routingJourneys } from './routing-journeys.mjs';

// Run after `npm run build`: markdown negotiation must be a routing middleware
// entry before the filesystem handler, or Vercel serves static HTML instead.
const output = new URL('../.vercel/output/', import.meta.url);
const config = JSON.parse(await readFile(new URL('config.json', output), 'utf8'));
const filesystem = config.routes.findIndex((route) => route.handle === 'filesystem');
const index = config.routes.findIndex(
	(route) => route.middlewarePath === 'markdown-negotiation',
);

assert.ok(index !== -1, 'no markdown-negotiation routing middleware route');
assert.ok(
	filesystem === -1 || index < filesystem,
	'markdown-negotiation route runs after the filesystem handler',
);

const funcDir = fileURLToPath(new URL('functions/markdown-negotiation.func/', output));
await access(new URL('index.js', new URL('functions/markdown-negotiation.func/', output)));
await access(new URL('docs-markdown.js', new URL('functions/markdown-negotiation.func/', output)));
await access(new URL('.vc-config.json', new URL('functions/markdown-negotiation.func/', output)));

const vcConfig = JSON.parse(
	await readFile(new URL('functions/markdown-negotiation.func/.vc-config.json', output), 'utf8'),
);
assert.equal(vcConfig.runtime, 'edge');
assert.equal(vcConfig.entrypoint, 'index.js');

// Tracking redirects should still run first so stripped query params never
// leak into the rewritten markdown URL.
const trackingIndexes = config.routes
	.map((route, i) => (route.middlewarePath === 'tracking-redirect' ? i : -1))
	.filter((i) => i !== -1);
assert.ok(trackingIndexes.length > 0, 'tracking-redirect routes missing');
assert.ok(
	Math.max(...trackingIndexes) < index,
	'markdown-negotiation should run after tracking-redirect routes',
);

// Exercise the generated entrypoint, including its actual built-page allowlist.
// This models the middleware and redirect stages, not Vercel's full CDN.
const { default: negotiate } = await import(new URL('functions/markdown-negotiation.func/index.js', output));
const { default: track } = await import(new URL('functions/tracking-redirect.func/index.js', output));
const vercel = JSON.parse(await readFile(new URL('../vercel.json', import.meta.url), 'utf8'));
const { routes, error } = routingUtils.getTransformedRoutes({
	trailingSlash: vercel.trailingSlash,
	redirects: vercel.redirects,
});
assert.equal(error, null);
const redirectRoutes = routes.filter((route) => route.status && route.headers?.Location)
	.map((route) => ({ ...route, re: new RegExp(route.src) }));

async function journey(path, accept) {
	let url = new URL(path, 'https://docs.warp.dev');
	const seen = new Set();
	let hops = 0;
	while (hops < 6) {
		assert.ok(!seen.has(url.href), `loop at ${url.href}`);
		seen.add(url.href);
		const request = new Request(url, { headers: { accept } });
		const tracking = track(request);
		let location = tracking.headers.get('location');
		if (!location) {
			const response = negotiate(request);
			const rewritten = response.headers.get('x-middleware-rewrite');
			if (rewritten) {
				const target = new URL(rewritten);
				assert.ok(!target.pathname.endsWith('/.md'), target.pathname);
				await access(new URL(`static${target.pathname}`, output));
				return { final: url.pathname + url.search, hops, markdown: true };
			}
			const route = redirectRoutes.find(({ re }) => re.test(url.pathname));
			if (route) {
				const match = route.re.exec(url.pathname);
				location = route.headers.Location.replace(/\$(\d+)/g, (_, n) => match[Number(n)] ?? '');
				const destination = new URL(location, url);
				if (!destination.search) destination.search = url.search;
				location = destination.href;
			}
		}
		if (!location) return { final: url.pathname + url.search, hops, markdown: false };
		url = new URL(location, url);
		hops += 1;
	}
	throw new Error(`Too many redirects from ${path}`);
}

for (const fixture of routingJourneys) {
	for (const accept of ['text/html', 'text/markdown']) {
		const actual = await journey(fixture.path, accept);
		assert.equal(actual.final, fixture.final, `${fixture.path} (${accept}) destination`);
		assert.equal(actual.hops, fixture.hops, `${fixture.path} (${accept}) hops`);
		const isDoc = !fixture.type && !fixture.status && !fixture.final.startsWith('/api')
			&& !fixture.final.endsWith('.html');
		assert.equal(actual.markdown, accept === 'text/markdown' && isDoc, `${fixture.path} (${accept}) negotiation`);
		if (fixture.status !== 404) {
			const pathname = new URL(fixture.final, 'https://docs.warp.dev').pathname;
			await access(new URL(`static${pathname}${pathname.endsWith('/') ? 'index.html' : ''}`, output));
		}
	}
}

console.log(
	`markdown-negotiation route OK at index ${index} (filesystem at ${filesystem}, function at ${funcDir}); ${routingJourneys.length * 2} modeled HTML/Markdown journeys passed`,
);
