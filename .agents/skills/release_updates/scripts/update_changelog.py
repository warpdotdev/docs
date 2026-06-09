#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from datetime import datetime
from datetime import timezone
from html import escape
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from common import docs_repo_root
from common import eprint
from common import load_json_from_url
from common import resolve_channel_versions_file

DEFAULT_CHANNEL_VERSIONS_URL = "https://releases.warp.dev/channel_versions.json"
RE_CHANGELOG_DATE = re.compile(r"^### (\d{4}\.\d{2}\.\d{2})\s", re.MULTILINE)
RE_BARE_CURLY_PATTERN = re.compile(
    r"(?<!`)(\S*\{[^}]+\}\S*)(?!`)",
)
RE_SLASH_COMMAND = re.compile(r"(?<![`\w/])(/[a-z][a-z0-9-]+)(?![`\w/])")
RE_CLI_FLAG = re.compile(r"(?<![`\w-])(--[a-z][a-z0-9-]*)(?![`\w-])")
RE_FIXES_TENSE = re.compile(r"^(\* )Fixes ", re.MULTILINE)


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


def _ensure_year_in_sidebar(sidebar_file: Path, year: int, dry_run: bool) -> bool:
    if not sidebar_file.exists():
        return False

    content = sidebar_file.read_text(encoding="utf-8")
    updated = content
    changed = False

    year_item_pattern = re.compile(
        rf"(?m)^\s*\{{ slug: 'changelog/{year}', label: '{year}' \}},$",
    )
    if not year_item_pattern.search(updated):
        all_years_match = re.search(
            r"(?m)^(\s*)\{ slug: 'changelog', label: 'All years' \},$",
            updated,
        )
        if all_years_match:
            indent = all_years_match.group(1)
            insertion = f"\n{indent}{{ slug: 'changelog/{year}', label: '{year}' }},"
            updated = (
                updated[: all_years_match.end()]
                + insertion
                + updated[all_years_match.end() :]
            )
            changed = True

    desired_link = f"/changelog/{year}/"
    if desired_link not in updated:
        updated, link_count = re.subn(
            r"(label:\s*'Changelog',\s*\n\s*link:\s*'/changelog/)\d{4}(/',)",
            rf"\g<1>{year}\g<2>",
            updated,
            count=1,
        )
        if link_count > 0:
            changed = True

    if not changed:
        return False

    if dry_run:
        eprint(f"[dry-run] Would update changelog sidebar year navigation in {sidebar_file}")
    else:
        sidebar_file.write_text(updated, encoding="utf-8")
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


def _normalize_changelog_prose(text: str) -> str:
    normalized = RE_FIXES_TENSE.sub(r"\1Fixed ", text)
    parts: list[str] = re.split(r"(`[^`]+`)", normalized)
    output: list[str] = []
    for part in parts:
        if part.startswith("`") and part.endswith("`"):
            output.append(part)
            continue
        candidate = RE_SLASH_COMMAND.sub(r"`\1`", part)
        candidate = RE_CLI_FLAG.sub(r"`\1`", candidate)
        output.append(candidate)
    return "".join(output)


def _wrap_curly_braces_in_backticks(text: str) -> str:
    parts: list[str] = re.split(r"(`[^`]+`)", text)
    output: list[str] = []
    for part in parts:
        if part.startswith("`") and part.endswith("`"):
            output.append(part)
            continue
        output.append(RE_BARE_CURLY_PATTERN.sub(r"`\1`", part))
    return "".join(output)


def _sanitize_image_url(image_url: Any) -> str | None:
    if not isinstance(image_url, str):
        return None
    candidate = image_url.strip()
    if not candidate:
        return None
    parsed = urlparse(candidate)
    if parsed.scheme != "https" or not parsed.netloc:
        return None
    return candidate


def _render_entry(version_key: str, changelog: dict[str, Any]) -> str:
    display_date = _parse_datetime(str(changelog["date"])).strftime("%Y.%m.%d")
    display_version = _display_version(version_key=version_key)
    lines: list[str] = [f"### {display_date} ({display_version})", ""]
    image_url = _sanitize_image_url(changelog.get("image_url"))
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
        if title == "New features" and image_url:
            safe_image_url = escape(image_url, quote=True)
            safe_alt_text = escape(f"Release image for {display_date}", quote=True)
            lines.append(
                f"<figure><img src=\"{safe_image_url}\" alt=\"{safe_alt_text}\"><figcaption></figcaption></figure>",
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

    rendered = "\n".join(lines).rstrip() + "\n"
    rendered = _normalize_changelog_prose(text=rendered)
    rendered = _wrap_curly_braces_in_backticks(text=rendered)
    return rendered


def _new_entries(
    stable_changelogs: dict[str, Any],
    cutoff_date: str | None,
    year: int,
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
        if parsed_date.astimezone(timezone.utc).year != year:
            continue
        display_date = parsed_date.strftime("%Y.%m.%d")
        if cutoff_date is not None and display_date <= cutoff_date:
            continue
        if display_date in seen_dates:
            continue
        seen_dates.add(display_date)
        entries.append(_render_entry(version_key=version_key, changelog=payload))
    return entries


def _normalize_changelog_body(body: str) -> str:
    if not body.strip():
        return body
    first_entry = RE_CHANGELOG_DATE.search(body)
    if not first_entry:
        return body
    next_entry = RE_CHANGELOG_DATE.search(body, first_entry.end())
    if next_entry:
        latest_entry_block = body[: next_entry.start()]
        remaining_body = body[next_entry.start() :]
    else:
        latest_entry_block = body
        remaining_body = ""
    normalized_latest_entry = _normalize_changelog_prose(text=latest_entry_block)
    normalized_latest_entry = _wrap_curly_braces_in_backticks(
        text=normalized_latest_entry,
    )
    if remaining_body:
        return normalized_latest_entry.rstrip() + "\n\n" + remaining_body.lstrip("\n")
    return normalized_latest_entry


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

    entries = _new_entries(
        stable_changelogs=stable_changelogs,
        cutoff_date=cutoff_date,
        year=year,
    )
    if entries:
        merged_body = "".join(entries)
        if existing_body.strip():
            merged_body = merged_body.rstrip() + "\n\n" + existing_body.lstrip()
    else:
        merged_body = existing_body
    merged_body = _normalize_changelog_body(body=merged_body)

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
    sidebar_file = docs_root / "src/sidebar.ts"
    if created_new_file:
        _ensure_year_in_changelog_index(
            index_file=index_file,
            year=year,
            dry_run=args.dry_run,
        )
        _ensure_year_in_sidebar(
            sidebar_file=sidebar_file,
            year=year,
            dry_run=args.dry_run,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

