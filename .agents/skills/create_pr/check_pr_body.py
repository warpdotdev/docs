#!/usr/bin/env python3
"""Detect degeneration/corruption in a PR body before creating or editing a PR.

Large language models occasionally emit "repetition-loop" corruption when
generating or rewriting long PR descriptions: the same phrase or bullet repeats
several times and often cuts off mid-token (for example, a sentence ending in an
unclosed inline-code span like "because `m"). This has shipped to real PRs.

This check is COMPLEMENTARY to using `gh ... --body-file`. Writing the body to a
file avoids shell-escaping corruption, but it does NOT catch repetition-loop
degeneration that is already present in the generated text — that text survives
`--body-file` unchanged. Run this check on the body file right before
`gh pr create --body-file` / `gh pr edit --body-file`. If it reports an issue,
do NOT submit: regenerate the affected section and re-check.

Checks performed:
  * Repeated span      - a long substring repeated many times anywhere in the
                         body (the core repetition-loop signature). Works across
                         line breaks and within a single Markdown line.
  * Unbalanced backtick- a non-code line with an odd number of backticks, which
                         usually means an inline-code span was truncated
                         mid-token (e.g. "... because `m").
  * Duplicate heading  - the same Markdown heading text appearing more than once.
  * Required heading    - (optional) assert specific headings are present exactly
                         once, for skills that emit a fixed body template.
  * Lead section        - (optional) assert a heading is the FIRST heading in the
                         body, has prose under it, and stays within a word budget.
                         Drafting PRs must open with a plain-language summary of
                         what the feature does for the user, so a reviewer learns
                         that before any pipeline bookkeeping.

Usage:
    python3 check_pr_body.py /tmp/pr-body.md
    cat /tmp/pr-body.md | python3 check_pr_body.py -
    python3 check_pr_body.py /tmp/pr-body.md \
        --require-heading "## Patterns addressed" \
        --require-heading "## Improvement targets"
    python3 check_pr_body.py /tmp/pr-body.md \
        --require-lead-section "## What this feature does"

Exit codes:
    0  no issues found
    1  one or more issues found (do NOT submit; regenerate and re-check)
    2  usage / file error
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

# Length of the sliding window (in characters) used to detect a repeated span,
# paired with the number of occurrences that trips the check. A short window must
# repeat more times; a long window only needs to repeat twice.
SHORT_WINDOW = 40
SHORT_MIN_COUNT = 3
LONG_WINDOW = 80
LONG_MIN_COUNT = 2

# Word budget for the lead section. "Drafts are too wordy" is a standing complaint,
# and a summary that runs past a short paragraph stops being a summary. Two to four
# sentences fit comfortably under this cap.
LEAD_SECTION_MAX_WORDS = 75


def _strip_urls(text: str) -> str:
    """Remove URLs so repeated link targets don't cause false positives.

    A PR body that legitimately lists many links (e.g. a changelog) can repeat a
    long URL prefix; that is not degeneration, so drop URLs before scanning.
    """
    return re.sub(r"https?://\S+", " ", text)


def find_repeated_span(text: str) -> Optional[Tuple[str, int]]:
    """Return (snippet, count) for the worst repeated span, or None if clean."""
    norm = re.sub(r"\s+", " ", _strip_urls(text)).strip()
    if len(norm) < SHORT_WINDOW * 2:
        return None

    worst: Optional[Tuple[str, int]] = None
    for window, min_count in ((LONG_WINDOW, LONG_MIN_COUNT), (SHORT_WINDOW, SHORT_MIN_COUNT)):
        if len(norm) < window * 2:
            continue
        counts: dict[str, int] = {}
        for i in range(len(norm) - window + 1):
            chunk = norm[i : i + window]
            counts[chunk] = counts.get(chunk, 0) + 1
        chunk, count = max(counts.items(), key=lambda kv: kv[1])
        if count >= min_count and (worst is None or count > worst[1]):
            worst = (chunk, count)
    return worst


def _iter_non_code_lines(lines: List[str]):
    """Yield (line_num, text) for lines outside fenced code blocks."""
    fence: Optional[str] = None
    for line_num, line in enumerate(lines, start=1):
        fence_match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence is not None:
            if fence_match and fence_match.group(1)[0] == fence[0]:
                fence = None
            continue
        if fence_match:
            fence = fence_match.group(1)
            continue
        yield line_num, line


def find_unbalanced_backticks(lines: List[str]) -> List[Tuple[int, str]]:
    """Return (line_num, line) for non-code lines with an odd backtick count."""
    issues = []
    for line_num, line in _iter_non_code_lines(lines):
        if line.count("`") % 2 == 1:
            issues.append((line_num, line.strip()))
    return issues


def find_duplicate_headings(lines: List[str]) -> List[str]:
    """Return heading texts that appear more than once (outside code fences)."""
    seen: dict[str, int] = {}
    for _, line in _iter_non_code_lines(lines):
        m = re.match(r"^(#{1,6})\s+(.*\S)\s*$", line)
        if m:
            key = f"{m.group(1)} {m.group(2)}"
            seen[key] = seen.get(key, 0) + 1
    return [h for h, c in seen.items() if c > 1]


def check_required_headings(lines: List[str], required: List[str]) -> List[str]:
    """Return messages for required headings that are missing or duplicated."""
    present: dict[str, int] = {}
    for _, line in _iter_non_code_lines(lines):
        stripped = line.strip()
        present[stripped] = present.get(stripped, 0) + 1
    problems = []
    for heading in required:
        count = present.get(heading.strip(), 0)
        if count == 0:
            problems.append(f"missing required heading: {heading!r}")
        elif count > 1:
            problems.append(f"required heading appears {count}x (expected once): {heading!r}")
    return problems


def check_lead_section(lines: List[str], heading: str) -> List[str]:
    """Return messages if the lead section is missing, misplaced, empty, or too long.

    The lead section is the plain-language answer to "what does this feature do for
    the user?", and it only does that job if the reviewer hits it first. Ambient
    drafts previously opened with pipeline bookkeeping (which spec, which workflow,
    which run), so the check asserts position as well as presence.
    """
    wanted = heading.strip()
    problems: List[str] = []

    headings: List[Tuple[int, str]] = []
    for line_num, line in _iter_non_code_lines(lines):
        if re.match(r"^#{1,6}\s+\S", line):
            headings.append((line_num, line.strip()))

    matches = [ln for ln, text in headings if text == wanted]
    if not matches:
        return [f"missing required lead section: {wanted!r} (must be the first heading in the body)"]
    if len(matches) > 1:
        problems.append(
            f"lead section appears {len(matches)}x (expected once): {wanted!r}"
        )

    first_line, first_text = headings[0]
    if first_text != wanted:
        problems.append(
            f"lead section is not first: {first_text!r} (line {first_line}) precedes "
            f"{wanted!r} (line {matches[0]}). The reader must get the feature summary "
            "before any other section."
        )

    # Collect the prose between the lead heading and the next heading.
    start = matches[0]
    body_words: List[str] = []
    for line_num, line in _iter_non_code_lines(lines):
        if line_num <= start:
            continue
        if re.match(r"^#{1,6}\s+\S", line):
            break
        body_words.extend(line.split())

    if not body_words:
        problems.append(f"lead section {wanted!r} has no content under it")
    elif len(body_words) > LEAD_SECTION_MAX_WORDS:
        problems.append(
            f"lead section {wanted!r} is {len(body_words)} words "
            f"(budget: {LEAD_SECTION_MAX_WORDS}). Cut it to a short paragraph: what the "
            "feature does for the user, plus the shipped-in version and date."
        )

    return problems


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("body", help="path to the PR body file, or '-' for stdin")
    parser.add_argument(
        "--require-heading",
        action="append",
        default=[],
        metavar="HEADING",
        help="assert this exact heading line is present exactly once (repeatable)",
    )
    parser.add_argument(
        "--require-lead-section",
        metavar="HEADING",
        help=(
            "assert this exact heading is the FIRST heading in the body, appears once, "
            f"and carries 1-{LEAD_SECTION_MAX_WORDS} words of prose"
        ),
    )
    args = parser.parse_args(argv)

    if args.body == "-":
        text = sys.stdin.read()
    else:
        path = Path(args.body)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"error: could not read {args.body}: {exc}", file=sys.stderr)
            return 2

    lines = text.splitlines()
    issues: List[str] = []

    repeated = find_repeated_span(text)
    if repeated:
        snippet, count = repeated
        issues.append(
            "repetition-loop: a span repeats "
            f"{count}x (likely model degeneration).\n    repeated text: {snippet!r}"
        )

    for line_num, line in find_unbalanced_backticks(lines):
        issues.append(
            f"unbalanced backtick on line {line_num} (possible truncated inline code): {line!r}"
        )

    for heading in find_duplicate_headings(lines):
        issues.append(f"duplicate heading: {heading!r}")

    issues.extend(check_required_headings(lines, args.require_heading))

    if args.require_lead_section:
        issues.extend(check_lead_section(lines, args.require_lead_section))

    if issues:
        print("PR body integrity check FAILED:\n", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        print(
            "\nDo NOT submit this body. Regenerate the affected section "
            "(or re-fetch and re-apply a minimal edit) and run this check again.",
            file=sys.stderr,
        )
        return 1

    print("PR body integrity check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
