#!/usr/bin/env python3
"""
Broken Link Checker for Warp Astro Starlight Documentation

Scans markdown source files to find and validate links.
- Internal links: validated by checking if the target file exists, and, when the
  link carries a #fragment, that the target page has a matching heading anchor
- External links: validated via HTTP HEAD requests
- Optional Slack notifications for CI/ambient agent integration
"""

import argparse
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse, unquote

DEFAULT_SLACK_CHANNEL = os.environ.get("GROWTH_DOCS_SLACK_CHANNEL_ID", "")

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# Regex patterns for extracting links
# Handle both normal links [text](url) and Astro Starlight angle-bracket links [text](<url with spaces>)
MARKDOWN_LINK_ANGLE = re.compile(r'\[([^\]]*)\]\(<([^>]+)>\)')
MARKDOWN_LINK_NORMAL = re.compile(r'\[([^\]]*)\]\(([^)<\s][^)\s]*)\)')
MARKDOWN_IMAGE_ANGLE = re.compile(r'!\[([^\]]*)\]\(<([^>]+)>\)')
MARKDOWN_IMAGE_NORMAL = re.compile(r'!\[([^\]]*)\]\(([^)<\s][^)\s]*)\)')
HTML_LINK = re.compile(r'<a[^>]+href=["\']([^"\']+)["\']', re.IGNORECASE)
HTML_IMG = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)
# Detects leftover GitBook embed syntax (should be migrated to <VideoEmbed />)
GITBOOK_EMBED = re.compile(r'\{%\s*embed\s+url=["\']([^"\']+)["\']')

MARKDOWN_EXTENSIONS = {'.md', '.mdx'}

# Domains that block bots or are unreliable
SKIP_DOMAINS = {'twitter.com', 'x.com', 'linkedin.com', 'facebook.com', 't.co'}

# Non-HTTP schemes to skip
SKIP_SCHEMES = {'mailto', 'tel', 'javascript', 'data', 'file', 'warp'}

# Directories to skip when scanning
SKIP_DIRECTORIES = {'_book', 'node_modules', '.git', '.vercel', 'dist'}

# A browser-like User-Agent. Several sites we legitimately link to (OpenAI,
# TikTok) reject an obvious bot UA with a 403 while serving the page fine to a
# real browser, which showed up as a wall of false positives.
BROWSER_UA = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
)

# Statuses that mean "the server refused to talk to an automated client",
# not "this page is gone". Cloudflare's interstitial (sourceforge.net), OpenAI's
# bot challenge, and login-gated destinations (Slack invites) all land here.
# These are reported separately and don't fail the run, because treating them as
# broken buries the 404s that actually need fixing.
BOT_BLOCK_STATUSES = {401, 403, 429}

# Transient failures worth one retry before we believe them.
RETRYABLE_ERRORS = {'Timeout', 'Connection Error'}

# --- Heading anchors -------------------------------------------------------
# A link to a heading that no longer exists resolves to a real page, so the
# file-existence check above passes and the reader silently lands at the top.
# These patterns rebuild the anchor ids Starlight emits (github-slugger) so
# fragments can be validated too.
ATX_HEADING = re.compile(r'^(#{1,6})\s+(.*?)\s*#*$')
EXPLICIT_ID = re.compile(r'\sid=["\']([^"\']+)["\']')
FENCE = re.compile(r'^\s*(`{3,}|~{3,})')


def slugify_heading(text):
    """Approximate github-slugger, which is what Starlight uses for anchor ids."""
    text = re.sub(r'\{[^}]*\}', '', text)                 # MDX expressions, e.g. {VARS.X}

    # A code span's content renders as literal text -- markdown never parses
    # `<name>` inside backticks as an HTML/JSX tag, so a heading like
    # `` ## `scorers/<name>/scorer.md` `` keeps "name" in its visible text and
    # thus its anchor id. Stash code-span content before the inline-HTML strip
    # below so that strip only touches real markup, then restore it verbatim.
    code_spans = []

    def _stash_code(match):
        code_spans.append(match.group(1))
        return f'\x00{len(code_spans) - 1}\x00'

    text = re.sub(r'`([^`]*)`', _stash_code, text)         # code spans (stashed)
    text = re.sub(r'<[^>]+>', '', text)                   # inline HTML/JSX
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)  # links keep their text
    text = re.sub(r'[*_]{1,3}', '', text)                 # emphasis
    text = re.sub(r'\x00(\d+)\x00', lambda m: code_spans[int(m.group(1))], text)
    text = text.strip().lower()
    text = re.sub(r'[^\w\- ]+', '', text, flags=re.UNICODE)
    return text.replace(' ', '-')


class LinkChecker:
    def __init__(self, docs_root, timeout=10, workers=16, strict=False):
        self.docs_root = Path(docs_root).resolve()
        self.timeout = timeout
        self.workers = max(1, workers)
        self.strict = strict
        self.files_scanned = 0
        self.internal_checked = 0
        self.external_checked = 0
        self.broken_links = []
        self.blocked_links = []
        self.external_cache = {}
        # slug set per target page, built lazily by _anchors_for()
        self.anchor_cache = {}

        # Astro Starlight projects may define additional pages outside
        # the content collection (e.g. `src/pages/api.astro` -> /api).
        # Collect those routes so absolute links like `/api` resolve.
        self.extra_routes = set()
        repo_root = self.docs_root
        for _ in range(4):
            candidate = repo_root / 'src' / 'pages'
            if candidate.is_dir():
                break
            if repo_root.parent == repo_root:
                break
            repo_root = repo_root.parent
        # Stash the public/ tree so /assets/... and /images/... refs
        # can be validated against on-disk files.
        self.public_root = repo_root / 'public'
        pages_dir = repo_root / 'src' / 'pages'
        if pages_dir.is_dir():
            for p in pages_dir.rglob('*'):
                if not p.is_file():
                    continue
                name = p.name
                # Skip dynamic routes and non-page outputs.
                if '[' in name or name.endswith('.md.ts'):
                    continue
                if p.suffix not in ('.astro', '.md', '.mdx'):
                    continue
                rel = p.relative_to(pages_dir)
                route = '/' + str(rel).rsplit('.', 1)[0]
                if route.endswith('/index'):
                    route = route[:-len('index')]
                self.extra_routes.add(route.rstrip('/') or '/')
        
        # Sessions are not thread-safe, so give each worker thread its own.
        self._local = threading.local()

    def find_markdown_files(self):
        files = []
        for root, dirs, filenames in os.walk(self.docs_root):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRECTORIES]
            for f in filenames:
                if Path(f).suffix.lower() in MARKDOWN_EXTENSIONS:
                    files.append(Path(root) / f)
        return sorted(files)

    def extract_links(self, filepath):
        links = []
        try:
            lines = filepath.read_text(encoding='utf-8').splitlines()
            in_html_comment = False
            in_fenced_code = None
            
            for line_num, raw_line in enumerate(lines, 1):
                line = raw_line

                # Skip fenced code blocks (``` or ~~~)
                if in_fenced_code:
                    fence_char = in_fenced_code[0]
                    fence_len = len(in_fenced_code)
                    if re.match(rf'^\s*{re.escape(fence_char)}{{{fence_len},}}\s*$', line):
                        in_fenced_code = None
                    continue

                fence_match = re.match(r'^\s*(`{3,}|~{3,})', line)
                if fence_match:
                    in_fenced_code = fence_match.group(1)
                    continue

                # Strip HTML comments while preserving same-line non-comment text.
                cleaned_segments = []
                index = 0
                while index < len(line):
                    if in_html_comment:
                        end_comment = line.find('-->', index)
                        if end_comment == -1:
                            index = len(line)
                            break
                        in_html_comment = False
                        index = end_comment + 3
                        continue

                    start_comment = line.find('<!--', index)
                    if start_comment == -1:
                        cleaned_segments.append(line[index:])
                        break

                    cleaned_segments.append(line[index:start_comment])
                    end_comment = line.find('-->', start_comment + 4)
                    if end_comment == -1:
                        in_html_comment = True
                        break
                    index = end_comment + 3

                line = ''.join(cleaned_segments)
                if not line.strip():
                    continue

                # Skip inline code spans like `...`
                # Skip inline code spans like `...` or ``...``
                line = re.sub(r'(`+)(?:(?!\1).)+\1', '', line)
                if not line.strip():
                    continue
                if not line.strip():
                    continue

                # Check angle-bracket links first (they take precedence)
                for pattern in [MARKDOWN_LINK_ANGLE, MARKDOWN_IMAGE_ANGLE]:
                    for match in pattern.finditer(line):
                        url = match.group(2).strip()
                        links.append({'url': url, 'line': line_num})
                
                # Check normal markdown links (excluding positions already matched by angle-bracket)
                for pattern in [MARKDOWN_LINK_NORMAL, MARKDOWN_IMAGE_NORMAL]:
                    for match in pattern.finditer(line):
                        url = match.group(2).strip()
                        # Skip if this looks like it was part of an angle-bracket link
                        if not url.startswith('>') and '<' not in url:
                            links.append({'url': url, 'line': line_num})
                
                for pattern in [HTML_LINK, HTML_IMG, GITBOOK_EMBED]:
                    for match in pattern.finditer(line):
                        url = match.group(1).strip()
                        links.append({'url': url, 'line': line_num})
        except Exception as e:
            print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
        return links

    def is_external(self, url):
        parsed = urlparse(url)
        return parsed.scheme in ('http', 'https')

    def should_skip(self, url):
        # A bare `#fragment` is a same-page link, not a no-op: it must still
        # resolve to a heading on the source page itself, so it falls through
        # to check_internal()/check_fragment() below instead of being skipped
        # here. Only a truly empty url has nothing to check.
        if not url:
            return True
        parsed = urlparse(url)
        if parsed.scheme in SKIP_SCHEMES:
            return True
        if self.is_external(url):
            for domain in SKIP_DOMAINS:
                if domain in parsed.netloc:
                    return True
        return False

    def resolve_internal(self, url, source_file):
        url = unquote(url.split('#')[0].split('?')[0])
        if not url:
            return None

        source_dir = source_file.parent
        if url.startswith('/'):
            # Absolute links are site-root paths (Starlight routes). Resolve
            # them against the content root, not the raw filesystem root.
            return self.docs_root / url.lstrip('/').rstrip('/')
        return (source_dir / url).resolve()

    def check_internal(self, url, source_file):
        # Resolve asset paths (served from public/) against the on-disk
        # public tree so we can catch broken /assets/foo.mp4 references
        # introduced by a missing file or a typo.
        asset_url = url.split('#')[0].split('?')[0]
        if asset_url.startswith('/assets/') or asset_url.startswith('/images/'):
            if self.public_root.is_dir():
                target = self.public_root / asset_url.lstrip('/')
                if target.exists() and target.is_file():
                    return True, None, None
                return False, "Asset not found in public/", None
            # No public/ tree on disk (unexpected): fall back to skipping.
            return True, None, None

        # Route defined by a non-collection Astro page under src/pages/ ?
        if asset_url.startswith('/') and self.extra_routes:
            normalized = asset_url.rstrip('/') or '/'
            if normalized in self.extra_routes:
                return True, None, None

        target = self.resolve_internal(url, source_file)
        if target is None:
            return True, None, None

        # Normalize: a Starlight route like `/foo/bar/` can be either a file
        # (`foo/bar.mdx`) or a directory with `index.mdx`. Check both.
        candidates = [
            target,
            Path(str(target) + '.mdx'),
            Path(str(target) + '.md'),
            target / 'index.mdx',
            target / 'index.md',
            target / 'README.md',
        ]
        for c in candidates:
            try:
                if c.exists() and c.is_file():
                    return True, None, None
            except OSError:
                continue

        # Check case mismatch against the parent directory, if any.
        parent = target.parent
        if parent.exists():
            name_lower = target.name.lower()
            for item in parent.iterdir():
                if item.name.lower() == name_lower and item.name != target.name:
                    return False, "File not found (case mismatch?)", f"Try: {item.name}"

        return False, "File not found", None

    def _anchors_for(self, page):
        """Heading slugs and explicit ids on a target page."""
        key = str(page)
        if key in self.anchor_cache:
            return self.anchor_cache[key]

        slugs = set()
        try:
            text = page.read_text(encoding='utf-8')
        except OSError:
            self.anchor_cache[key] = slugs
            return slugs

        in_fence = False
        in_frontmatter = False
        for n, line in enumerate(text.splitlines()):
            if n == 0 and line.strip() == '---':
                in_frontmatter = True
                continue
            if in_frontmatter:
                if line.strip() == '---':
                    in_frontmatter = False
                continue
            if FENCE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            m = ATX_HEADING.match(line)
            if m:
                slugs.add(slugify_heading(m.group(2)))
        # Hand-written anchors, e.g. <a id="foo"> or <h2 id="foo">.
        slugs.update(EXPLICIT_ID.findall(text))
        slugs.discard('')

        self.anchor_cache[key] = slugs
        return slugs

    def check_fragment(self, url, source_file):
        """Validate a link's #fragment against the target page's headings.

        The file-existence check passes for a link whose heading was renamed or
        removed, so the reader silently lands at the top of the page instead of
        the section they were sent to. Returns (valid, error, suggestion).
        """
        fragment = url.partition('#')[2].split('?')[0]
        if not fragment:
            return True, None, None

        route = url.split('#')[0]
        # A bare `#frag` and a self-referential `/page/#frag` are both
        # same-page links, so either way the target is the source file.
        page = self.resolve_internal(url, source_file) if route else source_file
        if page is None:
            page = source_file

        for candidate in (
            page,
            Path(str(page) + '.mdx'),
            Path(str(page) + '.md'),
            page / 'index.mdx',
            page / 'index.md',
        ):
            try:
                if candidate.exists() and candidate.is_file():
                    page = candidate
                    break
            except OSError:
                continue
        else:
            return True, None, None  # not a content page; nothing to check

        anchors = self._anchors_for(page)
        if not anchors or fragment in anchors:
            return True, None, None

        # Offer the closest heading that shares a word with the fragment.
        words = set(fragment.split('-'))
        near = [a for a in sorted(anchors) if words & set(a.split('-'))]
        suggestion = f"Try: #{', #'.join(near[:3])}" if near else None
        return False, f"Heading anchor '#{fragment}' not found on target page", suggestion

    def _session(self):
        """Return this thread's requests session, creating it on first use."""
        if not HAS_REQUESTS:
            return None
        session = getattr(self._local, 'session', None)
        if session is None:
            session = requests.Session()
            session.headers.update({
                'User-Agent': BROWSER_UA,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
            })
            self._local.session = session
        return session

    def _request_external(self, url):
        """Single attempt. Returns (valid, error, category).

        category is None when valid, 'blocked' when the server refused an
        automated client, and 'broken' for a genuine failure.
        """
        session = self._session()
        try:
            resp = session.head(url, timeout=self.timeout, allow_redirects=True)
            # Many servers mishandle HEAD. Retry anything that failed with GET
            # before concluding the link is bad.
            if resp.status_code >= 400:
                resp = session.get(url, timeout=self.timeout, allow_redirects=True, stream=True)
                resp.close()

            if resp.status_code < 400:
                return True, None, None
            if resp.status_code in BOT_BLOCK_STATUSES:
                return False, f"HTTP {resp.status_code}", 'blocked'
            return False, f"HTTP {resp.status_code}", 'broken'
        except requests.exceptions.Timeout:
            return False, "Timeout", 'broken'
        except requests.exceptions.SSLError:
            return False, "SSL Error", 'broken'
        except requests.exceptions.ConnectionError:
            return False, "Connection Error", 'broken'
        except Exception as e:
            return False, f"Error: {type(e).__name__}", 'broken'

    def check_external(self, url):
        if not HAS_REQUESTS:
            return True, "Skipped (requests not installed)", None

        if url in self.external_cache:
            return self.external_cache[url]

        valid, error, category = self._request_external(url)
        # Timeouts and connection resets are frequently transient; confirm once
        # before reporting, so a blip doesn't look like a broken link.
        if not valid and error in RETRYABLE_ERRORS:
            time.sleep(1)
            valid, error, category = self._request_external(url)

        result = (valid, error, category)
        self.external_cache[url] = result
        return result

    def warm_external_cache(self, files):
        """Resolve every unique external URL up front, in parallel.

        Checking these one at a time as files are walked is unusably slow: a
        single changelog page can carry hundreds of GitHub links, and one
        rate-limited host stalls the entire run. Populating the cache
        concurrently keeps the per-file pass to pure cache reads.
        """
        if not HAS_REQUESTS:
            return

        urls = set()
        for filepath in files:
            for link in self.extract_links(filepath):
                url = link['url']
                if not self.should_skip(url) and self.is_external(url):
                    urls.add(url)

        if not urls:
            return

        urls = sorted(urls)
        total = len(urls)
        print(f"Resolving {total} unique external URLs with {self.workers} workers...")

        done = 0
        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            for _ in pool.map(self.check_external, urls):
                done += 1
                if done % 25 == 0 or done == total:
                    print(f"\r  {done}/{total}", end='', flush=True)
        print()

    def check_file(self, filepath, check_internal=True, check_external=True):
        links = self.extract_links(filepath)
        broken = []
        blocked = []
        
        for link in links:
            url = link['url']
            if self.should_skip(url):
                continue
            
            is_ext = self.is_external(url)
            
            if is_ext and not check_external:
                continue
            if not is_ext and not check_internal:
                continue
            
            category = 'broken'
            if is_ext:
                self.external_checked += 1
                valid, error, category = self.check_external(url)
                suggestion = None
            else:
                self.internal_checked += 1
                valid, error, suggestion = self.check_internal(url, filepath)
                # The page resolves; now confirm the #fragment does too. Without
                # this the link passes and the reader lands at the top of the
                # page rather than the section it names.
                if valid and '#' in url:
                    valid, error, suggestion = self.check_fragment(url, filepath)
            
            if not valid:
                entry = {
                    'file': str(filepath.relative_to(self.docs_root)),
                    'line': link['line'],
                    'url': url,
                    'error': error,
                    'suggestion': suggestion,
                    'type': 'external' if is_ext else 'internal'
                }
                if category == 'blocked' and not self.strict:
                    blocked.append(entry)
                else:
                    broken.append(entry)
        
        return broken, blocked

    def run(self, check_internal=True, check_external=True):
        files = self.find_markdown_files()
        total = len(files)
        
        print(f"Scanning {total} markdown files...")
        modes = []
        if check_internal:
            modes.append("internal")
        if check_external:
            modes.append("external")
        print(f"Checking: {' + '.join(modes)} links\n")
        
        if check_external:
            self.warm_external_cache(files)
        
        for i, filepath in enumerate(files, 1):
            rel = filepath.relative_to(self.docs_root)
            print(f"\r[{i}/{total}] {rel}", end='', flush=True)
            
            self.files_scanned += 1
            broken, blocked = self.check_file(filepath, check_internal, check_external)
            self.broken_links.extend(broken)
            self.blocked_links.extend(blocked)
        
        print("\n")

    def print_report(self):
        print("=" * 60)
        print("BROKEN LINK REPORT")
        print("=" * 60)
        print(f"Files scanned: {self.files_scanned}")
        print(f"Internal links checked: {self.internal_checked}")
        print(f"External links checked: {self.external_checked}")
        print(f"Broken links found: {len(self.broken_links)}")
        if self.blocked_links:
            print(f"Bot-blocked (not failures): {len(self.blocked_links)}")
        print("=" * 60)
        
        internal = [l for l in self.broken_links if l['type'] == 'internal']
        external = [l for l in self.broken_links if l['type'] == 'external']
        
        if internal:
            print(f"\n### INTERNAL ({len(internal)} broken)\n")
            for link in internal:
                print(f"{link['file']}:{link['line']}")
                print(f"  Link: {link['url']}")
                print(f"  Error: {link['error']}")
                if link['suggestion']:
                    print(f"  Suggestion: {link['suggestion']}")
                print()
        
        if external:
            print(f"\n### EXTERNAL ({len(external)} broken)\n")
            for link in external:
                print(f"{link['file']}:{link['line']}")
                print(f"  Link: {link['url']}")
                print(f"  Error: {link['error']}")
                print()
        
        if self.blocked_links:
            # Grouped by URL: one bot-protected domain can appear on dozens of
            # lines, and listing every occurrence drowns out real breakage.
            by_url = {}
            for link in self.blocked_links:
                by_url.setdefault((link['url'], link['error']), []).append(
                    f"{link['file']}:{link['line']}"
                )
            print(f"\n### BOT-BLOCKED ({len(by_url)} URLs, not counted as broken)\n")
            print("These returned 401/403/429, which means the server refused an")
            print("automated request. Verify in a browser before changing them.\n")
            for (url, error), locations in sorted(by_url.items()):
                print(f"  {url}")
                print(f"    Error: {error} ({len(locations)} occurrence(s))")
                print(f"    First seen: {locations[0]}")
            print()
        
        if not self.broken_links:
            print("\n✓ No broken links found!")

    def get_results(self):
        return {
            'docs_root': str(self.docs_root),
            'files_scanned': self.files_scanned,
            'internal_checked': self.internal_checked,
            'external_checked': self.external_checked,
            'broken_count': len(self.broken_links),
            'broken_links': self.broken_links,
            'blocked_count': len(self.blocked_links),
            'blocked_links': self.blocked_links
        }

    def format_slack_message(self):
        internal = [l for l in self.broken_links if l['type'] == 'internal']
        external = [l for l in self.broken_links if l['type'] == 'external']
        
        blocked_note = ""
        if self.blocked_links:
            blocked_urls = {l['url'] for l in self.blocked_links}
            blocked_note = (
                f"\n\n_{len(blocked_urls)} URL(s) returned 401/403/429 (bot-blocked) "
                "and were not counted as broken._"
            )
        
        if not self.broken_links:
            return (
                ":white_check_mark: *Broken Link Check Passed*\n\n"
                "No broken links found in Astro Starlight docs." + blocked_note
            )
        
        lines = [
            ":warning: *Broken Link Check Found Issues*",
            "",
            f"• Files scanned: {self.files_scanned}",
            f"• Internal links checked: {self.internal_checked}",
            f"• External links checked: {self.external_checked}",
            f"• *Broken links found: {len(self.broken_links)}*",
        ]
        if self.blocked_links:
            blocked_urls = {l['url'] for l in self.blocked_links}
            lines.append(f"• Bot-blocked, not failures: {len(blocked_urls)} URL(s)")
        
        if internal:
            lines.append(f"\n*Internal ({len(internal)} broken):*")
            for link in internal[:10]:
                lines.append(f"  • `{link['file']}:{link['line']}` → {link['url']}")
            if len(internal) > 10:
                lines.append(f"  _...and {len(internal) - 10} more_")
        
        if external:
            lines.append(f"\n*External ({len(external)} broken):*")
            for link in external[:5]:
                lines.append(f"  • `{link['file']}:{link['line']}` → {link['error']}")
            if len(external) > 5:
                lines.append(f"  _...and {len(external) - 5} more_")
        
        lines.append("\n_Run the skill to fix these issues._")
        return "\n".join(lines)


def send_slack_notification(message, channel=DEFAULT_SLACK_CHANNEL):
    token = os.environ.get('SLACK_BOT_TOKEN')
    if not token:
        print("Error: SLACK_BOT_TOKEN environment variable not set", file=sys.stderr)
        print("Create it with: warp secret create SLACK_BOT_TOKEN --scope team", file=sys.stderr)
        return False
    
    if not HAS_REQUESTS:
        print("Error: 'requests' library required for Slack notifications", file=sys.stderr)
        return False
    
    try:
        resp = requests.post(
            'https://slack.com/api/chat.postMessage',
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
            },
            json={
                'channel': channel,
                'text': message,
                'mrkdwn': True,
            },
            timeout=10
        )
        data = resp.json()
        if not data.get('ok'):
            print(f"Slack API error: {data.get('error', 'unknown')}", file=sys.stderr)
            return False
        print(f"Slack notification sent to channel {channel}")
        return True
    except Exception as e:
        print(f"Failed to send Slack notification: {e}", file=sys.stderr)
        return False


def find_docs_root():
    """Locate the content root for this Astro Starlight docs site.

    Preference order, from most specific to most general:
    1. `src/content/docs/` relative to cwd or any ancestor (this repo's layout).
    2. `docs/` relative to cwd or any ancestor (older/legacy layout).
    3. Fall back to cwd.
    """
    cwd = Path.cwd()
    for base in (cwd, *cwd.parents):
        starlight = base / 'src' / 'content' / 'docs'
        if starlight.is_dir():
            return starlight
    for base in (cwd, *cwd.parents):
        legacy = base / 'docs'
        if legacy.is_dir():
            return legacy
    return cwd


def main():
    parser = argparse.ArgumentParser(description='Check Astro Starlight docs for broken links')
    parser.add_argument('--docs-root', help='Docs root directory (auto-detected if not set)')
    parser.add_argument('--internal-only', action='store_true', help='Only check internal links')
    parser.add_argument('--external-only', action='store_true', help='Only check external links')
    parser.add_argument('--timeout', type=int, default=10, help='HTTP timeout (default: 10)')
    parser.add_argument('--workers', type=int, default=16,
                        help='Concurrent external link requests (default: 16)')
    parser.add_argument('--strict', action='store_true',
                        help='Treat bot-blocked (401/403/429) responses as broken links')
    parser.add_argument('--output', help='Output JSON file')
    parser.add_argument('--slack-notify', action='store_true',
                        help='Send results to Slack (requires SLACK_BOT_TOKEN and GROWTH_DOCS_SLACK_CHANNEL_ID env vars)')
    parser.add_argument('--slack-channel', default=DEFAULT_SLACK_CHANNEL,
                        help=f'Slack channel ID (default: {DEFAULT_SLACK_CHANNEL})')
    
    args = parser.parse_args()
    
    docs_root = Path(args.docs_root) if args.docs_root else find_docs_root()
    
    if not docs_root.exists():
        print(f"Error: Docs root not found: {docs_root}", file=sys.stderr)
        sys.exit(1)
    
    check_internal = not args.external_only
    check_external = not args.internal_only
    
    if check_external and not HAS_REQUESTS:
        print("Warning: 'requests' not installed, external links will be skipped", file=sys.stderr)
        print("Install with: pip3 install requests\n", file=sys.stderr)
    
    print(f"Docs root: {docs_root}\n")
    
    checker = LinkChecker(docs_root, timeout=args.timeout, workers=args.workers,
                          strict=args.strict)
    
    start = time.time()
    checker.run(check_internal=check_internal, check_external=check_external)
    elapsed = time.time() - start
    
    print(f"Completed in {elapsed:.1f}s\n")
    checker.print_report()
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(checker.get_results(), f, indent=2)
        print(f"\nResults saved to: {args.output}")
    
    if args.slack_notify:
        message = checker.format_slack_message()
        send_slack_notification(message, channel=args.slack_channel)
    
    sys.exit(1 if checker.broken_links else 0)


if __name__ == '__main__':
    main()
