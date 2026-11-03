import assert from 'node:assert/strict';
import { mkdtemp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { pathToFileURL } from 'node:url';
import docsMarkdownIntegration, { convertHtmlToMarkdown } from './docs-markdown-integration.js';

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

// Matches Starlight's rendered structure, including inactive hidden panels.
function createTabs(labels, contents, offset = 1) {
	return `<starlight-tabs>
		<div class="tablist-wrapper not-content"><ul role="tablist">${labels.map((label, index) =>
			`<li role="presentation"><a role="tab" href="#tab-panel-${offset + index}"
				id="tab-${offset + index}" aria-selected="${index === 0}">${label}</a></li>`,
		).join('')}</ul></div>
		${contents.map((content, index) => `<div role="tabpanel" id="tab-panel-${offset + index}"
			aria-labelledby="tab-${offset + index}"${index ? ' hidden' : ''}>${content}</div>`).join('')}
	</starlight-tabs>`;
}

test('replaces provider navigation with labelled panels, including hidden providers', () => {
	const labels = ['GitHub', 'Azure DevOps', 'Linear', 'Jira', 'GitLab'];
	const html = createPage(`<h2 id="configure">Configure</h2>
		<p>See <a href="#tab-panel-744">Jira configuration</a> or <a href="#tab-744">Jira tab</a>.</p>
		${createTabs(labels, labels.map((label) => `<p>${label} instructions.</p>`), 741)}
		<h2 id="verify">Verify</h2><p>Done.</p>`);
	const markdown = convertHtmlToMarkdown(html);

	for (const label of labels) {
		const slug = label.toLowerCase().replaceAll(' ', '-');
		assert.ok(markdown.includes(`<a id="tabs-${slug}"></a>\n\n### ${label}\n\n${label} instructions.`));
		assert.equal(markdown.split(`### ${label}\n`).length - 1, 1);
	}
	assert.match(markdown, /\[Jira configuration\]\(#tabs-jira\)/);
	assert.match(markdown, /\[Jira tab\]\(#tabs-jira\)/);
	assert.doesNotMatch(markdown, /tab-panel-|#tab-744|\[GitHub\]|role=|hidden/);
	assert.match(markdown, /## Configure/);
	assert.match(markdown, /\n## Verify\n/);
	// Numeric component IDs can change between builds without changing Markdown.
	assert.equal(markdown, convertHtmlToMarkdown(html.replaceAll(/74([1-5])/g, '99$1')));
});

test('retains code metadata and nested lists within a procedure containing tabs', () => {
	const code = `<div class="expressive-code"><figure>
		<figcaption><span class="title">jira.yaml</span></figcaption>
		<pre data-language="yaml"><code><div class="ec-line"><div class="code">name: triage</div></div><div class="ec-line"><div class="code">prompt: &#96;&#96;&#96;literal&#96;&#96;&#96;</div></div></code></pre>
		</figure></div>`;
	const markdown = convertHtmlToMarkdown(createPage(`<h2>Set up</h2><ol>
		<li><p>Configure providers.</p>${createTabs(['GitHub', 'Jira'], [
			'<ul><li>First item<ul><li>Nested item</li></ul></li></ul>',
			code,
		])}<p>Keep this in the first step.</p></li>
		<li><p>Verify the result.</p></li></ol>`));

	assert.match(markdown, /1\. {2}Configure providers\./);
	assert.match(markdown, /\n {4}### GitHub\n/);
	assert.match(markdown, /\n {4}- {3}First item\n {8}- {3}Nested item/);
	assert.ok(markdown.includes('    ````yaml title="jira.yaml"\n    name: triage\n    prompt: ```literal```\n    ````'));
	assert.match(markdown, /\n {4}Keep this in the first step\./);
	assert.match(markdown, /\n2\. {2}Verify the result\./);
});

test('keeps nested and repeated labels distinct without changing ordinary headings', () => {
	const inner = createTabs(['GitHub', 'Jira'], [
		'<p>Inner GitHub.</p>', '<p>Inner Jira.</p>',
	], 30);
	const html = createPage(`<h2 id="tabs-github">Existing section</h2>
		${createTabs(['GitHub', 'Jira'], [
			`<p>Outer GitHub.</p>${inner}<h4>Panel detail</h4>`,
			'<p>Outer Jira.</p>',
		], 10)}
		<h2>Second group</h2>
		${createTabs(['GitHub', 'Jira'], ['<p>Second GitHub.</p>', '<p>Second Jira.</p>'], 50)}
		<h3>Ordinary subsection</h3>`);
	const markdown = convertHtmlToMarkdown(html);

	assert.match(markdown, /id="tabs-github-2"><\/a>\n\n### GitHub/);
	assert.match(markdown, /id="tabs-github-3"><\/a>\n\n#### GitHub/);
	assert.match(markdown, /id="tabs-jira"><\/a>\n\n#### Jira/);
	assert.match(markdown, /id="tabs-jira-2"><\/a>\n\n### Jira/);
	assert.match(markdown, /id="tabs-github-4"><\/a>\n\n### GitHub/);
	assert.match(markdown, /id="tabs-jira-3"><\/a>\n\n### Jira/);
	assert.match(markdown, /\n#### Panel detail\n/);
	assert.match(markdown, /\n### Ordinary subsection\n/);
	assert.equal(new Set([...markdown.matchAll(/<a id="([^"]+)"/g)].map((m) => m[1])).size, 6);
});

test('normalizes tabs in agent-only templates while removing search-only chrome', () => {
	const html = createPage(`<template data-agent-only data-pagefind-ignore>
		<h2>Agent setup</h2>${createTabs(['GitHub', 'Jira'], [
			'<p>Agent GitHub prompt.</p>', '<p>Agent Jira prompt.</p>',
		])}</template><p data-pagefind-ignore>Search-only chrome.</p>`);
	const markdown = convertHtmlToMarkdown(html);

	assert.match(markdown, /### GitHub\n\nAgent GitHub prompt\./);
	assert.match(markdown, /### Jira\n\nAgent Jira prompt\./);
	assert.doesNotMatch(markdown, /Search-only|template|tab-panel-/);
});

test('handles missing labels, broken references, and button-based tab controls', () => {
	const markdown = convertHtmlToMarkdown(createPage(`
		<ul role="tablist">
			<li><button role="tab" id="button" aria-controls="button-panel">Button provider</button></li>
			<li><a role="tab" id="orphan" href="#missing-panel">Orphan navigation</a></li>
		</ul>
		<p><a href="#orphan">Unavailable tab</a></p>
		<div role="tabpanel" id="button-panel" aria-labelledby="missing another-missing"><p>Button content.</p></div>
		<div role="tabpanel" aria-label="   " aria-labelledby="missing"><p>Unlabelled content.</p></div>
		<div role="tabpanel" aria-label="Named fallback"><p>Named content.</p></div>
		<div role="tabpanel" aria-label="!!!"><p>Punctuation content.</p></div>`));

	assert.match(markdown, /id="tabs-button-provider"><\/a>\n\n## Button provider/);
	assert.match(markdown, /id="tabs-tab-2"><\/a>\n\n## Tab 2/);
	assert.match(markdown, /id="tabs-named-fallback"><\/a>\n\n## Named fallback/);
	assert.match(markdown, /id="tabs-panel"><\/a>\n\n## !!!/);
	for (const content of ['Button', 'Unlabelled', 'Named', 'Punctuation']) {
		assert.ok(markdown.includes(`${content} content.`));
	}
	assert.match(markdown, /\nUnavailable tab\n/);
	assert.doesNotMatch(markdown, /Orphan navigation|#orphan|#missing-panel/);
});

test('build hook writes Markdown without changing browser HTML or hidden tab state', async (t) => {
	const directory = await mkdtemp(path.join(os.tmpdir(), 'docs-markdown-tabs-'));
	t.after(() => rm(directory, { recursive: true, force: true }));
	const pageDirectory = path.join(directory, 'example');
	await mkdir(pageDirectory);
	const html = createPage(createTabs(['GitHub', 'Jira'], ['<p>First.</p>', '<p>Hidden.</p>']));
	const htmlPath = path.join(pageDirectory, 'index.html');
	await writeFile(htmlPath, html);

	await docsMarkdownIntegration().hooks['astro:build:generated']({
		dir: pathToFileURL(`${directory}/`), logger: { info() {} },
	});

	assert.equal(await readFile(htmlPath, 'utf8'), html);
	const markdown = await readFile(path.join(directory, 'example.md'), 'utf8');
	assert.match(markdown, /## GitHub\n\nFirst\./);
	assert.match(markdown, /## Jira\n\nHidden\./);
});

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

test('preserves search-excluded file trees, directory nesting, and file comments', () => {
	const html = createPage(`<p>Example project structure:</p>
		<starlight-file-tree data-pagefind-ignore="true">
			<ul><li class="directory"><details open>
				<summary><span class="tree-entry"><span class="sr-only">Directory</span>project/</span></summary>
				<ul><li class="directory"><details>
					<summary><span class="tree-entry">api/</span></summary>
					<ul><li class="file"><span class="tree-entry">AGENTS.md <span class="comment">API-specific rules</span></span></li></ul>
				</details></li>
				<li class="file"><span class="tree-entry">AGENTS.md <span class="comment">Project-wide rules</span></span></li></ul>
			</details></li></ul>
		</starlight-file-tree>
		<p data-pagefind-ignore>Search-only chrome.</p><p>Following guidance.</p>`);
	const markdown = convertHtmlToMarkdown(html);

	assert.match(markdown, /- {3}project\/[\s\S]*\n {4}- {3}api\/[\s\S]*\n {8}- {3}AGENTS\.md API-specific rules/);
	assert.match(markdown, /\n {4}- {3}AGENTS\.md Project-wide rules/);
	assert.match(markdown, /Following guidance\./);
	assert.doesNotMatch(markdown, /Directory|Search-only chrome|starlight-file-tree|<details/);
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
		<a href="/agent-platform/capabilities/skills/#next-steps">Skills next steps</a> and
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
	assert.match(
		markdown,
		/\[Skills next steps\]\(https:\/\/docs\.warp\.dev\/agent-platform\/capabilities\/skills\/#next-steps\)/,
	);
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
	assert.doesNotMatch(markdown, /\]\(\/[^/)]/);
});
