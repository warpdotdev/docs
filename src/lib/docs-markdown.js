const AGENT_USER_AGENT_TOKENS = [
	'chatgpt',
	'claude',
	'anthropic',
	'openai',
	'cursor',
	'perplexity',
	'windsurf',
	'cline',
];

/**
 * @param {string} pathname
 */
export function getMarkdownPathFromHtmlPath(pathname) {
	const normalizedPath = normalizePathname(pathname);
	if (normalizedPath === '/') return '/index.md';
	return `${normalizedPath}.md`;
}

/**
 * @param {string} pathname
 */
export function isEligibleDocHtmlPath(pathname) {
	const normalizedPath = normalizePathname(pathname);
	if (normalizedPath === '/') return true;
	if (normalizedPath.startsWith('/_astro/')) return false;
	// API and agent endpoints are not doc HTML pages; never rewrite them to .md.
	if (normalizedPath === '/retrieve' || normalizedPath.startsWith('/api/')) return false;
	const lastSegment = normalizedPath.split('/').at(-1) ?? '';
	return lastSegment.length > 0 && !lastSegment.includes('.');
}

/**
 * True when Accept explicitly lists the `text/markdown` media type.
 * Ignores `text/plain` and user-agent heuristics.
 *
 * @param {Request} request
 */
export function acceptRequestsMarkdown(request) {
	const accept = request.headers.get('accept')?.toLowerCase() ?? '';
	return acceptIncludesMediaType(accept, 'text/markdown');
}

/**
 * Content negotiation for local/dev Astro middleware.
 *
 * Prefer explicit `Accept: text/markdown`. Keep `text/plain` and known agent
 * user-agent matching as a compatibility fallback for tools that omit a
 * markdown-specific Accept header. Production Build Output API middleware must
 * use {@link shouldServeMarkdownProduction} instead so human WebViews whose UA
 * contains agent tokens still receive HTML.
 *
 * @param {Request} request
 */
export function shouldServeMarkdown(request) {
	if (acceptRequestsMarkdown(request)) return true;

	const accept = request.headers.get('accept')?.toLowerCase() ?? '';
	if (acceptIncludesMediaType(accept, 'text/plain')) {
		return true;
	}

	const userAgent = request.headers.get('user-agent')?.toLowerCase() ?? '';
	return AGENT_USER_AGENT_TOKENS.some((token) => userAgent.includes(token));
}

/**
 * Removes a leading YAML frontmatter block (`---` ... `---`) and the blank
 * lines after it. Generated `.md` twins start with frontmatter for crawlers
 * and agents; the Copy page button removes it because the copied body already
 * starts with the page title and description.
 *
 * @param {string} markdown
 */
export function stripFrontmatter(markdown) {
	return markdown.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n(?:\r?\n)*/, '');
}

/**
 * Production static hosting: rewrite only when Accept explicitly asks for
 * `text/markdown`. Direct `*.md` URLs remain available without negotiation.
 *
 * @param {Request} request
 */
export function shouldServeMarkdownProduction(request) {
	return acceptRequestsMarkdown(request);
}

/**
 * @param {string} acceptHeader
 * @param {string} mediaType
 */
function acceptIncludesMediaType(acceptHeader, mediaType) {
	if (!acceptHeader) return false;
	for (const part of acceptHeader.split(',')) {
		const type = part.trim().split(';')[0]?.trim();
		if (type === mediaType) return true;
	}
	return false;
}

function normalizePathname(pathname) {
	if (!pathname || pathname === '/') return '/';
	const trimmedPath = pathname.replace(/\/+$/, '');
	return trimmedPath || '/';
}
