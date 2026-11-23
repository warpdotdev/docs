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
import { socialImageSection } from '../lib/social-image.js';

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

test('resolves stable content homes across route forms without prefix or navigation-order guesses', () => {
	for (const [family, section] of [
		['terminal', 'Terminal'], ['code', 'Terminal'],
		['knowledge-and-collaboration', 'Terminal'], ['getting-started', 'Terminal'],
		['quickstart', 'Terminal'], ['agents', 'Agents'], ['factories', 'Factories'],
		['api', 'Factories'], ['platform', 'Automation Platform'], ['changelog', 'Changelog'],
		['support-and-community', 'Support'], ['enterprise', 'Enterprise'], ['guides', 'Guides'],
	]) {
		for (const route of [`/${family}`, `/${family}/`, `${family}/index.html`, `/${family}.html`,
			`/${family}/new-page/`, `/${family}/new-page/index.html`, `/${family}/new-page.html`,
			`/${family}/new-page/?from=other#heading`]) {
			assert.equal(socialImageSection(route), section, route);
		}
		assert.equal(socialImageSection(`/${family}-extra/page`), '');
	}
	assert.equal(socialImageSection('/support-and-community/plans-and-billing/credits/'), 'Support');
	assert.equal(socialImageSection('/support-and-community/plans-and-billing/add-on-credits/'), 'Support');
	assert.equal(socialImageSection('/platform/transitioning-from-oz/'), 'Automation Platform');
	assert.equal(socialImageSection('/factories/guides/unlisted'), 'Factories');
	assert.equal(socialImageSection('/guides/factory-tutorial'), 'Guides');
	for (const route of ['/', '/index.html', 'index.html', '/404', '/404.html', '/unknown/', '/constructor', '/toString', '/__proto__']) {
		assert.equal(socialImageSection(route), '', route);
	}
});

test('fits short, multiline, extreme, unbroken and Unicode titles within the safe area', async () => {
	const cards = new Set();
	for (const title of examples) {
		const png = await renderOgImage(title, 'Automation Platform');
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

test('places every 32px gray section label above the unchanged black title with readable contrast', async () => {
	const title = 'Skills for agents';
	const original = await renderOgImage(title);
	for (const section of ['Terminal', 'Agents', 'Factories', 'Automation Platform', 'Changelog', 'Support', 'Enterprise', 'Guides']) {
		const png = await renderOgImage(title, section);
		const { data, info } = await sharp(png).removeAlpha().raw().toBuffer({ resolveWithObject: true });
		const gray = [];
		const black = [];
		for (let y = 200; y < 630; y++) {
			for (let x = 0; x < 1200; x++) {
				const offset = (y * info.width + x) * 3;
				const rgb = data.subarray(offset, offset + 3);
				if (rgb.every((channel) => channel === 85)) gray.push([x, y]);
				if (rgb.every((channel) => channel === 0)) black.push([x, y]);
			}
		}
		assert.ok(gray.length > 100, `${section}: opaque #555555 text must be visible`);
		const left = Math.min(...gray.map(([x]) => x));
		const right = Math.max(...gray.map(([x]) => x));
		const top = Math.min(...gray.map(([, y]) => y));
		const bottom = Math.max(...gray.map(([, y]) => y));
		const titleTop = Math.min(...black.map(([, y]) => y));
		assert.ok(left >= 64 && right < 1136 && top > 108);
		assert.ok(bottom - top >= 20 && bottom - top < 37, `${section}: preserve enlarged 32px text on one line`);
		assert.ok(titleTop - bottom >= 24 && titleTop - bottom <= 28, `${section}: preserve the 24px title gap`);
		const region = { left: 0, top: titleTop, width: 1200, height: 630 - titleTop };
		const actualTitle = await sharp(png).extract(region).raw().toBuffer();
		const originalTitle = await sharp(original).extract(region).raw().toBuffer();
		assert.ok(actualTitle.equals(originalTitle), 'Section labels must not change the full title or its layout');
	}
	const luminance = (rgb) => rgb.map((channel) => {
		const value = channel / 255;
		return value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
	}).reduce((sum, value, index) => sum + value * [0.2126, 0.7152, 0.0722][index], 0);
	const contrast = (luminance([213, 223, 226]) + 0.05) / (luminance([85, 85, 85]) + 0.05);
	assert.ok(contrast >= 4.5);
	assert.ok(Math.abs(contrast - 5.4964) < 0.0001);
});

test('rejects unavailable or changed brand fonts and renders from an offline cache', async () => {
	const expected = await renderOgImage('Tabs', 'Terminal');
	const cache = fileURLToPath(new URL('../../node_modules/.cache/warp-og-fonts', import.meta.url));
	const backup = path.join(await mkdtemp(`${cache}-test-`), 'fonts');
	const renderer = new URL('../lib/og-image.js', import.meta.url).href;
	const integration = new URL('./og-images.js', import.meta.url).href;
	const run = (scenario) => spawnSync(process.execPath, ['--input-type=module', '-e', `
		const scenario = process.argv[1];
		globalThis.fetch = async () => {
			if (scenario === 'offline') throw Error('Network disabled');
			if (scenario === 'unavailable') return new Response('', { status: 503 });
			return new Response('corrupt font');
		};
		if (scenario === 'offline') {
			const { renderOgImage } = await import(process.argv[2]);
			process.stdout.write(await renderOgImage('Tabs', 'Terminal'));
		} else {
			const { generateOgImages } = await import(process.argv[3]);
			await generateOgImages('/unused-output', { warn() { throw Error('Unexpected fallback'); } });
		}
	`, scenario, renderer, integration]);
	await rename(cache, backup);
	try {
		for (const [scenario, message] of [
			['unavailable', /Cannot download OG font/],
			['corrupt', /OG font checksum mismatch/],
		]) {
			const result = run(scenario);
			assert.notEqual(result.status, 0);
			assert.match(result.stderr.toString(), message);
		}
	} finally {
		await rename(backup, cache);
	}
	const result = run('offline');
	assert.equal(result.status, 0, result.stderr.toString());
	assert.ok(result.stdout.equals(expected), 'Offline rendering must use the pinned brand fonts');
});

test('generates hashed assets and replaces duplicate metadata without altering scripts or article HTML', async () => {
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
	assert.equal(meta('og:image:alt')[0].getAttribute('content'), 'Warp Docs — Factories — Créer & <configure> 🚀');
	assert.equal(meta('twitter:image:alt')[0].getAttribute('content'), 'Warp Docs — Factories — Créer & <configure> 🚀');
	assert.equal(meta('og:title')[0].getAttribute('content'), 'Keep title');
	assert.equal(meta('description')[0].getAttribute('content'), 'Keep description');
	assert.equal((await readdir(path.join(root, 'assets/og'))).length, 2);
	assert.equal((await sharp(path.join(root, new URL(image).pathname)).metadata()).width, 1200);
	assert.ok((await readFile(path.join(root, new URL(image).pathname))).equals(await renderOgImage('Créer & <configure> 🚀', 'Factories')));
	await validateOutput(root);
});

test('deduplicates equal title-section pairs but separates equal titles in different sections', async () => {
	const root = await mkdtemp(path.join(os.tmpdir(), 'docs-og-sections-'));
	const images = [];
	for (const route of ['agents/index.html', 'agents/another/index.html', 'guides/index.html']) {
		const filename = path.join(root, route);
		await mkdir(path.dirname(filename), { recursive: true });
		await writeFile(filename, '<html><head></head><body><h1>Quickstart</h1></body></html>');
	}
	const warnings = [];
	await generateOgImages(root, { warn: (message) => warnings.push(message) });
	assert.deepEqual(warnings, []);
	for (const [route, section] of [['agents/index.html', 'Agents'], ['agents/another/index.html', 'Agents'], ['guides/index.html', 'Guides']]) {
		const { document } = parseHTML(await readFile(path.join(root, route), 'utf8'));
		images.push(document.querySelector('meta[property="og:image"]').getAttribute('content'));
		for (const attribute of ['property="og:image:alt"', 'name="twitter:image:alt"']) {
			assert.equal(document.querySelector(`meta[${attribute}]`).getAttribute('content'), `Warp Docs — ${section} — Quickstart`);
		}
	}
	assert.equal(images[0], images[1]);
	assert.notEqual(images[0], images[2]);
	assert.equal((await readdir(path.join(root, 'assets/og'))).length, 2);
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
	await writeFile(path.join(root, 'agents.html'), '<html><head></head><body><h1>Quickstart</h1></body></html>');
	await mkdir(path.join(root, 'assets'));
	await writeFile(path.join(root, 'assets/og'), 'Not a directory');
	const warnings = [];
	await generateOgImages(root, { warn: (message) => warnings.push(message) });
	assert.equal(warnings.length, 1);
	const { document } = parseHTML(await readFile(path.join(root, 'agents.html'), 'utf8'));
	assert.equal(document.querySelector('meta[property="og:image"]').getAttribute('content'), 'https://docs.warp.dev/og-image.png');
	await validateOutput(root);
});
