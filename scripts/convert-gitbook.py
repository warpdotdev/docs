#!/usr/bin/env python3
"""Convert GitBook markdown files to Astro Starlight MDX format.

Usage:
    python scripts/convert-gitbook.py <gitbook_space_dir> <starlight_docs_dir> <space_slug> [--skip-existing]

Example:
    python scripts/convert-gitbook.py \
        /path/to/gitbook/docs/agent-platform \
        /path/to/docs/src/content/docs/agent-platform \
        agent-platform \
        --skip-existing
"""

import re
import sys
import shutil
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

HINT_MAP = {
    "info": "note",
    "warning": "caution",
    "danger": "danger",
    "success": "tip",
}

KEEP_FRONTMATTER_KEYS = {"title", "description"}

# ---------------------------------------------------------------------------
# Frontmatter
# ---------------------------------------------------------------------------


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body) from raw file content."""
    if not content.startswith("---"):
        return {}, content
    end = content.find("\n---", 3)
    if end == -1:
        return {}, content
    raw_fm = content[3:end].strip()
    body = content[end + 4:]  # skip past closing ---\n

    fm: dict = {}
    current_key = None
    current_val_lines: list[str] = []

    for line in raw_fm.split("\n"):
        # Continuation of multi-line value (indented or >- style)
        if current_key and (line.startswith("  ") or line.strip() == ""):
            current_val_lines.append(line)
            continue

        # Save previous key
        if current_key:
            fm[current_key] = "\n".join(current_val_lines).strip()
            current_key = None
            current_val_lines = []

        m = re.match(r"^(\w[\w-]*):\s*(.*)", line)
        if m:
            current_key = m.group(1)
            rest = m.group(2).strip()
            if rest == ">-" or rest == ">":
                current_val_lines = []
            else:
                current_val_lines = [rest]

    if current_key:
        fm[current_key] = "\n".join(current_val_lines).strip()

    return fm, body


def build_frontmatter(fm: dict, body: str) -> str:
    """Build clean YAML frontmatter string."""
    # If there's no title in frontmatter, extract from first H1
    if "title" not in fm:
        m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        if m:
            fm["title"] = m.group(1).strip()

    lines = ["---"]
    if "title" in fm:
        title = fm["title"].strip('"').strip("'")
        if any(c in title for c in ":#{}[]|>&*!%@`"):
            lines.append(f'title: "{title}"')
        else:
            lines.append(f"title: {title}")
    if "description" in fm:
        desc = fm["description"].strip()
        lines.append("description: >-")
        words = desc.split()
        current_line = "  "
        for word in words:
            if len(current_line) + len(word) + 1 > 78:
                lines.append(current_line)
                current_line = "  " + word
            else:
                current_line += (" " if len(current_line) > 2 else "") + word
        if current_line.strip():
            lines.append(current_line)
    lines.append("---")
    return "\n".join(lines)


def strip_first_h1(body: str) -> str:
    """Remove the first H1 heading (title is now in frontmatter)."""
    return re.sub(r"^#\s+.+\n?", "", body, count=1, flags=re.MULTILINE)


# ---------------------------------------------------------------------------
# Hints -> Asides
# ---------------------------------------------------------------------------


def convert_hints(content: str) -> str:
    """Convert {% hint style='X' %}...{% endhint %} to :::type asides.

    Tolerates extra attributes after `style="..."` (e.g. `icon="comment"`).
    """

    def _replace_hint(m):
        style = m.group(1)
        aside_type = HINT_MAP.get(style, "note")
        inner = m.group(2).strip()
        return f":::{aside_type}\n{inner}\n:::"

    pattern = r'\{%\s*hint\s+style="(\w+)"[^%]*%\}(.*?)\{%\s*endhint\s*%\}'
    return re.sub(pattern, _replace_hint, content, flags=re.DOTALL)


# ---------------------------------------------------------------------------
# Tabs -> MDX Tabs / TabItem
# ---------------------------------------------------------------------------


def convert_tabs(content: str) -> str:
    """Convert {% tabs %}...{% endtabs %} to <Tabs>/<TabItem> components."""

    def _replace_tabs_block(m):
        inner = m.group(1)
        result_parts = ["<Tabs>"]

        tab_pattern = r'\{%\s*tab\s+title="([^"]+)"\s*%\}(.*?)\{%\s*endtab\s*%\}'
        tabs = re.findall(tab_pattern, inner, flags=re.DOTALL)

        for title, tab_content in tabs:
            content_stripped = tab_content.strip()
            result_parts.append(f'  <TabItem label="{title}">')
            for line in content_stripped.split("\n"):
                result_parts.append(f"    {line}" if line.strip() else "")
            result_parts.append("  </TabItem>")

        result_parts.append("</Tabs>")
        return "\n".join(result_parts)

    pattern = r"\{%\s*tabs\s*%\}(.*?)\{%\s*endtabs\s*%\}"
    return re.sub(pattern, _replace_tabs_block, content, flags=re.DOTALL)


# ---------------------------------------------------------------------------
# Embeds -> VideoEmbed
# ---------------------------------------------------------------------------


def convert_embeds(content: str) -> str:
    """Convert {% embed url='X' %} to <VideoEmbed url='X' />."""

    # Pattern 1: embed with endembed (may have caption text between)
    def _replace_embed_with_end(m):
        url = m.group(1)
        caption = m.group(2).strip()
        if caption:
            return f'<VideoEmbed url="{url}" title="{caption}" />'
        return f'<VideoEmbed url="{url}" />'

    # Use negative lookahead to prevent spanning across other embed blocks
    content = re.sub(
        r'\{%\s*embed\s+url="([^"]+)"\s*%\}\s*\n?((?:(?!\{%\s*embed).)*?)\{%\s*endembed\s*%\}',
        _replace_embed_with_end,
        content,
        flags=re.DOTALL,
    )

    # Pattern 2: standalone embed (no endembed)
    content = re.sub(
        r'\{%\s*embed\s+url="([^"]+)"\s*%\}',
        r'<VideoEmbed url="\1" />',
        content,
    )

    return content


# ---------------------------------------------------------------------------
# Figures -> Markdown images
# ---------------------------------------------------------------------------


def convert_figures(content: str, rel_asset_prefix: str) -> str:
    """Convert <figure> tags to markdown images."""

    def _replace_figure(m):
        full = m.group(0)
        src_m = re.search(r'src="([^"]*)"', full)
        alt_m = re.search(r'alt="([^"]*)"', full)
        caption_m = re.search(
            r"<figcaption>(?:<p>)?(.*?)(?:</p>)?</figcaption>", full, re.DOTALL
        )

        if not src_m:
            return full

        src = src_m.group(1)
        alt = alt_m.group(1) if alt_m else ""
        caption = caption_m.group(1).strip() if caption_m else ""
        display_alt = alt or caption

        # Rewrite .gitbook/assets/ paths
        asset_filename = src.split("/")[-1]
        if ".gitbook/assets/" in src:
            # Sanitize filename for web compatibility
            safe_filename = sanitize_asset_filename(asset_filename)
            new_src = f"{rel_asset_prefix}{safe_filename}"
        else:
            new_src = src

        return f"![{display_alt}]({new_src})"

    pattern = r"<figure>.*?</figure>"
    return re.sub(pattern, _replace_figure, content, flags=re.DOTALL)


def convert_inline_images(content: str, rel_asset_prefix: str) -> str:
    """Rewrite plain markdown images that point at `.gitbook/assets/` to the
    Starlight asset directory.

    Some pages use `![alt](../../.gitbook/assets/foo.png)` directly instead of
    wrapping in `<figure>`. The figure converter doesn't touch those, so we
    handle them here.
    """

    def _rewrite(m):
        alt = m.group(1)
        src = m.group(2)
        if ".gitbook/assets/" not in src:
            return m.group(0)
        # Strip any URL fragment / query and pull the filename off the end.
        bare = src.split("#", 1)[0].split("?", 1)[0]
        asset_filename = bare.split("/")[-1]
        safe_filename = sanitize_asset_filename(asset_filename)
        return f"![{alt}]({rel_asset_prefix}{safe_filename})"

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", _rewrite, content)


# ---------------------------------------------------------------------------
# Code blocks
# ---------------------------------------------------------------------------


def convert_code_blocks(content: str) -> str:
    """Convert {% code %} wrappers (strip them; fenced blocks are fine as-is)."""
    content = re.sub(r"\{%\s*code[^%]*%\}\s*\n", "", content)
    content = re.sub(r"\{%\s*endcode\s*%\}\s*\n?", "", content)
    return content


# ---------------------------------------------------------------------------
# Internal links
# ---------------------------------------------------------------------------


def convert_links(content: str, file_rel_dir: str, space: str) -> str:
    """Rewrite relative .md links to absolute /space/... paths."""

    def _rewrite_link(m):
        text = m.group(1)
        href = m.group(2)
        fragment = ""

        # Skip external, absolute, anchor-only, and mailto links
        if href.startswith(("http://", "https://", "/", "#", "mailto:")):
            return m.group(0)

        # Separate fragment
        if "#" in href:
            href, fragment = href.split("#", 1)
            fragment = "#" + fragment

        if not href:
            return m.group(0)

        # Normalise the path relative to the current file's directory
        parts = ((file_rel_dir + "/" + href) if file_rel_dir else href).split("/")
        normalised = []
        for p in parts:
            if p == "..":
                if normalised:
                    normalised.pop()
            elif p and p != ".":
                normalised.append(p)
        rel = "/".join(normalised)

        # README.md -> directory path
        rel = re.sub(r"/README\.md$", "/", rel)
        rel = re.sub(r"^README\.md$", "", rel)
        # .md -> /
        rel = re.sub(r"\.md$", "/", rel)

        # Build absolute path
        abs_path = f"/{space}/{rel}" if rel else f"/{space}/"

        # Clean up double slashes
        while "//" in abs_path:
            abs_path = abs_path.replace("//", "/")

        # Ensure trailing slash before fragment
        if not abs_path.endswith("/"):
            abs_path += "/"

        return f"[{text}]({abs_path}{fragment})"

    # Negative lookbehind to skip image links ![alt](url)
    return re.sub(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)", _rewrite_link, content)


# ---------------------------------------------------------------------------
# MDX imports
# ---------------------------------------------------------------------------


def inject_imports(content: str) -> str:
    """Insert required MDX imports after frontmatter."""
    imports = []
    if "<Tabs>" in content or "<TabItem" in content:
        imports.append(
            "import { Tabs, TabItem } from '@astrojs/starlight/components';"
        )
    if "<VideoEmbed" in content:
        imports.append("import VideoEmbed from '@components/VideoEmbed.astro';")
    if "<Steps>" in content:
        imports.append(
            "import { Steps } from '@astrojs/starlight/components';"
        )

    if not imports:
        return content

    import_block = "\n".join(imports)

    # Insert after frontmatter closing ---
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            insert_pos = end + 4
            return (
                content[:insert_pos] + "\n" + import_block + "\n" + content[insert_pos:]
            )

    return import_block + "\n\n" + content


# ---------------------------------------------------------------------------
# HTML comments -> MDX-safe comments
# ---------------------------------------------------------------------------


def convert_html_comments(content: str) -> str:
    """Wrap HTML comments in {/* */} for MDX compatibility."""

    def _replace_comment(m):
        body = m.group(1)
        return "{/* " + body.strip() + " */}"

    return re.sub(r"<!--(.*?)-->", _replace_comment, content, flags=re.DOTALL)


# ---------------------------------------------------------------------------
# Steppers -> Steps component
# ---------------------------------------------------------------------------


def convert_steppers(content: str) -> str:
    """Convert {% stepper %}...{% endstepper %} to <Steps> with ordered list."""

    def _replace_stepper(m):
        inner = m.group(1)

        # Split into individual steps
        step_pattern = r'\{%\s*step\s*%\}(.*?)\{%\s*endstep\s*%\}'
        steps = re.findall(step_pattern, inner, flags=re.DOTALL)

        if not steps:
            return inner.strip()

        result_parts = ["<Steps>"]
        for i, step_content in enumerate(steps, 1):
            lines = step_content.strip().split("\n")
            # Indent all content under the list item
            indented = []
            for j, line in enumerate(lines):
                if j == 0:
                    # First line starts the ordered list item
                    indented.append(f"{i}. {line}")
                else:
                    indented.append(f"   {line}" if line.strip() else "")
            result_parts.append("\n".join(indented))

        result_parts.append("</Steps>")
        return "\n\n".join(result_parts)

    pattern = r'\{%\s*stepper\s*%\}(.*?)\{%\s*endstepper\s*%\}'
    return re.sub(pattern, _replace_stepper, content, flags=re.DOTALL)


# ---------------------------------------------------------------------------
# GitBook card tables -> ImageGrid
# ---------------------------------------------------------------------------


def convert_gitbook_card_tables(
    content: str, rel_asset_prefix: str, src_label: str = ""
) -> str:
    """Convert <table data-view='cards'> blocks to <ImageGrid>/<ImageGridItem>.

    GitBook's card tables come in two flavours:
      1. Image showcase grids (icons, themes) – each row has an <img> + label.
      2. Link-card grids (guide landing pages) – each row has a content-ref link.

    This function converts image-based card tables to the custom ImageGrid
    component.  Link-card tables (no <img> tags) are stripped; they should be
    rebuilt manually with Starlight's <LinkCard>/<CardGrid> components.
    """

    def _replace_card_table(m):
        table_html = m.group(0)

        # Extract rows: each <tr> in <tbody> is one card
        row_pattern = r'<tr>(.*?)</tr>'
        rows = re.findall(row_pattern, table_html, flags=re.DOTALL)
        if not rows:
            return ''  # empty table, strip it

        # Check if this is an image grid (contains <img> tags)
        if '<img' not in table_html:
            # Link-card table – strip it; needs manual conversion
            label = src_label or '(unknown file)'
            print(f"  ⚠ {label}: stripped link-card table — convert manually to <LinkCard>/<CardGrid>")
            return '{/* TODO: convert link-card table to <LinkCard>/<CardGrid> */}'

        items = []
        for row in rows:
            # Extract image src
            src_m = re.search(r'src="([^"]*)"', row)
            if not src_m:
                continue
            src = src_m.group(1)
            asset_filename = src.split('/')[-1]
            if '.gitbook/assets/' in src:
                safe_filename = sanitize_asset_filename(asset_filename)
            else:
                safe_filename = asset_filename

            # Extract label: text content of a <td> that doesn't contain <img>
            label = ''
            td_pattern = r'<td[^>]*>(.*?)</td>'
            tds = re.findall(td_pattern, row, flags=re.DOTALL)
            for td_content in tds:
                stripped = re.sub(r'<[^>]+>', '', td_content).strip()
                if stripped and '<img' not in td_content:
                    label = stripped
                    break

            if not label:
                label = asset_filename.rsplit('.', 1)[0]

            # Build a safe variable name for the import
            var_name = re.sub(r'[^a-zA-Z0-9]', '', asset_filename.rsplit('.', 1)[0])
            items.append((var_name, safe_filename, label))

        if not items:
            return ''

        # Build component usage.  The required imports (ImageGrid,
        # ImageGridItem, and each image) are emitted as a comment so the
        # author can move them into the import block at the top of the file.
        grid_lines = ['<ImageGrid>']
        for var_name, _filename, label in items:
            grid_lines.append(f'  <ImageGridItem src={{{var_name}}} label="{label}" />')
        grid_lines.append('</ImageGrid>')

        import_comment_lines = [
            '{/* ImageGrid imports needed:',
            "import ImageGrid from '@components/ImageGrid.astro';",
            "import ImageGridItem from '@components/ImageGridItem.astro';",
        ]
        for var_name, filename, _label in items:
            import_comment_lines.append(
                f"import {var_name} from '{rel_asset_prefix}{filename}';"
            )
        import_comment_lines.append('*/}')

        return '\n'.join(import_comment_lines) + '\n\n' + '\n'.join(grid_lines)

    return re.sub(
        r'<table\s+data-view="cards">.*?</table>',
        _replace_card_table,
        content,
        flags=re.DOTALL,
    )


def strip_gitbook_content_refs(content: str) -> str:
    """Strip {% content-ref %}...{% endcontent-ref %} wrappers, keeping inner.

    GitBook renders these as link cards. In Starlight we just preserve the
    inner markdown link (the converter's link rewrite step already handled
    the URL).
    """
    return re.sub(
        r'\{%\s*content-ref[^%]*%\}\s*\n?(.*?)\{%\s*endcontent-ref\s*%\}',
        lambda m: m.group(1).strip(),
        content,
        flags=re.DOTALL,
    )


# ---------------------------------------------------------------------------
# Misc cleanup
# ---------------------------------------------------------------------------


def strip_custom_anchors(content: str) -> str:
    """Remove GitBook custom anchor HTML like <a href='#x' id='x'></a>."""
    return re.sub(r'\s*<a\s+href="#[^"]*"\s+id="[^"]*"\s*>\s*</a>', "", content)


def convert_horizontal_rules(content: str) -> str:
    """Normalise *** horizontal rules to ---."""
    return re.sub(r"^\*{3,}$", "---", content, flags=re.MULTILINE)


def sanitize_html_tables(content: str) -> str:
    """Escape markdown-special characters inside HTML table content for MDX."""

    def _sanitize_table(m):
        table = m.group(0)
        # Escape * and _ when they appear as text content inside <code> tags
        # <code>*</code> -> <code>{'*'}</code>
        table = re.sub(
            r"<code>([^<]*\*[^<]*)</code>",
            lambda cm: "<code>" + cm.group(1).replace("*", "{'*'}") + "</code>",
            table,
        )
        # Escape bare * between tags that could be interpreted as emphasis
        # Only in table cells: > * < pattern
        table = re.sub(r">\s*\*\s*<", "> {'*'} <", table)
        return table

    return re.sub(r"<table>.*?</table>", _sanitize_table, content, flags=re.DOTALL)


def fix_html_void_elements(content: str) -> str:
    """Convert void HTML elements to self-closing for MDX compatibility."""
    # <br> -> <br />, <img ...> -> <img ... />, <hr> -> <hr />
    for tag in ["br", "hr", "img"]:
        content = re.sub(
            rf"<({tag})(\s[^>]*)?>(?!\s*/)",
            lambda m: f"<{m.group(1)}{m.group(2) or ''} />",
            content,
        )
    return content


def convert_autolinks(content: str) -> str:
    """Convert markdown autolinks `<https://example.com>` to inline link form.

    MDX treats `<...>` as JSX, so the bare-URL autolink syntax that's valid
    GitHub-Flavored Markdown breaks the MDX parser. Rewrite each occurrence as
    `[https://example.com](https://example.com)` so the rendered link is
    identical.
    """
    return re.sub(
        r"<((?:https?|mailto):[^\s<>]+)>",
        lambda m: f"[{m.group(1)}]({m.group(1)})",
        content,
    )


# ---------------------------------------------------------------------------
# Asset prefix calculation
# ---------------------------------------------------------------------------


def compute_rel_asset_prefix(dst_rel_path: Path, space: str) -> str:
    """Compute relative path from a doc file to src/assets/<space>/.

    dst_rel_path is relative to the space docs dir (e.g. 'capabilities/skills.mdx').
    The docs dir is at src/content/docs/<space>/ and assets at src/assets/<space>/.
    """
    depth = len(dst_rel_path.parent.parts)
    # From content/docs/<space>/<subdirs> up to src/: 3 + depth
    ups = 3 + depth
    return "../" * ups + f"assets/{space}/"


# ---------------------------------------------------------------------------
# Main conversion
# ---------------------------------------------------------------------------


def convert_file(
    src_path: Path, dst_path: Path, space: str, gitbook_root: Path
) -> str:
    """Convert a single GitBook markdown file to Starlight MDX."""
    content = src_path.read_text(encoding="utf-8")

    # Determine relative directory within the space
    try:
        file_rel = src_path.relative_to(gitbook_root)
    except ValueError:
        file_rel = Path(src_path.name)
    file_rel_dir = str(file_rel.parent) if str(file_rel.parent) != "." else ""

    # Compute asset prefix from destination path
    dst_str = str(dst_path)
    space_marker = f"docs/{space}/"
    if space_marker in dst_str:
        after_space = dst_str.split(space_marker, 1)[1]
        dst_rel_in_space = Path(after_space)
    else:
        dst_rel_in_space = Path(dst_path.name)

    rel_asset_prefix = compute_rel_asset_prefix(dst_rel_in_space, space)

    # 1. Parse and rebuild frontmatter
    fm, body = parse_frontmatter(content)
    for key in list(fm.keys()):
        if key not in KEEP_FRONTMATTER_KEYS:
            del fm[key]
    new_fm = build_frontmatter(fm, body)
    body = strip_first_h1(body)

    # 2. Apply transforms (order matters)
    body = convert_hints(body)
    body = convert_embeds(body)
    body = convert_tabs(body)
    body = convert_code_blocks(body)
    body = convert_steppers(body)
    body = convert_gitbook_card_tables(body, rel_asset_prefix, src_label=str(file_rel))
    body = strip_gitbook_content_refs(body)
    body = convert_figures(body, rel_asset_prefix)
    body = convert_inline_images(body, rel_asset_prefix)
    body = convert_links(body, file_rel_dir, space)
    body = convert_html_comments(body)
    body = strip_custom_anchors(body)
    body = convert_horizontal_rules(body)
    body = sanitize_html_tables(body)
    body = fix_html_void_elements(body)
    body = convert_autolinks(body)

    # 3. Reassemble
    result = new_fm + "\n" + body

    # 4. Inject MDX imports
    result = inject_imports(result)

    # 5. Clean up excessive blank lines
    result = re.sub(r"\n{3,}", "\n\n", result)

    if not result.endswith("\n"):
        result += "\n"

    return result


def sanitize_asset_filename(name: str) -> str:
    """Replace spaces and parens in asset filenames for web compatibility."""
    return name.replace(" ", "-").replace("(", "").replace(")", "")


def collect_referenced_assets(gitbook_root: Path) -> dict[str, str]:
    """Find all asset filenames referenced in GitBook source files.

    Returns a dict mapping original_filename -> sanitized_filename.
    """
    assets: dict[str, str] = {}
    for md_file in gitbook_root.rglob("*.md"):
        if md_file.name == "SUMMARY.md":
            continue
        content = md_file.read_text(encoding="utf-8")
        # Match .gitbook/assets/FILENAME where filename may contain spaces
        for m in re.finditer(r'\.gitbook/assets/([^"]+)', content):
            original = m.group(1).strip()
            if original:
                assets[original] = sanitize_asset_filename(original)
    return assets


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)

    gitbook_root = Path(sys.argv[1]).resolve()
    starlight_docs = Path(sys.argv[2]).resolve()
    space = sys.argv[3]
    skip_existing = "--skip-existing" in sys.argv

    if not gitbook_root.is_dir():
        print(f"Error: {gitbook_root} is not a directory")
        sys.exit(1)

    # Collect all .md files (skip SUMMARY.md)
    md_files = sorted(
        p for p in gitbook_root.rglob("*.md") if p.name != "SUMMARY.md"
    )

    # Determine which files to skip (already migrated)
    skip_set: set[str] = set()
    if skip_existing:
        for existing in starlight_docs.rglob("*.mdx"):
            try:
                rel = existing.relative_to(starlight_docs)
            except ValueError:
                continue
            src_name = (
                "README.md" if rel.name == "index.mdx" else rel.stem + ".md"
            )
            src_rel = rel.parent / src_name
            skip_set.add(str(src_rel))

    converted = 0
    skipped = 0

    for src_path in md_files:
        rel = src_path.relative_to(gitbook_root)
        if str(rel) in skip_set:
            skipped += 1
            print(f"  ⊘ {rel} (already exists)")
            continue

        # Compute destination path
        dst_rel = rel
        if dst_rel.name == "README.md":
            dst_rel = dst_rel.parent / "index.mdx"
        else:
            dst_rel = dst_rel.with_suffix(".mdx")

        dst_path = starlight_docs / dst_rel
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        result = convert_file(src_path, dst_path, space, gitbook_root)
        dst_path.write_text(result, encoding="utf-8")
        converted += 1
        print(f"  ✓ {rel} → {dst_rel}")

    print(f"\nConverted: {converted}, Skipped: {skipped}")

    # Copy referenced assets
    gitbook_assets = gitbook_root / ".gitbook" / "assets"
    if gitbook_assets.is_dir():
        referenced = collect_referenced_assets(gitbook_root)
        src_dir = starlight_docs.parents[2]  # up to src/
        asset_dst = src_dir / "assets" / space
        asset_dst.mkdir(parents=True, exist_ok=True)

        copied = 0
        for original_name, safe_name in sorted(referenced.items()):
            asset_src = gitbook_assets / original_name
            if asset_src.exists():
                dest = asset_dst / safe_name
                if not dest.exists():
                    shutil.copy2(asset_src, dest)
                    copied += 1
        print(f"Assets copied: {copied} (of {len(referenced)} referenced)")


if __name__ == "__main__":
    main()
