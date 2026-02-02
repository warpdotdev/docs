#!/usr/bin/env python3
"""
Broken Link Checker for Warp GitBook Documentation

Scans markdown source files to find and validate links.
- Internal links: validated by checking if the target file exists
- External links: validated via HTTP HEAD requests
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse, unquote

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# Regex patterns for extracting links
MARKDOWN_LINK = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')
MARKDOWN_IMAGE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
HTML_LINK = re.compile(r'<a[^>]+href=["\']([^"\']+)["\']', re.IGNORECASE)
HTML_IMG = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)
GITBOOK_EMBED = re.compile(r'\{%\s*embed\s+url=["\']([^"\']+)["\']')

MARKDOWN_EXTENSIONS = {'.md', '.mdx'}

# Domains that block bots or are unreliable
SKIP_DOMAINS = {'twitter.com', 'x.com', 'linkedin.com', 'facebook.com', 't.co'}

# Non-HTTP schemes to skip
SKIP_SCHEMES = {'mailto', 'tel', 'javascript', 'data', 'file', 'warp'}


class LinkChecker:
    def __init__(self, docs_root, timeout=10):
        self.docs_root = Path(docs_root).resolve()
        self.timeout = timeout
        self.files_scanned = 0
        self.internal_checked = 0
        self.external_checked = 0
        self.broken_links = []
        self.external_cache = {}
        
        if HAS_REQUESTS:
            self.session = requests.Session()
            self.session.headers['User-Agent'] = 'WarpDocsLinkChecker/1.0'
        else:
            self.session = None

    def find_markdown_files(self):
        files = []
        for root, _, filenames in os.walk(self.docs_root):
            for f in filenames:
                if Path(f).suffix.lower() in MARKDOWN_EXTENSIONS:
                    files.append(Path(root) / f)
        return sorted(files)

    def extract_links(self, filepath):
        links = []
        try:
            content = filepath.read_text(encoding='utf-8')
            lines = content.splitlines()
            
            for line_num, line in enumerate(lines, 1):
                for pattern in [MARKDOWN_LINK, MARKDOWN_IMAGE]:
                    for match in pattern.finditer(line):
                        url = match.group(2).strip()
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
            return self.docs_root / url.lstrip('/')
        return (source_dir / url).resolve()

    def check_internal(self, url, source_file):
        target = self.resolve_internal(url, source_file)
        if target is None:
            return True, None, None
        
        if target.exists():
            return True, None, None
        
        if target.is_dir():
            if (target / 'README.md').exists():
                return True, None, None
        
        # Check common fixes
        with_md = Path(str(target) + '.md')
        if with_md.exists():
            return False, "File not found", f"Try: {url}.md"
        
        readme = target / 'README.md'
        if readme.exists():
            return False, "File not found", f"Try: {url}/README.md"
        
        # Check case mismatch
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


def find_docs_root():
    cwd = Path.cwd()
    
    if (cwd / 'docs').is_dir():
        return cwd / 'docs'
    if (cwd / 'SUMMARY.md').exists():
        return cwd
    
    for parent in cwd.parents:
        if (parent / 'docs').is_dir():
            return parent / 'docs'
    
    return cwd


def main():
    parser = argparse.ArgumentParser(description='Check GitBook docs for broken links')
    parser.add_argument('--docs-root', help='Docs root directory (auto-detected if not set)')
    parser.add_argument('--internal-only', action='store_true', help='Only check internal links')
    parser.add_argument('--external-only', action='store_true', help='Only check external links')
    parser.add_argument('--timeout', type=int, default=10, help='HTTP timeout (default: 10)')
    parser.add_argument('--output', help='Output JSON file')
    
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
    
    sys.exit(1 if checker.broken_links else 0)


if __name__ == '__main__':
    main()
