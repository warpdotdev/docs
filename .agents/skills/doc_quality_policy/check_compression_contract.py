#!/usr/bin/env python3
"""Check the mechanically-checkable parts of the shared compression contract.

Word-budget and callout-count checks only — the rest of the contract (lead
summary, "Cut again" pass, no duplication) needs human/agent judgment and is
covered by `draft_docs`'s checklist and `review-docs-pr`. Generated
changelog/license/telemetry pages are exempt from the word budget (see
`.agents/references/doc-quality-policy.md`).

Usage:
    python3 check_compression_contract.py FILE --content-type quickstart
    python3 check_compression_contract.py FILE --content-type feature-doc

Exit codes:
    0  within budget
    1  over budget (a reportable finding for review-docs-pr, not a hard CI gate)
    2  usage / file error
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional

# ~600 words for a quickstart; <=1500 words for a combined feature page.
# Other content types have no fixed budget here; the drafting skills' own
# length guidance applies.
WORD_BUDGETS = {
    "quickstart": 600,
    "feature-doc": 1500,
}

# Generated data is exempt from the page-summary/word-budget rules, per the
# compression contract, but not from duplicate-content/style/technical checks
# (enforced elsewhere).
EXEMPT_CONTENT_TYPES = {"changelog", "license", "telemetry"}

MAX_CALLOUTS = 2
_CALLOUT_OPEN_RE = re.compile(r"^:::(note|tip|caution|danger)\b")


def _strip_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    return text[end + 4:]


def _strip_code_fences(lines: List[str]) -> List[str]:
    out = []
    in_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return out


def count_words(text: str) -> int:
    """Count words in page body prose, excluding frontmatter and code fences."""
    body = _strip_frontmatter(text)
    lines = _strip_code_fences(body.splitlines())
    prose = "\n".join(lines)
    prose = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", prose)  # images
    prose = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", prose)  # link text only
    return len(re.findall(r"\S+", prose))


def count_callouts(text: str) -> int:
    """Count Starlight `:::note` / `:::tip` / etc. callout blocks."""
    body = _strip_frontmatter(text)
    return sum(1 for line in body.splitlines() if _CALLOUT_OPEN_RE.match(line.strip()))


def check_compression_contract(text: str, content_type: str) -> List[str]:
    """Return a list of findings; empty means within the mechanical budget."""
    findings: List[str] = []
    if content_type in EXEMPT_CONTENT_TYPES:
        return findings

    budget = WORD_BUDGETS.get(content_type)
    if budget is not None:
        words = count_words(text)
        if words > budget:
            findings.append(
                f"word count {words} exceeds the {content_type} budget of {budget} "
                "(a justified overage is an important review decision, not an automatic split)"
            )

    callouts = count_callouts(text)
    if callouts > MAX_CALLOUTS:
        findings.append(f"{callouts} callouts exceed the linted budget of {MAX_CALLOUTS}")

    return findings


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help="path to the markdown/MDX file, or '-' for stdin")
    parser.add_argument(
        "--content-type", required=True,
        help="content type (e.g. quickstart, feature-doc, conceptual, changelog, license, telemetry)",
    )
    args = parser.parse_args(argv)

    if args.file == "-":
        text = sys.stdin.read()
    else:
        try:
            text = Path(args.file).read_text(encoding="utf-8")
        except OSError as exc:
            print(f"error: could not read {args.file}: {exc}", file=sys.stderr)
            return 2

    findings = check_compression_contract(text, args.content_type)
    if findings:
        print("Compression contract findings:", file=sys.stderr)
        for finding in findings:
            print(f"  - {finding}", file=sys.stderr)
        return 1

    print("Compression contract check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
