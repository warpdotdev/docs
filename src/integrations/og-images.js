import { createHash } from 'node:crypto';
import { mkdir, readFile, readdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseHTML } from 'linkedom';
import { renderOgImage } from '../lib/og-image.js';
import { socialImageMeta, socialImageTitle } from '../lib/social-image.js';

export default function ogImages() {
	return {
		name: 'warp-og-images',
		hooks: {
			'astro:build:generated': async ({ dir, logger }) => {
				const count = await generateOgImages(fileURLToPath(dir), logger);
				logger.info(`Generated social previews for ${count} HTML pages`);
			},
		},
	};
}

export async function generateOgImages(outputRoot, logger) {
	const images = new Map();
	let count = 0;

	async function imageForTitle(title) {
		if (!title) return '/og-image.png';
		if (images.has(title)) return images.get(title);
		let imagePath = '/og-image.png';
		try {
			const png = await renderOgImage(title);
			const hash = createHash('sha256').update(png).digest('hex').slice(0, 24);
			imagePath = `/assets/og/${hash}.png`;
			await mkdir(path.join(outputRoot, 'assets/og'), { recursive: true });
			await writeFile(path.join(outputRoot, imagePath), png);
		} catch (error) {
			logger.warn(`Using default social image for "${title}": ${error.message}`);
			imagePath = '/og-image.png';
		}
		images.set(title, imagePath);
		return imagePath;
	}

	async function walk(directory) {
		for (const entry of await readdir(directory, { withFileTypes: true })) {
			const filename = path.join(directory, entry.name);
			if (entry.isDirectory()) {
				await walk(filename);
			} else if (entry.isFile() && entry.name.endsWith('.html')) {
				const html = await readFile(filename, 'utf8');
				const { document } = parseHTML(html);
				if (!document.head) continue;
				const title = socialImageTitle(document);
				const imagePath = await imageForTitle(title);
				await writeFile(filename, replaceSocialImageMeta(html, document, imagePath, title));
				count++;
			}
		}
	}

	await walk(outputRoot);
	return count;
}

function replaceSocialImageMeta(html, document, imagePath, title) {
	for (const meta of document.head.querySelectorAll('meta')) {
		const key = meta.getAttribute('property') ?? meta.getAttribute('name') ?? '';
		if (/^(og:image(?::.*)?|twitter:image(?::.*)?|twitter:card)$/.test(key)) meta.remove();
	}
	for (const { attrs } of socialImageMeta(imagePath, title)) {
		const meta = document.createElement('meta');
		for (const [name, value] of Object.entries(attrs)) meta.setAttribute(name, value);
		document.head.append(meta);
	}

	// Leave article HTML byte-for-byte intact; only the head needs new metadata.
	return html.replace(/<head\b[^>]*>[\s\S]*?<\/head>/i, () => document.head.outerHTML);
}
