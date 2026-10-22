import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const fonts = [
	['Inter', 'Inter.ttf'],
	['Noto Sans CJK SC', 'NotoSansCJKsc-Regular.otf'],
	['Noto Sans Arabic', 'NotoSansArabic.ttf'],
	['Noto Emoji', 'NotoEmoji.ttf'],
];
const fontFamily = fonts.map(([family]) => family).join(',');
let assets;

function loadAssets() {
	return assets ??= (async () => {
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
		const logo = await sharp(await readFile(new URL('../assets/warp-logo-dark.svg', import.meta.url)))
			.resize(264, 92).png().toBuffer();
		const label = await renderText('DOCUMENTATION', 23, 600, '#a4a7ae');
		const footer = await renderText('docs.warp.dev', 25, 500, '#a4a7ae');
		return { logo, label: label.data, footer: footer.data };
	})();
}

function escapeMarkup(text) {
	return text.replace(/[&<>"']/g, (character) => ({
		'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;',
	})[character]);
}

function renderText(text, size, weight, color) {
	return sharp({
		text: {
			text: `<span foreground="${color}" weight="${weight}">${escapeMarkup(text)}</span>`,
			font: `${fontFamily} ${size}`,
			width: 1040,
			dpi: 72,
			rgba: true,
			wrap: 'word-char',
		},
	}).png().toBuffer({ resolveWithObject: true });
}

export async function renderOgImage(title) {
	title = title?.replace(/\s+/g, ' ').trim();
	if (!title || title.length > 2000) throw new Error('Title cannot fit a legible social image');
	const { logo, label, footer } = await loadAssets();

	let text;
	for (let size = 80; size >= 28; size -= 2) {
		const candidate = await renderText(title, size, 700, '#faf9f6');
		if (candidate.info.width <= 1040 && candidate.info.height <= 290) {
			text = candidate;
			break;
		}
	}
	if (!text) throw new Error('Title cannot fit a legible social image');

	const background = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630">
		<defs><pattern id="grid" width="150" height="105" patternUnits="userSpaceOnUse">
			<path d="M150 0H0V105" fill="none" stroke="#faf9f6" stroke-opacity=".04"/>
		</pattern></defs>
		<rect width="1200" height="630" fill="#121212"/>
		<rect width="1200" height="630" fill="url(#grid)"/>
		<rect x="80" y="190" width="80" height="4" rx="2" fill="#51a6ec"/>
		<path d="M80 530H1120" stroke="#414651"/>
	</svg>`);

	return sharp(background).composite([
		{ input: logo, left: 80, top: 48 },
		{ input: label, left: 382, top: 96 },
		{ input: text.data, left: 80, top: 220 + Math.floor((290 - text.info.height) / 2) },
		{ input: footer, left: 80, top: 558 },
	]).png().toBuffer();
}
