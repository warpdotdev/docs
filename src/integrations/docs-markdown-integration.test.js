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

function pageWith(content) {
	return `
		<html>
			<head><meta name="description" content="Test description."></head>
			<body>
				<main>
					<h1 data-page-title>Test page</h1>
					<div class="sl-markdown-content">${content}</div>
				</main>
			</body>
		</html>
	`;
}

// Mirrors the HTML Expressive Code emits for a fenced block: the language on
// `<pre>`, an optional title in the figcaption, one `div.ec-line` per source
// line with no newline characters between them (an empty line is a cell
// holding a lone newline), and a copy button whose `data-code` encodes
// newlines as U+007F.
function expressiveCodeBlock({ language, title, lines }) {
	const header = title
		? `<figcaption class="header"><span class="title">${title}</span></figcaption>`
		: '<figcaption class="header"></figcaption>';
	const body = lines
		.map((line) => {
			if (line === '') return '<div class="ec-line"><div class="code">\n</div></div>';
			const indent = line.match(/^ */)[0];
			const rest = line.slice(indent.length);
			const indentSpan = indent ? `<span class="indent"><span>${indent}</span></span>` : '';
			return `<div class="ec-line"><div class="code">${indentSpan}<span>${rest}</span></div></div>`;
		})
		.join('');
	return (
		`<div class="expressive-code"><figure class="frame${title ? ' has-title' : ''} not-content">${header}` +
		`<pre data-language="${language}"><code>${body}</code></pre>` +
		`<div class="copy"><button title="Copy to clipboard" data-copied="Copied!" data-code="${lines.join('\u007f')}"><div></div></button></div>` +
		'</figure></div>'
	);
}

test('keeps one line per source line in Expressive Code blocks', () => {
	const html = pageWith(
		expressiveCodeBlock({
			language: 'yaml',
			lines: ['repositories:', '  - owner: acme', '    name: payments-service'],
		}),
	);

	const markdown = convertHtmlToMarkdown(html);

	assert.match(markdown, /```yaml\nrepositories:\n {2}- owner: acme\n {4}name: payments-service\n```/);
	assert.doesNotMatch(markdown, /Copied!/);
});

test('carries the language and title onto the fence', () => {
	const html = pageWith(
		expressiveCodeBlock({
			language: 'markdown',
			title: 'agents/reviewer/agent.md',
			lines: ['---', 'agentType: REVIEW', '---', '', 'Review each pull request.'],
		}),
	);

	const markdown = convertHtmlToMarkdown(html);

	assert.match(
		markdown,
		/```markdown title="agents\/reviewer\/agent\.md"\n---\nagentType: REVIEW\n---\n\nReview each pull request\.\n```/,
	);
});

test('falls back to the code text for blocks without ec-line wrappers', () => {
	const html = pageWith(
		'<div class="expressive-code"><figure class="frame"><figcaption class="header"></figcaption>' +
			'<pre><code class="language-bash">echo one\necho two\n</code></pre></figure></div>',
	);

	const markdown = convertHtmlToMarkdown(html);

	assert.match(markdown, /```bash\necho one\necho two\n```/);
});
