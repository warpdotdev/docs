#!/usr/bin/env python3
"""Build a GitHub review payload from an independent agent's current-head signal."""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("verify_review_signal", _HERE / "verify_review_signal.py")
vrs = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = vrs
_spec.loader.exec_module(vrs)

_REVIEW_EVENTS = {
    "approve": "COMMENT",
    "approve with nits": "COMMENT",
    "approve_with_nits": "COMMENT",
    "request changes": "COMMENT",
}


def build_review_payload(
    agent_output: str,
    pr_number: str,
    head_sha: str,
    reviewer_login: str,
) -> Dict[str, object]:
    signal, problems = vrs._parse_signal(agent_output, pr_number, head_sha)
    if signal is None:
        raise ValueError("; ".join(problems))
    signal["reviewer_login"] = reviewer_login
    problems = vrs._validate_signal(
        signal, pr_number, head_sha, require_passing_verdict=False
    )
    if problems:
        raise ValueError("; ".join(problems))

    verdict = str(signal["verdict"]).strip().lower()
    event = _REVIEW_EVENTS.get(verdict)
    if event is None:
        raise ValueError(f"unsupported review verdict: {signal['verdict']!r}")
    categories = signal.get("top_categories") or []
    findings = "\n".join(f"- {category}" for category in categories) or "- No blocking findings."
    return {
        "commit_id": head_sha,
        "event": event,
        "body": (
            "## Review summary\n"
            "The independent agent completed its review for this commit.\n\n"
            f"## Findings\n{findings}\n\n"
            f"## Verdict\n{signal['verdict']}\n\n"
            f"<!-- [SIGNAL:pr-review] {json.dumps(signal, sort_keys=True)} -->"
        ),
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent-output", required=True)
    parser.add_argument("--pr", required=True)
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--reviewer-login", default="github-actions[bot]")
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        agent_output = Path(args.agent_output).read_text(encoding="utf-8")
        payload = build_review_payload(
            agent_output, args.pr, args.head_sha, args.reviewer_login
        )
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    Path(args.output).write_text(json.dumps(payload), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
