import assert from 'node:assert/strict';
import test from 'node:test';
import {
	acceptRequestsMarkdown,
	getMarkdownPathFromHtmlPath,
	isEligibleDocHtmlPath,
	shouldServeMarkdown,
	shouldServeMarkdownProduction,
} from './docs-markdown.js';

test('/retrieve and /api paths are not markdown-negotiated doc HTML', () => {
	assert.equal(isEligibleDocHtmlPath('/retrieve'), false);
	assert.equal(isEligibleDocHtmlPath('/retrieve/'), false);
	assert.equal(isEligibleDocHtmlPath('/api/support-handoff'), false);
	assert.equal(isEligibleDocHtmlPath('/agents/capabilities/skills'), true);
	assert.equal(isEligibleDocHtmlPath('/'), true);
	assert.equal(isEligibleDocHtmlPath('/quickstart.md'), false);
	assert.equal(isEligibleDocHtmlPath('/_astro/page.js'), false);
});

test('maps HTML paths to pre-rendered markdown paths', () => {
	assert.equal(getMarkdownPathFromHtmlPath('/'), '/index.md');
	assert.equal(getMarkdownPathFromHtmlPath('/quickstart'), '/quickstart.md');
	assert.equal(getMarkdownPathFromHtmlPath('/quickstart/'), '/quickstart.md');
	assert.equal(
		getMarkdownPathFromHtmlPath('/support-and-community/'),
		'/support-and-community.md',
	);
});

test('shouldServeMarkdown (dev) prefers Accept and falls back to agent UAs', () => {
	assert.equal(
		shouldServeMarkdown(new Request('https://docs.warp.dev/', { headers: { accept: 'text/markdown' } })),
		true,
	);
	assert.equal(
		shouldServeMarkdown(new Request('https://docs.warp.dev/', { headers: { accept: 'text/plain' } })),
		true,
	);
	assert.equal(
		shouldServeMarkdown(
			new Request('https://docs.warp.dev/', {
				headers: { accept: 'text/html', 'user-agent': 'Cursor/1.0' },
			}),
		),
		true,
	);
	assert.equal(
		shouldServeMarkdown(
			new Request('https://docs.warp.dev/', {
				headers: { accept: 'text/html', 'user-agent': 'Mozilla/5.0' },
			}),
		),
		false,
	);
});

test('production negotiation requires explicit text/markdown Accept', () => {
	assert.equal(
		shouldServeMarkdownProduction(
			new Request('https://docs.warp.dev/', { headers: { accept: 'text/markdown' } }),
		),
		true,
	);
	assert.equal(
		shouldServeMarkdownProduction(
			new Request('https://docs.warp.dev/', {
				headers: { accept: 'text/html, application/xhtml+xml, text/markdown;q=0.9' },
			}),
		),
		true,
	);
	assert.equal(
		shouldServeMarkdownProduction(
			new Request('https://docs.warp.dev/', { headers: { accept: 'text/plain' } }),
		),
		false,
	);
	assert.equal(
		shouldServeMarkdownProduction(
			new Request('https://docs.warp.dev/', {
				headers: { accept: 'text/html', 'user-agent': 'Claude-User/1.0' },
			}),
		),
		false,
	);
	assert.equal(
		acceptRequestsMarkdown(
			new Request('https://docs.warp.dev/', { headers: { accept: 'text/markdown,text/html' } }),
		),
		true,
	);
});
