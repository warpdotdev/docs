import assert from 'node:assert/strict';
import test from 'node:test';
import { convertHtmlToMarkdown } from './docs-markdown-integration.js';

function createPage(content) {
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

test('reconstructs Expressive Code lines and fence metadata', () => {
	const html = createPage(`
		<div class="expressive-code">
			<figure>
				<figcaption><span class="title">factory.yaml</span></figcaption>
				<pre data-language="yaml"><code>
					<div class="ec-line"><div class="gutter">1</div><div class="code">name: docs</div></div>
					<div class="ec-line"><div class="gutter">2</div><div class="code">&#10;</div></div>
					<div class="ec-line"><div class="gutter">3</div><div class="code">version: 1</div></div>
				</code></pre>
			</figure>
		</div>
	`);

	const markdown = convertHtmlToMarkdown(html);

	assert.ok(markdown.includes('```yaml title="factory.yaml"\nname: docs\n\nversion: 1\n```'));
	assert.doesNotMatch(markdown, /\n1name: docs|\n2\n|\n3version: 1/);
});

test('uses code text when Expressive Code line markup is absent', () => {
	const html = createPage(`
		<div class="expressive-code">
			<pre data-language="bash"><code>printf 'one'\nprintf 'two'\n</code></pre>
		</div>
	`);

	const markdown = convertHtmlToMarkdown(html);

	assert.ok(markdown.includes("```bash\nprintf 'one'\nprintf 'two'\n```"));
});

test('leaves non-Expressive-Code blocks to the default fenced-code rule', () => {
	const html = createPage(`
		<pre><code class="language-shell">printf 'one'\nprintf 'two'\n</code></pre>
	`);

	const markdown = convertHtmlToMarkdown(html);

	assert.ok(markdown.includes("```shell\nprintf 'one'\nprintf 'two'\n```"));
});

test('rewrites root-relative links and images to absolute docs.warp.dev URLs', () => {
	const html = createPage(`
		<p>See <a href="/agent-platform/capabilities/skills/">Skills</a> and
		<a href="https://docs.warp.dev/reference/cli/">CLI</a>.
		Jump to <a href="#next-steps">Next steps</a>.
		External: <a href="https://example.com/docs">Example</a>.
		Relative: <a href="../reference/cli/">Relative CLI</a>.</p>
		<img src="/_astro/example.webp" alt="Example diagram">
		<img src="../assets/relative.webp" alt="Relative diagram">
		<img src="//cdn.example.com/protocol-relative.webp" alt="Protocol-relative diagram">
	`);

	const markdown = convertHtmlToMarkdown(html);

	assert.match(markdown, /\[Skills\]\(https:\/\/docs\.warp\.dev\/agent-platform\/capabilities\/skills\/\)/);
	assert.match(markdown, /\[CLI\]\(https:\/\/docs\.warp\.dev\/reference\/cli\/\)/);
	assert.match(markdown, /\[Next steps\]\(#next-steps\)/);
	assert.match(markdown, /\[Example\]\(https:\/\/example\.com\/docs\)/);
	assert.match(markdown, /\[Relative CLI\]\(\.\.\/reference\/cli\/\)/);
	assert.match(
		markdown,
		/!\[Example diagram\]\(https:\/\/docs\.warp\.dev\/_astro\/example\.webp\)/,
	);
	assert.match(markdown, /!\[Relative diagram\]\(\.\.\/assets\/relative\.webp\)/);
	assert.match(
		markdown,
		/!\[Protocol-relative diagram\]\(\/\/cdn\.example\.com\/protocol-relative\.webp\)/,
	);
	assert.match(
		markdown,
		/\[llms\.txt\]\(https:\/\/docs\.warp\.dev\/llms\.txt\)/,
	);
	assert.doesNotMatch(markdown, /\]\(\/[a-zA-Z_]/);
});
