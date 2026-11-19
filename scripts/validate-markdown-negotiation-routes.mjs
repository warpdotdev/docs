import assert from 'node:assert/strict';
import { access, readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

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

console.log(
	`markdown-negotiation route OK at index ${index} (filesystem at ${filesystem}, function at ${funcDir})`,
);
