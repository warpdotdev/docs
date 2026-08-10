import type { APIRoute } from 'astro';
import { createHighlighter } from 'shiki';

type ThemeMode = 'light' | 'dark';

const LANGUAGE_ALIASES: Record<string, string> = {
	shell: 'bash',
	zsh: 'bash',
	pwsh: 'powershell',
	plaintext: 'text',
};

const SUPPORTED_LANGUAGES = new Set([
	'bash',
	'powershell',
	'json',
	'javascript',
	'typescript',
	'tsx',
	'jsx',
	'python',
	'go',
	'rust',
	'yaml',
	'markdown',
	'html',
	'css',
	'text',
]);

const highlighterPromise = createHighlighter({
	themes: ['github-light', 'github-dark'],
	langs: [...SUPPORTED_LANGUAGES],
});

function normalizeLanguage(language: unknown): string {
	if (typeof language !== 'string') return 'text';
	const normalized = language.toLowerCase();
	return LANGUAGE_ALIASES[normalized] ?? normalized;
}

function normalizeTheme(theme: unknown): ThemeMode {
	return theme === 'light' ? 'light' : 'dark';
}

export const POST: APIRoute = async ({ request }) => {
	try {
		const payload = (await request.json()) as {
			code?: unknown;
			language?: unknown;
			theme?: unknown;
		};
		const code = typeof payload.code === 'string' ? payload.code : '';
		if (!code.trim()) {
			return new Response(JSON.stringify({ preHtml: null }), {
				status: 200,
				headers: { 'Content-Type': 'application/json' },
			});
		}

		const requestedLanguage = normalizeLanguage(payload.language);
		const language = SUPPORTED_LANGUAGES.has(requestedLanguage) ? requestedLanguage : 'text';
		const theme = normalizeTheme(payload.theme) === 'light' ? 'github-light' : 'github-dark';

		const highlighter = await highlighterPromise;
		const html = highlighter.codeToHtml(code, {
			lang: language,
			theme,
		});
		const preMatch = html.match(/<pre[^>]*>[\s\S]*?<\/pre>/i);

		return new Response(JSON.stringify({ preHtml: preMatch?.[0] ?? null }), {
			status: 200,
			headers: {
				'Content-Type': 'application/json',
				'Cache-Control': 'no-store',
			},
		});
	} catch (error) {
		console.error('[highlight-code] Failed to highlight code', error);
		return new Response(JSON.stringify({ error: 'Failed to highlight code' }), {
			status: 500,
			headers: { 'Content-Type': 'application/json' },
		});
	}
};
