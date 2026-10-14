import { copyFile, mkdir, readFile, writeFile } from 'node:fs/promises';

// Astro's Vercel adapter serves prerendered pages before its own middleware.
// Emit a native routing middleware before the filesystem phase instead:
// https://vercel.com/docs/build-output-api/features#routing-middleware
const output = new URL('../.vercel/output/', import.meta.url);
const configPath = new URL('config.json', output);
const config = JSON.parse(await readFile(configPath, 'utf8'));
const functionPath = new URL('functions/tracking-redirect.func/', output);
await mkdir(functionPath, { recursive: true });
await copyFile(
	new URL('../src/lib/tracking-redirect.js', import.meta.url),
	new URL('index.js', functionPath),
);
await writeFile(new URL('.vc-config.json', functionPath), JSON.stringify({
	runtime: 'edge',
	entrypoint: 'index.js',
}));
config.routes.unshift({
	src: '/(.*)',
	has: [{ type: 'query', key: 'trk' }],
	middlewarePath: 'tracking-redirect',
	continue: true,
});
await writeFile(configPath, JSON.stringify(config, null, 2));
