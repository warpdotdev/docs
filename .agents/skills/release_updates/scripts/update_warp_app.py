#!/usr/bin/env python3
from __future__ import annotations

import argparse
import platform
import subprocess
from pathlib import Path
from typing import Any
from urllib.request import Request
from urllib.request import urlopen

from common import DEFAULT_WORK_DIR
from common import USER_AGENT
from common import eprint
from common import utc_now_iso
from common import write_json_file

APP_DOWNLOAD_CONFIG = {
    "stable": {
        "channel": "stable",
        "package_x86_64": "appimage",
        "package_arm64": "appimage_arm64",
    },
    "preview": {
        "channel": "preview",
        "package_x86_64": "appimage",
        "package_arm64": "appimage_arm64",
    },
}


def _detect_arch() -> str:
    machine = platform.machine().lower()
    if machine in {"aarch64", "arm64"}:
        return "arm64"
    return "x86_64"


def _download_url(package_name: str, channel: str) -> str:
    if channel == "preview":
        return f"https://app.warp.dev/download?package={package_name}&channel=preview"
    return f"https://app.warp.dev/download?package={package_name}"


def _download_file(url: str, output_path: Path, dry_run: bool) -> str | None:
    if dry_run:
        eprint(f"[dry-run] Would download: {url} -> {output_path}")
        return None

    output_path.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url=url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=180) as response:  # nosec B310
        resolved_url = response.geturl()
        with output_path.open("wb") as handle:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                handle.write(chunk)
    output_path.chmod(0o755)
    return resolved_url


def _extract_appimage(appimage_path: Path, destination_dir: Path, dry_run: bool) -> Path | None:
    if dry_run:
        eprint(f"[dry-run] Would extract AppImage: {appimage_path}")
        return None

    destination_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(  # nosec B603
        [str(appimage_path), "--appimage-extract"],
        cwd=destination_dir,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    extracted_root = destination_dir / "squashfs-root"
    if not extracted_root.exists():
        return None
    return extracted_root


def _find_file(root: Path, filename: str) -> Path | None:
    for candidate in root.rglob(filename):
        if candidate.is_file():
            return candidate
    return None


def _build_telemetry_command(appimage_path: Path) -> list[str]:
    return [
        str(appimage_path),
        "--appimage-extract-and-run",
        "--print-telemetry-events",
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download and prepare latest Warp Linux artifacts for release docs updates.",
    )
    parser.add_argument(
        "--work-dir",
        default=str(DEFAULT_WORK_DIR),
        help=f"Working directory for downloaded artifacts (default: {DEFAULT_WORK_DIR})",
    )
    parser.add_argument(
        "--manifest",
        default=None,
        help="Path to write artifact manifest JSON (default: <work-dir>/warp_artifacts.json)",
    )
    parser.add_argument(
        "--apps",
        nargs="+",
        choices=["stable", "preview"],
        default=["stable", "preview"],
        help="Which app channels to prepare",
    )
    parser.add_argument(
        "--skip-extract",
        action="store_true",
        help="Skip AppImage extraction even on Linux.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without downloading or extracting.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    work_dir = Path(args.work_dir).expanduser().resolve()
    manifest_path = (
        Path(args.manifest).expanduser().resolve()
        if args.manifest
        else work_dir / "warp_artifacts.json"
    )

    arch = _detect_arch()
    is_linux = platform.system() == "Linux"
    should_extract = is_linux and not args.skip_extract
    if not is_linux and not args.skip_extract:
        eprint(
            "Non-Linux system detected; extraction is skipped by default. "
            "Use Linux/Oz for full extraction + telemetry/license discovery.",
        )

    manifest: dict[str, Any] = {
        "generated_at_utc": utc_now_iso(),
        "platform": platform.platform(),
        "system": platform.system(),
        "arch": arch,
        "work_dir": str(work_dir),
        "apps": {},
    }

    for app_name in args.apps:
        config = APP_DOWNLOAD_CONFIG[app_name]
        package_key = "package_arm64" if arch == "arm64" else "package_x86_64"
        package_name = config[package_key]
        channel = config["channel"]
        download_url = _download_url(package_name=package_name, channel=channel)

        app_dir = work_dir / app_name
        artifact_path = app_dir / f"{app_name}.AppImage"
        eprint(f"Preparing {app_name}: {download_url}")
        resolved_url = _download_file(
            url=download_url,
            output_path=artifact_path,
            dry_run=args.dry_run,
        )

        extracted_root: Path | None = None
        licenses_path: Path | None = None
        if should_extract and not args.dry_run:
            extracted_root = _extract_appimage(
                appimage_path=artifact_path,
                destination_dir=app_dir / "extracted",
                dry_run=False,
            )
            if extracted_root:
                licenses_path = _find_file(
                    root=extracted_root,
                    filename="THIRD_PARTY_LICENSES.txt",
                )

        manifest["apps"][app_name] = {
            "channel": channel,
            "package": package_name,
            "download_url": download_url,
            "resolved_url": resolved_url,
            "artifact_path": str(artifact_path),
            "extracted_dir": str(extracted_root) if extracted_root else None,
            "third_party_licenses_path": str(licenses_path) if licenses_path else None,
            "telemetry_command": (
                _build_telemetry_command(appimage_path=artifact_path)
                if app_name == "preview"
                else None
            ),
        }

    if args.dry_run:
        eprint(f"[dry-run] Would write manifest: {manifest_path}")
    else:
        write_json_file(path=manifest_path, payload=manifest)
        eprint(f"Wrote manifest: {manifest_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

