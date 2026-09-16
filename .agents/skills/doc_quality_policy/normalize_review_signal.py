#!/usr/bin/env python3
"""Apply workflow-owned identifiers to an agent-written review signal."""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import List, Optional

_HERE = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location(
    "verify_review_signal", _HERE / "verify_review_signal.py"
)
vrs = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = vrs
_SPEC.loader.exec_module(vrs)


def normalize_review_signal(
    agent_output: str, pr_number: str, head_sha: str, reviewer_login: str
) -> str:
    signal, problems = vrs._parse_signal(agent_output)
    if signal is None:
        raise ValueError("; ".join(problems))
    signal["pr"] = str(pr_number)
    signal["head_sha"] = head_sha
    signal["reviewer_login"] = reviewer_login
    return f"[SIGNAL:pr-review] {json.dumps(signal, sort_keys=True)}\n"


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent-output", required=True)
    parser.add_argument("--pr", required=True)
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--reviewer-login", default="github-actions[bot]")
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        normalized = normalize_review_signal(
            Path(args.agent_output).read_text(encoding="utf-8"),
            args.pr,
            args.head_sha,
            args.reviewer_login,
        )
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    Path(args.output).write_text(normalized, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
