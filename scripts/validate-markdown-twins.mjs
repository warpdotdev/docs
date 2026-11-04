// Checks the generated Markdown twins after `npm run build`.
//
// Every sitemap page that advertises a twin with
// `<link rel="alternate" type="text/markdown">` has one at `<path>.md`
// (`/` -> `/index.md`), written by
// src/integrations/docs-markdown-integration.js. Each twin must exist and start
// with YAML frontmatter whose `canonical` is the HTML page's own
// `<link rel="canonical">`, so the twin, its `Link` header (vercel.json), and
// the HTML page all name the same URL.
//
// Usage: node scripts/validate-markdown-twins.mjs [outputDir]
// outputDir defaults to .vercel/output/static.
import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { DOCS_ORIGIN } from '../src/lib/site.js';

const outputDir = path.resolve(process.argv[2] ?? '.vercel/output/static');

const sitemapFiles = (await readdir(outputDir)).filter((name) => /^sitemap-\d+\.xml$/.test(name));
if (sitemapFiles.length === 0) {
	console.error(`No sitemap-N.xml in ${outputDir}. Run npm run build first.`);
	process.exit(1);
}
const pageUrls = new Set();
for (const name of sitemapFiles) {
	const xml = await readFile(path.join(outputDir, name), 'utf8');
	for (const [, loc] of xml.matchAll(/<loc>([^<]+)<\/loc>/g)) pageUrls.add(loc.trim());
}

const problems = [];
let checked = 0;
let skipped = 0;
for (const url of pageUrls) {
	if (!url.startsWith(`${DOCS_ORIGIN}/`)) continue;
	const pagePath = new URL(url).pathname.replace(/\/$/, '');
	const htmlFile = path.join(outputDir, pagePath, 'index.html');
	const markdownFile = path.join(outputDir, pagePath ? `${pagePath}.md` : 'index.md');

	let html;
	try {
		html = await readFile(htmlFile, 'utf8');
	} catch {
		problems.push(`${url}: missing ${path.relative(outputDir, htmlFile)}`);
		continue;
	}
	// Pages without a twin, such as the API reference at /api/, do not advertise one.
	if (!/<link rel="alternate" type="text\/markdown"/.test(html)) {
		skipped += 1;
		continue;
	}
	let markdown;
	try {
		markdown = await readFile(markdownFile, 'utf8');
	} catch {
		problems.push(`${url}: advertises ${path.relative(outputDir, markdownFile)}, which was not generated`);
		continue;
	}
	checked += 1;

	const htmlCanonical = html.match(/<link rel="canonical" href="([^"]+)"/)?.[1];
	const frontmatter = markdown.match(/^---\n([\s\S]*?)\n---\n/)?.[1];
	if (!frontmatter) {
		problems.push(`${url}: .md twin does not start with YAML frontmatter`);
		continue;
	}
	const fields = {};
	for (const line of frontmatter.split('\n')) {
		const index = line.indexOf(': ');
		try {
			fields[line.slice(0, index)] = JSON.parse(line.slice(index + 2));
		} catch {
			problems.push(`${url}: frontmatter line is not a quoted value: ${line}`);
		}
	}
	if (!fields.title) problems.push(`${url}: frontmatter has no title`);
	if (fields.canonical !== url) {
		problems.push(`${url}: frontmatter canonical is ${fields.canonical}`);
	}
	if (htmlCanonical && htmlCanonical !== fields.canonical) {
		problems.push(`${url}: HTML canonical ${htmlCanonical} differs from twin canonical ${fields.canonical}`);
	}
}

if (checked === 0) problems.push('No Markdown twins were checked.');

if (problems.length > 0) {
	console.error(`${problems.length} Markdown twin problem(s):`);
	for (const problem of problems.slice(0, 50)) console.error(`  ${problem}`);
	process.exit(1);
}
console.log(
	`OK: ${checked} Markdown twins start with frontmatter that points to their HTML page ` +
		`(${skipped} sitemap page(s) advertise no twin).`,
);
