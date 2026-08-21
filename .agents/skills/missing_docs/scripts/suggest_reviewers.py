#!/usr/bin/env python3
"""Suggest PR reviewers for missing_docs drift-watch changes.

Every docs change the drift-watch flow makes traces back to a concrete source
surface (a feature flag, CLI command, API route, slash command, or setting). This
script maps those *source* files to the engineers who own them, using the
CODEOWNERS-format ownership files that already live in the code repos:

  - warp client repo : .github/STAKEHOLDERS   (advisory, broad coverage)
  - warp-server      : .github/STAKEHOLDERS   (advisory) + .github/CODEOWNERS (enforced)

Those files are the source of truth for ownership (warp-server keeps STAKEHOLDERS
fresh via the `sync-stakeholders` skill), so this script never duplicates owner
lists — it just resolves against them with standard CODEOWNERS precedence
(last matching rule wins).

Usage:
  python3 suggest_reviewers.py \
    --warp ../warp --warp-server ../warp-server \
    warp:app/src/settings/ssh.rs \
    warp:app/src/search/slash_command_menu/static_commands/commands.rs \
    warp-server:router/handlers/public_api/runs.go

Source paths may also be piped on stdin (one `repo:relpath` per line). `repo`
is `warp` (the client repo passed via --warp; `warp-internal` is accepted as an
alias) or `warp-server`.

Output: a per-path resolution table, the deduped reviewer set (users and teams),
and a ready-to-run `gh pr edit --add-reviewer` snippet. Exit code is always 0;
unresolved paths are reported but never fatal (so a scheduled run is not blocked
by an ownership gap — it just falls back to the default owners or none).

Pass `--reviewers-only` to print just the comma-joined argument for
`gh pr edit --add-reviewer` (empty output when nothing resolved). That is the form
the mandatory reviewer-request step consumes, so callers never have to scrape the
human-readable table:

  REVIEWERS=$(python3 suggest_reviewers.py --reviewers-only --warp ../warp warp:app/src/x.rs)
  [[ -z "$REVIEWERS" ]] && REVIEWERS=dannyneira   # never drop the review request
"""

import argparse
import fnmatch
import sys
from pathlib import Path


def parse_ownership(path):
    """Parse a CODEOWNERS-format file into an ordered list of (pattern, [owners])."""
    rules = []
    if not path or not path.is_file():
        return rules
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        pattern = parts[0]
        owners = [tok for tok in parts[1:] if tok.startswith("@")]
        if owners:
            rules.append((pattern, owners))
    return rules


def pattern_matches(pattern, rel_path):
    """Practical CODEOWNERS matching for a repo-relative POSIX path."""
    pat = pattern.lstrip("/")  # all our rules are root-anchored
    p = rel_path.lstrip("/")
    if pat in ("", "*", "**"):
        return True  # default fallback rule (e.g. `/ @org/team`)
    if pat.endswith("/"):  # directory prefix: matches the dir and everything under it
        return p == pat[:-1] or p.startswith(pat)
    if any(ch in pat for ch in "*?["):  # glob pattern
        return fnmatch.fnmatch(p, pat) or fnmatch.fnmatch(p, pat + "/*")
    # bare path: exact file, or a directory given without a trailing slash
    return p == pat or p.startswith(pat + "/")


def owners_for(rel_path, rules):
    """Return (owners, matched_pattern) using last-match-wins precedence."""
    match = None
    for pattern, owners in rules:
        if pattern_matches(pattern, rel_path):
            match = (owners, pattern)
    return match if match else (None, None)


def main():
    ap = argparse.ArgumentParser(description="Suggest PR reviewers from code ownership.")
    ap.add_argument("--warp", help="Path to the warp client repo root (warp-internal accepted).")
    ap.add_argument("--warp-server", dest="warp_server", help="Path to the warp-server repo root.")
    ap.add_argument(
        "--reviewers-only",
        action="store_true",
        help=(
            "Print only the comma-joined `gh pr edit --add-reviewer` argument "
            "(empty when nothing resolved), for scripted use."
        ),
    )
    ap.add_argument("paths", nargs="*", help="Source paths as repo:relpath.")
    args = ap.parse_args()
    quiet = args.reviewers_only

    # Build per-repo rule lists (STAKEHOLDERS first, then CODEOWNERS so enforced
    # rules take precedence as later matches).
    repos = {}
    if args.warp:
        root = Path(args.warp)
        repos["warp"] = parse_ownership(root / ".github" / "STAKEHOLDERS") + parse_ownership(
            root / ".github" / "CODEOWNERS"
        )
        repos["warp-internal"] = repos["warp"]  # alias
    if args.warp_server:
        root = Path(args.warp_server)
        repos["warp-server"] = parse_ownership(root / ".github" / "STAKEHOLDERS") + parse_ownership(
            root / ".github" / "CODEOWNERS"
        )

    inputs = list(args.paths)
    if not sys.stdin.isatty():
        inputs += [ln.strip() for ln in sys.stdin if ln.strip()]

    if not inputs:
        print("No source paths given. Pass repo:relpath args or pipe them on stdin.", file=sys.stderr)
        return 0

    def report(message=""):
        """Print human-readable progress on stdout, suppressed under --reviewers-only."""
        if not quiet:
            print(message)

    def diagnose(message):
        """Report a resolution problem.

        Under --reviewers-only this goes to stderr, so `$(...)` still captures only
        the reviewer list while the run log keeps a record of why a fallback
        happened. A silent fallback is indistinguishable from a correct resolution
        when you are reading the log afterwards.
        """
        print(message, file=sys.stderr if quiet else sys.stdout)

    users, teams = [], []
    unresolved = []
    report("Reviewer resolution:")
    for item in inputs:
        if ":" not in item:
            unresolved.append(item)
            diagnose(f"  ? {item} — missing repo prefix (use warp: or warp-server:)")
            continue
        repo, rel = item.split(":", 1)
        rules = repos.get(repo)
        if rules is None:
            unresolved.append(item)
            diagnose(f"  ? {item} — no ownership file loaded for repo '{repo}'")
            continue
        owners, pattern = owners_for(rel, rules)
        if not owners:
            unresolved.append(item)
            diagnose(f"  ? {repo}:{rel} — no owner match")
            continue
        report(f"  - {repo}:{rel} -> {' '.join(owners)}  (matched: {pattern})")
        for o in owners:
            handle = o.lstrip("@")
            bucket = teams if "/" in handle else users
            if handle not in bucket:
                bucket.append(handle)

    # gh accepts users by login and teams as org/team; both via --add-reviewer.
    review_args = users + teams
    joined = ",".join(review_args)

    if quiet:
        # Sole *stdout* output: the --add-reviewer argument, or nothing at all. An
        # empty result is the caller's cue to use the fallback reviewer, never to
        # skip the request. Diagnostics already went to stderr.
        if not joined:
            print(
                "suggest_reviewers: no owners resolved from "
                f"{len(inputs)} path(s); caller must use its fallback reviewer.",
                file=sys.stderr,
            )
        else:
            print(joined)
        return 0

    report()
    report(f"Reviewers (users): {', '.join(users) if users else '(none)'}")
    report(f"Reviewers (teams): {', '.join(teams) if teams else '(none)'}")
    if unresolved:
        report(f"Unresolved paths: {len(unresolved)} (left for manual assignment)")

    if review_args:
        report()
        report("Suggested command (replace <PR> with the PR number):")
        report(f"  gh pr edit <PR> --add-reviewer {joined}")
    else:
        report()
        report("No owners resolved. Do NOT skip the review request — assign the")
        report("fallback reviewer (dannyneira) so the PR still reaches a human.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
