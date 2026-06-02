#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime
from datetime import timezone
from pathlib import Path
from typing import Any
from urllib.request import Request
from urllib.request import urlopen

USER_AGENT = "Mozilla/5.0 (release-updates-skill)"
DEFAULT_WORK_DIR = Path("/tmp/release-updates")
DEFAULT_ONCALL_RESOLVER_SCRIPT = (
    Path(__file__).resolve().parent / "resolve_oncall_reviewers.py"
).resolve()


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def utc_now_iso() -> str:
    return datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat()


def script_dir() -> Path:
    return Path(__file__).resolve().parent


def docs_repo_root(explicit_docs_repo: str | None = None) -> Path:
    if explicit_docs_repo:
        docs_root = Path(explicit_docs_repo).expanduser().resolve()
        if not docs_root.exists():
            raise FileNotFoundError(
                f"--docs-repo path does not exist: {docs_root}",
            )
        return docs_root

    for parent in Path(__file__).resolve().parents:
        if (parent / "package.json").exists() and (parent / "src/content/docs").exists():
            return parent

    # Fallback for unexpected layout:
    return Path(__file__).resolve().parents[4]


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def read_json_file(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object at {path}")
    return data


def write_json_file(path: Path, payload: dict[str, Any]) -> None:
    ensure_parent_dir(path=path)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def load_json_from_url(url: str) -> dict[str, Any]:
    request = Request(url=url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:  # nosec B310
        payload = json.load(response)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object from {url}")
    return payload


def resolve_channel_versions_file(
    docs_root: Path,
    explicit_file: str | None = None,
    explicit_repo: str | None = None,
) -> Path | None:
    candidates: list[Path] = []

    if explicit_file:
        candidates.append(Path(explicit_file).expanduser().resolve())

    if explicit_repo:
        repo_path = Path(explicit_repo).expanduser().resolve()
        candidates.extend(
            [
                repo_path / "channel_versions.json",
                repo_path / "channel-versions" / "channel_versions.json",
            ],
        )

    candidates.extend(
        [
            docs_root / "channel_versions.json",
            docs_root / "channel-versions" / "channel_versions.json",
            docs_root.parent / "channel-versions" / "channel_versions.json",
            docs_root.parent / "channel_versions" / "channel_versions.json",
            Path("/channel-versions/channel_versions.json"),
            Path("/channel_versions/channel_versions.json"),
            docs_root.parent.parent / "channel-versions" / "channel_versions.json",
            docs_root.parent.parent / "channel_versions" / "channel_versions.json",
            docs_root.parent / "src/channel-versions/channel_versions.json",
        ],
    )

    seen: set[Path] = set()
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if resolved.exists():
            return resolved
    return None


def sanitize_table_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", "<br/>").strip()

