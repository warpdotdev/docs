#!/usr/bin/env python3
"""Shared agent-doc quality policy for warpdotdev/docs.

Pure, stdlib-only functions for:
  * the canonical agent marker and risk levels,
  * parsing the `## Documentation risk` and `## Unverified claims` PR-body
    sections,
  * finding `{/* VERIFY: ... */}` markers in changed content,
  * classifying risk from explicit diff signals (the low-risk allowlist), and
  * validating the human-gate contract, including docs-team overrides.

See `.agents/references/doc-quality-policy.md` for the rules this module
enforces. This module has no side effects (no `gh`, no network, no git) so it
stays trivially unit-testable; `check_pr_contract.py` wraps it for CI/CLI use.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, fields
from typing import Dict, List, Optional, Sequence

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

AGENT_MARKER = "warpy-factory"

RISK_LOW = "low"
RISK_ENGINEERING_REVIEW_REQUIRED = "engineering-review-required"
VALID_RISK_LEVELS = (RISK_LOW, RISK_ENGINEERING_REVIEW_REQUIRED)

DOC_RISK_HEADING = "## Documentation risk"
UNVERIFIED_CLAIMS_HEADING = "## Unverified claims"

OVERRIDE_MODE_VERIFIED = "docs-verified"
OVERRIDE_MODE_WAIVER = "docs-waiver"
OVERRIDE_MODE_NONE = "none"
VALID_OVERRIDE_MODES = (OVERRIDE_MODE_VERIFIED, OVERRIDE_MODE_WAIVER, OVERRIDE_MODE_NONE)
VALID_ENGINEERING_REVIEW_STATUSES = ("not-applicable", "pending", "approved")

# {/* VERIFY: flag name from PRD, unconfirmed against warp-internal */}
VERIFY_MARKER_RE = re.compile(r"\{/\*\s*VERIFY:\s*(.*?)\s*\*/\}", re.DOTALL)


# ---------------------------------------------------------------------------
# VERIFY marker accounting
# ---------------------------------------------------------------------------

def find_verify_markers(text: str) -> List[str]:
    """Return the claim text of every `{/* VERIFY: ... */}` marker in `text`."""
    return [m.group(1).strip() for m in VERIFY_MARKER_RE.finditer(text)]


# ---------------------------------------------------------------------------
# PR-body section parsing
# ---------------------------------------------------------------------------

def extract_section(body: str, heading: str) -> Optional[str]:
    """Return the text under `heading` up to the next heading of the same-or-
    higher level, or None if the heading is absent.
    """
    lines = body.splitlines()
    level = len(heading) - len(heading.lstrip("#"))
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading.strip():
            start = i + 1
            break
    if start is None:
        return None
    end = len(lines)
    for i in range(start, len(lines)):
        stripped = lines[i]
        m = re.match(r"^(#{1,6})\s+\S", stripped)
        if m and len(m.group(1)) <= level:
            end = i
            break
    return "\n".join(lines[start:end]).strip("\n")


_FIELD_LINE_RE = re.compile(r"^\s*([A-Za-z][A-Za-z ]*[A-Za-z]):\s*(.*)$")

# Maps a human-readable field label (case-insensitive) to the canonical key
# used in the parsed dict.
_FIELD_LABELS = {
    "risk": "risk",
    "rationale": "rationale",
    "source files consulted": "source_files_consulted",
    "requested engineering reviewers": "requested_engineering_reviewers",
    "engineering review status": "engineering_review_status",
    "docs override": "docs_override",
    "override reviewer": "override_reviewer",
    "override reason": "override_reason",
    "override evidence": "override_evidence",
    "override head sha": "override_head_sha",
}

_LIST_FIELDS = {"source_files_consulted", "requested_engineering_reviewers"}


@dataclass
class DocumentationRisk:
    risk: Optional[str] = None
    rationale: Optional[str] = None
    source_files_consulted: List[str] = None
    requested_engineering_reviewers: List[str] = None
    engineering_review_status: Optional[str] = None
    docs_override: str = OVERRIDE_MODE_NONE
    override_reviewer: Optional[str] = None
    override_reason: Optional[str] = None
    override_evidence: Optional[str] = None
    override_head_sha: Optional[str] = None

    def __post_init__(self) -> None:
        if self.source_files_consulted is None:
            self.source_files_consulted = []
        if self.requested_engineering_reviewers is None:
            self.requested_engineering_reviewers = []


def parse_documentation_risk_section(body: str) -> Optional[DocumentationRisk]:
    """Parse the `## Documentation risk` section into a `DocumentationRisk`.

    Returns None when the section is absent. Unrecognized lines are ignored
    so free-form prose alongside the `Key: value` lines does not break parsing.
    """
    section = extract_section(body, DOC_RISK_HEADING)
    if section is None:
        return None

    values: Dict[str, str] = {}
    for line in section.splitlines():
        m = _FIELD_LINE_RE.match(line)
        if not m:
            continue
        label = m.group(1).strip().lower()
        key = _FIELD_LABELS.get(label)
        if key is None:
            continue
        values[key] = m.group(2).strip()

    kwargs: Dict[str, object] = {}
    for key, raw in values.items():
        if key in _LIST_FIELDS:
            kwargs[key] = [item.strip() for item in raw.split(",") if item.strip()]
        else:
            kwargs[key] = raw

    risk = kwargs.get("risk")
    if isinstance(risk, str):
        kwargs["risk"] = risk.strip().lower()
    docs_override = kwargs.get("docs_override")
    if isinstance(docs_override, str):
        kwargs["docs_override"] = docs_override.strip().lower()
    else:
        kwargs["docs_override"] = OVERRIDE_MODE_NONE
    engineering_review_status = kwargs.get("engineering_review_status")
    if isinstance(engineering_review_status, str):
        kwargs["engineering_review_status"] = engineering_review_status.strip().lower()

    return DocumentationRisk(**kwargs)


def parse_unverified_claims_section(body: str) -> Optional[List[str]]:
    """Return the bullet items under `## Unverified claims`, or None if absent.

    A section containing only the "None — ..." sentinel line returns [].
    """
    section = extract_section(body, UNVERIFIED_CLAIMS_HEADING)
    if section is None:
        return None
    items: List[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.lower().startswith("none"):
            continue
        if stripped.startswith(("-", "*")):
            items.append(stripped.lstrip("-* ").strip())
    return items


# ---------------------------------------------------------------------------
# Risk classification (the low-risk allowlist)
# ---------------------------------------------------------------------------

@dataclass
class RiskSignals:
    """Explicit, per-category signals describing what a diff touches.

    Each field is one of the engineering-review triggers in the low-risk
    allowlist (see `.agents/references/doc-quality-policy.md`). Every field
    defaults to True (the conservative/unknown default) so a caller must
    affirmatively clear a trigger before it can be excluded — this encodes
    "ambiguous risk classification defaults to engineering-review-required"
    at the type level rather than relying on every call site remembering it.
    """

    adds_new_or_changed_feature_page: bool = True
    changes_commands_or_code_examples: bool = True
    changes_api_behavior: bool = True
    changes_ui_labels_or_paths: bool = True
    changes_defaults: bool = True
    changes_permissions: bool = True
    changes_availability_or_platform_support: bool = True
    changes_plan_eligibility: bool = True
    changes_billing_behavior: bool = True
    changes_security_or_privacy_claims: bool = True
    changes_data_handling: bool = True
    changes_self_hosting_behavior: bool = True
    changes_integration_setup: bool = True
    # Low risk requires a positive match to one of these allowlisted
    # categories after every technical-claim trigger above has been cleared.
    is_editorial_or_metadata_only: bool = False
    # Internal docs tooling, skills, and CI changes that make no public
    # product claim may use the low-risk path when every technical-claim
    # trigger above has been affirmatively cleared.
    is_docs_workflow_tooling_only: bool = False

    # Not allowlist triggers themselves, but always force engineering review
    # when true, per the VERIFY-accounting and review-severity rules.
    has_unresolved_verify_marker: bool = False
    has_critical_or_important_review_finding: bool = False

    @classmethod
    def all_clear(cls, **overrides: bool) -> "RiskSignals":
        """Build signals with every allowlist trigger cleared (False) except
        `overrides`. Convenience for tests and callers who have positively
        confirmed a PR touches none of the trigger categories.
        """
        clear = {f.name: False for f in fields(cls) if f.name not in (
            "has_unresolved_verify_marker", "has_critical_or_important_review_finding",
        )}
        clear["is_editorial_or_metadata_only"] = True
        clear.update(overrides)
        return cls(**clear)


_ALLOWLIST_TRIGGER_FIELDS: Sequence[str] = tuple(
    f.name for f in fields(RiskSignals)
    if f.name not in (
        "is_docs_workflow_tooling_only",
        "is_editorial_or_metadata_only",
        "has_unresolved_verify_marker",
        "has_critical_or_important_review_finding",
    )
)


def classify_risk(signals: RiskSignals) -> str:
    """Classify a PR's risk from explicit low-risk-allowlist signals.

    Any allowlist trigger, an unresolved VERIFY marker, or a critical/
    important review finding forces `engineering-review-required`. Only a PR
    with every trigger cleared is `low`.
    """
    if signals.has_unresolved_verify_marker:
        return RISK_ENGINEERING_REVIEW_REQUIRED
    if signals.has_critical_or_important_review_finding:
        return RISK_ENGINEERING_REVIEW_REQUIRED
    if any(getattr(signals, name) for name in _ALLOWLIST_TRIGGER_FIELDS):
        return RISK_ENGINEERING_REVIEW_REQUIRED
    if not (signals.is_editorial_or_metadata_only or signals.is_docs_workflow_tooling_only):
        return RISK_ENGINEERING_REVIEW_REQUIRED
    return RISK_LOW


# ---------------------------------------------------------------------------
# Contract validation
# ---------------------------------------------------------------------------

def validate_pr_contract(
    body: str,
    verify_markers: Sequence[str],
    *,
    current_head_sha: Optional[str] = None,
    authorized_docs_reviewers: Sequence[str] = (),
    deterministic_checks_passed: bool = True,
    has_unresolved_critical_or_important_finding: bool = False,
    source_owner_approved_current_head: bool = False,
    approved_reviewers_current_head: Sequence[str] = (),
    enforce_engineering_gate: bool = False,
) -> List[str]:
    """Validate the PR contract. Returns a list of violation messages.

    Structural validation (the required CI check) always verifies the risk
    metadata and VERIFY accounting. The human engineering gate is deliberately
    opt-in because a pending approval is normal while an
    engineering-review-required PR is being drafted and reviewed.
    """
    problems: List[str] = []

    risk_section = parse_documentation_risk_section(body)
    if risk_section is None:
        return [f"missing required section: {DOC_RISK_HEADING!r}"]

    claims = parse_unverified_claims_section(body)
    if claims is None:
        problems.append(f"missing required section: {UNVERIFIED_CLAIMS_HEADING!r}")
        claims = []

    if risk_section.risk not in VALID_RISK_LEVELS:
        problems.append(
            f"invalid risk level {risk_section.risk!r}; must be one of {VALID_RISK_LEVELS}"
        )
    if (
        risk_section.engineering_review_status is not None
        and risk_section.engineering_review_status not in VALID_ENGINEERING_REVIEW_STATUSES
    ):
        problems.append(
            "invalid engineering review status "
            f"{risk_section.engineering_review_status!r}; must be one of "
            f"{VALID_ENGINEERING_REVIEW_STATUSES}"
        )
    if (
        risk_section.risk == RISK_LOW
        and risk_section.engineering_review_status not in (None, "not-applicable")
    ):
        problems.append(
            "low-risk PRs must omit Engineering review status or set it to 'not-applicable'"
        )

    unlisted = [m for m in verify_markers if m not in claims]
    if unlisted:
        problems.append(
            f"{len(unlisted)} VERIFY marker(s) not listed in {UNVERIFIED_CLAIMS_HEADING!r}: "
            f"{unlisted}"
        )

    if verify_markers and risk_section.risk == RISK_LOW:
        problems.append(
            "risk is 'low' but the diff has an unresolved VERIFY marker; "
            f"must be {RISK_ENGINEERING_REVIEW_REQUIRED!r}"
        )

    if enforce_engineering_gate and risk_section.risk == RISK_ENGINEERING_REVIEW_REQUIRED:
        problems.extend(
            validate_engineering_gate(
                risk_section,
                current_head_sha=current_head_sha,
                authorized_docs_reviewers=authorized_docs_reviewers,
                deterministic_checks_passed=deterministic_checks_passed,
                has_unresolved_critical_or_important_finding=has_unresolved_critical_or_important_finding,
                source_owner_approved_current_head=source_owner_approved_current_head,
                approved_reviewers_current_head=approved_reviewers_current_head,
            )
        )

    return problems


def validate_engineering_gate(
    risk_section: DocumentationRisk,
    *,
    current_head_sha: Optional[str],
    authorized_docs_reviewers: Sequence[str],
    deterministic_checks_passed: bool,
    has_unresolved_critical_or_important_finding: bool,
    source_owner_approved_current_head: bool,
    approved_reviewers_current_head: Sequence[str] = (),
) -> List[str]:
    """Validate the engineering-review-required human gate for one PR.

    Satisfied by a source-owner approval on the current head, or by a
    complete, non-stale, authorized docs-team override. Neither path can
    substitute for a failing deterministic check or an unresolved
    critical/important review finding.
    """
    problems: List[str] = []

    blocking = not deterministic_checks_passed or has_unresolved_critical_or_important_finding
    if blocking:
        if not deterministic_checks_passed:
            problems.append("deterministic checks have not passed; no override can bypass this")
        if has_unresolved_critical_or_important_finding:
            problems.append(
                "an unresolved critical/important review-docs-pr finding exists; "
                "no override can bypass this"
            )

    if source_owner_approved_current_head and not blocking:
        return problems

    override_mode = risk_section.docs_override or OVERRIDE_MODE_NONE
    if override_mode == OVERRIDE_MODE_NONE:
        if not blocking:
            problems.append(
                "engineering-review-required PR has no source-owner approval on the "
                "current head and no docs-team override recorded"
            )
        return problems

    if override_mode not in (OVERRIDE_MODE_VERIFIED, OVERRIDE_MODE_WAIVER):
        problems.append(f"invalid docs override mode: {override_mode!r}")
        return problems

    if blocking:
        problems.append(
            f"docs override ({override_mode}) cannot satisfy the gate while a "
            "deterministic check is failing or a critical/important finding is unresolved"
        )
        return problems

    required = ("override_reviewer", "override_reason", "override_evidence", "override_head_sha")
    missing = [f for f in required if not getattr(risk_section, f)]
    if missing:
        problems.append(f"docs override ({override_mode}) missing required field(s): {missing}")
        return problems

    # No truthy-guard on `authorized_docs_reviewers`: an empty allowlist (a
    # failed or unavailable trusted-ref lookup) must fail closed -- treated
    # as "no one is authorized" -- never as "the allowlist check is skipped".
    if risk_section.override_reviewer not in authorized_docs_reviewers:
        problems.append(
            f"docs override author {risk_section.override_reviewer!r} is not an "
            "authorized Pod-Docs reviewer"
        )
    elif risk_section.override_reviewer not in approved_reviewers_current_head:
        problems.append(
            f"docs override author {risk_section.override_reviewer!r} has not approved "
            "the current head"
        )

    if not current_head_sha:
        problems.append(
            "cannot verify docs override freshness: no current head SHA was supplied"
        )
    elif risk_section.override_head_sha != current_head_sha:
        problems.append(
            f"docs override head SHA {risk_section.override_head_sha!r} does not match "
            f"the current head {current_head_sha!r}; a new commit invalidates the override"
        )

    return problems
