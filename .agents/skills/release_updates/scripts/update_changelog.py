#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from datetime import datetime
from datetime import timezone
from pathlib import Path
from typing import Any

from common import docs_repo_root
from common import eprint
from common import load_json_from_url
from common import resolve_channel_versions_file

DEFAULT_CHANNEL_VERSIONS_URL = "https://releases.warp.dev/channel_versions.json"
RE_CHANGELOG_DATE = re.compile(r"^### (\d{4}\.\d{2}\.\d{2})\s", re.MULTILINE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Incrementally update docs changelog from channel_versions.json.",
    )
    parser.add_argument(
        "--docs-repo",
        default=None,
        help="Path to docs repo root (auto-detected if omitted).",
    )
    parser.add_argument(
        "--channel-versions-file",
        default=None,
        help="Path to channel_versions.json.",
    )
    parser.add_argument(
        "--channel-versions-repo",
        default=None,
        help="Path to channel-versions repo or directory containing channel_versions.json.",
    )
    parser.add_argument(
        "--channel-versions-url",
        default=DEFAULT_CHANNEL_VERSIONS_URL,
        help=f"Fallback URL when no local channel_versions.json is found (default: {DEFAULT_CHANNEL_VERSIONS_URL})",
    )
    parser.add_argument(
        "--year",
        type=int,
        default=None,
        help="Target changelog year (defaults to current UTC year).",
    )
    parser.add_argument(
        "--output-file",
        default=None,
        help="Override changelog output path.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute and print summary without writing files.",
    )
    return parser.parse_args()


def _parse_datetime(value: str) -> datetime:
    candidates = [
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
    ]
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        for fmt in candidates:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
    raise ValueError(f"Unable to parse changelog date: {value}")


def _display_version(version_key: str) -> str:
    if "." not in version_key:
        return version_key
    return version_key.rsplit(".", 1)[0]


def _extract_intro_and_body(existing_content: str) -> tuple[str, str, str | None]:
    date_match = RE_CHANGELOG_DATE.search(existing_content)
    if date_match:
        intro = existing_content[: date_match.start()].rstrip() + "\n\n"
        body = existing_content[date_match.start() :].lstrip("\n")
        cutoff_date = date_match.group(1)
        return intro, body, cutoff_date
    return existing_content.rstrip() + "\n\n", "", None


def _ensure_year_in_changelog_index(index_file: Path, year: int, dry_run: bool) -> bool:
    if not index_file.exists():
        return False

    content = index_file.read_text(encoding="utf-8")
    year_line = f"* [**{year}**](/changelog/{year}/)"
    if year_line in content:
        return False

    lines = content.splitlines()
    insert_at = next(
        (idx for idx, line in enumerate(lines) if line.startswith("* [**")),
        len(lines),
    )
    lines.insert(insert_at, year_line)
    updated = "\n".join(lines).rstrip() + "\n"
    if dry_run:
        eprint(f"[dry-run] Would add {year} to {index_file}")
    else:
        index_file.write_text(updated, encoding="utf-8")
    return True


def _coerce_markdown_sections(changelog: dict[str, Any]) -> list[dict[str, str]]:
    raw_sections = changelog.get("markdown_sections")
    if isinstance(raw_sections, list):
        sections: list[dict[str, str]] = []
        for section in raw_sections:
            if not isinstance(section, dict):
                continue
            title = str(section.get("title", "")).strip()
            markdown = str(section.get("markdown", "")).strip("\n")
            if title:
                sections.append({"title": title, "markdown": markdown})
        if sections:
            return sections

    legacy_sections = changelog.get("sections")
    converted: list[dict[str, str]] = []
    if isinstance(legacy_sections, list):
        for section in legacy_sections:
            if not isinstance(section, dict):
                continue
            title = str(section.get("title", "")).strip()
            items = section.get("items")
            if not title or not isinstance(items, list):
                continue
            lines = [f"* {str(item).strip()}" for item in items if str(item).strip()]
            converted.append({"title": title, "markdown": "\n".join(lines)})
    return converted


def _normalize_bullets(markdown_blob: str) -> list[str]:
    lines: list[str] = []
    for raw_line in markdown_blob.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("* "):
            lines.append(line)
        elif line.startswith("- "):
            lines.append(f"* {line[2:].strip()}")
        else:
            lines.append(f"* {line}")
    return lines


def _render_entry(version_key: str, changelog: dict[str, Any]) -> str:
    display_date = _parse_datetime(str(changelog["date"])).strftime("%Y.%m.%d")
    display_version = _display_version(version_key=version_key)
    lines: list[str] = [f"### {display_date} ({display_version})", ""]

    image_url = changelog.get("image_url")
    sections = _coerce_markdown_sections(changelog=changelog)
    for section in sections:
        title = section["title"].strip()
        if title == "Coming soon":
            continue
        bullets = _normalize_bullets(section["markdown"])
        if not bullets:
            continue
        lines.append(f"**{title}**")
        lines.append("")
        if title == "New features" and isinstance(image_url, str) and image_url.strip():
            lines.append(
                f"<figure><img src=\"{image_url.strip()}\" alt=\"Release image for {display_date}\"><figcaption></figcaption></figure>",
            )
            lines.append("")
        lines.extend(bullets)
        lines.append("")

    oz_updates = changelog.get("oz_updates")
    if isinstance(oz_updates, list):
        bullets = [
            f"* {str(item).strip().lstrip('* ').strip()}"
            for item in oz_updates
            if str(item).strip()
        ]
        if bullets:
            lines.append("**Oz updates**")
            lines.append("")
            lines.extend(bullets)
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _new_entries(
    stable_changelogs: dict[str, Any],
    cutoff_date: str | None,
) -> list[str]:
    sortable: list[tuple[datetime, str, dict[str, Any]]] = []
    for version_key, payload in stable_changelogs.items():
        if not isinstance(payload, dict) or "date" not in payload:
            continue
        try:
            parsed_date = _parse_datetime(str(payload["date"]))
        except ValueError:
            continue
        sortable.append((parsed_date, version_key, payload))
    sortable.sort(key=lambda item: (item[0], item[1]), reverse=True)

    seen_dates: set[str] = set()
    entries: list[str] = []
    for parsed_date, version_key, payload in sortable:
        display_date = parsed_date.strftime("%Y.%m.%d")
        if cutoff_date is not None and display_date <= cutoff_date:
            continue
        if display_date in seen_dates:
            continue
        seen_dates.add(display_date)
        entries.append(_render_entry(version_key=version_key, changelog=payload))
    return entries


def _load_channel_versions(
    docs_root: Path,
    channel_versions_file: str | None,
    channel_versions_repo: str | None,
    fallback_url: str,
) -> dict[str, Any]:
    resolved_file = resolve_channel_versions_file(
        docs_root=docs_root,
        explicit_file=channel_versions_file,
        explicit_repo=channel_versions_repo,
    )
    if resolved_file:
        eprint(f"Using local channel versions file: {resolved_file}")
        import json

        return json.loads(resolved_file.read_text(encoding="utf-8"))

    eprint(f"No local channel versions file found; fetching: {fallback_url}")
    return load_json_from_url(url=fallback_url)


def main() -> int:
    args = parse_args()
    docs_root = docs_repo_root(explicit_docs_repo=args.docs_repo)
    year = args.year or datetime.now(tz=timezone.utc).year

    output_file = (
        Path(args.output_file).expanduser().resolve()
        if args.output_file
        else docs_root / "src/content/docs/changelog" / f"{year}.mdx"
    )
    output_file.parent.mkdir(parents=True, exist_ok=True)

    channel_versions_payload = _load_channel_versions(
        docs_root=docs_root,
        channel_versions_file=args.channel_versions_file,
        channel_versions_repo=args.channel_versions_repo,
        fallback_url=args.channel_versions_url,
    )
    stable_changelogs = (
        channel_versions_payload.get("changelogs", {})
        .get("stable", {})
    )
    if not isinstance(stable_changelogs, dict):
        raise ValueError("Invalid channel versions payload: changelogs.stable missing or invalid")

    created_new_file = not output_file.exists()
    if output_file.exists():
        existing_content = output_file.read_text(encoding="utf-8")
        intro, existing_body, cutoff_date = _extract_intro_and_body(
            existing_content=existing_content,
        )
    else:
        intro = (
            "---\n"
            f"title: \"Changelog — {year}\"\n"
            "description: >-\n"
            f"  Warp release notes for {year}. Updates ship weekly, typically on Thursdays.\n"
            "---\n\n"
            "Submit bugs and feature requests on our [GitHub board!](https://github.com/warpdotdev/Warp/issues/new/choose)\n\n"
        )
        existing_body = ""
        cutoff_date = None

    entries = _new_entries(stable_changelogs=stable_changelogs, cutoff_date=cutoff_date)
    if entries:
        merged_body = "".join(entries)
        if existing_body.strip():
            merged_body = merged_body.rstrip() + "\n\n" + existing_body.lstrip()
    else:
        merged_body = existing_body

    final_content = intro.rstrip() + "\n\n"
    if merged_body.strip():
        final_content += merged_body.rstrip() + "\n"

    if args.dry_run:
        eprint(
            f"[dry-run] Would write {output_file} with {len(entries)} new entr"
            f"{'y' if len(entries) == 1 else 'ies'}.",
        )
    else:
        output_file.write_text(final_content, encoding="utf-8")
        eprint(f"Wrote changelog file: {output_file}")

    index_file = docs_root / "src/content/docs/changelog/index.mdx"
    if created_new_file:
        _ensure_year_in_changelog_index(
            index_file=index_file,
            year=year,
            dry_run=args.dry_run,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

