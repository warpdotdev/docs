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
	const lastSegment = normalizedPath.split('/').at(-1) ?? '';
	return lastSegment.length > 0 && !lastSegment.includes('.');
}

/**
 * Prefer explicit content negotiation and keep user-agent matching as a
 * compatibility fallback for tools that do not send a markdown-specific
 * Accept header.
 *
 * @param {Request} request
 */
export function shouldServeMarkdown(request) {
	const accept = request.headers.get('accept')?.toLowerCase() ?? '';
	if (accept.includes('text/markdown') || accept.includes('text/plain')) {
		return true;
	}

	const userAgent = request.headers.get('user-agent')?.toLowerCase() ?? '';
	return AGENT_USER_AGENT_TOKENS.some((token) => userAgent.includes(token));
}

function normalizePathname(pathname) {
	if (!pathname || pathname === '/') return '/';
	const trimmedPath = pathname.replace(/\/+$/, '');
	return trimmedPath || '/';
}
