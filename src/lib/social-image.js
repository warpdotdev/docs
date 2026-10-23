import { DOCS_ORIGIN } from './site.js';

export function socialImageTitle(document) {
	// Read the rendered heading so MDX variables and custom pages use
	// the same title a reader sees, not raw frontmatter tokens.
	return (document.querySelector('h1')?.textContent ??
		document.querySelector('title')?.textContent?.replace(/\s+\|\s+Warp$/, '') ??
		'').replace(/\s+/g, ' ').trim();
}

/** @returns {Array<{ tag: 'meta', attrs: Record<string, string> }>} */
export function socialImageMeta(imagePath = '/og-image.png', title = '') {
	const url = new URL(imagePath, DOCS_ORIGIN).href;
	const alt = title ? `Warp Docs — ${title}` : 'Warp Docs';
	return [
		{ tag: 'meta', attrs: { property: 'og:image', content: url } },
		{ tag: 'meta', attrs: { property: 'og:image:secure_url', content: url } },
		{ tag: 'meta', attrs: { property: 'og:image:type', content: 'image/png' } },
		{ tag: 'meta', attrs: { property: 'og:image:width', content: '1200' } },
		{ tag: 'meta', attrs: { property: 'og:image:height', content: '630' } },
		{ tag: 'meta', attrs: { property: 'og:image:alt', content: alt } },
		{ tag: 'meta', attrs: { name: 'twitter:card', content: 'summary_large_image' } },
		{ tag: 'meta', attrs: { name: 'twitter:image', content: url } },
		{ tag: 'meta', attrs: { name: 'twitter:image:alt', content: alt } },
	];
}
