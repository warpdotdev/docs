import assert from 'node:assert/strict';
import test from 'node:test';
import { convertHtmlToMarkdown } from './docs-markdown-integration.js';

test('includes inert agent-only templates in generated Markdown', () => {
	const html = `
		<html>
			<head><meta name="description" content="Test description."></head>
			<body>
				<main>
					<h1 data-page-title>Test page</h1>
					<div class="sl-markdown-content">
						<p>Visible guidance.</p>
						<template data-agent-only data-pagefind-ignore>
							<h2>Agent setup</h2>
							<p>Restart the coding agent after installing MCP.</p>
						</template>
						<p data-pagefind-ignore>Search-only chrome.</p>
					</div>
				</main>
			</body>
		</html>
	`;

	const markdown = convertHtmlToMarkdown(html);

	assert.match(markdown, /Visible guidance\./);
	assert.match(markdown, /## Agent setup/);
	assert.match(markdown, /Restart the coding agent after installing MCP\./);
	assert.doesNotMatch(markdown, /Search-only chrome\./);
});
