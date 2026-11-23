import { createHash } from 'node:crypto';
import { mkdir, mkdtemp, readFile, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';
import wawoff2 from 'wawoff2';

const fonts = [
	['Inter', 'Inter.ttf'],
	['Noto Sans CJK SC', 'NotoSansCJKsc-Regular.otf'],
	['Noto Sans Arabic', 'NotoSansArabic.ttf'],
	['Noto Emoji', 'NotoEmoji.ttf'],
];
const fontFamily = ['Azeret SemiMono', ...fonts.map(([family]) => family)].join(',');
const brandFonts = [
	['AzeretSemiMono-Regular', 'Azeret SemiMono', 'ec128d9217ae3efad5ddbea95d91b1484bdab1bcc31c81632203cc6848534498'],
	['AzeretSemiMono-Medium', 'Azeret SemiMono Medium', 'f244c345ee26ef329bcba90dcca72191483d178e66b2dedea781c6af1f45a956'],
];
let assets;

export function loadOgAssets() {
	return assets ??= (async () => {
		const cache = new URL('../../node_modules/.cache/warp-og-fonts/', import.meta.url);
		const temporary = await mkdtemp(path.join(tmpdir(), 'warp-og-fonts-'));
		for (const [name, family, hash] of brandFonts) {
			const cached = new URL(`${hash}.woff2`, cache);
			let compressed;
			try {
				compressed = await readFile(cached);
			} catch (error) {
				if (error.code !== 'ENOENT') throw error;
				const response = await fetch(`https://www.warp.dev/fonts/${name}.woff2`, {
					signal: AbortSignal.timeout(30_000),
				});
				if (!response.ok) throw new Error(`Cannot download OG font ${name}: HTTP ${response.status}`);
				compressed = Buffer.from(await response.arrayBuffer());
			}
			if (createHash('sha256').update(compressed).digest('hex') !== hash) {
				throw new Error(`OG font checksum mismatch: ${name}`);
			}
			await mkdir(cache, { recursive: true });
			await writeFile(cached, compressed);
			// Pango needs the decoded font, kept outside the public build output.
			const fontfile = path.join(temporary, `${name}.ttf`);
			await writeFile(fontfile, await wawoff2.decompress(compressed));
			await sharp({ text: { text: 'A', font: family, fontfile } }).png().toBuffer();
		}
		// Register fallback faces with Pango, even on hosts without system fonts.
		for (const [font, filename] of fonts) {
			await sharp({
				text: {
					text: 'A',
					font,
					fontfile: fileURLToPath(new URL(`../assets/og/fonts/${filename}`, import.meta.url)),
				},
			}).png().toBuffer();
		}
		const logoSvg = (await readFile(new URL('../assets/warp-logo-light.svg', import.meta.url), 'utf8'))
			.replaceAll('#121212', '#000000');
		const logo = await sharp(Buffer.from(logoSvg)).resize({ width: 160 }).trim().png().toBuffer();
		const label = await renderText('DOCUMENTATION', 18, '#FFFFFF', 'Azeret SemiMono Medium', -0.02);
		return { logo, label };
	})();
}

function escapeMarkup(text) {
	return text.replace(/[&<>"']/g, (character) => ({
		'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;',
	})[character]);
}

function renderText(text, size, color, family = fontFamily, tracking = -0.05) {
	return sharp({
		text: {
			text: `<span foreground="${color}" letter_spacing="${Math.round(size * tracking * 1024)}" line_height="${Math.round(size * 1.15 * 1024)}">${escapeMarkup(text)}</span>`,
			font: `${family} ${size}`,
			width: 1072,
			dpi: 72,
			rgba: true,
			wrap: 'word-char',
		},
	}).png().toBuffer({ resolveWithObject: true });
}

export async function renderOgImage(title, section = '') {
	title = title?.replace(/\s+/g, ' ').trim().toUpperCase();
	if (!title || title.length > 2000) throw new Error('Title cannot fit a legible social image');
	const { logo, label } = await loadOgAssets();

	let text;
	for (let size = 112; size >= 28; size -= 2) {
		const candidate = await renderText(title, size, '#000000');
		if (candidate.info.width <= 1072 && candidate.info.height <= 280) {
			text = candidate;
			break;
		}
	}
	if (!text) throw new Error('Title cannot fit a legible social image');

	const background = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630">
		<rect width="1200" height="630" fill="#D5DFE2"/>
		<rect x="920.5" y="64.5" width="215" height="43" rx="21.5" fill="#1008FF" stroke="#000000"/>
	</svg>`);

	const eyebrow = section
		? await renderText(section.toUpperCase(), 48, '#555555', 'Azeret SemiMono Medium', -0.02)
		: undefined;
	return sharp(background).composite([
		{ input: logo, left: 64, top: 64 },
		{ input: label.data, left: 920 + Math.round((216 - label.info.width) / 2), top: 64 + Math.round((44 - label.info.height) / 2) },
		...(eyebrow ? [{ input: eyebrow.data, left: 64, top: 566 - text.info.height - 24 - eyebrow.info.height }] : []),
		{ input: text.data, left: 64, top: 566 - text.info.height },
	]).png().toBuffer();
}
