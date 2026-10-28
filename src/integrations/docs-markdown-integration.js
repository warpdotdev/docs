import { mkdir, readdir, readFile, rm, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseHTML } from 'linkedom';
import TurndownService from 'turndown';
import { gfm } from 'turndown-plugin-gfm';
import { DOCS_ORIGIN } from '../lib/site.js';

export default function docsMarkdownIntegration() {
	return {
		name: 'warp-docs-markdown',
		hooks: {
			'astro:build:generated': async ({ dir, logger }) => {
				const outputRoot = fileURLToPath(dir);
				const markdownCount = await generateMarkdownFiles(outputRoot);
				logger.info(`Generated ${markdownCount} Markdown docs`);
			},
		},
	};
}

export { convertHtmlToMarkdown };

const turndown = createMarkdownConverter();

async function generateMarkdownFiles(outputRoot) {
	const htmlFiles = await collectHtmlFiles(outputRoot, readdir);
	let markdownCount = 0;

	for (const htmlFile of htmlFiles) {
		const relativeHtmlPath = path.relative(outputRoot, htmlFile);
		if (!isDocHtmlFile(relativeHtmlPath)) continue;

		const markdownPath = getMarkdownOutputPath(outputRoot, relativeHtmlPath);
		const html = await readFile(htmlFile, 'utf8');
		const markdown = convertHtmlToMarkdown(html);
		if (!markdown) continue;

		await mkdir(path.dirname(markdownPath), { recursive: true });
		await writeFile(markdownPath, markdown, 'utf8');
		await rm(`${markdownPath}.html`, { force: true });
		markdownCount += 1;
	}

	return markdownCount;
}

async function collectHtmlFiles(rootDir, readdir) {
	/** @type {string[]} */
	const htmlFiles = [];

	async function walk(currentDir) {
		const entries = await readdir(currentDir, { withFileTypes: true });
		for (const entry of entries) {
			const entryPath = path.join(currentDir, entry.name);
			if (entry.isDirectory()) {
				await walk(entryPath);
				continue;
			}
			if (entry.isFile() && entry.name.endsWith('.html')) {
				htmlFiles.push(entryPath);
			}
		}
	}

	await walk(rootDir);
	return htmlFiles;
}

function isDocHtmlFile(relativeHtmlPath) {
	if (relativeHtmlPath === '404.html') return false;
	return relativeHtmlPath === 'index.html' || relativeHtmlPath.endsWith('/index.html');
}

function getMarkdownOutputPath(outputRoot, relativeHtmlPath) {
	if (relativeHtmlPath === 'index.html') {
		return path.join(outputRoot, 'index.md');
	}

	const htmlDir = path.dirname(relativeHtmlPath);
	return path.join(outputRoot, `${htmlDir}.md`);
}

function convertHtmlToMarkdown(html) {
	const { document } = parseHTML(html);
	const title = document.querySelector('h1[data-page-title], main h1')?.textContent?.trim();
	const description = document.querySelector('meta[name="description"]')?.getAttribute('content')?.trim();
	const contentRoot = document.querySelector('main .sl-markdown-content');
	if (!title || !contentRoot) return '';

	const clone = /** @type {HTMLElement} */ (contentRoot.cloneNode(true));
	expandAgentOnlyTemplates(clone);
	normalizeTabPanels(clone);
	sanitizeRoot(clone);
	absolutizeInternalLinks(clone);
	const markdownBody = turndown.turndown(clone.innerHTML).trim();
	const llmsDirective =
		`> For the complete documentation index, see [llms.txt](${DOCS_ORIGIN}/llms.txt).\n` +
		'> Markdown versions of each page are available by appending .md to any URL.';
	const sections = [llmsDirective, `# ${normalizeWhitespace(title)}`];

	if (description) {
		sections.push(description);
	}

	if (markdownBody) {
		sections.push(markdownBody);
	}

	return `${sections.join('\n\n').trim()}\n`;
}

/**
 * Rewrite root-relative links/resources to absolute docs.warp.dev URLs so
 * served markdown remains portable when copied outside the site.
 *
 * @param {HTMLElement} root
 */
function absolutizeInternalLinks(root) {
	for (const anchor of root.querySelectorAll('a[href]')) {
		const absolute = toAbsoluteDocsUrl(anchor.getAttribute('href'));
		if (absolute) anchor.setAttribute('href', absolute);
	}

	for (const image of root.querySelectorAll('img[src]')) {
		const absolute = toAbsoluteDocsUrl(image.getAttribute('src'));
		if (absolute) image.setAttribute('src', absolute);
	}
}

/**
 * @param {string | null} value
 * @returns {string | null} absolute docs URL when the value should be rewritten
 */
function toAbsoluteDocsUrl(value) {
	if (!value?.startsWith('/') || value.startsWith('//')) return null;
	return `${DOCS_ORIGIN}${value}`;
}

function expandAgentOnlyTemplates(root) {
	for (const template of root.querySelectorAll('template[data-agent-only]')) {
		const content = /** @type {HTMLTemplateElement} */ (template).content;
		template.replaceWith(content.cloneNode(true));
	}
}

// Tabs are interactive navigation in HTML, but every panel must be readable in
// Markdown. Work on the clone, before sanitization can remove accessible labels.
function normalizeTabPanels(root) {
	const panels = Array.from(root.querySelectorAll('[role="tabpanel"]'));
	const controls = Array.from(root.querySelectorAll('[role="tab"]'));
	const elementsById = new Map(
		Array.from(root.querySelectorAll('[id]')).map((node) => [node.id, node]),
	);
	const usedIds = new Set(elementsById.keys());
	const fragmentTargets = new Map();

	for (const [index, panel] of panels.entries()) {
		const labelledBy = (panel.getAttribute('aria-labelledby') ?? '').split(/\s+/);
		const control = controls.find((node) =>
			panel.id && (node.getAttribute('href') === `#${panel.id}` ||
				node.getAttribute('aria-controls')?.split(/\s+/).includes(panel.id)),
		);
		const label = [
			panel.getAttribute('aria-label'),
			labelledBy.map((id) => elementsById.get(id)?.textContent ?? '').join(' '),
			control?.textContent,
		].map((value) => normalizeWhitespace(value ?? '')).find(Boolean) || `Tab ${index + 1}`;
		const slug = label.normalize('NFKD').toLowerCase().replace(/\p{M}/gu, '')
			.replace(/[^\p{L}\p{N}]+/gu, '-').replace(/^-|-$/g, '') || 'panel';
		const baseId = `tabs-${slug}`;
		let id = baseId;
		let suffix = 2;
		while (usedIds.has(id)) id = `${baseId}-${suffix++}`;
		usedIds.add(id);

		if (panel.id) fragmentTargets.set(panel.id, id);
		for (const node of controls) {
			if (node.id && (labelledBy.includes(node.id) || node === control)) {
				fragmentTargets.set(node.id, id);
			}
		}
		const heading = root.ownerDocument.createElement('h2');
		heading.id = id;
		heading.setAttribute('data-markdown-tab', '');
		heading.textContent = label;
		panel.prepend(heading);
	}

	// Panel headings inherit the surrounding section depth. A sibling panel's
	// headings must not change the depth of the next panel or the following prose.
	function setHeadingLevels(container, level) {
		for (const node of Array.from(container.children)) {
			if (node.getAttribute('role') === 'tabpanel') {
				const heading = node.firstElementChild;
				const depth = Math.min(level + 1, 6);
				const replacement = root.ownerDocument.createElement(`h${depth}`);
				for (const attribute of Array.from(heading.attributes)) {
					replacement.setAttribute(attribute.name, attribute.value);
				}
				replacement.textContent = heading.textContent;
				heading.replaceWith(replacement);
				setHeadingLevels(node, depth);
			} else if (/^H[1-6]$/.test(node.tagName)) {
				level = Number(node.tagName.slice(1));
			} else {
				level = setHeadingLevels(node, level);
			}
		}
		return level;
	}
	setHeadingLevels(root, 1);

	root.querySelectorAll('[role="tablist"], [role="tab"]').forEach((node) => node.remove());
	for (const anchor of root.querySelectorAll('a[href^="#"]')) {
		const target = fragmentTargets.get(anchor.getAttribute('href').slice(1));
		if (target) anchor.setAttribute('href', `#${target}`);
		else if (controls.some((node) => `#${node.id}` === anchor.getAttribute('href'))) {
			anchor.replaceWith(...anchor.childNodes);
		}
	}
}

function sanitizeRoot(root) {
	for (const selector of [
		'script',
		'style',
		'noscript',
		'.sl-anchor-link',
		'.expressive-code .copy',
		'.sr-only',
		'[data-pagefind-ignore]',
	]) {
		root.querySelectorAll(selector).forEach((node) => node.remove());
	}
}

function createMarkdownConverter() {
	const service = new TurndownService({
		headingStyle: 'atx',
		codeBlockStyle: 'fenced',
		bulletListMarker: '-',
		emDelimiter: '*',
		strongDelimiter: '**',
	});

	service.use(gfm);

	service.addRule('tabPanelHeading', {
		filter: (node) => isElement(node) && node.hasAttribute('data-markdown-tab'),
		replacement(content, node) {
			// Explicit targets avoid renderer-dependent heading slugs, particularly
			// for repeated labels and nested groups.
			const prefix = '#'.repeat(Number(node.nodeName.slice(1)));
			return `\n\n<a id="${node.id}"></a>\n\n${prefix} ${content.trim()}\n\n`;
		},
	});

	service.addRule('expressiveCodeBlock', {
		filter: (node) => isElement(node) && node.classList.contains('expressive-code'),
		replacement(_content, node) {
			if (!isElement(node)) return '\n\n';

			const pre = node.querySelector('pre');
			const code = node.querySelector('pre code');
			if (!pre || !code) return '\n\n';

			const rawCode = getCodeBlockText(code);
			const fence = getFence(rawCode);
			const info = [getCodeBlockLanguage(pre, code), getCodeBlockTitleAttribute(node)]
				.filter(Boolean)
				.join(' ');
			const openingFence = info ? `${fence}${info}` : fence;

			return `\n\n${openingFence}\n${rawCode}\n${fence}\n\n`;
		},
	});

	return service;
}

function isElement(node) {
	return node.nodeType === 1;
}

// Expressive Code renders each source line as its own `div.ec-line` and never
// emits newline characters between them, so `textContent` on the `<code>`
// element runs every line together. Rebuild the text line by line, taking
// only each line's `.code` cell so gutter content (line numbers) stays out.
// An empty source line is rendered as a cell holding a lone newline
// character, so newlines inside a cell are dropped rather than kept.
function getCodeBlockText(code) {
	const lines = Array.from(code.querySelectorAll('.ec-line'));
	const text =
		lines.length > 0
			? lines
					.map((line) => ((line.querySelector('.code') ?? line).textContent ?? '').replace(/\r?\n/g, ''))
					.join('\n')
			: (code.textContent ?? '');
	return normalizeNewlines(text).replace(/\n$/, '');
}

// Expressive Code puts `data-language` on the `<pre>`; the `<code>` fallbacks
// cover blocks rendered by anything else.
function getCodeBlockLanguage(pre, code) {
	return (
		pre.getAttribute('data-language') ??
		code.getAttribute('data-language') ??
		code.className.match(/language-([\w-]+)/)?.[1] ??
		''
	);
}

// A block's title (the file name on a ```yaml title="factory.yaml" fence) is
// often the only thing that says which file a snippet belongs to, so it is
// carried on the fence's info string in the same form the source uses.
function getCodeBlockTitleAttribute(block) {
	const title = block.querySelector('figcaption .title')?.textContent?.trim() ?? '';
	// JSON.stringify yields a double-quoted string with backslashes and quotes escaped.
	return title ? `title=${JSON.stringify(title)}` : '';
}

function getFence(code) {
	const matches = code.match(/`+/g) ?? [''];
	const maxBackticks = Math.max(...matches.map((value) => value.length));
	return '`'.repeat(Math.max(3, maxBackticks + 1));
}

function normalizeNewlines(text) {
	return text.replace(/\r\n?/g, '\n');
}

function normalizeWhitespace(text) {
	return text.replace(/\s+/g, ' ').trim();
}
