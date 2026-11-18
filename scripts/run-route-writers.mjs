// Runs the postbuild route writers present in this checkout, in a fixed order.
// Each writer edits .vercel/output/config.json, removes only the routes it
// generated, and inserts its routes before `handle: filesystem`, so any subset
// composes. Listing them here keeps `postbuild` identical across branches that
// add writers, which avoids merge conflicts that would silently drop one.
import { execFileSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const writers = [
	'build-markdown-negotiation-routes.mjs',
	'build-markdown-canonical-routes.mjs',
];

for (const name of writers) {
	const file = fileURLToPath(new URL(`./${name}`, import.meta.url));
	if (!existsSync(file)) {
		console.log(`run-route-writers: ${name} not present, skipped`);
		continue;
	}
	execFileSync(process.execPath, [file], { stdio: 'inherit' });
}
