#!/usr/bin/env python3
"""
Broken Link Checker for Warp Astro Starlight Documentation

Scans markdown source files to find and validate links.
- Internal links: validated by checking if the target file exists
- External links: validated via HTTP HEAD requests
- Optional Slack notifications for CI/ambient agent integration
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse, unquote

DEFAULT_SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL_ID", "")

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


class LinkChecker:
    def __init__(self, docs_root, timeout=10):
        self.docs_root = Path(docs_root).resolve()
        self.timeout = timeout
        self.files_scanned = 0
        self.internal_checked = 0
        self.external_checked = 0
        self.broken_links = []
        self.external_cache = {}

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
        
        if HAS_REQUESTS:
            self.session = requests.Session()
            self.session.headers['User-Agent'] = 'WarpDocsLinkChecker/1.0'
        else:
            self.session = None

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
        if not url or url.startswith('#'):
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

    def check_external(self, url):
        if not self.session:
            return True, "Skipped (requests not installed)", None
        
        if url in self.external_cache:
            return self.external_cache[url]
        
        try:
            resp = self.session.head(url, timeout=self.timeout, allow_redirects=True)
            if resp.status_code == 405:
                resp = self.session.get(url, timeout=self.timeout, allow_redirects=True, stream=True)
            
            if resp.status_code < 400:
                result = (True, None, None)
            else:
                result = (False, f"HTTP {resp.status_code}", None)
        except requests.exceptions.Timeout:
            result = (False, "Timeout", None)
        except requests.exceptions.SSLError:
            result = (False, "SSL Error", None)
        except requests.exceptions.ConnectionError:
            result = (False, "Connection Error", None)
        except Exception as e:
            result = (False, f"Error: {type(e).__name__}", None)
        
        self.external_cache[url] = result
        return result

    def check_file(self, filepath, check_internal=True, check_external=True):
        links = self.extract_links(filepath)
        broken = []
        
        for link in links:
            url = link['url']
            if self.should_skip(url):
                continue
            
            is_ext = self.is_external(url)
            
            if is_ext and not check_external:
                continue
            if not is_ext and not check_internal:
                continue
            
            if is_ext:
                self.external_checked += 1
                valid, error, suggestion = self.check_external(url)
            else:
                self.internal_checked += 1
                valid, error, suggestion = self.check_internal(url, filepath)
            
            if not valid:
                broken.append({
                    'file': str(filepath.relative_to(self.docs_root)),
                    'line': link['line'],
                    'url': url,
                    'error': error,
                    'suggestion': suggestion,
                    'type': 'external' if is_ext else 'internal'
                })
        
        return broken

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
        
        for i, filepath in enumerate(files, 1):
            rel = filepath.relative_to(self.docs_root)
            print(f"\r[{i}/{total}] {rel}", end='', flush=True)
            
            self.files_scanned += 1
            broken = self.check_file(filepath, check_internal, check_external)
            self.broken_links.extend(broken)
            
            if check_external:
                time.sleep(0.05)
        
        print("\n")

    def print_report(self):
        print("=" * 60)
        print("BROKEN LINK REPORT")
        print("=" * 60)
        print(f"Files scanned: {self.files_scanned}")
        print(f"Internal links checked: {self.internal_checked}")
        print(f"External links checked: {self.external_checked}")
        print(f"Broken links found: {len(self.broken_links)}")
        print("=" * 60)
        
        if not self.broken_links:
            print("\n✓ No broken links found!")
            return
        
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

    def get_results(self):
        return {
            'docs_root': str(self.docs_root),
            'files_scanned': self.files_scanned,
            'internal_checked': self.internal_checked,
            'external_checked': self.external_checked,
            'broken_count': len(self.broken_links),
            'broken_links': self.broken_links
        }

    def format_slack_message(self):
        internal = [l for l in self.broken_links if l['type'] == 'internal']
        external = [l for l in self.broken_links if l['type'] == 'external']
        
        if not self.broken_links:
            return ":white_check_mark: *Broken Link Check Passed*\n\nNo broken links found in Astro Starlight docs."
        
        lines = [
            ":warning: *Broken Link Check Found Issues*",
            "",
            f"• Files scanned: {self.files_scanned}",
            f"• Internal links checked: {self.internal_checked}",
            f"• External links checked: {self.external_checked}",
            f"• *Broken links found: {len(self.broken_links)}*",
        ]
        
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
    parser.add_argument('--output', help='Output JSON file')
    parser.add_argument('--slack-notify', action='store_true', 
                        help='Send results to Slack (requires SLACK_BOT_TOKEN and SLACK_CHANNEL_ID env vars)')
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
    
    checker = LinkChecker(docs_root, timeout=args.timeout)
    
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
