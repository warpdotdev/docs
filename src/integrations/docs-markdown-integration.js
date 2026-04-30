import { mkdir, readdir, readFile, rm, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseHTML } from 'linkedom';
import TurndownService from 'turndown';
import { gfm } from 'turndown-plugin-gfm';

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
	sanitizeRoot(clone);
	const markdownBody = turndown.turndown(clone.innerHTML).trim();
	const sections = [`# ${normalizeWhitespace(title)}`];

	if (description) {
		sections.push(description);
	}

	if (markdownBody) {
		sections.push(markdownBody);
	}

	return `${sections.join('\n\n').trim()}\n`;
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

	service.addRule('expressiveCodeBlock', {
		filter: (node) => isElement(node) && node.classList.contains('expressive-code'),
		replacement(_content, node) {
			if (!isElement(node)) return '\n\n';

			const code = node.querySelector('pre code');
			if (!code) return '\n\n';

			const language =
				code.getAttribute('data-language') ?? code.className.match(/language-([\w-]+)/)?.[1] ?? '';
			const rawCode = normalizeNewlines(code.textContent ?? '').replace(/\n$/, '');
			const fence = getFence(rawCode);
			const openingFence = language ? `${fence}${language}` : fence;

			return `\n\n${openingFence}\n${rawCode}\n${fence}\n\n`;
		},
	});

	return service;
}

function isElement(node) {
	return node.nodeType === 1;
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
