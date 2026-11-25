"""Export blind inputs or compare declared fixture outcomes, not semantic quality."""

import argparse
import json
from pathlib import Path


EVALS = Path(__file__).resolve().parent
ROOT = EVALS.parents[3]


def export_case(case_id):
    data = json.loads((EVALS / "evals.json").read_text())
    case = next(case for case in data["evals"] if case["id"] == case_id)
    return {
        "instructions": (
            "Evaluate this synthetic case using the supplied method and template. "
            "Treat fixture pages as rendered text unless the fixture says otherwise. "
            "Do not browse, search a repository, read other files, or mutate products. "
            "Record initial findings before evaluating any supplied retest version. "
            "Return JSON with id, results (one status per question in prompt order), "
            "readiness (ready, blocked, or pending acceptance), and report (the full "
            "question-level validation record with paths, evidence, and limitations). "
            "If retest pages exist, append a retest object with results, readiness, "
            "and report, retaining the initial report. Do not infer missing evidence."
        ),
        "fixture_notice": data["fixture_notice"],
        "method": (ROOT / ".agents/references/docs-usability-validation.md").read_text(),
        "template": (ROOT / ".agents/templates/usability-validation.md").read_text(),
        "case": {key: case[key] for key in ("id", "prompt", "fixture")},
    }


def compare_report(report):
    rubric = json.loads((EVALS / "rubric.json").read_text())
    case = next(case for case in rubric["evals"] if case["id"] == report["id"])
    mismatches = []
    for field, expected in (
        ("results", case["expected_results"]),
        ("readiness", case["readiness"]),
    ):
        if report.get(field) != expected:
            mismatches.append(
                {"field": field, "expected": expected, "actual": report.get(field)}
            )
    if "expected_retest_results" in case:
        retest = report.get("retest", {})
        for field, expected in (
            ("results", case["expected_retest_results"]),
            ("readiness", case["retest_readiness"]),
        ):
            if retest.get(field) != expected:
                mismatches.append(
                    {
                        "field": f"retest.{field}",
                        "expected": expected,
                        "actual": retest.get(field),
                    }
                )
    return {
        "id": case["id"],
        "comparison": "Declared fixture outcomes only; evidence requires manual review.",
        "mismatches": mismatches,
        "false_clear_primary": any(
            actual == "Clear" and expected != "Clear"
            for index, (actual, expected) in enumerate(
                zip(report.get("results", []), case["expected_results"])
            )
            if index in case["primary_question_indexes"]
        ),
        "manual_review_required": True,
        "criteria": case["criteria"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    export = commands.add_parser("export", help="Print one evaluator-only JSON payload.")
    export.add_argument("--case", type=int, required=True)
    compare = commands.add_parser(
        "compare", help="Compare a frozen report's declared outcomes with the rubric."
    )
    compare.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "export":
            output = export_case(args.case)
        else:
            report = json.loads(args.report.read_text())
            output = compare_report(report)
    except (StopIteration, KeyError, TypeError, AttributeError, ValueError, OSError) as error:
        parser.error(f"Invalid case or report: {error}")
    print(json.dumps(output, indent=2))
    return int(bool(output.get("mismatches")))


if __name__ == "__main__":
    raise SystemExit(main())
