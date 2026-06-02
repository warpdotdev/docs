#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from common import DEFAULT_ONCALL_RESOLVER_SCRIPT
from common import DEFAULT_WORK_DIR
from common import docs_repo_root
from common import eprint
from common import resolve_channel_versions_file
from common import utc_now_iso
from common import write_json_file

DEFAULT_CHANNEL_VERSIONS_REPO_URL = "https://github.com/warpdotdev/channel-versions.git"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Preflight and optionally bootstrap repositories + credentials for "
            "release_updates skill runs."
        ),
    )
    parser.add_argument(
        "--docs-repo",
        default=None,
        help="Path to docs repo root (auto-detected if omitted).",
    )
    parser.add_argument(
        "--channel-versions-repo",
        default=None,
        help=(
            "Path to a local channel-versions checkout. "
            "If omitted, auto-detection is used."
        ),
    )
    parser.add_argument(
        "--channel-versions-url",
        default=DEFAULT_CHANNEL_VERSIONS_REPO_URL,
        help=(
            "Git clone URL for channel-versions repo when "
            "--clone-channel-versions-if-missing is set."
        ),
    )
    parser.add_argument(
        "--clone-channel-versions-if-missing",
        action="store_true",
        help=(
            "Clone channel-versions repo if not detected locally "
            "(target: --channel-versions-repo or sibling directory)."
        ),
    )
    parser.add_argument(
        "--require-local-channel-versions",
        action="store_true",
        help="Fail if local channel_versions.json is not present.",
    )
    parser.add_argument(
        "--require-pr-flow",
        action="store_true",
        help=(
            "Validate PR prerequisites (gh CLI availability + authenticated session)."
        ),
    )
    parser.add_argument(
        "--require-oncall-reviewer",
        action="store_true",
        help=(
            "Validate on-call reviewer prerequisites "
            "(resolver script + GRAFANA_API_KEY)."
        ),
    )
    parser.add_argument(
        "--oncall-resolver-script",
        default=str(DEFAULT_ONCALL_RESOLVER_SCRIPT),
        help=(
            "Path to local on-call reviewer resolver script "
            f"(default: {DEFAULT_ONCALL_RESOLVER_SCRIPT})."
        ),
    )
    parser.add_argument(
        "--report-file",
        default=None,
        help=(
            "Where to write environment report JSON "
            "(default: <work-dir>/environment_report.json)."
        ),
    )
    parser.add_argument(
        "--work-dir",
        default=str(DEFAULT_WORK_DIR),
        help=f"Working directory for generated setup artifacts (default: {DEFAULT_WORK_DIR})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without cloning repositories.",
    )
    return parser.parse_args()


def _run_command(
    command: list[str],
    *,
    cwd: Path | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(  # nosec B603
        command,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        stderr_or_stdout = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(
            "Command failed "
            f"({' '.join(command)}):\n"
            f"{stderr_or_stdout}",
        )
    return result


def _clone_repo(
    *,
    repo_url: str,
    destination: Path,
    dry_run: bool,
) -> None:
    if destination.exists():
        return

    if dry_run:
        eprint(f"[dry-run] Would clone {repo_url} -> {destination}")
        return

    destination.parent.mkdir(parents=True, exist_ok=True)
    _run_command(
        ["git", "clone", repo_url, str(destination)],
        check=True,
    )
    eprint(f"Cloned repository: {destination}")


def _gh_authenticated() -> tuple[bool, str]:
    result = _run_command(
        ["gh", "auth", "status"],
        check=False,
    )
    details = result.stderr.strip() or result.stdout.strip()
    if result.returncode == 0:
        return True, details

    normalized = details.lower()
    if "active account: true" in normalized and "timeout trying to log in" in normalized:
        return True, details

    return False, details


def main() -> int:
    args = parse_args()
    docs_root = docs_repo_root(explicit_docs_repo=args.docs_repo)
    work_dir = Path(args.work_dir).expanduser().resolve()
    report_path = (
        Path(args.report_file).expanduser().resolve()
        if args.report_file
        else work_dir / "environment_report.json"
    )

    errors: list[str] = []
    warnings: list[str] = []
    checks: dict[str, Any] = {
        "commands": {},
        "gh_authenticated": None,
        "grafana_api_key_present": None,
        "oncall_resolver_exists": None,
        "local_channel_versions_present": None,
    }

    required_commands = ["python3", "git"]
    if args.require_pr_flow:
        required_commands.append("gh")

    for command_name in required_commands:
        available = shutil.which(command_name) is not None
        checks["commands"][command_name] = available
        if not available:
            errors.append(f"Missing required command: {command_name}")

    channel_versions_repo_path = (
        Path(args.channel_versions_repo).expanduser().resolve()
        if args.channel_versions_repo
        else docs_root.parent / "channel-versions"
    )
    channel_versions_file = resolve_channel_versions_file(
        docs_root=docs_root,
        explicit_repo=args.channel_versions_repo,
    )

    if channel_versions_file is None and args.clone_channel_versions_if_missing:
        _clone_repo(
            repo_url=args.channel_versions_url,
            destination=channel_versions_repo_path,
            dry_run=args.dry_run,
        )
        channel_versions_file = resolve_channel_versions_file(
            docs_root=docs_root,
            explicit_repo=str(channel_versions_repo_path),
        )

    checks["local_channel_versions_present"] = channel_versions_file is not None
    if channel_versions_file is None:
        message = (
            "Local channel_versions.json not found. "
            "Changelog updates can still run using URL fallback."
        )
        if args.require_local_channel_versions and not (
            args.dry_run and args.clone_channel_versions_if_missing
        ):
            errors.append(message)
        else:
            warnings.append(message)

    if args.require_pr_flow and checks["commands"].get("gh"):
        gh_ok, gh_details = _gh_authenticated()
        checks["gh_authenticated"] = gh_ok
        if not gh_ok:
            errors.append(
                "GitHub CLI is not authenticated. Run `gh auth login` before PR mode.",
            )
            if gh_details:
                warnings.append(gh_details)
        elif gh_details and "timeout trying to log in" in gh_details.lower():
            warnings.append(
                "gh auth status reported a keyring timeout but Active account is true; "
                "continuing.",
            )

    resolver_path = Path(args.oncall_resolver_script).expanduser().resolve()

    checks["oncall_resolver_exists"] = resolver_path.exists()
    if args.require_oncall_reviewer and not resolver_path.exists():
        errors.append(
            "On-call resolver script not found at "
            f"{resolver_path}. Pass --oncall-resolver-script.",
        )

    grafana_api_key_present = bool(os.environ.get("GRAFANA_API_KEY"))
    checks["grafana_api_key_present"] = grafana_api_key_present
    if args.require_oncall_reviewer and not grafana_api_key_present:
        errors.append("Missing required env var for reviewer assignment: GRAFANA_API_KEY")

    report: dict[str, Any] = {
        "generated_at_utc": utc_now_iso(),
        "docs_repo": str(docs_root),
        "channel_versions_repo": str(channel_versions_repo_path),
        "channel_versions_file": str(channel_versions_file) if channel_versions_file else None,
        "oncall_resolver_script": str(resolver_path),
        "checks": checks,
        "warnings": warnings,
        "errors": errors,
        "dry_run": args.dry_run,
    }

    if args.dry_run:
        eprint(f"[dry-run] Would write setup report: {report_path}")
    else:
        write_json_file(path=report_path, payload=report)
        eprint(f"Wrote setup report: {report_path}")

    if warnings:
        for warning in warnings:
            eprint(f"WARNING: {warning}")

    if errors:
        for error in errors:
            eprint(f"ERROR: {error}")
        raise RuntimeError("Environment setup checks failed.")

    eprint("Environment setup checks passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        eprint(f"ERROR: {exc}")
        raise SystemExit(1) from exc
