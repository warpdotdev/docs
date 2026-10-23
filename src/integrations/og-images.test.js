import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { copyFile, mkdtemp, mkdir, readFile, readdir, writeFile } from 'node:fs/promises';
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
			.extract({ left: 0, top: 210, width: 1200, height: 310 })
			.removeAlpha().raw().toBuffer({ resolveWithObject: true });
		let titlePixels = 0;
		for (let y = 0; y < info.height; y++) {
			for (let x = 0; x < info.width; x++) {
				const offset = (y * info.width + x) * info.channels;
				if (data[offset] < 180 || data[offset + 1] < 180 || data[offset + 2] < 180) continue;
				titlePixels++;
				assert.ok(x >= 80 && x < 1120 && y >= 10 && y < 300, `Title escaped padding: ${title}`);
			}
		}
		assert.ok(titlePixels > 1000, 'Title must be visible, not blank');
	}
	assert.equal(cards.size, examples.length, 'Every title must produce its own image');
	assert.deepEqual(await renderOgImage('Quickstart'), await renderOgImage('Quickstart'));
});

test('leaves the auxiliary header and footer regions free of text', async () => {
	const png = await renderOgImage('Skills for agents');
	for (const region of [
		{ left: 370, top: 70, width: 750, height: 80 },
		{ left: 80, top: 540, width: 1040, height: 70 },
	]) {
		const pixels = await sharp(png).extract(region).removeAlpha().raw().toBuffer();
		assert.ok(pixels.every((channel) => channel < 50), 'Only the logo and page title belong on the card');
	}
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
	assert.deepEqual(await readFile(path.join(root, new URL(image).pathname)), await renderOgImage('Créer & <configure> 🚀'));
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
	assert.deepEqual(await readFile(path.join(root, customImage.pathname)), await renderOgImage('API reference'));
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
