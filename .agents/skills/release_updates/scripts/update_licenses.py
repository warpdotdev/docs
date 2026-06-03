#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import DEFAULT_WORK_DIR
from common import docs_repo_root
from common import eprint
from common import read_json_file

SEPARATOR_RE = re.compile(r"^-{10,}$")
DEP_RE = re.compile(r"^  - (.+)$")
ALT_RE = re.compile(r"^(.+?)\s+\(([^)]+)\)$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Regenerate open-source-licenses.mdx from THIRD_PARTY_LICENSES.txt.",
    )
    parser.add_argument(
        "--docs-repo",
        default=None,
        help="Path to docs repo root (auto-detected if omitted).",
    )
    parser.add_argument(
        "--work-dir",
        default=str(DEFAULT_WORK_DIR),
        help=f"Working directory used by update_warp_app.py (default: {DEFAULT_WORK_DIR})",
    )
    parser.add_argument(
        "--manifest",
        default=None,
        help="Artifact manifest path (default: <work-dir>/warp_artifacts.json)",
    )
    parser.add_argument(
        "--licenses-file",
        default=None,
        help="Explicit path to THIRD_PARTY_LICENSES.txt.",
    )
    parser.add_argument(
        "--output-file",
        default=None,
        help="Output MDX file (default: docs open-source-licenses path).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute and print summary without writing files.",
    )
    return parser.parse_args()


def _extract_intro(content: str) -> str:
    marker = "\n## Dependencies"
    index = content.find(marker)
    if index == -1:
        return content.rstrip() + "\n"
    return content[:index].rstrip() + "\n"


def _parse_groups(content: str) -> list[tuple[str, list[str], str]]:
    lines = content.splitlines()
    total = len(lines)
    i = 0
    groups: list[tuple[str, list[str], str]] = []

    def is_dep_group_start(index: int) -> bool:
        if index + 1 >= total:
            return False
        line = lines[index]
        return bool(
            line.strip()
            and not line.startswith(" ")
            and not SEPARATOR_RE.match(line)
            and not line.startswith("=")
            and DEP_RE.match(lines[index + 1]),
        )

    def is_alt_group_start(index: int) -> bool:
        if index + 1 >= total:
            return False
        return bool(
            ALT_RE.match(lines[index]) and SEPARATOR_RE.match(lines[index + 1]),
        )

    while i < total and not is_dep_group_start(i):
        i += 1

    while i < total:
        if not lines[i].strip():
            i += 1
            continue
        if is_alt_group_start(i):
            break
        if not is_dep_group_start(i):
            i += 1
            continue

        license_type = lines[i].strip()
        i += 1
        deps: list[str] = []
        while i < total:
            match = DEP_RE.match(lines[i])
            if not match:
                break
            deps.append(match.group(1))
            i += 1

        if i < total and SEPARATOR_RE.match(lines[i]):
            i += 1

        body_lines: list[str] = []
        while i < total:
            if is_dep_group_start(i) or is_alt_group_start(i):
                break
            if lines[i].strip() == "" and (i + 1 >= total or lines[i + 1].strip() == ""):
                break
            body_lines.append(lines[i])
            i += 1
        while i < total and lines[i].strip() == "":
            i += 1
        groups.append((license_type, deps, "\n".join(body_lines).strip()))

    while i < total:
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        alt_match = ALT_RE.match(line)
        if not alt_match:
            i += 1
            continue

        dep_name = alt_match.group(1).strip()
        alt_license_type = alt_match.group(2).strip()
        i += 1
        if i < total and SEPARATOR_RE.match(lines[i]):
            i += 1
        body_lines: list[str] = []
        while i < total:
            if lines[i].strip() == "" and (i + 1 >= total or lines[i + 1].strip() == ""):
                break
            body_lines.append(lines[i])
            i += 1
        while i < total and lines[i].strip() == "":
            i += 1
        groups.append((alt_license_type, [dep_name], "\n".join(body_lines).strip()))

    return groups


def _render_licenses_markdown(content: str) -> tuple[str, int]:
    groups = _parse_groups(content=content)
    lines: list[str] = [
        "## Dependencies",
        "",
        "| Dependency | License |",
        "|---|---|",
    ]
    dep_count = 0
    for license_type, deps, _ in groups:
        for dep in deps:
            dep_count += 1
            lines.append(f"| {dep} | {license_type} |")

    lines.extend(
        [
            "",
            "## Full License Text",
            "",
            "```text",
            content.strip(),
            "```",
            "",
        ],
    )
    return "\n".join(lines).rstrip() + "\n", dep_count


def _licenses_path_from_manifest(manifest_path: Path) -> Path | None:
    if not manifest_path.exists():
        return None
    manifest = read_json_file(path=manifest_path)
    apps = manifest.get("apps", {})
    if not isinstance(apps, dict):
        return None
    preview = apps.get("preview", {})
    if not isinstance(preview, dict):
        return None
    path_value = preview.get("third_party_licenses_path")
    if isinstance(path_value, str) and path_value.strip():
        candidate = Path(path_value).expanduser().resolve()
        if candidate.exists():
            return candidate
    return None


def main() -> int:
    args = parse_args()
    docs_root = docs_repo_root(explicit_docs_repo=args.docs_repo)
    work_dir = Path(args.work_dir).expanduser().resolve()
    manifest_path = (
        Path(args.manifest).expanduser().resolve()
        if args.manifest
        else work_dir / "warp_artifacts.json"
    )

    output_file = (
        Path(args.output_file).expanduser().resolve()
        if args.output_file
        else docs_root
        / "src/content/docs/support-and-community/community/open-source-licenses.mdx"
    )

    licenses_path: Path | None = None
    if args.licenses_file:
        candidate = Path(args.licenses_file).expanduser().resolve()
        if not candidate.exists():
            raise FileNotFoundError(f"--licenses-file not found: {candidate}")
        licenses_path = candidate
    else:
        licenses_path = _licenses_path_from_manifest(manifest_path=manifest_path)

    if licenses_path is None:
        if args.dry_run:
            eprint(
                "[dry-run] No THIRD_PARTY_LICENSES source found from manifest or "
                "--licenses-file. Skipping source-dependent license preview.",
            )
            eprint(
                f"[dry-run] Would write {output_file} once a licenses source is available.",
            )
            return 0
        raise FileNotFoundError(
            "Unable to find THIRD_PARTY_LICENSES.txt. "
            "Run update_warp_app.py first, or pass --licenses-file explicitly.",
        )

    licenses_content = licenses_path.read_text(encoding="utf-8")
    rendered_body, dep_count = _render_licenses_markdown(content=licenses_content)

    existing = output_file.read_text(encoding="utf-8") if output_file.exists() else ""
    intro = _extract_intro(content=existing)
    final_output = intro.rstrip() + "\n\n" + rendered_body

    if args.dry_run:
        eprint(
            f"[dry-run] Would write {output_file} using {licenses_path} "
            f"({dep_count} dependency rows).",
        )
    else:
        output_file.write_text(final_output, encoding="utf-8")
        eprint(f"Wrote licenses doc: {output_file}")
        eprint(f"Source licenses file: {licenses_path}")
        eprint(f"Dependency rows written: {dep_count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

