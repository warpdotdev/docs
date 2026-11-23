import { DOCS_ORIGIN } from './site.js';

const sections = new Map([
	['terminal', 'Terminal'],
	['code', 'Terminal'],
	['knowledge-and-collaboration', 'Terminal'],
	['getting-started', 'Terminal'],
	['quickstart', 'Terminal'],
	['agents', 'Agents'],
	['factories', 'Factories'],
	['api', 'Factories'],
	['platform', 'Automation Platform'],
	['changelog', 'Changelog'],
	['support-and-community', 'Support'],
	['enterprise', 'Enterprise'],
	['guides', 'Guides'],
]);

export function socialImageSection(pathname) {
	const [family] = pathname.split(/[?#]/, 1)[0]
		.replace(/^\/+|\/+$/g, '')
		.replace(/(?:^|\/)index\.html$/, '')
		.replace(/\.html$/, '')
		.split('/');
	return sections.get(family) ?? '';
}

export function socialImageTitle(document) {
	// Read the rendered heading so MDX variables and custom pages use
	// the same title a reader sees, not raw frontmatter tokens.
	return (document.querySelector('h1')?.textContent ??
		document.querySelector('title')?.textContent?.replace(/\s+\|\s+Warp$/, '') ??
		'').replace(/\s+/g, ' ').trim();
}

/** @returns {Array<{ tag: 'meta', attrs: Record<string, string> }>} */
export function socialImageMeta(imagePath = '/og-image.png', title = '', section = '') {
	const url = new URL(imagePath, DOCS_ORIGIN).href;
	const alt = ['Warp Docs', section, title].filter(Boolean).join(' — ');
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
