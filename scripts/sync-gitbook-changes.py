#!/usr/bin/env python3
"""Incrementally sync new/modified gitbook files into the Starlight docs repo.

Reuses the conversion logic in `migrate-all.py` (which itself imports
`convert-gitbook.py`) and limits the work to the files reported by
`git diff --name-status <baseline>..<head>` in the gitbook repo.

Usage:
    python scripts/sync-gitbook-changes.py /path/to/gitbook \\
        [--baseline bf06b82f] [--head main] [--dry-run]

Behavior:
- Files added or modified under `docs/<space>/...` or `guides/...` are
  converted via `migrate_all.convert_file_enhanced` and written into
  `src/content/docs/...` using the same path mapping as the original migration.
- Files deleted in gitbook are deleted in docs.
- README.md/SUMMARY.md/.gitbook/* changes that aren't content are skipped.
- Existing docs files that were intentionally diverged from gitbook (e.g.
  `agent-modality.mdx` keeping the legacy slug) are still overwritten when
  their gitbook source changed; the caller is expected to do post-processing
  for renames or splits (self-hosting/, migrate-to-warp/, terminal/settings/).

This script never touches `vercel.json` or `src/sidebar.ts` — those are
edited separately so reviewers can see the navigation and redirect changes
clearly.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from importlib.machinery import SourceFileLoader
from pathlib import Path
from typing import Iterable

SCRIPT_DIR = Path(__file__).resolve().parent
DOCS_ROOT = SCRIPT_DIR.parent
STARLIGHT_DOCS = DOCS_ROOT / "src" / "content" / "docs"

# Load the existing conversion machinery
migrate_all = SourceFileLoader(
    "migrate_all", str(SCRIPT_DIR / "migrate-all.py")
).load_module()


SPACE_PREFIXES = (
    ("docs/warp/", "warp"),
    ("docs/agent-platform/", "agent-platform"),
    ("docs/reference/", "reference"),
    ("docs/support-and-community/", "support-and-community"),
    ("docs/enterprise/", "enterprise"),
    ("docs/changelog/", "changelog"),
    ("guides/", "guides"),
)

# These paths are content but should not be auto-converted; they need manual
# handling (see plan).
SKIP_FILES = {
    # SUMMARY.md drives sidebars; we map them to src/sidebar.ts manually.
    "SUMMARY.md",
    # .gitbook.yaml drives redirects; we port them to vercel.json manually.
    ".gitbook.yaml",
}

# JSX components that are docs-only design improvements (introduced after the
# original full migration, e.g. the FileTree migration in PR #50 and the
# DemoVideo component). When the docs file already uses one of these, the
# sync script will skip the file and report it instead of overwriting; the
# operator should hand-merge the gitbook diff in those cases.
DOCS_ONLY_JSX_GUARDS = (
    "<FileTree",
    "<DemoVideo",
)


def gitbook_space_root(gitbook_root: Path, space: str) -> Path:
    if space == "guides":
        return gitbook_root / "guides"
    return gitbook_root / "docs" / space


def classify(rel_path: str) -> tuple[str, str] | None:
    """Return (space, rel_in_space) or None for non-content paths."""
    name = rel_path.rsplit("/", 1)[-1]
    if name in SKIP_FILES:
        return None
    if "/.gitbook/" in rel_path or rel_path.startswith(".gitbook/"):
        return None
    if rel_path.startswith("docs/_book/"):
        return None
    if not rel_path.endswith(".md"):
        return None

    for prefix, space in SPACE_PREFIXES:
        if rel_path.startswith(prefix):
            return space, rel_path[len(prefix):]
    return None


def list_changes(
    gitbook_root: Path, baseline: str, head: str
) -> list[tuple[str, str]]:
    """Return [(status, path), ...] from git diff --name-status."""
    out = subprocess.check_output(
        [
            "git",
            "-C",
            str(gitbook_root),
            "--no-pager",
            "diff",
            "--name-status",
            f"{baseline}..{head}",
        ],
        text=True,
    )
    rows: list[tuple[str, str]] = []
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status = parts[0][0]
        # For renames, the new path is the last column.
        path = parts[-1]
        rows.append((status, path))
    return rows


def docs_dst_for(space: str, rel_in_space: str) -> Path:
    dst_rel = migrate_all.map_gitbook_path(space, rel_in_space)
    return STARLIGHT_DOCS / dst_rel


def has_docs_only_jsx(dst: Path) -> list[str]:
    """Return the list of docs-only JSX guards present in `dst`, or [] if none."""
    if not dst.exists():
        return []
    text = dst.read_text(encoding="utf-8")
    return [g for g in DOCS_ONLY_JSX_GUARDS if g in text]


def convert_one(gitbook_root: Path, space: str, rel_in_space: str, dry_run: bool) -> str:
    src = gitbook_space_root(gitbook_root, space) / rel_in_space
    dst = docs_dst_for(space, rel_in_space)
    if not src.exists():
        return f"  ⚠ source missing: {src}"
    # Refuse to overwrite a docs file that contains docs-only JSX components.
    # The operator must 3-way merge the gitbook diff manually (restore docs/
    # main, then re-apply just the gitbook content updates) so the design
    # components are preserved.
    guards = has_docs_only_jsx(dst)
    if guards:
        return (
            f"  ⚠ SKIPPED (docs-only JSX present, hand-merge required): "
            f"{space}/{rel_in_space} → {dst.relative_to(DOCS_ROOT)} "
            f"[{','.join(guards)}]"
        )
    if dry_run:
        return f"  [dry-run] {space}/{rel_in_space} → {dst.relative_to(DOCS_ROOT)}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    result = migrate_all.convert_file_enhanced(
        src, dst, space, gitbook_space_root(gitbook_root, space), DOCS_ROOT
    )
    dst.write_text(result, encoding="utf-8")
    return f"  ✓ {space}/{rel_in_space} → {dst.relative_to(DOCS_ROOT)}"


def delete_one(space: str, rel_in_space: str, dry_run: bool) -> str:
    dst = docs_dst_for(space, rel_in_space)
    if not dst.exists():
        return f"  ⊘ docs file already absent: {dst.relative_to(DOCS_ROOT)}"
    if dry_run:
        return f"  [dry-run] delete {dst.relative_to(DOCS_ROOT)}"
    dst.unlink()
    # Clean up empty parent dirs
    parent = dst.parent
    while parent != STARLIGHT_DOCS and parent.exists() and not any(parent.iterdir()):
        parent.rmdir()
        parent = parent.parent
    return f"  ✗ deleted {dst.relative_to(DOCS_ROOT)}"


def copy_changed_assets(
    gitbook_root: Path, changed: Iterable[tuple[str, str]], dry_run: bool
) -> int:
    """Copy any asset images that changed (under docs/<space>/.gitbook/assets/)."""
    copied = 0
    for status, path in changed:
        if status == "D":
            continue
        if "/.gitbook/assets/" not in path:
            continue
        # Determine which space the asset belongs to
        for prefix, space in SPACE_PREFIXES:
            if path.startswith(prefix):
                break
        else:
            continue
        asset_dir = migrate_all.map_asset_space(space)
        src = gitbook_root / path
        if not src.exists():
            continue
        dst = DOCS_ROOT / "src" / "assets" / asset_dir / migrate_all.sanitize_asset_filename(src.name)
        if dry_run:
            print(f"  [dry-run] asset {src.relative_to(gitbook_root)} → {dst.relative_to(DOCS_ROOT)}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied += 1
        print(f"  📎 asset {src.relative_to(gitbook_root)} → {dst.relative_to(DOCS_ROOT)}")
    return copied


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("gitbook", type=Path, help="Path to the gitbook repo root")
    ap.add_argument("--baseline", default="bf06b82f", help="Git ref representing the last sync")
    ap.add_argument("--head", default="main", help="Git ref to sync to")
    ap.add_argument("--dry-run", action="store_true", help="Plan only; don't write")
    args = ap.parse_args()

    gitbook_root = args.gitbook.resolve()
    if not (gitbook_root / "docs").is_dir():
        print(f"Error: {gitbook_root}/docs is not a directory")
        return 1

    rows = list_changes(gitbook_root, args.baseline, args.head)
    print(f"Found {len(rows)} changed paths between {args.baseline}..{args.head}")

    converted = deleted = skipped = 0
    log: list[str] = []
    for status, path in rows:
        cls = classify(path)
        if cls is None:
            skipped += 1
            continue
        space, rel = cls
        # Honor docs-specific skip set for orphaned/duplicate gitbook files.
        if rel in migrate_all.SKIP_PATHS.get(space, set()):
            log.append(f"  ⊘ skipped (intentional drop): {space}/{rel}")
            skipped += 1
            continue
        if status == "D":
            log.append(delete_one(space, rel, args.dry_run))
            deleted += 1
        else:
            # A, M, or R (treated as add/modify of the new path)
            log.append(convert_one(gitbook_root, space, rel, args.dry_run))
            converted += 1

    print()
    for line in log:
        print(line)
    print()

    asset_count = copy_changed_assets(gitbook_root, rows, args.dry_run)

    print()
    print(f"Summary: {converted} converted, {deleted} deleted, {skipped} skipped (non-content), {asset_count} assets copied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
