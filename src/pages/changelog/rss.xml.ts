import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { getEntry } from 'astro:content';

/**
 * RSS feed for the Warp changelog.
 *
 * The legacy GitBook docs auto-generated `/changelog/rss.xml` and
 * `vercel.json` already redirects a handful of legacy paths
 * (`/changelog/changelog/rss`, `/changelog/rss`, etc.) to `/changelog/`.
 * We restore the canonical feed at `/changelog/rss.xml` so existing
 * subscribers (and any external links) keep working.
 *
 * The changelog is a single MDX file with H3 headings of the form
 * `### YYYY.MM.DD (vX.Y...)`. We split on those headings so each
 * release becomes its own RSS item with a stable pubDate.
 */
const RELEASE_HEADING = /^###\s+(\d{4})\.(\d{2})\.(\d{2})(?:\s*\(([^)]*)\))?\s*$/m;

interface ReleaseSection {
	title: string;
	pubDate: Date;
	body: string;
}

function splitReleases(body: string): ReleaseSection[] {
	const lines = body.split('\n');
	const releases: ReleaseSection[] = [];
	let current: { headerMatch: RegExpMatchArray; lines: string[] } | null = null;

	for (const line of lines) {
		const match = line.match(RELEASE_HEADING);
		if (match) {
			if (current) {
				releases.push(buildRelease(current));
			}
			current = { headerMatch: match, lines: [] };
			continue;
		}
		if (current) {
			current.lines.push(line);
		}
	}
	if (current) {
		releases.push(buildRelease(current));
	}
	return releases;
}

function buildRelease({
	headerMatch,
	lines,
}: {
	headerMatch: RegExpMatchArray;
	lines: string[];
}): ReleaseSection {
	const [, year, month, day, version] = headerMatch;
	const date = `${year}.${month}.${day}`;
	const title = version ? `${date} (${version})` : date;
	// Use noon UTC so the ordering is stable regardless of the reader's TZ.
	const pubDate = new Date(`${year}-${month}-${day}T12:00:00Z`);
	return { title, pubDate, body: lines.join('\n').trim() };
}

export async function GET(context: APIContext) {
	const entry = await getEntry('docs', 'changelog');
	if (!entry) {
		return new Response('Changelog not found', { status: 404 });
	}

	const releases = splitReleases(entry.body ?? '');
	const site = context.site ?? new URL('https://docs.warp.dev');
	const channelLink = new URL('/changelog/', site).href;

	return rss({
		title: 'Warp Changelog',
		description:
			entry.data.description ??
			'Updates and release notes for Warp, the Agentic Development Environment.',
		site,
		items: releases.map((release) => ({
			title: release.title,
			pubDate: release.pubDate,
			// Anchor each item to the corresponding release on the changelog page.
			link: `${channelLink}#${release.title
				.toLowerCase()
				.replace(/[^a-z0-9]+/g, '-')
				.replace(/^-|-$/g, '')}`,
			description: release.body,
		})),
		customData: '<language>en-us</language>',
	});
}
