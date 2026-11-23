import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { copyFile, mkdtemp, mkdir, readFile, readdir, rename, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';
import { parseHTML } from 'linkedom';
import sharp from 'sharp';
import { generateOgImages } from './og-images.js';
import { renderOgImage } from '../lib/og-image.js';

async function validateOutput(root) {
	await copyFile(new URL('../../public/og-image.png', import.meta.url), path.join(root, 'og-image.png'));
	const result = spawnSync(process.execPath, [
		fileURLToPath(new URL('../../scripts/validate-og-images.mjs', import.meta.url)),
		root,
	], { encoding: 'utf8' });
	assert.equal(result.status, 0, result.stderr);
}

const examples = [
	'Quickstart',
	'Configuring self-hosted workers and repository access for cloud agents across multiple environments',
	'W'.repeat(180),
	'Creating and coordinating agents with permissions, environments, integrations, schedules, and repositories '.repeat(4).trim(),
	'Créer des agents — Καλημέρα · Привет · 你好 · مرحبًا 🚀',
	'CLI: <flags> & "quoted values" — what’s next?',
];

test('fits short, multiline, extreme, unbroken and Unicode titles within the safe area', async () => {
	const cards = new Set();
	for (const title of examples) {
		const png = await renderOgImage(title);
		const metadata = await sharp(png).metadata();
		assert.equal(metadata.format, 'png');
		assert.equal(metadata.width, 1200);
		assert.equal(metadata.height, 630);
		cards.add(png.toString('base64'));

		const { data, info } = await sharp(png)
			.extract({ left: 0, top: 200, width: 1200, height: 430 })
			.removeAlpha().raw().toBuffer({ resolveWithObject: true });
		let titlePixels = 0;
		for (let y = 0; y < info.height; y++) {
			for (let x = 0; x < info.width; x++) {
				const offset = (y * info.width + x) * info.channels;
				if (data[offset] > 40 || data[offset + 1] > 40 || data[offset + 2] > 40) continue;
				titlePixels++;
				assert.ok(x >= 64 && x < 1136 && y < 366, `Title escaped padding: ${title}`);
			}
		}
		assert.ok(titlePixels > 1000, 'Title must be visible, not blank');
	}
	assert.equal(cards.size, examples.length, 'Every title must produce its own image');
	assert.ok((await renderOgImage('Quickstart')).equals(await renderOgImage('Quickstart')));
});

test('uses the chrome-blue design with a documentation pill and bottom-aligned uppercase title', async () => {
	const png = await renderOgImage('Skills for agents');
	const { data, info } = await sharp(png).removeAlpha().raw().toBuffer({ resolveWithObject: true });
	const pixel = (x, y) => [...data.subarray((y * info.width + x) * 3, (y * info.width + x) * 3 + 3)];
	assert.deepEqual(pixel(0, 0), [213, 223, 226]);
	assert.ok(png.equals(await renderOgImage('SKILLS FOR AGENTS')), 'Titles must be uppercase');
	assert.deepEqual(pixel(1000, 66), [16, 8, 255]);
	assert.deepEqual(pixel(1000, 64), [0, 0, 0]);
	let whitePillPixels = 0;
	let blackTitlePixels = 0;
	for (let y = 64; y < 108; y++) {
		for (let x = 920; x < 1120; x++) {
			if (pixel(x, y).every((channel) => channel === 255)) whitePillPixels++;
		}
	}
	for (let x = 64; x < 1136; x++) {
		if (pixel(x, 565).every((channel) => channel < 40)) blackTitlePixels++;
	}
	assert.ok(whitePillPixels > 300, 'The documentation label must be white and visible');
	assert.ok(blackTitlePixels > 20, 'The title must reach the 64px bottom margin');
	for (const region of [
		{ left: 64, top: 150, width: 1072, height: 50 },
		{ left: 0, top: 566, width: 1200, height: 64 },
	]) {
		const pixels = await sharp(png).extract(region).removeAlpha().raw().toBuffer();
		assert.ok(pixels.every((channel, index) => channel === [213, 223, 226][index % 3]), 'No subtitle, divider, or footer belongs on the card');
	}
});

test('rejects unavailable or changed brand fonts and renders from an offline cache', async () => {
	const expected = await renderOgImage('Tabs');
	const cache = fileURLToPath(new URL('../../node_modules/.cache/warp-og-fonts', import.meta.url));
	const backup = path.join(await mkdtemp(`${cache}-test-`), 'fonts');
	const renderer = new URL('../lib/og-image.js', import.meta.url).href;
	const integration = new URL('./og-images.js', import.meta.url).href;
	const run = (script) => spawnSync(process.execPath, ['--input-type=module', '-e', script]);
	await rename(cache, backup);
	try {
		for (const [response, message] of [
			["new Response('', { status: 503 })", /Cannot download OG font/],
			["new Response('corrupt font')", /OG font checksum mismatch/],
		]) {
			const result = run(`globalThis.fetch = async () => ${response};
				const { generateOgImages } = await import(${JSON.stringify(integration)});
				await generateOgImages('/unused-output', { warn() { throw Error('Unexpected fallback'); } });`);
			assert.notEqual(result.status, 0);
			assert.match(result.stderr.toString(), message);
		}
	} finally {
		await rename(backup, cache);
	}
	const result = run(`globalThis.fetch = async () => { throw Error('Network disabled'); };
		const { renderOgImage } = await import(${JSON.stringify(renderer)});
		process.stdout.write(await renderOgImage('Tabs'));`);
	assert.equal(result.status, 0, result.stderr.toString());
	assert.ok(result.stdout.equals(expected), 'Offline rendering must use the pinned brand fonts');
});

test('generates shared hashed assets and replaces duplicate metadata without altering scripts or article HTML', async () => {
	const root = await mkdtemp(path.join(os.tmpdir(), 'docs-og-'));
	const script = '<script>const example = \'<meta property="og:image" content="example">\';</script>';
	const body = '<body><h1>Cr&eacute;er &amp; &lt;configure&gt; 🚀</h1><p class="page-subtitle">Do not put this subtitle in the image.</p><p data-test=\'preserve\'>Article.</p></body>';
	const html = `<!doctype html><html><head><title>Other title | Warp</title>
		<meta property="og:image" content="/old.png">
		<meta property="og:image" content="/duplicate.png">
		<meta name="twitter:image" content="/old.png">
		<meta name="twitter:card" content="summary">
		<meta property="og:title" content="Keep title">
		<meta name="description" content="Keep description">${script}</head>${body}</html>`;
	await writeFile(path.join(root, 'index.html'), html);
	await mkdir(path.join(root, 'api'));
	await writeFile(path.join(root, 'api/index.html'), html);
	const warnings = [];
	assert.equal(await generateOgImages(root, { warn: (message) => warnings.push(message) }), 2);
	assert.deepEqual(warnings, []);
	const result = await readFile(path.join(root, 'api/index.html'), 'utf8');
	assert.ok(result.includes(body));
	assert.ok(result.includes(script));
	const { document } = parseHTML(result);
	const meta = (key) => document.querySelectorAll(`meta[property="${key}"],meta[name="${key}"]`);
	const image = meta('og:image')[0].getAttribute('content');
	assert.match(image, /^https:\/\/docs\.warp\.dev\/assets\/og\/[a-f0-9]{24}\.png$/);
	for (const key of ['og:image', 'twitter:image', 'og:image:secure_url']) {
		assert.equal(meta(key).length, 1);
		assert.equal(meta(key)[0].getAttribute('content'), image);
	}
	assert.equal(meta('twitter:card')[0].getAttribute('content'), 'summary_large_image');
	assert.equal(meta('og:image:alt')[0].getAttribute('content'), 'Warp Docs — Créer & <configure> 🚀');
	assert.equal(meta('twitter:image:alt')[0].getAttribute('content'), 'Warp Docs — Créer & <configure> 🚀');
	assert.equal(meta('og:title')[0].getAttribute('content'), 'Keep title');
	assert.equal(meta('description')[0].getAttribute('content'), 'Keep description');
	assert.equal((await readdir(path.join(root, 'assets/og'))).length, 1);
	assert.equal((await sharp(path.join(root, new URL(image).pathname)).metadata()).width, 1200);
	assert.ok((await readFile(path.join(root, new URL(image).pathname))).equals(await renderOgImage('Créer & <configure> 🚀')));
	await validateOutput(root);
});

test('uses document titles for custom pages and the existing default for untitled or unrenderable pages', async () => {
	const root = await mkdtemp(path.join(os.tmpdir(), 'docs-og-fallback-'));
	await writeFile(path.join(root, 'custom.html'), '<html><head><title>API reference | Warp</title></head><body></body></html>');
	await writeFile(path.join(root, 'untitled.html'), '<html><head></head><body><h1>  </h1></body></html>');
	await writeFile(path.join(root, 'extreme.html'), `<html><head></head><body><h1>${'W'.repeat(1200)}</h1></body></html>`);
	await writeFile(path.join(root, 'renderer-error.html'), '<html><head></head><body><h1>\u0000</h1></body></html>');
	const warnings = [];
	await generateOgImages(root, { warn: (message) => warnings.push(message) });
	for (const filename of ['untitled.html', 'extreme.html', 'renderer-error.html']) {
		const { document } = parseHTML(await readFile(path.join(root, filename), 'utf8'));
		assert.equal(document.querySelector('meta[property="og:image"]').getAttribute('content'), 'https://docs.warp.dev/og-image.png');
		assert.equal(document.querySelector('meta[name="twitter:image"]').getAttribute('content'), 'https://docs.warp.dev/og-image.png');
	}
	assert.equal(warnings.length, 2);
	assert.ok(warnings.some((message) => message.includes('Title cannot fit')));
	assert.ok(warnings.some((message) => message.includes('text: invalid markup')));
	const { document } = parseHTML(await readFile(path.join(root, 'custom.html'), 'utf8'));
	assert.match(document.querySelector('meta[property="og:image"]').getAttribute('content'), /\/assets\/og\//);
	assert.equal(document.querySelector('meta[property="og:image:alt"]').getAttribute('content'), 'Warp Docs — API reference');
	const customImage = new URL(document.querySelector('meta[property="og:image"]').getAttribute('content'));
	assert.ok((await readFile(path.join(root, customImage.pathname))).equals(await renderOgImage('API reference')));
	const fallback = await sharp(new URL('../../public/og-image.png', import.meta.url).pathname).metadata();
	assert.equal(fallback.format, 'png');
	assert.equal(fallback.width, 1200);
	assert.equal(fallback.height, 630);
	await validateOutput(root);
});

test('keeps metadata on a valid fallback when writing the rendered asset fails', async () => {
	const root = await mkdtemp(path.join(os.tmpdir(), 'docs-og-write-failure-'));
	await writeFile(path.join(root, 'index.html'), '<html><head></head><body><h1>Quickstart</h1></body></html>');
	await mkdir(path.join(root, 'assets'));
	await writeFile(path.join(root, 'assets/og'), 'Not a directory');
	const warnings = [];
	await generateOgImages(root, { warn: (message) => warnings.push(message) });
	assert.equal(warnings.length, 1);
	const { document } = parseHTML(await readFile(path.join(root, 'index.html'), 'utf8'));
	assert.equal(document.querySelector('meta[property="og:image"]').getAttribute('content'), 'https://docs.warp.dev/og-image.png');
	await validateOutput(root);
});
