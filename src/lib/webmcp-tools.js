/**
 * Build read-only tools without loading Pagefind until a search is requested.
 * Pagefind's browser API exposes search().results[].data() for result details.
 */
export function buildWebMcpTools({ origin, fetch: fetchPage, loadPagefind }) {
	return [
		{
			name: 'search_docs_pages',
			description:
				'Look up Warp documentation pages by title and keywords using Pagefind. Returns up to 8 matching pages; use Kapa for semantic knowledge-source search.',
			annotations: { readOnlyHint: true },
			inputSchema: {
				type: 'object',
				properties: {
					query: {
						type: 'string',
						minLength: 1,
						description: 'Title words or keywords to find in Warp documentation.',
					},
				},
				required: ['query'],
				additionalProperties: false,
			},
			async execute({ query }) {
				if (typeof query !== 'string' || !query.trim()) {
					throw new Error('Provide a non-empty search query.');
				}
				const pagefind = await loadPagefind();
				const { results } = await pagefind.search(query.trim());
				const pages = await Promise.all(
					results.slice(0, 8).map(async (result) => {
						const data = await result.data();
						return {
							title: data.meta.title,
							url: new URL(data.url, origin).href,
							excerpt: data.excerpt,
						};
					}),
				);
				return { pages };
			},
		},
		{
			name: 'get_page_markdown',
			description:
				'Read the Markdown version of a Warp documentation page by its same-origin path. Returns the Markdown URL and content without navigating.',
			annotations: { readOnlyHint: true },
			inputSchema: {
				type: 'object',
				properties: {
					path: {
						type: 'string',
						minLength: 1,
						description:
							'Root-relative documentation page path, such as /agents/capabilities/skills/ or /. Absolute URLs, queries, and fragments are not accepted.',
					},
				},
				required: ['path'],
				additionalProperties: false,
			},
			async execute({ path }) {
				if (
					typeof path !== 'string' ||
					!path.startsWith('/') ||
					path.startsWith('//') ||
					/[\\?#\s]/.test(path) ||
					/%(?:2f|5c|00|0a|0d)/i.test(path)
				) {
					throw new Error('Provide a root-relative documentation path without a query or fragment.');
				}
				const page = new URL(path, origin);
				if (page.origin !== new URL(origin).origin) {
					throw new Error('The documentation path must be same-origin.');
				}
				const pathname = page.pathname.replace(/\/+$/, '');
				const url = new URL(pathname ? `${pathname}.md` : '/index.md', origin).href;
				const response = await fetchPage(url, { redirect: 'error', credentials: 'omit' });
				if (!response.ok) {
					throw new Error(`Could not fetch page Markdown (${response.status}).`);
				}
				return { url, markdown: await response.text() };
			},
		},
		{
			name: 'list_docs_pages',
			description:
				'Navigate the Warp documentation tree by listing page titles and URLs from the generated documentation catalog. Omit section to list all pages, or select a top-level section such as agents or factories.',
			annotations: { readOnlyHint: true },
			inputSchema: {
				type: 'object',
				properties: {
					section: {
						type: 'string',
						minLength: 1,
						description:
							'Optional top-level documentation path segment, such as agents or factories. Must match a section present in the current documentation catalog.',
					},
				},
				required: [],
				additionalProperties: false,
			},
			async execute({ section } = {}) {
				if (section !== undefined && (
					typeof section !== 'string' || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(section)
				)) {
					throw new Error('Provide a top-level documentation section without slashes.');
				}
				const response = await fetchPage(new URL('/llms-small.txt', origin).href, {
					redirect: 'error',
					credentials: 'omit',
				});
				if (!response.ok) {
					throw new Error(`Could not fetch the documentation catalog (${response.status}).`);
				}
				const catalog = await response.text();
				// Generated page headers pair the title with its root-relative canonical path.
				const headers = catalog.matchAll(
					/^# ([^\n]+)\r?\n\r?\nCanonical page: \[(\/[^\]\s]*)\]\([^)]+\)\r?$/gm,
				);
				const pages = new Map();
				for (const [, title, path] of headers) {
					const url = new URL(path, origin);
					if (url.origin === new URL(origin).origin) {
						pages.set(url.href, { title: title.trim(), url: url.href });
					}
				}
				if (!pages.size) throw new Error('The documentation catalog contains no page entries.');
				const entries = [...pages.values()];
				const sections = new Set(entries.map(({ url }) => new URL(url).pathname.split('/')[1]).filter(Boolean));
				if (section !== undefined && !sections.has(section)) {
					throw new Error(`Unknown documentation section. Choose one of: ${[...sections].join(', ')}.`);
				}
				return {
					pages: entries.filter(({ url }) =>
						section === undefined || new URL(url).pathname.split('/')[1] === section),
				};
			},
		},
	];
}

/** Register only our tools, leaving Kapa's independent registration untouched. */
export function registerWebMcpTools() {
	const documentContext = globalThis.document?.modelContext;
	const context =
		typeof documentContext?.registerTool === 'function'
			? documentContext
			: globalThis.navigator?.modelContext;
	if (typeof context?.registerTool !== 'function') return () => {};

	const controller = new AbortController();
	const tools = buildWebMcpTools({
		origin: globalThis.location.origin,
		fetch: globalThis.fetch.bind(globalThis),
		loadPagefind: () => import(/* @vite-ignore */ '/pagefind/pagefind.js'),
	});
	const registered = [];
	const cleanup = () => {
		for (const name of registered.splice(0)) {
			context.unregisterTool?.(name);
		}
		controller.abort();
	};
	try {
		for (const tool of tools) {
			context.registerTool(tool, { signal: controller.signal });
			registered.push(tool.name);
		}
	} catch (error) {
		cleanup();
		console.warn('Could not register Warp documentation tools.', error);
	}
	return cleanup;
}
