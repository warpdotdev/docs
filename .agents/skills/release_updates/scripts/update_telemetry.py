#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from pathlib import Path
from typing import Any

from common import DEFAULT_WORK_DIR
from common import docs_repo_root
from common import eprint
from common import read_json_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Regenerate privacy.mdx telemetry table from telemetry JSON.",
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
        help="Artifact manifest path (default: <work-dir>/warp_artifacts.json).",
    )
    parser.add_argument(
        "--telemetry-json-file",
        default=None,
        help="Use an existing telemetry JSON file instead of running a command.",
    )
    parser.add_argument(
        "--telemetry-command",
        default=None,
        help="Command string that prints telemetry JSON to stdout.",
    )
    parser.add_argument(
        "--telemetry-output-file",
        default=None,
        help="Where to store fetched telemetry JSON (default: <work-dir>/telemetry.json).",
    )
    parser.add_argument(
        "--output-file",
        default=None,
        help="Output privacy doc path (default: docs privacy path).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute and print summary without writing files.",
    )
    return parser.parse_args()


# Keep this in sync with the heading emitted by `_table_markdown`. The heading is
# matched literally to find where the generated table starts, so renaming it in
# privacy.mdx without updating it here makes the whole file look like intro and
# appends a duplicate table on the next run.
TELEMETRY_TABLE_HEADING = "### Exhaustive telemetry table"


def _extract_intro(content: str) -> str:
    marker = f"\n{TELEMETRY_TABLE_HEADING}"
    index = content.find(marker)
    if index == -1:
        return content.rstrip() + "\n"
    return content[:index].rstrip() + "\n"


def _table_markdown(events: dict[str, Any]) -> str:
    lines: list[str] = [
        TELEMETRY_TABLE_HEADING,
        "",
        "| Event Name | Description |",
        "|---|---|",
    ]
    for event_name, event_description in events.items():
        event_name_text = str(event_name).strip()
        if event_description is None:
            event_description_text = ""
        else:
            event_description_text = str(event_description).rstrip()
        lines.append(f"| `{event_name_text}` | {event_description_text} |")
    lines.append("")
    lines.append("")
    return "\n".join(lines)


def _events_from_manifest(manifest_path: Path) -> tuple[list[str] | None, Path | None]:
    if not manifest_path.exists():
        return None, None
    manifest = read_json_file(path=manifest_path)
    apps = manifest.get("apps", {})
    if not isinstance(apps, dict):
        return None, None
    preview = apps.get("preview", {})
    if not isinstance(preview, dict):
        return None, None

    telemetry_command = preview.get("telemetry_command")
    command_list: list[str] | None = None
    if isinstance(telemetry_command, list) and all(
        isinstance(item, str) for item in telemetry_command
    ):
        command_list = list(telemetry_command)

    telemetry_json_path: Path | None = None
    telemetry_json_value = preview.get("telemetry_json_path")
    if isinstance(telemetry_json_value, str) and telemetry_json_value.strip():
        candidate = Path(telemetry_json_value).expanduser().resolve()
        if candidate.exists():
            telemetry_json_path = candidate
    return command_list, telemetry_json_path


def _load_events_from_file(path: Path) -> dict[str, Any]:
    payload = read_json_file(path=path)
    return payload


def _run_telemetry_command(command: list[str]) -> dict[str, Any]:
    result = subprocess.run(  # nosec B603
        command,
        check=True,
        capture_output=True,
        text=True,
        timeout=180,
    )
    payload = json.loads(result.stdout)
    if not isinstance(payload, dict):
        raise ValueError("Telemetry command did not return a JSON object.")
    return payload


def main() -> int:
    args = parse_args()
    docs_root = docs_repo_root(explicit_docs_repo=args.docs_repo)
    work_dir = Path(args.work_dir).expanduser().resolve()
    manifest_path = (
        Path(args.manifest).expanduser().resolve()
        if args.manifest
        else work_dir / "warp_artifacts.json"
    )

    output_privacy_file = (
        Path(args.output_file).expanduser().resolve()
        if args.output_file
        else docs_root
        / "src/content/docs/support-and-community/privacy-and-security/privacy.mdx"
    )
    telemetry_output_file = (
        Path(args.telemetry_output_file).expanduser().resolve()
        if args.telemetry_output_file
        else work_dir / "telemetry.json"
    )

    manifest_command, manifest_telemetry_json = _events_from_manifest(
        manifest_path=manifest_path,
    )

    events: dict[str, Any] | None = None
    source_description = ""

    if args.telemetry_json_file:
        telemetry_json_path = Path(args.telemetry_json_file).expanduser().resolve()
        if not telemetry_json_path.exists():
            raise FileNotFoundError(f"--telemetry-json-file not found: {telemetry_json_path}")
        events = _load_events_from_file(path=telemetry_json_path)
        source_description = str(telemetry_json_path)
    elif manifest_telemetry_json is not None:
        events = _load_events_from_file(path=manifest_telemetry_json)
        source_description = str(manifest_telemetry_json)
    else:
        command: list[str] | None = None
        if args.telemetry_command:
            command = shlex.split(args.telemetry_command)
        elif manifest_command:
            command = manifest_command

        if command:
            if args.dry_run:
                eprint(
                    "[dry-run] Would execute telemetry command: "
                    f"{shlex.join(command)}",
                )
                eprint(
                    f"[dry-run] Would write telemetry JSON file: {telemetry_output_file}",
                )
                eprint(
                    f"[dry-run] Would write {output_privacy_file} "
                    "from telemetry command output.",
                )
                return 0
            events = _run_telemetry_command(command=command)
            source_description = "telemetry command output"
            if args.dry_run:
                eprint(
                    f"[dry-run] Would write telemetry JSON file: {telemetry_output_file}",
                )
            else:
                telemetry_output_file.parent.mkdir(parents=True, exist_ok=True)
                telemetry_output_file.write_text(
                    json.dumps(events, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
        elif telemetry_output_file.exists():
            events = _load_events_from_file(path=telemetry_output_file)
            source_description = str(telemetry_output_file)

    if events is None:
        if args.dry_run:
            eprint(
                "[dry-run] No telemetry source available from manifest, "
                "--telemetry-command, --telemetry-json-file, or telemetry.json.",
            )
            eprint(
                f"[dry-run] Would write {output_privacy_file} "
                "once telemetry source input is available.",
            )
            return 0
        raise RuntimeError(
            "No telemetry source available. "
            "Run update_warp_app.py first, pass --telemetry-command, "
            "or pass --telemetry-json-file.",
        )

    existing_privacy = output_privacy_file.read_text(encoding="utf-8")
    intro = _extract_intro(content=existing_privacy)
    telemetry_section = _table_markdown(events=events)
    final_output = intro.rstrip() + "\n\n" + telemetry_section

    if args.dry_run:
        eprint(
            f"[dry-run] Would write {output_privacy_file} with {len(events)} telemetry rows "
            f"from {source_description}.",
        )
    else:
        output_privacy_file.write_text(final_output, encoding="utf-8")
        eprint(f"Wrote telemetry doc: {output_privacy_file}")
        eprint(f"Telemetry source: {source_description}")
        eprint(f"Telemetry rows written: {len(events)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

