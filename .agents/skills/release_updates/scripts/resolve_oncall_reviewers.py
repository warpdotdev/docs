#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from typing import Any


def chunks(value: str) -> list[str]:
    return [chunk.lower() for chunk in re.findall(r"[a-zA-Z0-9]+", value)]


def contains_all_chunks(haystack: str, needle_chunks: list[str]) -> bool:
    normalized_haystack = haystack.lower()
    return all(chunk in normalized_haystack for chunk in needle_chunks)


def chunks_equal(left: list[str], right: list[str]) -> bool:
    return set(left) == set(right)


_EMAIL_TO_GITHUB: dict[str, str] = {
    "david@warp.dev": "vorporeal",
    "ian@warp.dev": "ianhodge",
    "zach@warp.dev": "zachlloyd",
    "kevin@warp.dev": "kevinyang372",
    "andy@warp.dev": "acarl005",
    "john@warp.dev": "johnarector",
    "ben@warp.dev": "bnavetta",
    "mac@warp.dev": "tpmbenny",
}


def _normalize_username(username: str) -> str:
    if "@" in username:
        return username.split("@", 1)[0]
    return username


def matches_member(
    *,
    gh_login: str,
    gh_name: str,
    grafana_email_local: str,
    grafana_username: str,
) -> bool:
    login = gh_login.lower()
    name = gh_name.lower()
    local = grafana_email_local.lower()
    user = _normalize_username(grafana_username).lower()

    if local and (local in login or local in name):
        return True
    if user and (user in login or user in name):
        return True

    if login and (login in local or (user and login in user)):
        return True

    login_chunks = chunks(gh_login)
    local_chunks = chunks(grafana_email_local)
    user_chunks = chunks(user)

    if not login_chunks:
        return False

    if local_chunks and contains_all_chunks(login, local_chunks):
        return True
    if user_chunks and contains_all_chunks(login, user_chunks):
        return True

    if local and contains_all_chunks(local, login_chunks):
        return True
    if user and contains_all_chunks(user, login_chunks):
        return True

    if local_chunks and chunks_equal(login_chunks, local_chunks):
        return True
    if user_chunks and chunks_equal(login_chunks, user_chunks):
        return True

    return False


def _run_command(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(  # nosec B603
        command,
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


def get_oncall_users(
    *,
    schedule_id: str,
    api_url: str,
    grafana_url: str,
    api_key: str,
) -> list[dict[str, str]]:
    url = f"{api_url}/api/v1/schedules/{schedule_id}/current_oncall/"
    request = urllib.request.Request(
        url=url,
        headers={
            "Authorization": api_key,
            "X-Grafana-URL": grafana_url,
        },
    )
    with urllib.request.urlopen(request) as response:  # nosec B310
        payload = json.loads(response.read())

    users = payload.get("users", [])
    if not isinstance(users, list):
        return []

    normalized: list[dict[str, str]] = []
    for user in users:
        if not isinstance(user, dict):
            continue
        email = str(user.get("email", "")).strip().lower()
        username = str(user.get("username", "")).strip()
        if email or username:
            normalized.append(
                {
                    "email": email,
                    "username": username,
                },
            )
    return normalized


def search_github_email(email: str) -> str | None:
    result = _run_command(
        [
            "gh",
            "api",
            "-X",
            "GET",
            "/search/users",
            "-f",
            f"q={email} in:email",
            "--jq",
            ".items[0].login // empty",
        ],
        check=False,
    )
    if result.returncode != 0:
        return None

    login = result.stdout.strip()
    return login or None


def get_org_members(org: str) -> list[dict[str, Any]]:
    query = (
        '{ organization(login: "'
        + org
        + '") { membersWithRole(first: 100) { nodes { login name } } } }'
    )
    result = _run_command(
        [
            "gh",
            "api",
            "graphql",
            "-f",
            f"query={query}",
            "--jq",
            ".data.organization.membersWithRole.nodes",
        ],
    )
    payload = json.loads(result.stdout)
    if not isinstance(payload, list):
        return []
    members: list[dict[str, Any]] = []
    for item in payload:
        if isinstance(item, dict):
            members.append(item)
    return members


def resolve_user_to_login(
    *,
    user: dict[str, str],
    members: list[dict[str, Any]],
) -> tuple[str | None, dict[str, Any] | None]:
    email = user.get("email", "").lower()
    username = user.get("username", "")

    if email in _EMAIL_TO_GITHUB:
        return _EMAIL_TO_GITHUB[email], None

    if email:
        from_email = search_github_email(email)
        if from_email:
            return from_email, None

    email_local = email.split("@", 1)[0] if "@" in email else email
    matched = sorted(
        {
            str(member.get("login", ""))
            for member in members
            if str(member.get("login", "")).strip()
            and matches_member(
                gh_login=str(member.get("login", "")),
                gh_name=str(member.get("name", "") or ""),
                grafana_email_local=email_local,
                grafana_username=username,
            )
        },
    )

    if len(matched) == 1:
        return matched[0], None

    unresolved = {
        "oncall_email": email,
        "oncall_username": username,
        "matched_candidates": matched,
    }
    return None, unresolved


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Resolve current Grafana on-call users to GitHub reviewers. "
            "By default returns up to two reviewers (primary + secondary)."
        ),
    )
    parser.add_argument("schedule_id", help="Grafana IRM schedule ID")
    parser.add_argument(
        "--max-reviewers",
        type=int,
        default=2,
        help="Maximum number of on-call users to resolve (default: 2).",
    )
    parser.add_argument(
        "--oncall-api-url",
        default=os.environ.get(
            "ONCALL_API_URL",
            "https://oncall-prod-us-central-0.grafana.net/oncall",
        ),
        help="Grafana OnCall API base URL",
    )
    parser.add_argument(
        "--grafana-url",
        default=os.environ.get("GRAFANA_URL", "https://warp.grafana.net"),
        help="Grafana URL for X-Grafana-URL header",
    )
    parser.add_argument(
        "--github-org",
        default=os.environ.get("GITHUB_ORG", "warpdotdev"),
        help="GitHub org used for fuzzy member matching",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    api_key = os.environ.get("GRAFANA_API_KEY")
    if not api_key:
        print("GRAFANA_API_KEY env var required", file=sys.stderr)
        return 1

    users = get_oncall_users(
        schedule_id=args.schedule_id,
        api_url=args.oncall_api_url,
        grafana_url=args.grafana_url,
        api_key=api_key,
    )
    if not users:
        print(
            f"no users currently on-call for schedule {args.schedule_id}",
            file=sys.stderr,
        )
        return 1

    max_reviewers = max(1, int(args.max_reviewers))
    selected_users = users[:max_reviewers]
    members = get_org_members(args.github_org)

    reviewers: list[str] = []
    unresolved_users: list[dict[str, Any]] = []
    for user in selected_users:
        reviewer, unresolved = resolve_user_to_login(
            user=user,
            members=members,
        )
        if reviewer:
            if reviewer not in reviewers:
                reviewers.append(reviewer)
        elif unresolved:
            unresolved_users.append(unresolved)

    if unresolved_users:
        payload = {
            "schedule_id": args.schedule_id,
            "reviewers": reviewers,
            "unresolved_users": unresolved_users,
            "candidates": [
                {
                    "login": str(member.get("login", "")),
                    "name": str(member.get("name", "") or ""),
                }
                for member in members
                if str(member.get("login", "")).strip()
            ],
        }
        print(json.dumps(payload, indent=2))
        return 2

    if not reviewers:
        print(
            "could not resolve any on-call users to GitHub reviewers",
            file=sys.stderr,
        )
        return 1

    print(
        json.dumps(
            {
                "schedule_id": args.schedule_id,
                "reviewers": reviewers,
                "oncall_users": selected_users,
            },
            indent=2,
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
