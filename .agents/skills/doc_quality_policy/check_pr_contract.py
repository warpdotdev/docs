#!/usr/bin/env python3
"""CI-callable checker for the agent-doc quality PR contract.

Wraps `policy.py` with the I/O CI needs: reading a PR body file, discovering
`{/* VERIFY: ... */}` markers in the changed docs files, and optionally taking
live signals (head SHA, review outcome, deterministic-check result) as flags
so this stays callable from a GitHub Actions step without a live `gh` call
baked into the checker itself.

Usage:
    python3 check_pr_contract.py --body /tmp/pr-body.md [changed_file ...]
    python3 check_pr_contract.py --body /tmp/pr-body.md \\
        --repo owner/repo --pr 123 --head-sha "$HEAD_SHA"

When `--repo`/`--pr` are given, the engineering-review gate signals
(deterministic-check outcome, source-owner approval, unresolved review
findings) are derived live from GitHub via `gh api` for the exact head SHA,
rather than trusted from caller-supplied flags -- a PR cannot claim its own
deterministic checks passed or its own review approved. Any live lookup
failure fails closed (treated as not-yet-satisfied), never as success. The
`--deterministic-checks-failed` / `--source-owner-approved` /
`--unresolved-important-finding` flags remain for local/offline dry runs when
`--repo`/`--pr` are omitted.

The authorized-docs-reviewer allowlist is always read from a trusted git ref
(`--authorized-reviewers-ref`, default `origin/main`) rather than the PR's own
working-tree checkout, so a PR cannot add its own author to the allowlist in
the same diff that claims an override.

When no changed-file paths are given, changed `.md`/`.mdx` files under
`src/content/docs` are discovered via `git diff --diff-filter=d
origin/main...HEAD`, matching `style_lint.py --changed` and
`validate_ui_refs.py --changed`'s scope. Unlike `style_lint`'s `--changed`,
this never falls back to a full-tree scan: a diff that can't be resolved is a
hard failure, so required CI never silently widens scope.

Exit codes:
    0  the PR contract is satisfied
    1  one or more contract violations (see stderr)
    2  usage / file error
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence

_HERE = Path(__file__).resolve().parent
_DOCS_ROOT = "src/content/docs"
_AUTHORIZED_REVIEWERS_REPO_PATH = ".agents/skills/doc_quality_policy/authorized_docs_reviewers.json"
# Only the sibling job: this contract check itself runs as a step inside the
# "Docs technical references" job, so that job's check-run is still
# "in_progress" (never "success") at the moment this step executes -- it
# cannot verify its own conclusion mid-run. Its earlier steps having reached
# this one already proves they passed (a step failure would have stopped the
# job before this step ran).
_REQUIRED_CHECK_NAMES = ("Docs editorial quality",)

_spec = importlib.util.spec_from_file_location("doc_quality_policy", _HERE / "policy.py")
policy = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = policy  # required for dataclass field resolution
_spec.loader.exec_module(policy)

AGENT_MARKER = policy.AGENT_MARKER


def should_run_contract_check(event_name: str, pr_labels: Sequence[str]) -> bool:
    """Mirror of `.github/workflows/ci.yml`'s "Check documentation-risk PR
    contract" step condition: only an agent-marked pull request runs this
    check. An ordinary human PR (no `warpy-factory` label) has no
    `## Documentation risk` section and must not be failed for lacking one; a
    `push` event has no PR body to fetch at all. Kept here, tested, and
    mirrored exactly in the workflow `if:` expression so the two never drift.
    """
    return event_name == "pull_request" and AGENT_MARKER in pr_labels


def _autodiscover_changed_files() -> List[Path]:
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=d", "origin/main...HEAD", "--", _DOCS_ROOT],
            capture_output=True, text=True, check=True,
        )
    except (subprocess.CalledProcessError, OSError) as exc:
        raise RuntimeError(f"could not determine changed files vs origin/main...HEAD: {exc}") from exc
    files = []
    for line in result.stdout.strip().splitlines():
        line = line.strip()
        if not line or not (line.endswith(".md") or line.endswith(".mdx")):
            continue
        p = Path(line)
        if p.exists():
            files.append(p)
    return files


def _load_authorized_reviewers_from_file(path: Path) -> List[str]:
    """Offline/local-testing helper only -- reads a plain file path, with no
    trust guarantee. CI must always use `_load_authorized_reviewers_from_ref`.
    """
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return list(data.get("authorized_docs_reviewers", []))


def _load_authorized_reviewers_from_ref(ref: str, repo_path: str = _AUTHORIZED_REVIEWERS_REPO_PATH) -> List[str]:
    """Load the authorized-override allowlist from a trusted ref, never from
    the PR's own working-tree checkout. A PR that edits this file to add its
    own author must not thereby authorize its own override -- so this always
    reads the version committed on `ref` (the base branch by default),
    ignoring any local modification in the current checkout entirely.
    """
    try:
        result = subprocess.run(
            ["git", "show", f"{ref}:{repo_path}"],
            capture_output=True, text=True, check=True,
        )
    except (subprocess.CalledProcessError, OSError):
        return []
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return []
    return list(data.get("authorized_docs_reviewers", []))


@dataclass
class LiveReviewSignals:
    deterministic_checks_passed: bool
    source_owner_approved_current_head: bool
    has_unresolved_critical_or_important_finding: bool


def _run_gh_json(args: List[str]):
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed: {result.stderr.strip()}")
    return json.loads(result.stdout) if result.stdout.strip() else None


def _resolve_required_checks_passed(repo: str, head_sha: str) -> bool:
    """True only when every required check name has a successful conclusion
    on `head_sha`, verified live rather than assumed. A missing, pending, or
    failed run -- or an unreachable API -- is not-passed, never passed.
    """
    try:
        data = _run_gh_json(["api", f"repos/{repo}/commits/{head_sha}/check-runs", "--paginate"])
    except RuntimeError:
        return False
    runs = (data or {}).get("check_runs", [])
    conclusions = {}
    for run in runs:
        name = run.get("name")
        if name in _REQUIRED_CHECK_NAMES:
            conclusions[name] = run.get("conclusion")
    return all(conclusions.get(name) == "success" for name in _REQUIRED_CHECK_NAMES)


def _fetch_reviews(repo: str, pr_number: str) -> List[dict]:
    return _run_gh_json(["api", f"repos/{repo}/pulls/{pr_number}/reviews", "--paginate"]) or []


def _fetch_requested_reviewers(repo: str, pr_number: str) -> List[str]:
    data = _run_gh_json(["pr", "view", pr_number, "--repo", repo, "--json", "reviewRequests"])
    return [r.get("login") for r in (data or {}).get("reviewRequests", []) if r.get("login")]


def _compute_review_signals(
    reviews: List[dict], requested_reviewers: Sequence[str], head_sha: str, checks_passed: bool,
) -> LiveReviewSignals:
    """Pure computation over already-fetched review data, kept separate from
    the `gh` calls so the review-state logic (stale-review exclusion, latest-
    state-wins, source-owner matching) has fixture coverage without a live
    API dependency.

    A review's `commit_id` is the head SHA it was submitted against, so
    filtering on it is what makes a stale review (submitted before the latest
    push) not count -- the reviewer must re-review the current head.
    """
    head_reviews = [r for r in reviews if r.get("commit_id") == head_sha and r.get("state") in ("APPROVED", "CHANGES_REQUESTED")]
    latest_state_by_user: dict = {}
    for review in head_reviews:
        user = (review.get("user") or {}).get("login")
        if user:
            latest_state_by_user[user] = review.get("state")  # last one wins; reviews arrive in submission order

    has_unresolved = any(state == "CHANGES_REQUESTED" for state in latest_state_by_user.values())
    approvers = {user for user, state in latest_state_by_user.items() if state == "APPROVED"}
    source_owner_approved = bool(approvers & set(requested_reviewers))

    return LiveReviewSignals(checks_passed, source_owner_approved, has_unresolved)


def resolve_live_review_signals(repo: str, pr_number: str, head_sha: str) -> LiveReviewSignals:
    """Derive the engineering-review gate signals from live GitHub state for
    the exact current head SHA, instead of trusting caller-supplied flags.
    Any lookup failure fails closed: checks are treated as not-passed, no
    approval is treated as found, and an unresolved finding is assumed --
    the same "never convert an unavailable result into success" rule the
    final mergeability gate uses.
    """
    checks_passed = _resolve_required_checks_passed(repo, head_sha)

    try:
        reviews = _fetch_reviews(repo, pr_number)
    except RuntimeError:
        return LiveReviewSignals(checks_passed, False, True)

    try:
        requested_reviewers = _fetch_requested_reviewers(repo, pr_number)
    except RuntimeError:
        requested_reviewers = []

    return _compute_review_signals(reviews, requested_reviewers, head_sha, checks_passed)


def _collect_verify_markers(files: List[Path]) -> List[str]:
    markers: List[str] = []
    seen = set()
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for marker in policy.find_verify_markers(text):
            if marker not in seen:
                seen.add(marker)
                markers.append(marker)
    return markers


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--body", required=True, help="path to the PR body file")
    parser.add_argument("changed_files", nargs="*", help="changed content files (auto-discovered if omitted)")
    parser.add_argument("--head-sha", help="current PR head SHA")
    parser.add_argument("--repo", help="owner/repo; when given with --pr, resolves gate signals live from GitHub")
    parser.add_argument("--pr", help="PR number; when given with --repo, resolves gate signals live from GitHub")
    parser.add_argument(
        "--authorized-reviewers-ref", default="origin/main",
        help="trusted git ref to load the authorized-reviewer allowlist from (never the PR's own working tree)",
    )
    parser.add_argument(
        "--authorized-reviewers-file",
        help="offline/local testing ONLY: read the allowlist directly from this file instead of "
             "--authorized-reviewers-ref. Never pass this in CI -- it reads the PR's own working tree.",
    )
    parser.add_argument(
        "--deterministic-checks-failed", action="store_true",
        help="offline dry run only (ignored when --repo/--pr are given): pass when checks did not pass",
    )
    parser.add_argument(
        "--unresolved-important-finding", action="store_true",
        help="offline dry run only (ignored when --repo/--pr are given): pass when a finding is unresolved",
    )
    parser.add_argument(
        "--source-owner-approved", action="store_true",
        help="offline dry run only (ignored when --repo/--pr are given): pass when an engineer approved",
    )
    args = parser.parse_args(argv)

    body_path = Path(args.body)
    try:
        body = body_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: could not read {args.body}: {exc}", file=sys.stderr)
        return 2

    if args.changed_files:
        changed_files = [Path(p) for p in args.changed_files]
    else:
        try:
            changed_files = _autodiscover_changed_files()
        except RuntimeError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2

    verify_markers = _collect_verify_markers(changed_files)
    if args.authorized_reviewers_file:
        authorized_reviewers = _load_authorized_reviewers_from_file(Path(args.authorized_reviewers_file))
    else:
        authorized_reviewers = _load_authorized_reviewers_from_ref(args.authorized_reviewers_ref)

    if args.repo and args.pr:
        if not args.head_sha:
            print("error: --head-sha is required together with --repo/--pr", file=sys.stderr)
            return 2
        signals = resolve_live_review_signals(args.repo, args.pr, args.head_sha)
        deterministic_checks_passed = signals.deterministic_checks_passed
        has_unresolved_finding = signals.has_unresolved_critical_or_important_finding
        source_owner_approved = signals.source_owner_approved_current_head
        print(
            f"Live gate signals for {args.repo}#{args.pr}@{args.head_sha}: "
            f"checks_passed={deterministic_checks_passed} "
            f"source_owner_approved={source_owner_approved} "
            f"unresolved_finding={has_unresolved_finding}"
        )
    else:
        deterministic_checks_passed = not args.deterministic_checks_failed
        has_unresolved_finding = args.unresolved_important_finding
        source_owner_approved = args.source_owner_approved

    problems = policy.validate_pr_contract(
        body,
        verify_markers,
        current_head_sha=args.head_sha,
        authorized_docs_reviewers=authorized_reviewers,
        deterministic_checks_passed=deterministic_checks_passed,
        has_unresolved_critical_or_important_finding=has_unresolved_finding,
        source_owner_approved_current_head=source_owner_approved,
    )

    if problems:
        print("Documentation risk contract check FAILED:\n", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1

    print(
        f"Documentation risk contract check passed "
        f"({len(verify_markers)} VERIFY marker(s), {len(changed_files)} changed file(s))."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
