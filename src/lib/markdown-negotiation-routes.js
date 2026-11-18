// Markdown content negotiation for docs pages.
//
// A request for a page URL (`/`, `/agents/`, `/agents`) whose `Accept` header
// names `text/markdown` gets the page's generated Markdown twin (`/index.md`,
// `/agents.md`) with `Content-Type: text/markdown` and `Vary: Accept`. Every
// other request gets the HTML page, also with `Vary: Accept`, so caches keep
// the two variants apart.
//
// vercel.json `rewrites` with a `has` header condition do not work for this:
// Vercel applies them only after the filesystem phase, and every page URL
// matches a static `index.html` first. These routes go into
// .vercel/output/config.json before `handle: filesystem`, written by
// scripts/build-markdown-negotiation-routes.mjs after `astro build`. Only
// paths with a generated twin get routes, so other URLs are unaffected.

// Keeps each route's `src` regex well below Vercel's per-pattern size limit.
const MAX_SOURCE_LENGTH = 3500;

// Matches an Accept header that lists text/markdown with no q parameter or a
// q above zero, so `text/markdown;q=0` (explicitly unacceptable) and `*/*`
// keep getting HTML. Lookahead-free so the same pattern works in Vercel's
// router; vercel.json's after-filesystem rewrites use the same value.
// Limitation: a text/markdown entry with parameters other than q (for example
// `text/markdown;charset=utf-8`) is treated as not accepting Markdown.
export const MARKDOWN_ACCEPT = { type: 'header', key: 'accept', value: '^(.*,)?\\s*text/markdown\\s*(;\\s*q=(1(\\.0{0,3})?|0\\.[0-9]*[1-9][0-9]*)\\s*)?(,.*)?$' };
export const MARKDOWN_HEADERS = { 'Content-Type': 'text/markdown; charset=utf-8', Vary: 'Accept' };

const escapeRegExp = (value) => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

/** True for a route this module generated (used to drop stale routes on rerun). */
export function isNegotiationRoute(route) {
	return (
		route.headers?.Vary === 'Accept' &&
		(route.has?.some((h) => h.key === 'accept' && h.value === MARKDOWN_ACCEPT.value) || route.continue === true)
	);
}

/**
 * @param {string[]} twinPaths twin paths without the leading slash or `.md`
 *   (`agents`, `terminal/blocks`, or `index` for the homepage)
 * @returns Build Output API routes: for each group, a `continue` route that adds
 *   `Vary: Accept` to the HTML response, then a route that serves the twin when
 *   the request accepts Markdown.
 */
export function buildMarkdownNegotiationRoutes(twinPaths) {
	const routes = [];
	const paths = [...new Set(twinPaths)].sort();
	const add = (src, dest) => {
		routes.push({ src, headers: { Vary: 'Accept' }, caseSensitive: true, continue: true });
		routes.push({ src, has: [MARKDOWN_ACCEPT], dest, headers: { ...MARKDOWN_HEADERS }, caseSensitive: true });
	};
	if (paths.includes('index')) add('^/$', '/index.md');

	let group = [];
	let length = 0;
	const flush = () => {
		if (group.length === 0) return;
		add(`^/(${group.join('|')})/?$`, '/$1.md');
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
 * Resolves `pathname` against the routes the way Vercel does for this subset:
 * routes are tried in order, `has` must match, `continue` routes add headers and
 * keep going, and the first matching route with `dest` ends routing.
 *
 * @returns {{ dest: string | null, headers: Record<string, string> }}
 */
export function resolve(routes, pathname, accept = '') {
	const headers = {};
	for (const route of routes) {
		const match = pathname.match(new RegExp(route.src, route.caseSensitive ? '' : 'i'));
		if (!match) continue;
		if (route.has && !route.has.every((h) => h.type === 'header' && new RegExp(h.value, 'i').test(accept))) continue;
		Object.assign(headers, route.headers ?? {});
		if (route.dest) {
			return { dest: route.dest.replace(/\$(\d+)/g, (_, i) => match[Number(i)] ?? ''), headers };
		}
		if (!route.continue) break;
	}
	return { dest: null, headers };
}
