import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseHTML } from 'linkedom';
import sharp from 'sharp';
import { socialImageMeta, socialImageTitle } from '../src/lib/social-image.js';

const root = process.argv[2]
	? path.resolve(process.argv[2])
	: fileURLToPath(new URL('../.vercel/output/static/', import.meta.url));
const images = new Set();
let pages = 0;
let fallbackPages = 0;

async function walk(directory) {
	for (const entry of await readdir(directory, { withFileTypes: true })) {
		const filename = path.join(directory, entry.name);
		if (entry.isDirectory()) {
			await walk(filename);
			continue;
		}
		if (!entry.name.endsWith('.html')) continue;
		const { document } = parseHTML(await readFile(filename, 'utf8'));
		const title = socialImageTitle(document);
		const imageTags = document.querySelectorAll('meta[property="og:image"]');
		assert.equal(imageTags.length, 1, `${filename}: duplicate or missing image`);
		const url = new URL(imageTags[0].getAttribute('content'));
		assert.equal(url.origin, 'https://docs.warp.dev');
		assert.match(url.pathname, title
			? /^\/(?:assets\/og\/[a-f0-9]{24}|og-image)\.png$/
			: /^\/og-image\.png$/);
		if (url.pathname === '/og-image.png') fallbackPages++;
		for (const { attrs } of socialImageMeta(url.pathname, title)) {
			const key = attrs.property ?? attrs.name;
			const attribute = attrs.property ? 'property' : 'name';
			const tags = document.querySelectorAll(`meta[${attribute}="${key}"]`);
			assert.equal(tags.length, 1, `${filename}: ${key} must be unique`);
			assert.equal(tags[0].getAttribute('content'), attrs.content, `${filename}: ${key}`);
		}
		images.add(url.pathname);
		pages++;
	}
}

await walk(root);
assert.ok(pages > 0, 'Build the docs before validating social previews');
for (const imagePath of [...images, '/og-image.png']) {
	const metadata = await sharp(path.join(root, imagePath)).metadata();
	assert.equal(metadata.format, 'png', imagePath);
	assert.equal(metadata.width, 1200, imagePath);
	assert.equal(metadata.height, 630, imagePath);
}
console.log(`Verified OG/Twitter metadata on ${pages} pages and ${images.size} PNG previews (1200×630); ${fallbackPages} pages use the default image.`);
