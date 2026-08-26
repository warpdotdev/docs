#!/usr/bin/env python3
"""Release gate for the missing_docs drift-watch agent.

The drift-watch schedule runs daily so it can pick up a stable release whenever it
lands -- release timing is deliberately flexible (Thursday evening, Friday morning).
But the triage work should happen once per release, not once per day. This script is
the gate that makes a daily schedule behave like a per-release trigger.

Exit codes:
    0   A new stable release is available. Continue the run.
    10  No new release since the last processed version. Stop; this is a normal no-op.
    1   Could not determine the current release (network, HTTP, or parse failure).
        Stop and report -- do NOT treat this as "nothing shipped".

Usage:
    check_new_release.py                 Check and report. Does not write state.
    check_new_release.py --commit        Record the current release as processed.
    check_new_release.py --json          Machine-readable output.
    check_new_release.py --state PATH    Override the state file location.

The check and the commit are deliberately separate. The agent checks at the start of a
run and commits only after triage succeeds, so a run that crashes mid-triage retries the
same release on the next day instead of silently skipping it.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CLIENT_VERSION_URL = "https://app.warp.dev/client_version?include_changelogs=true"
DEFAULT_STATE_PATH = (
    Path(__file__).resolve().parent.parent / "references" / "last_release_processed.json"
)
FETCH_TIMEOUT_SECONDS = 30

EXIT_NEW_RELEASE = 0
EXIT_FETCH_FAILED = 1
EXIT_NO_NEW_RELEASE = 10


def fetch_current_stable() -> tuple[str, str | None, dict]:
    """Return (version, release_date, changelog) for the current stable release.

    Raises RuntimeError with an actionable message on any failure. The caller must not
    swallow this into a no-op -- a fetch failure is not evidence that nothing shipped.
    """
    try:
        with urllib.request.urlopen(CLIENT_VERSION_URL, timeout=FETCH_TIMEOUT_SECONDS) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code} fetching {CLIENT_VERSION_URL}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not reach {CLIENT_VERSION_URL}: {exc.reason}") from exc
    except (TimeoutError, OSError) as exc:
        raise RuntimeError(f"Network failure fetching {CLIENT_VERSION_URL}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Response from {CLIENT_VERSION_URL} was not valid JSON: {exc}") from exc

    try:
        version = payload["stable"]["version"]
    except (KeyError, TypeError) as exc:
        raise RuntimeError(
            "Response is missing stable.version -- the client_version payload shape "
            "may have changed."
        ) from exc

    if not isinstance(version, str) or not version:
        raise RuntimeError(f"stable.version was not a usable string: {version!r}")

    changelog = payload.get("changelogs", {}).get("stable", {}).get(version, {})
    if not isinstance(changelog, dict):
        changelog = {}

    return version, changelog.get("date"), changelog


def read_state(state_path: Path) -> dict:
    """Read the state file. A missing or unreadable file means 'never processed'."""
    if not state_path.exists():
        return {}
    try:
        with state_path.open(encoding="utf-8") as handle:
            state = json.load(handle)
    except (json.JSONDecodeError, OSError) as exc:
        print(
            f"warning: could not read state file {state_path} ({exc}); "
            "treating this release as unprocessed",
            file=sys.stderr,
        )
        return {}
    return state if isinstance(state, dict) else {}


def write_state(state_path: Path, version: str, release_date: str | None, changelog: dict) -> None:
    """Record the processed release, with enough context to debug a stuck gate."""
    entry_count = sum(
        len([line for line in section.get("markdown", "").splitlines() if line.strip().startswith("*")])
        for section in changelog.get("markdown_sections", [])
        if isinstance(section, dict)
    )
    state = {
        "last_processed_version": version,
        "release_date": release_date,
        "processed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "changelog_entry_count": entry_count,
        "oz_updates_count": len(changelog.get("oz_updates", []) or []),
        "_comment": (
            "Written by check_new_release.py --commit after a drift-watch run completes "
            "triage. Kept separate from surface_snapshot.json, which is regenerated "
            "wholesale and would lose this marker. Do not hand-edit; to force a re-run "
            "of the current release, delete this file."
        ),
    }
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with state_path.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)
        handle.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gate the drift-watch run on a new stable release.",
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Record the current stable release as processed. Run this only after triage succeeds.",
    )
    parser.add_argument(
        "--state",
        type=Path,
        default=DEFAULT_STATE_PATH,
        help=f"Path to the state file (default: {DEFAULT_STATE_PATH}).",
    )
    parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="Emit machine-readable JSON instead of prose.",
    )
    args = parser.parse_args()

    try:
        version, release_date, changelog = fetch_current_stable()
    except RuntimeError as exc:
        message = f"Release check failed: {exc}"
        if args.as_json:
            print(json.dumps({"status": "error", "error": str(exc)}, indent=2))
        else:
            print(message, file=sys.stderr)
            print(
                "Stopping. A failed check is not the same as 'no new release' -- "
                "do not continue as if nothing shipped.",
                file=sys.stderr,
            )
        return EXIT_FETCH_FAILED

    state = read_state(args.state)
    last_processed = state.get("last_processed_version")
    is_new = version != last_processed

    if args.commit:
        write_state(args.state, version, release_date, changelog)
        if args.as_json:
            print(
                json.dumps(
                    {
                        "status": "committed",
                        "version": version,
                        "release_date": release_date,
                        "state_file": str(args.state),
                    },
                    indent=2,
                )
            )
        else:
            print(f"Recorded {version} as processed in {args.state}")
        return EXIT_NEW_RELEASE

    # `oz_updates` is a separate array in the client_version payload, not part
    # of the markdown changelog the audit parses. The audit is offline by
    # design and never sees it, so this is the only place those bullets surface
    # — print the content, not just a count, or the skill's instruction to
    # triage them cannot be carried out. The field name is the API's, and stays
    # `oz_updates` regardless of product naming.
    oz_updates = changelog.get("oz_updates", []) or []

    if args.as_json:
        print(
            json.dumps(
                {
                    "status": "new_release" if is_new else "no_new_release",
                    "current_version": version,
                    "last_processed_version": last_processed,
                    "release_date": release_date,
                    "oz_updates_count": len(oz_updates),
                    "oz_updates": oz_updates,
                },
                indent=2,
            )
        )
    elif is_new:
        previous = last_processed or "(none recorded)"
        print(f"New stable release: {version}")
        print(f"  Released:        {release_date or 'unknown'}")
        print(f"  Last processed:  {previous}")
        print(f"  Oz updates:      {len(oz_updates)}")
        for bullet in oz_updates:
            print(f"    - {bullet}")
        if oz_updates:
            print(
                "  These are platform-side changes the audit cannot see. "
                "Triage them against the worthiness criteria like changelog bullets."
            )
        print("Proceed with the audit.")
    else:
        print(f"No new release. Current stable {version} was already processed.")
        print("This is a normal no-op. Record the outcome and stop.")

    return EXIT_NEW_RELEASE if is_new else EXIT_NO_NEW_RELEASE


if __name__ == "__main__":
    sys.exit(main())
