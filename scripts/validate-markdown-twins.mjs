// Checks the generated Markdown twins after `npm run build`.
//
// For every sitemap page that advertises a twin with
// `<link rel="alternate" type="text/markdown">`:
// - the advertised href is the expected twin, `/<path>.md` (`/` -> `/index.md`);
// - the HTML page has a `<link rel="canonical">`;
// - the twin exists and starts with YAML frontmatter whose `canonical` equals
//   both the sitemap URL and the HTML canonical, and it has a `title`;
// - the routes in .vercel/output/config.json (written by
//   scripts/build-markdown-canonical-routes.mjs) give the twin exactly one
//   `Link: <HTML canonical>; rel="canonical"` header.
// Paths that are not twins, including reserved directories, missing files, and
// case variants, must get no canonical `Link` header.
//
// Usage: node scripts/validate-markdown-twins.mjs [outputDir]
// outputDir defaults to .vercel/output.
import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { canonicalLinkValue, linkHeadersFor } from '../src/lib/markdown-canonical-routes.js';
import { DOCS_ORIGIN } from '../src/lib/site.js';

const outputRoot = path.resolve(process.argv[2] ?? '.vercel/output');
const outputDir = path.join(outputRoot, 'static');

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
const { routes } = JSON.parse(await readFile(path.join(outputRoot, 'config.json'), 'utf8'));

const problems = [];
let checked = 0;
let skipped = 0;
for (const url of pageUrls) {
	if (!url.startsWith(`${DOCS_ORIGIN}/`)) continue;
	const pagePath = new URL(url).pathname.replace(/\/$/, '');
	const twinUrlPath = `${pagePath || '/index'}.md`;
	const htmlFile = path.join(outputDir, pagePath, 'index.html');
	const markdownFile = path.join(outputDir, twinUrlPath);

	let html;
	try {
		html = await readFile(htmlFile, 'utf8');
	} catch {
		problems.push(`${url}: missing ${path.relative(outputDir, htmlFile)}`);
		continue;
	}
	// Pages without a twin, such as the API reference at /api/, do not advertise one.
	const alternate = html.match(/<link rel="alternate" type="text\/markdown" href="([^"]*)"/);
	if (!alternate) {
		skipped += 1;
		continue;
	}
	checked += 1;
	if (alternate[1] !== twinUrlPath) {
		problems.push(`${url}: advertises Markdown at ${alternate[1]}, expected ${twinUrlPath}`);
	}
	const htmlCanonical = html.match(/<link rel="canonical" href="([^"]+)"/)?.[1];
	if (!htmlCanonical) problems.push(`${url}: HTML page has no <link rel="canonical">`);

	const headers = linkHeadersFor(routes, twinUrlPath);
	const expectedHeader = canonicalLinkValue(htmlCanonical ?? url);
	if (headers.length !== 1 || headers[0] !== expectedHeader) {
		problems.push(`${url}: ${twinUrlPath} Link headers are ${JSON.stringify(headers)}, expected [${expectedHeader}]`);
	}

	let markdown;
	try {
		markdown = await readFile(markdownFile, 'utf8');
	} catch {
		problems.push(`${url}: advertises ${twinUrlPath}, which was not generated`);
		continue;
	}
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
	if (fields.canonical !== htmlCanonical) {
		problems.push(`${url}: HTML canonical ${htmlCanonical} differs from twin canonical ${fields.canonical}`);
	}
}

if (checked === 0) problems.push('No Markdown twins were checked.');

const notTwins = [
	'/', '/factories/', '/llms.txt', '/sitemap-0.xml', '/openapi.yaml',
	'/assets/not-a-twin.md', '/_astro/not-a-twin.md', '/.well-known/not-a-twin.md',
	'/robots.md', '/AGENTS.md', '/not-a-twin.md', '/Factories.md', '/INDEX.md', '/factories.MD',
];
for (const pathname of notTwins) {
	const headers = linkHeadersFor(routes, pathname);
	if (headers.length > 0) problems.push(`${pathname} is not a twin but gets Link ${JSON.stringify(headers)}`);
}

if (problems.length > 0) {
	console.error(`${problems.length} Markdown twin problem(s):`);
	for (const problem of problems.slice(0, 50)) console.error(`  ${problem}`);
	process.exit(1);
}
console.log(
	`OK: ${checked} Markdown twins have frontmatter and exactly one canonical Link header that match ` +
		`their HTML page; ${notTwins.length} non-twin paths get none ` +
		`(${skipped} sitemap page(s) advertise no twin).`,
);
