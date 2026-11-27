// Canonical `Link` headers for the generated Markdown twins.
//
// Each twin (`/factories.md`, `/index.md`) duplicates an HTML page, so its
// response carries `Link: <https://docs.warp.dev/factories/>; rel="canonical"`.
// The header is emitted only for twins the build generated: a pattern such as
// `/:path.md` in vercel.json would also label 404 responses for any other
// `.md` request. scripts/build-markdown-canonical-routes.mjs writes these routes
// into .vercel/output/config.json after `astro build`.
import { DOCS_ORIGIN } from './site.js';

// Keeps each route's `src` regex well below Vercel's per-pattern size limit.
const MAX_SOURCE_LENGTH = 3500;

/** @param {string} url */
export const canonicalLinkValue = (url) => `<${url}>; rel="canonical"`;

/**
 * @param {string} twinPath twin path without the leading slash or `.md`
 *   (`factories`, `terminal/blocks`, or `index` for the homepage)
 */
export function canonicalUrlForTwin(twinPath) {
	return twinPath === 'index' ? `${DOCS_ORIGIN}/` : `${DOCS_ORIGIN}/${twinPath}/`;
}

const escapeRegExp = (value) => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

/**
 * Builds Build Output API routes that add the canonical `Link` header to the
 * listed twins and to nothing else. Paths are grouped into a few alternation
 * routes; `$1` in the header value is the matched path. Matching is
 * case-sensitive because the static files are.
 *
 * @param {string[]} twinPaths see `canonicalUrlForTwin`
 */
export function buildMarkdownCanonicalRoutes(twinPaths) {
	const routes = [];
	const paths = [...new Set(twinPaths)].sort();
	if (paths.includes('index')) {
		routes.push({
			src: '^/index\\.md$',
			headers: { Link: canonicalLinkValue(canonicalUrlForTwin('index')) },
			caseSensitive: true,
			continue: true,
		});
	}

	let group = [];
	let length = 0;
	const flush = () => {
		if (group.length === 0) return;
		routes.push({
			src: `^/(${group.join('|')})\\.md$`,
			headers: { Link: canonicalLinkValue(`${DOCS_ORIGIN}/$1/`) },
			caseSensitive: true,
			continue: true,
		});
		group = [];
		length = 0;
	};
	for (const twinPath of paths) {
		if (twinPath === 'index') continue;
		const pattern = escapeRegExp(twinPath);
		if (length + pattern.length + 1 > MAX_SOURCE_LENGTH) flush();
		group.push(pattern);
		length += pattern.length + 1;
	}
	flush();
	return routes;
}

/**
 * Returns every `Link` header value the given routes add to a response for
 * `pathname`, using Vercel's route semantics: `src` is a regex matched
 * case-insensitively unless `caseSensitive` is set, and `$N` in a header value
 * is replaced with capture group N.
 *
 * @param {Array<{ src?: string, headers?: Record<string, string>, caseSensitive?: boolean }>} routes
 * @param {string} pathname
 */
export function linkHeadersFor(routes, pathname) {
	const values = [];
	for (const route of routes) {
		if (!route.src || !route.headers) continue;
		const key = Object.keys(route.headers).find((name) => name.toLowerCase() === 'link');
		if (!key) continue;
		const match = pathname.match(new RegExp(route.src, route.caseSensitive ? '' : 'i'));
		if (!match) continue;
		values.push(route.headers[key].replace(/\$(\d+)/g, (_, index) => match[Number(index)] ?? ''));
	}
	return values;
}
