#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from common import DEFAULT_WORK_DIR
from common import eprint

TASK_ORDER = ["warp_app_update", "changelog", "licenses", "telemetry"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run release update scripts in order, with optional task selection.",
    )
    parser.add_argument(
        "--tasks",
        nargs="+",
        choices=TASK_ORDER,
        default=TASK_ORDER.copy(),
        help="Subset of tasks to run (default: all tasks in order).",
    )
    parser.add_argument(
        "--docs-repo",
        default=None,
        help="Path to docs repo root (auto-detected if omitted).",
    )
    parser.add_argument(
        "--work-dir",
        default=str(DEFAULT_WORK_DIR),
        help=f"Working directory for intermediate artifacts (default: {DEFAULT_WORK_DIR})",
    )
    parser.add_argument(
        "--manifest",
        default=None,
        help="Artifact manifest path (default: <work-dir>/warp_artifacts.json).",
    )
    parser.add_argument(
        "--channel-versions-file",
        default=None,
        help="Path to channel_versions.json for changelog update.",
    )
    parser.add_argument(
        "--channel-versions-repo",
        default=None,
        help="Path to channel-versions repo for changelog update.",
    )
    parser.add_argument(
        "--channel-versions-url",
        default=None,
        help="Fallback URL for channel versions if no local file is found.",
    )
    parser.add_argument(
        "--licenses-file",
        default=None,
        help="Explicit THIRD_PARTY_LICENSES.txt path for licenses update.",
    )
    parser.add_argument(
        "--telemetry-json-file",
        default=None,
        help="Explicit telemetry JSON path for telemetry update.",
    )
    parser.add_argument(
        "--telemetry-command",
        default=None,
        help="Explicit telemetry command string for telemetry update.",
    )
    parser.add_argument(
        "--skip-warp-app-extract",
        action="store_true",
        help="Skip AppImage extraction in warp_app_update (useful for non-Linux local tests).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run all scripts in dry-run mode.",
    )
    return parser.parse_args()


def _run_script(script_path: Path, script_args: list[str]) -> None:
    command = [sys.executable, str(script_path), *script_args]
    eprint(f"Running: {' '.join(command)}")
    subprocess.run(command, check=True)  # nosec B603


def main() -> int:
    args = parse_args()
    selected = set(args.tasks)
    ordered_tasks = [task for task in TASK_ORDER if task in selected]
    scripts_dir = Path(__file__).resolve().parent
    work_dir = Path(args.work_dir).expanduser().resolve()
    manifest_path = (
        Path(args.manifest).expanduser().resolve()
        if args.manifest
        else work_dir / "warp_artifacts.json"
    )

    if not ordered_tasks:
        eprint("No tasks selected.")
        return 0

    for task in ordered_tasks:
        if task == "warp_app_update":
            script_args = [
                "--work-dir",
                str(work_dir),
                "--manifest",
                str(manifest_path),
            ]
            if args.skip_warp_app_extract:
                script_args.append("--skip-extract")
            if args.dry_run:
                script_args.append("--dry-run")
            _run_script(
                script_path=scripts_dir / "update_warp_app.py",
                script_args=script_args,
            )

        elif task == "changelog":
            script_args = []
            if args.docs_repo:
                script_args.extend(["--docs-repo", args.docs_repo])
            if args.channel_versions_file:
                script_args.extend(["--channel-versions-file", args.channel_versions_file])
            if args.channel_versions_repo:
                script_args.extend(["--channel-versions-repo", args.channel_versions_repo])
            if args.channel_versions_url:
                script_args.extend(["--channel-versions-url", args.channel_versions_url])
            if args.dry_run:
                script_args.append("--dry-run")
            _run_script(
                script_path=scripts_dir / "update_changelog.py",
                script_args=script_args,
            )

        elif task == "licenses":
            script_args = [
                "--work-dir",
                str(work_dir),
                "--manifest",
                str(manifest_path),
            ]
            if args.docs_repo:
                script_args.extend(["--docs-repo", args.docs_repo])
            if args.licenses_file:
                script_args.extend(["--licenses-file", args.licenses_file])
            if args.dry_run:
                script_args.append("--dry-run")
            _run_script(
                script_path=scripts_dir / "update_licenses.py",
                script_args=script_args,
            )

        elif task == "telemetry":
            script_args = [
                "--work-dir",
                str(work_dir),
                "--manifest",
                str(manifest_path),
            ]
            if args.docs_repo:
                script_args.extend(["--docs-repo", args.docs_repo])
            if args.telemetry_json_file:
                script_args.extend(["--telemetry-json-file", args.telemetry_json_file])
            if args.telemetry_command:
                script_args.extend(["--telemetry-command", args.telemetry_command])
            if args.dry_run:
                script_args.append("--dry-run")
            _run_script(
                script_path=scripts_dir / "update_telemetry.py",
                script_args=script_args,
            )

    eprint(f"Completed tasks: {', '.join(ordered_tasks)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
