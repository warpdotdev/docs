#!/usr/bin/env python3
"""Collect data-only editorial signals over an exact UTC [start, end) window.

Writes feedback.jsonl, automated.jsonl and coverage.json. Exit 2 means partial
coverage, not a clean no-change result. Never writes git state or sends messages.
Raw conversations and API error bodies are not persisted. GitHub review markers
are an additional automated source when historical run access is unavailable.
"""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

AGENT_LABELS = {"oz-agent", "warpy-factory", "factory:docs-factory"}
AGENT_LOGINS = {
    "oz-agent", "warp-agent", "warp-agent-staging[bot]", "warp-agent[bot]",
    "warp-factories", "warp-for-oss", "github-actions[bot]", "vercel[bot]",
}
TAGS = ("[skill-feedback]", "[template-feedback]", "[style-rule-gap]")
INJECTION = re.compile(
    r"ignore (?:all |the )?(?:previous|prior|system) instructions|your new task is|"
    r"(?:reveal|print|modify|override).{0,30}(?:system prompt|credentials)|"
    r"(?:curl|wget).{0,100}\|\s*(?:bash|sh)", re.I,
)
SECRETS = re.compile(
    r"(?:gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+|"
    r"xox[baprs]-[A-Za-z0-9-]+|sk-[A-Za-z0-9_-]{16,}|"
    r"(?i:bearer)\s+[A-Za-z0-9._-]+|"
    r"(?i:(?:password|token|api[_ -]?key|secret)\s*[:=]\s*)"
    r"(?:\"[^\"]*\"|'[^']*'|[^\s,;]+))"
)
CATEGORIES = {
    "header_case": r"heading.{0,20}(?:case|capital)|sentence case",
    "frontmatter": r"frontmatter|meta description",
    "settings_path": r"settings.{0,20}path",
    "terminology": r"terminology|product name",
    "link_quality": r"broken link|link text|dead link",
    "template_structure": r"\[template-feedback\]",
    "style_rule": r"\[style-rule-gap\]",
}


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamps must include a timezone")
    return parsed.astimezone(timezone.utc)


def in_window(value, start, end):
    try:
        return start <= timestamp(value) < end
    except (ValueError, TypeError, AttributeError):
        return False


def bot(actor):
    return (
        not actor or actor.get("type") == "Bot"
        or (actor.get("login") or "").lower() in AGENT_LOGINS
        or (actor.get("login") or "").endswith("[bot]")
    )


def agent_commit(commit):
    return (
        bool(commit.get("author")) and bot(commit["author"])
    ) or (
        commit.get("commit", {}).get("author", {}).get("email")
        == "oz-agent@warp.dev"
    )


def sanitize(text):
    if INJECTION.search(text):
        return None
    return SECRETS.sub("[REDACTED]", text)


def human_record(item, pr, kind, start, end):
    actor = item.get("user")
    when = item.get("submitted_at") or item.get("created_at")
    if bot(actor) or not in_window(when, start, end):
        return None, "bot_or_outside_window"
    text = sanitize(item.get("body") or "")
    if text is None:
        return None, "injection"
    if not text.strip():
        return None, "empty"
    tag = next((tag for tag in TAGS if tag in text), "")
    category = next(
        (name for name, pattern in CATEGORIES.items() if re.search(pattern, text, re.I)),
        "general",
    )
    return {
        "date": when[:10], "timestamp": when, "pr": str(pr["number"]),
        "skill_used": "factory/editorial", "file": item.get("path", ""),
        "feedback_type": kind, "severity": "unknown", "comment": text,
        "tag": tag, "pattern_category": category, "resolved_by": "unknown",
        "verified_human": actor.get("type") == "User" and
        item.get("author_association") in {"OWNER", "MEMBER", "COLLABORATOR"},
        "author_login": actor.get("login"), "head_sha": pr["headRefOid"],
        "risk": pr.get("risk", "unknown"), "check_outcome": pr.get("check_outcome", "unknown"),
        "review_outcome": "unknown", "source_id": f"github:{kind}:{item['id']}",
    }, None


def assistant_texts(value):
    if isinstance(value, dict):
        if value.get("role") == "assistant":
            for block in value.get("content", []):
                if isinstance(block, dict) and block.get("type") == "text":
                    yield value.get("timestamp"), block.get("text", "")
            return
        for child in value.values():
            yield from assistant_texts(child)
    elif isinstance(value, list):
        for child in value:
            yield from assistant_texts(child)


def markers(text, provenance, when, start, end):
    records, invalid = [], 0
    for match in re.finditer(r"\[SIGNAL:(pr-review|style-lint)\]\s*", text):
        try:
            payload, _ = json.JSONDecoder().raw_decode(text[match.end():])
            if not isinstance(payload, dict) or not str(payload.get("pr", "")).isdigit():
                raise ValueError("missing PR")
            if not in_window(when, start, end):
                continue
            categories = {}
            if match[1] == "style-lint":
                categories = payload["violations"]
            else:
                for item in payload["top_categories"]:
                    parsed = re.fullmatch(r"([a-zA-Z][a-zA-Z0-9_-]*) \((\d+)\)", item)
                    if not parsed:
                        raise ValueError("invalid category")
                    categories[parsed[1]] = int(parsed[2])
            if not isinstance(categories, dict) or any(
                not re.fullmatch(r"[a-zA-Z][a-zA-Z0-9_-]*", key)
                or type(count) is not int or count < 0 for key, count in categories.items()
            ):
                raise ValueError("invalid counts")
            record = {
                "date": when[:10], "timestamp": when, "pr": str(payload["pr"]),
                "head_sha": payload.get("head_sha") if re.fullmatch(
                    r"[0-9a-f]{40}", str(payload.get("head_sha", ""))
                ) else "unknown",
                "signal_type": match[1], "categories": categories,
                "verdict": payload.get("verdict") if payload.get("verdict") in {
                    "Approve", "Approve with nits", "Request changes",
                    "approve", "approve_with_nits", "request_changes",
                } else "unknown",
                "source": provenance,
            }
            records.append(record)
        except (ValueError, KeyError, TypeError):
            invalid += 1
    return records, invalid


def unique(records):
    found = {}
    for record in records:
        identity = record.get("source_id")
        if record.get("signal_type"):
            identity = json.dumps(
                [record["signal_type"], record["pr"], record["head_sha"], record["categories"]],
                sort_keys=True,
            )
        if not identity:
            identity = hashlib.sha256(
                json.dumps(record, sort_keys=True).encode()
            ).hexdigest()
        found[identity] = record
    return list(found.values())


class Collector:
    def __init__(self, args):
        self.args = args
        self.start, self.end = timestamp(args.start), timestamp(args.end)
        self.coverage = {"window": {"start": args.start, "end": args.end, "semantics": "[start,end) UTC"},
                         "counts": {}, "omissions": [], "discarded": {}}
        self.feedback, self.automated = [], []

    def command(self, argv):
        result = subprocess.run(argv, capture_output=True, text=True, timeout=120,
                                env={**os.environ, "GH_PAGER": "cat"})
        if result.returncode:
            raise ValueError(f"{argv[0]} {argv[1]} failed (exit {result.returncode})")
        return json.loads(result.stdout)

    def api(self, suffix, paginated=False):
        argv = ["gh", "api", f"repos/{self.args.repo}/{suffix}"]
        if paginated:
            pages = self.command(argv + ["--paginate", "--slurp"])
            return [item for page in pages for item in page]
        return self.command(argv)

    def github(self):
        prs = self.command([
            "gh", "pr", "list", "--repo", self.args.repo, "--state", "merged",
            "--search", f"merged:{self.start.date()}..{self.end.date()}",
            "--limit", "1000", "--json", "number,mergedAt,labels,author,body,headRefOid",
        ])
        if len(prs) == 1000:
            self.coverage["omissions"].append("GitHub PR search reached the 1000-result cap")
        prs = [pr for pr in prs if in_window(pr["mergedAt"], self.start, self.end)]
        self.coverage["counts"]["merged_prs"] = len(prs)
        candidates, discarded = 0, Counter()
        for pr in prs:
            number = pr["number"]
            try:
                commits = self.api(f"pulls/{number}/commits?per_page=100", True)
                if len(commits) >= 250:
                    self.coverage["omissions"].append(f"PR {number}: GitHub 250-commit cap")
                if not (AGENT_LABELS & {label["name"] for label in pr["labels"]}
                        or bot(pr.get("author")) or any(agent_commit(c) for c in commits)):
                    continue
                candidates += 1
                risk = re.search(r"^Risk:\s*(low|engineering-review-required)\s*$",
                                 pr.get("body", ""), re.M)
                pr["risk"] = risk[1] if risk else "unknown"
                try:
                    checks = self.api(f"commits/{pr['headRefOid']}/check-runs?per_page=100")
                    required = [c for c in checks["check_runs"] if c["name"] in {
                        "Docs editorial quality", "Docs technical references"}]
                    pr["check_outcome"] = (
                        "pass" if len(required) == 2 and all(c["conclusion"] == "success" for c in required)
                        else "fail" if any(c["conclusion"] in {"failure", "timed_out", "cancelled"} for c in required)
                        else "unknown"
                    )
                except (OSError, ValueError, KeyError, subprocess.TimeoutExpired):
                    self.coverage["omissions"].append(f"PR {number}: head checks unavailable")
                for suffix, kind in (("reviews", "review_verdict"), ("comments", "review_comment")):
                    items = self.api(f"pulls/{number}/{suffix}?per_page=100", True)
                    for item in items:
                        if bot(item.get("user")) and suffix == "reviews":
                            signals, invalid = markers(
                                item.get("body") or "", f"github-review:{item['id']}",
                                item.get("submitted_at"), self.start, self.end,
                            )
                            self.automated.extend(signals)
                            if invalid:
                                self.coverage["omissions"].append(f"PR {number}: {invalid} invalid review markers")
                        record, reason = human_record(item, pr, kind, self.start, self.end)
                        if record:
                            self.feedback.append(record)
                        else:
                            discarded[reason] += 1
                last_agent = max((i for i, c in enumerate(commits) if agent_commit(c)), default=None)
                if last_agent is None:
                    self.coverage["omissions"].append(f"PR {number}: no identifiable agent commit for human-edit boundary")
                    continue
                for commit in commits[last_agent + 1:]:
                    when = commit["commit"]["author"]["date"]
                    if bot(commit.get("author")) or not in_window(when, self.start, self.end):
                        continue
                    detail = self.api(f"commits/{commit['sha']}")
                    if len(detail["files"]) >= 300:
                        self.coverage["omissions"].append(f"commit {commit['sha']}: file list may be truncated")
                    for file in detail["files"]:
                        if not file["filename"].startswith("src/content/docs/"):
                            continue
                        self.feedback.append({
                            "date": when[:10], "timestamp": when, "pr": str(number),
                            "skill_used": "factory/editorial", "file": file["filename"],
                            "feedback_type": "human_edit", "severity": "unknown",
                            "comment": f"Human edit after agent commit: +{file['additions']} -{file['deletions']} lines",
                            "tag": "", "pattern_category": "general", "resolved_by": "human_edit",
                            "verified_human": False, "head_sha": pr["headRefOid"],
                            "source_id": f"github:commit:{commit['sha']}:{file['filename']}",
                        })
            except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired):
                self.coverage["omissions"].append(f"PR {number}: collection incomplete")
        self.coverage["counts"]["agent_prs"] = candidates
        self.coverage["discarded"] = dict(discarded)

    def runs(self):
        cli = os.environ.get("OZ_CLI")
        if not cli:
            self.coverage["omissions"].append("OZ_CLI unavailable")
            return
        cursor, seen, runs = None, set(), []
        while True:
            argv = [cli, "run", "list", "--environment", self.args.environment,
                    "--created-after", self.args.start, "--created-before", self.args.end,
                    "--sort-by", "created-at", "--sort-order", "asc",
                    "--limit", "100", "--output-format", "json"]
            if cursor:
                argv += ["--cursor", cursor]
            try:
                page = self.command(argv)
                runs.extend(page["runs"])
                info = page["page_info"]
                if not info["has_next_page"]:
                    break
                cursor = info["next_cursor"]
                if not cursor or cursor in seen:
                    raise ValueError("invalid pagination cursor")
                seen.add(cursor)
            except (OSError, ValueError, KeyError, subprocess.TimeoutExpired):
                self.coverage["omissions"].append("Factory run pagination incomplete")
                break
        runs = {r["run_id"]: r for r in runs if in_window(r["created_at"], self.start, self.end)
                and r["run_id"] != os.environ.get("OZ_RUN_ID")}
        self.coverage["counts"]["environment_runs"] = len(runs)

        def collect(run_id):
            try:
                detail = self.command([cli, "run", "get", run_id, "--output-format", "json"])
                if detail.get("factory_uid") != self.args.factory:
                    return "other_factory", [], 0
                conversation = self.command([cli, "run", "get", run_id, "--conversation", "--output-format", "json"])
                if not isinstance(conversation.get("steps"), list):
                    raise ValueError("conversation schema")
                found, invalid = [], 0
                for when, text in assistant_texts(conversation):
                    rows, bad = markers(text, f"run:{run_id}", when, self.start, self.end)
                    found.extend(rows)
                    invalid += bad
                return "retrieved", found, invalid
            except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired):
                return "unavailable", [], 0

        statuses = Counter()
        with ThreadPoolExecutor(max_workers=4) as pool:
            for run_id, (status, records, invalid) in zip(runs, pool.map(collect, runs)):
                statuses[status] += 1
                self.automated.extend(records)
                if status == "unavailable" or invalid:
                    self.coverage["omissions"].append(f"run {run_id}: {status}, invalid_markers={invalid}")
        self.coverage["counts"]["conversations"] = dict(statuses)

    def write(self):
        self.feedback = unique(self.feedback)
        self.automated = unique(self.automated)
        verdicts = {(r["pr"], r["head_sha"]): r["verdict"].lower().replace(" ", "_")
                    for r in self.automated if r["signal_type"] == "pr-review"
                    and r["head_sha"] != "unknown"}
        for record in self.feedback:
            record["review_outcome"] = verdicts.get(
                (record["pr"], record["head_sha"]), "unknown")
        self.coverage["counts"].update(feedback=len(self.feedback), automated=len(self.automated))
        self.coverage["status"] = "partial" if self.coverage["omissions"] else "complete-for-selected-sources"
        output = Path(self.args.output_dir)
        output.mkdir(parents=True, exist_ok=True)
        for name, records in (("feedback", self.feedback), ("automated", self.automated)):
            (output / f"{name}.jsonl").write_text(
                "".join(json.dumps(r, sort_keys=True) + "\n" for r in records), encoding="utf-8")
        (output / "coverage.json").write_text(
            json.dumps(self.coverage, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("repo", "environment", "factory", "start", "end", "output-dir"):
        parser.add_argument(f"--{name}", required=True)
    args = parser.parse_args()
    collector = Collector(args)
    if collector.end <= collector.start:
        parser.error("end must be after start")
    for name in ("github", "runs"):
        try:
            getattr(collector, name)()
        except (OSError, ValueError, KeyError, subprocess.TimeoutExpired):
            collector.coverage["omissions"].append(f"{name} source unavailable")
    collector.write()
    print(json.dumps(collector.coverage, sort_keys=True))
    return 2 if collector.coverage["omissions"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
