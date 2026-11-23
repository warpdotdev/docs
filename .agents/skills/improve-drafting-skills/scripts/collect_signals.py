#!/usr/bin/env python3
"""Collect data-only editorial signals over an exact UTC [start, end) window.

Writes feedback, automated, human-edit evidence and coverage files. Exit 2 means partial
coverage, not a clean no-change result. Never writes git state or sends messages.
Raw conversations and API error bodies are not persisted. GitHub review markers
are an additional automated source when historical run access is unavailable.
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.parse import quote

AGENT_LABELS = {"oz-agent", "warpy-factory", "factory:docs-factory"}
AGENT_LOGINS = {
    "oz-agent", "warp-agent", "warp-agent-staging[bot]", "warp-agent[bot]",
    "warp-factories", "warp-for-oss", "github-actions[bot]", "vercel[bot]",
}
REVIEW_PUBLISHERS = {
    "github-actions[bot]", "warp-agent[bot]", "warp-agent-staging[bot]",
    "warp-for-oss",
}
TAGS = ("[skill-feedback]", "[template-feedback]", "[style-rule-gap]")
AGENT_ATTRIBUTION = re.compile(
    r"^\s*(?:\*\*)?Warp agent implementation update(?:\*\*)?\s*"
    r"|\[SIGNAL:(?:pr-review|style-lint)\]\s*\{"
    r"|<!--\s*warp:(?:pr-artifacts-comment|attribution)\s+(?:start|end)\s*-->"
    r"|^\s*_?Posted by a Warp agent_?\s*$"
    r"|^Responding as [^\n]+:\s*\[(?:Open session|View in factory)\]",
    re.I | re.M,
)
INJECTION = re.compile(
    r"ignore (?:all |the )?(?:previous|prior|system) instructions|your new task is|"
    r"(?:reveal|print|modify|override).{0,30}(?:system prompt|credentials)|"
    r"(?:curl|wget).{0,100}\|\s*(?:bash|sh)", re.I,
)
SECRETS = re.compile(
    r"(?:-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----[\s\S]*?"
    r"-----END (?:[A-Z0-9]+ )*PRIVATE KEY-----|"
    r"gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+|"
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
    ) or bool(
        re.search(
            r"(?im)^Co-authored-by:.*(?:oz-agent@warp\.dev|\[bot\]|"
            r"noreply@anthropic\.com|warp-agent|<[^>]*@openai\.com>)",
            commit.get("commit", {}).get("message", ""),
        )
    )


def sanitize(text):
    if INJECTION.search(text):
        return None
    redacted = SECRETS.sub("[REDACTED]", text)
    if re.search(r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----", redacted):
        return None
    return redacted


def human_record(item, pr, kind, start, end):
    actor = item.get("user")
    when = item.get("submitted_at") or item.get("created_at")
    if bot(actor):
        return None, "bot"
    if AGENT_ATTRIBUTION.search(item.get("body") or ""):
        return None, "agent_attribution"
    try:
        moment = timestamp(when)
    except (ValueError, TypeError, AttributeError):
        return None, "invalid_timestamp"
    if not start <= moment < end:
        return None, "outside_window"
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


def markers(text, provenance, when, start, end, *, pr_number=None,
            reviewed_head=None, publisher=None):
    records, invalid = [], 0
    for match in re.finditer(r"\[SIGNAL:(pr-review|style-lint)\]\s*", text):
        try:
            payload, _ = json.JSONDecoder().raw_decode(text[match.end():])
            if not isinstance(payload, dict) or not str(payload.get("pr", "")).isdigit():
                raise ValueError("missing PR")
            moment = timestamp(when)
            if not start <= moment < end:
                continue
            head = str(payload.get("head_sha", ""))
            if match[1] == "pr-review" and not re.fullmatch(r"[0-9a-f]{40}", head):
                raise ValueError("missing reviewed head")
            if pr_number is not None and (
                publisher not in REVIEW_PUBLISHERS
                or str(payload["pr"]) != str(pr_number)
                or not re.fullmatch(r"[0-9a-f]{40}", str(reviewed_head or ""))
                or head != reviewed_head
                or payload.get("reviewer_login", publisher) != publisher
            ):
                raise ValueError("review provenance mismatch")
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
                "head_sha": head if re.fullmatch(r"[0-9a-f]{40}", head) else "unknown",
                "signal_type": match[1], "categories": categories,
                "verdict": payload.get("verdict") if payload.get("verdict") in {
                    "Approve", "Approve with nits", "Request changes",
                    "approve", "approve_with_nits", "request_changes",
                } else "unknown",
                "source": provenance,
            }
            records.append(record)
        except (ValueError, KeyError, TypeError, AttributeError):
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
        if identity in found and record.get("feedback_type") == "human_edit":
            previous = found[identity]
            prs = sorted(set(previous["prs"] + record["prs"]), key=int)
            priority = {"agent": 3, "agent_assisted": 3, "content_corroborated": 2}
            if priority.get(previous.get("attribution", {}).get("status"), 0) > priority.get(
                    record.get("attribution", {}).get("status"), 0):
                record = previous
            record = {**record, "prs": prs}
            record["pr"] = record["prs"][0]
        found[identity] = record
    return list(found.values())


def edit_attribution(detail, comments, before, after, path):
    message = detail["commit"].get("message") or ""
    suggestion_author = re.fullmatch(
        r"Apply suggestion from @([\w-]+(?:\[bot\])?)", message.splitlines()[0] if message else "")
    if bot(detail.get("author")):
        return {"status": "agent", "confidence": "explicit", "reason": "bot account", "sources": []}
    if agent_commit(detail):
        return {"status": "agent_assisted", "confidence": "explicit",
                "reason": "agent author or coauthor attribution",
                "sources": []}
    if suggestion_author and bot({"login": suggestion_author[1]}):
        return {"status": "agent_assisted", "confidence": "explicit",
                "reason": "commit applies a bot-authored suggestion", "sources": []}
    attributed = []
    for item in comments:
        body = item.get("body") or ""
        if AGENT_ATTRIBUTION.search(body) and any(
            detail["sha"].startswith(ref)
            for ref in re.findall(r"\b[0-9a-f]{7,40}\b", body)
        ):
            attributed.append(str(item["id"]))
    if attributed:
        return {"status": "agent", "confidence": "explicit",
                "reason": "explicit agent reply links this commit",
                "sources": attributed}
    actor = detail.get("author") or {}
    verification = detail["commit"].get("verification") or {}
    if ((detail.get("committer") or {}).get("login") == "web-flow"
            and verification.get("verified") is True
            and actor.get("type") == "User" and suggestion_author):
        for item in comments:
            body = item.get("body") or ""
            if ((item.get("user") or {}).get("login") != suggestion_author[1]
                    or bot(item.get("user"))
                    or item.get("author_association") not in {"OWNER", "MEMBER", "COLLABORATOR"}
                    or item.get("path") != path
                    or item.get("commit_id") != detail["parents"][0]["sha"]
                    or AGENT_ATTRIBUTION.search(body) or sanitize(body) is None):
                continue
            try:
                if timestamp(item.get("created_at")) > timestamp(detail["commit"]["author"]["date"]):
                    continue
            except (ValueError, TypeError, AttributeError):
                continue
            suggestions = re.findall(r"```suggestion[^\n]*\n(.*?)\n```", body, re.S)
            line = item.get("original_line") or item.get("line")
            start_line = item.get("original_start_line") or item.get("start_line") or line
            original = before.splitlines()
            if (item.get("side") != "RIGHT" or type(line) is not int
                    or type(start_line) is not int or not 1 <= start_line <= line <= len(original)):
                continue
            if any(s.strip() and before != after and
                   original[:start_line - 1] + s.splitlines() + original[line:] == after.splitlines()
                   for s in suggestions):
                return {"status": "content_corroborated", "confidence": "content-only",
                        "reason": "suggestion matches parent/path diff; personal-account human origin unverified",
                        "sources": [str(item["id"])]}
    return {"status": "unresolved", "confidence": "unverified",
            "reason": "human account does not establish human authorship",
            "sources": []}


def patch_categories(patch):
    evidence = []
    for hunk in re.split(r"(?=^@@ )", patch, flags=re.M):
        removed = [line[1:] for line in hunk.splitlines() if line.startswith("-")]
        added = [line[1:] for line in hunk.splitlines() if line.startswith("+")]
        for old, new in zip(removed[:100], added[:100]):
            if (re.match(r"^#{1,6} ", old) and old != new
                    and old.casefold() == new.casefold() and len(old) <= 500):
                evidence.append({"change_category": "heading_case_change", "quality_direction": "unverified",
                                 "before": old, "after": new, "hunk": hunk.splitlines()[0]})
                if len(evidence) == 5:
                    return evidence
        old_counts = Counter(link for line in removed
                             for link in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", line))
        new_counts = Counter(link for line in added
                             for link in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", line))
        removed_counts, added_counts = old_counts - new_counts, new_counts - old_counts
        for label in sorted({label for label, _ in old_counts} & {label for label, _ in new_counts}):
            removed_urls = {url: count for (name, url), count in removed_counts.items() if name == label}
            added_urls = {url: count for (name, url), count in added_counts.items() if name == label}
            if removed_urls and added_urls and len(json.dumps([label, removed_urls, added_urls])) <= 1000:
                evidence.append({"change_category": "link_destination_change", "quality_direction": "unverified",
                                 "label": label, "removed_destinations": removed_urls,
                                 "added_destinations": added_urls, "hunk": hunk.splitlines()[0]})
                if len(evidence) == 5:
                    return evidence
    return evidence


class Collector:
    def __init__(self, args):
        self.args = args
        self.start, self.end = timestamp(args.start), timestamp(args.end)
        self.coverage = {"window": {"start": args.start, "end": args.end, "semantics": "[start,end) UTC"},
                         "counts": {}, "omissions": [], "discarded": {}}
        self.feedback, self.automated, self.edits = [], [], []
        self.commit_cache, self.blob_cache = {}, {}
        self.commit_status = {}

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
            if pages and isinstance(pages[0], dict) and "files" in pages[0]:
                if any(p["sha"] != pages[0]["sha"] or p["parents"] != pages[0]["parents"]
                       for p in pages):
                    raise ValueError("commit pagination provenance mismatch")
                files = [f for page in pages for f in page["files"]]
                if len(files) != len({f["filename"] for f in files}):
                    raise ValueError("duplicate paginated commit files")
                return {**pages[0], "files": files}
            return [item for page in pages for item in page]
        return self.command(argv)

    def blob(self, revision, path):
        key = revision, path
        if key not in self.blob_cache:
            value = self.api(f"contents/{quote(path, safe='/')}?ref={revision}")
            if value.get("type") != "file":
                raise ValueError("blob unavailable")
            if value.get("encoding") != "base64":
                raise ValueError("oversized_blob")
            raw = base64.b64decode("".join(value["content"].split()), validate=True)
            if len(raw) > 1000000:
                raise ValueError("oversized_blob")
            if b"\0" in raw:
                raise UnicodeError("binary blob")
            actual = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            if actual != value["sha"]:
                raise ValueError("blob identity mismatch")
            self.blob_cache[key] = raw.decode("utf-8"), value["sha"]
        return self.blob_cache[key]

    def human_edits(self, pr, commits, comments):
        first_agent = next((i for i, c in enumerate(commits) if agent_commit(c)), None)
        if first_agent is None:
            self.coverage["omissions"].append(
                f"PR {pr['number']}: no identifiable agent baseline for edit evidence")
            return
        for commit in commits[first_agent + 1:]:
            if bot(commit.get("author")):
                continue
            sha = commit["sha"]
            self.commit_status[sha] = "outside_window"
            try:
                when = commit["commit"]["author"]["date"]
                moment = timestamp(when)
            except (ValueError, KeyError, TypeError, AttributeError):
                self.commit_status[sha] = "invalid_timestamp"
                self.coverage["omissions"].append(f"commit {sha}: invalid human-edit timestamp")
                continue
            if not self.start <= moment < self.end:
                continue
            try:
                if sha not in self.commit_cache:
                    self.commit_cache[sha] = self.api(f"commits/{sha}?per_page=100", True)
                detail = self.commit_cache[sha]
                if detail["sha"] != sha:
                    raise ValueError("commit identity mismatch")
                parents = [p["sha"] for p in detail["parents"]]
                if any(not re.fullmatch(r"[0-9a-f]{40}", value) for value in [sha, *parents]):
                    raise ValueError("invalid commit provenance")
                self.commit_status[sha] = "inspected"
                if len(detail["files"]) >= 3000:
                    self.coverage["omissions"].append(f"commit {sha}: GitHub 3000-file cap")
                for file in detail["files"]:
                    if file["filename"].startswith("src/content/docs/"):
                        self.edit_file(pr, detail, file, parents, comments, when)
            except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired):
                self.commit_status[sha] = "source_unavailable"
                self.coverage["omissions"].append(f"commit {sha}: edit source unavailable")

    def edit_file(self, pr, detail, file, parents, comments, when):
        sha, path = detail["sha"], file["filename"]
        old_path = file.get("previous_filename", path) if file["status"] != "added" else ""
        new_path = path if file["status"] != "removed" else ""
        parent = parents[0] if parents else ""
        identity = [self.args.repo.lower(), sha, parent, old_path, new_path]
        source_id = "github:edit:" + hashlib.sha256(json.dumps(identity).encode()).hexdigest()
        record = {
            "date": when[:10], "timestamp": when, "pr": str(pr["number"]),
            "prs": [str(pr["number"])], "repo": self.args.repo.lower(),
            "commit_sha": sha, "parent_shas": parents, "parent_sha": parent,
            "file": path, "old_path": old_path, "new_path": new_path,
            "head_sha": pr["headRefOid"], "source_id": source_id,
            "legacy_source_id": f"github:commit:{sha}:{path}",
            "legacy_source_identity_sha256": hashlib.sha256(
                f"github:commit:{sha}:{path}".encode()).hexdigest(),
            "feedback_type": "human_edit", "skill_used": "factory/editorial",
            "verified_human": False, "pattern_category": "general", "tag": "",
            "severity": "unknown", "resolved_by": "unknown",
            "disposition": "unresolved_attribution", "patch_status": "not_retrieved",
            "author_login": (detail.get("author") or {}).get("login"),
        }
        if any(sanitize(p) != p or any(ord(c) < 32 for c in p) for p in [path, old_path, new_path]):
            record.update(file="unsafe-path", old_path="", new_path="",
                          legacy_source_id="", disposition="unsafe_path")
        elif len(parents) != 1:
            record["disposition"] = "merge_noise" if len(parents) > 1 else "parent_unavailable"
        else:
            try:
                before, before_sha = self.blob(parent, old_path) if old_path else ("", None)
                after, after_sha = self.blob(sha, new_path) if new_path else ("", None)
                if new_path and after_sha != file["sha"]:
                    raise ValueError("changed blob identity mismatch")
                record.update(before_blob_sha=before_sha, after_blob_sha=after_sha)
                record["attribution"] = edit_attribution(detail, comments, before, after, path)
                record["patch_source"] = "verified_parent_and_commit_blobs"
                record["before_url"] = (
                    f"https://github.com/{self.args.repo}/blob/{parent}/{quote(old_path, safe='/')}"
                    if old_path else None)
                record["after_url"] = (
                    f"https://github.com/{self.args.repo}/blob/{sha}/{quote(new_path, safe='/')}"
                    if new_path else None)
                raw_patch = "\n".join(difflib.unified_diff(
                    before.splitlines(), after.splitlines(), n=2, lineterm=""))
                patch = sanitize(raw_patch)
                if patch is None:
                    record.update(disposition="injection_excluded", patch_status="injection_excluded")
                else:
                    record.update(
                        patch=patch[:12000],
                        sanitized_patch_sha256=hashlib.sha256(patch.encode()).hexdigest(),
                        stored_patch_sha256=hashlib.sha256(patch[:12000].encode()).hexdigest(),
                        patch_status="complete" if len(patch) <= 12000 else "truncated",
                        redacted=patch != raw_patch,
                        category_evidence=patch_categories(patch[:12000]),
                    )
                    status = record["attribution"]["status"]
                    record["disposition"] = (
                        "agent_assisted" if status in {"agent", "agent_assisted"}
                        else "unresolved_attribution")
            except UnicodeError:
                record.update(disposition="binary_unavailable", patch_status="binary_unavailable")
            except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as error:
                status = "oversized_blob" if str(error) == "oversized_blob" else "blob_unavailable"
                record.update(disposition=status, patch_status=status)
        self.edits.append(record)
        if record["disposition"] not in {"merge_noise", "agent_assisted"}:
            self.coverage["omissions"].append(f"edit {source_id}: {record['disposition']}")
        elif record["patch_status"] == "truncated" or record.get("redacted"):
            self.coverage["omissions"].append(f"edit {source_id}: incomplete or redacted patch")

    def reconciliation(self):
        prior = getattr(self.args, "prior_feedback", None)
        if not prior:
            return []
        originals = {}
        for line in Path(prior).read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            if row.get("feedback_type") == "human_edit":
                originals[row["source_id"]] = row
        recovered = {row["legacy_source_identity_sha256"]: row for row in self.edits}
        manifest = []
        for source, original in sorted(originals.items()):
            digest = hashlib.sha256(source.encode()).hexdigest()
            row = recovered.get(digest)
            commit_match = re.match(r"github:commit:([0-9a-f]{40}):", source)
            sha = commit_match[1] if commit_match else ""
            entry = {
                "original_source_identity_sha256": digest,
                "original_source_id": source if sanitize(source) == source else "redacted:" + digest,
                "pr": original["pr"], "commit_sha": sha,
                "corrected_source_id": row["source_id"] if row else None,
                "disposition": row["disposition"] if row else "not_recovered",
                "reason": (
                    row.get("attribution", {}).get("reason", row["disposition"])
                    if row else self.commit_status.get(sha, "commit not found after identifiable agent baseline")),
            }
            manifest.append(entry)
        missing = sum(row["disposition"] == "not_recovered" for row in manifest)
        if missing:
            self.coverage["omissions"].append(f"{missing} original edit sources not recovered; see manifest")
        self.coverage["counts"]["original_edit_sources"] = len(manifest)
        self.coverage["counts"]["original_edit_dispositions"] = dict(Counter(
            row["disposition"] for row in manifest))
        return manifest

    def github(self):
        edits_only = getattr(self.args, "human_edits_only", False)
        prs = self.command([
            "gh", "pr", "list", "--repo", self.args.repo, "--state", "merged",
            "--search", f"merged:{self.start.date()}..{self.end.date()}",
            "--limit", "1000", "--json", "number,mergedAt,labels,author,body,headRefOid",
        ])
        if len(prs) == 1000:
            self.coverage["omissions"].append("GitHub PR search reached the 1000-result cap")
        selected = []
        for pr in prs:
            try:
                moment = timestamp(pr.get("mergedAt"))
            except (ValueError, TypeError, AttributeError):
                self.coverage["omissions"].append(
                    f"PR {pr.get('number', 'unknown')}: invalid merge timestamp")
                continue
            if self.start <= moment < self.end:
                selected.append(pr)
        prs = selected
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
                if not edits_only:
                    try:
                        checks = self.api(f"commits/{pr['headRefOid']}/check-runs?per_page=100")
                        if checks["total_count"] > len(checks["check_runs"]):
                            self.coverage["omissions"].append(f"PR {number}: head check list truncated")
                        required = [c for c in checks["check_runs"] if c["name"] in {
                            "Docs editorial quality", "Docs technical references"}]
                        pr["check_outcome"] = (
                            "pass" if len(required) == 2 and all(c["conclusion"] == "success" for c in required)
                            else "fail" if any(c["conclusion"] in {"failure", "timed_out", "cancelled"} for c in required)
                            else "unknown"
                        )
                    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired):
                        self.coverage["omissions"].append(f"PR {number}: head checks unavailable")
                inline_comments = []
                sources = (("comments", "review_comment"),) if edits_only else (
                    ("reviews", "review_verdict"), ("comments", "review_comment"))
                for suffix, kind in sources:
                    items = self.api(f"pulls/{number}/{suffix}?per_page=100", True)
                    if suffix == "comments":
                        inline_comments = items
                    if edits_only:
                        continue
                    for item in items:
                        if bot(item.get("user")) and suffix == "reviews":
                            signals, invalid = markers(
                                item.get("body") or "", f"github-review:{item['id']}",
                                item.get("submitted_at"), self.start, self.end,
                                pr_number=number, reviewed_head=item.get("commit_id"),
                                publisher=(item.get("user") or {}).get("login"),
                            )
                            self.automated.extend(signals)
                            if invalid:
                                self.coverage["omissions"].append(f"PR {number}: {invalid} invalid review markers")
                        record, reason = human_record(item, pr, kind, self.start, self.end)
                        if record:
                            self.feedback.append(record)
                        else:
                            discarded[reason] += 1
                            if reason == "invalid_timestamp":
                                self.coverage["omissions"].append(
                                    f"PR {number}: feedback {item['id']} has invalid timestamp")
                self.human_edits(pr, commits, inline_comments)
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
        selected = {}
        for run in runs:
            try:
                moment = timestamp(run.get("created_at"))
            except (ValueError, TypeError, AttributeError):
                self.coverage["omissions"].append(
                    f"run {run.get('run_id', 'unknown')}: invalid creation timestamp")
                continue
            if self.start <= moment < self.end and run["run_id"] != os.environ.get("OZ_RUN_ID"):
                selected[run["run_id"]] = run
        runs = selected
        self.coverage["counts"]["environment_runs"] = len(runs)

        def collect(run_id):
            try:
                detail = self.command([cli, "run", "get", run_id, "--output-format", "json"])
                if (not isinstance(detail, dict) or detail.get("run_id") != run_id
                        or "factory_uid" not in detail):
                    raise ValueError("missing factory provenance")
                if detail["factory_uid"] is None:
                    return "standalone", [], 0
                if not isinstance(detail["factory_uid"], str) or not detail["factory_uid"]:
                    raise ValueError("invalid factory provenance")
                if detail["factory_uid"] != self.args.factory:
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
        self.edits = unique(self.edits)
        accepted_edits = {row["source_id"] for row in self.edits if row["verified_human"]}
        self.feedback = unique([
            row for row in self.feedback
            if row.get("feedback_type") != "human_edit" or row["source_id"] in accepted_edits])
        self.automated = unique(self.automated)
        reconciliation = self.reconciliation()
        self.coverage["counts"]["edit_dispositions"] = dict(Counter(
            r["disposition"] for r in self.edits))
        self.coverage["counts"]["edit_file_identities"] = len(self.edits)
        self.coverage["counts"]["edit_commits"] = len({r["commit_sha"] for r in self.edits})
        self.coverage["scope"] = (
            "github-human-edits-only" if getattr(self.args, "human_edits_only", False)
            else "github-and-selected-environment")
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
        for name, records in (("feedback", self.feedback), ("automated", self.automated),
                              ("human-edits", self.edits), ("source-reconciliation", reconciliation)):
            (output / f"{name}.jsonl").write_text(
                "".join(json.dumps(r, sort_keys=True) + "\n" for r in records), encoding="utf-8")
        (output / "coverage.json").write_text(
            json.dumps(self.coverage, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("repo", "environment", "factory", "start", "end", "output-dir"):
        parser.add_argument(f"--{name}", required=True)
    parser.add_argument("--human-edits-only", action="store_true",
                        help="Revalidate GitHub edits without recollecting comments or run signals.")
    parser.add_argument("--prior-feedback",
                        help="Prior JSONL collection whose human-edit sources must be reconciled.")
    args = parser.parse_args()
    collector = Collector(args)
    if collector.end <= collector.start:
        parser.error("end must be after start")
    for name in (("github",) if args.human_edits_only else ("github", "runs")):
        try:
            getattr(collector, name)()
        except (OSError, ValueError, KeyError, subprocess.TimeoutExpired):
            collector.coverage["omissions"].append(f"{name} source unavailable")
    collector.write()
    print(json.dumps(collector.coverage, sort_keys=True))
    return 2 if collector.coverage["omissions"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
