#!/usr/bin/env python3
"""Report warp-server feature flags that are not enabled in production.

Docs agents use this to apply Gate 0 (`.agents/references/docs-worthiness-criteria.md`)
to server-backed surfaces. A field the parser accepts, a JSON schema that
advertises it, a merged PR, a CHANGELOG marker, or a staging environment that
runs it is not evidence that customers can use it. `config/prod.yaml` is.

Commands:
    staging-only            List flags that are on in staging but not in production.
    check TERM [TERM ...]   Find flags related to each term: flags whose name contains
                            the term, and flags checked by Go functions that mention it.
    flag NAME [NAME ...]    Show the rollout of specific flags, by config key or Go
                            accessor name (for example `example_feature` or
                            `ExampleFeatureEnabled`).

Examples:
    python3 .agents/skills/doc_quality_policy/server_rollout.py staging-only
    python3 .agents/skills/doc_quality_policy/server_rollout.py check deferred required_repos
    python3 .agents/skills/doc_quality_policy/server_rollout.py flag example_feature

The warp-server checkout defaults to a sibling of the docs repo (`../warp-server`);
pass `--warp-server PATH` otherwise.

The output names private server flags and unreleased features. This repo is
public: never paste it into a page, PR body, PR comment, or committed file.
Record the verdict and the warp-server revision you checked instead.

Exit codes:
    0  No matched flag is off in production (`check`, `flag`), or the listing printed.
    1  At least one matched flag is off in production. For `check`, read the evidence:
       a name match is strong, a code match is a co-occurrence that needs judgment.
    2  Usage or environment error (missing checkout, unknown flag).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

DOCS_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_WARP_SERVER = DOCS_ROOT.parent / "warp-server"

FEATURES_GO = Path("config/features/features.go")
ENV_CONFIGS = {
    "prod": Path("config/prod.yaml"),
    "staging": Path("config/staging.yaml"),
}
# Config blocks that hold flag keys read by accessors in features.go.
FLAG_BLOCKS = ("features", "self_improvement")

SKIPPED_DIRS = {".git", "node_modules", "vendor", "client", "generated", "testdata"}
MIN_TERM_LENGTH = 4
MAX_CODE_MATCHES = 25
# A flag check counts as related to a term only when both sit in the same Go
# function within this many lines of each other. Large functions such as
# server.go's main() otherwise relate every flag to every term.
CO_OCCURRENCE_WINDOW = 20

_FUNC_HEADER = re.compile(r"^func ([A-Z]\w*)\(\) bool \{\s*$")
_GO_FUNC_HEADER = re.compile(r"^func (?:\([^)]*\) )?(\w+)\(")
_KEY_CALLS = (
    (re.compile(r'getFeatureEnabled\("([^"]+)"\)'), "features"),
    (re.compile(r'getSelfImprovementFlagEnabled\("([^"]+)"\)'), "self_improvement"),
    (re.compile(r'"features\.([A-Za-z0-9_]+)"'), "features"),
    (re.compile(r'"self_improvement\.([A-Za-z0-9_]+)"'), "self_improvement"),
)
_CALL = re.compile(r"\b([A-Za-z_][\w.]*)\(")
_KNOWN_CALLS = {
    "getFeatureEnabled",
    "getSelfImprovementFlagEnabled",
    "viper.GetBool",
    "viper.IsSet",
    "config.IsDogfood",
    "config.IsStaging",
}
_FEATURE_CALL = re.compile(r"\bfeatures\.([A-Z]\w*)\(")


@dataclass
class Accessor:
    """One exported `func Name() bool` in config/features/features.go."""

    name: str
    keys: List[Tuple[str, str]] = field(default_factory=list)
    env_conditions: List[str] = field(default_factory=list)
    delegates: List[str] = field(default_factory=list)
    unknown_calls: List[str] = field(default_factory=list)
    has_or: bool = False
    default_when_unset: bool = False


@dataclass
class Rollout:
    name: str
    keys: List[str]
    prod: Optional[bool]
    staging: Optional[bool]

    @property
    def state(self) -> str:
        if self.prod is True:
            return "on-in-prod"
        if self.prod is False and self.staging is True:
            return "staging-only"
        if self.prod is False:
            return "off"
        return "unknown"

    def to_dict(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "keys": self.keys,
            "prod": self.prod,
            "staging": self.staging,
            "state": self.state,
        }


def parse_accessors(features_go: str) -> Dict[str, Accessor]:
    """Parse every `func Name() bool` body in features.go into its conditions."""
    accessors: Dict[str, Accessor] = {}
    lines = features_go.splitlines()
    index = 0
    while index < len(lines):
        match = _FUNC_HEADER.match(lines[index])
        if not match:
            index += 1
            continue
        name = match.group(1)
        body_lines = []
        index += 1
        while index < len(lines) and lines[index] != "}":
            body_lines.append(lines[index])
            index += 1
        accessors[name] = _accessor_from_body(name, "\n".join(body_lines))
        index += 1
    for accessor in accessors.values():
        for call in list(accessor.unknown_calls):
            if call in accessors:
                accessor.unknown_calls.remove(call)
                accessor.delegates.append(call)
    return accessors


def _accessor_from_body(name: str, body: str) -> Accessor:
    accessor = Accessor(name=name)
    code = "\n".join(line.split("//", 1)[0] for line in body.splitlines())
    for pattern, block in _KEY_CALLS:
        for key in pattern.findall(code):
            if (block, key) not in accessor.keys:
                accessor.keys.append((block, key))
    if "config.IsDogfood(" in code:
        accessor.env_conditions.append("dogfood")
    if "config.IsStaging(" in code:
        accessor.env_conditions.append("staging")
    if "viper.IsSet(" in code and re.search(r"\breturn true\b", code):
        accessor.default_when_unset = True
    accessor.has_or = "||" in code
    for call in _CALL.findall(code):
        if call in _KNOWN_CALLS or call in accessor.unknown_calls:
            continue
        accessor.unknown_calls.append(call)
    return accessor


def parse_flag_blocks(config_yaml: str, blocks: Sequence[str] = FLAG_BLOCKS) -> Dict[Tuple[str, str], Optional[bool]]:
    """Read first-level `key: bool` entries under each named top-level YAML block.

    Non-boolean values map to None. Deeper nesting is ignored.
    """
    values: Dict[Tuple[str, str], Optional[bool]] = {}
    current: Optional[str] = None
    child_indent: Optional[int] = None
    for raw in config_yaml.splitlines():
        line = raw.split(" #", 1)[0].rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent == 0:
            key = line.split(":", 1)[0].strip()
            current = key if key in blocks and line.rstrip().endswith(":") else None
            child_indent = None
            continue
        if current is None:
            continue
        if child_indent is None:
            child_indent = indent
        if indent != child_indent or ":" not in line:
            continue
        key, _, value = line.strip().partition(":")
        value = value.strip().strip("'\"").lower()
        if value in ("true", "false"):
            values[(current, key.strip())] = value == "true"
        else:
            values[(current, key.strip())] = None
    return values


def _and(values: Iterable[Optional[bool]]) -> Optional[bool]:
    result: Optional[bool] = True
    for value in values:
        if value is False:
            return False
        if value is None:
            result = None
    return result


def evaluate(
    name: str,
    accessors: Dict[str, Accessor],
    env: str,
    config: Dict[Tuple[str, str], Optional[bool]],
    _stack: Tuple[str, ...] = (),
) -> Optional[bool]:
    """Evaluate an accessor in one environment. None means it can't be determined."""
    accessor = accessors.get(name)
    if accessor is None or name in _stack:
        return None
    conditions: List[Optional[bool]] = []
    for key in accessor.keys:
        if key in config:
            conditions.append(config[key])
        else:
            conditions.append(True if accessor.default_when_unset else False)
    for condition in accessor.env_conditions:
        conditions.append(env != "prod" if condition in ("dogfood", "staging") else None)
    for delegate in accessor.delegates:
        conditions.append(evaluate(delegate, accessors, env, config, _stack + (name,)))
    if accessor.unknown_calls:
        conditions.append(None)
    if not conditions:
        return None
    result = _and(conditions)
    if accessor.has_or and result is False:
        # An OR can still be true when one operand is false; don't guess.
        return None
    return result


@dataclass
class ServerRollouts:
    accessors: Dict[str, Accessor]
    configs: Dict[str, Dict[Tuple[str, str], Optional[bool]]]

    def rollout(self, name: str) -> Rollout:
        accessor = self.accessors[name]
        return Rollout(
            name=name,
            keys=[f"{block}.{key}" for block, key in accessor.keys],
            prod=evaluate(name, self.accessors, "prod", self.configs["prod"]),
            staging=evaluate(name, self.accessors, "staging", self.configs["staging"]),
        )

    def key_rollout(self, block: str, key: str) -> Rollout:
        prod = self.configs["prod"].get((block, key), False)
        staging = self.configs["staging"].get((block, key), False)
        return Rollout(name=f"{block}.{key}", keys=[f"{block}.{key}"], prod=prod, staging=staging)

    def all_rollouts(self) -> List[Rollout]:
        rollouts = [self.rollout(name) for name in sorted(self.accessors)]
        accessor_keys = {key for accessor in self.accessors.values() for key in accessor.keys}
        config_keys = set(self.configs["prod"]) | set(self.configs["staging"])
        for block, key in sorted(config_keys - accessor_keys):
            rollouts.append(self.key_rollout(block, key))
        return rollouts

    def find(self, name: str) -> List[Rollout]:
        """Look up an accessor by Go name, or a config key (bare or block-qualified)."""
        if name in self.accessors:
            return [self.rollout(name)]
        known_keys = (
            set(self.configs["prod"])
            | set(self.configs["staging"])
            | {key for accessor in self.accessors.values() for key in accessor.keys}
        )
        for block in FLAG_BLOCKS:
            bare = name.split(".", 1)[1] if name.startswith(block + ".") else name
            if (block, bare) in known_keys:
                return [self.key_rollout(block, bare)]
        return []


def load(warp_server: Path) -> ServerRollouts:
    features_go = warp_server / FEATURES_GO
    if not features_go.is_file():
        raise FileNotFoundError(f"{features_go} not found; pass --warp-server PATH")
    configs = {}
    for env, relative in ENV_CONFIGS.items():
        path = warp_server / relative
        if not path.is_file():
            raise FileNotFoundError(f"{path} not found; pass --warp-server PATH")
        configs[env] = parse_flag_blocks(path.read_text(encoding="utf-8"))
    return ServerRollouts(parse_accessors(features_go.read_text(encoding="utf-8")), configs)


def normalize(text: str) -> str:
    return re.sub(r"[_\-\s]", "", text.lower())


@dataclass
class CodeMatch:
    path: str
    line: int
    function: str
    rollout: Rollout


def iter_go_functions(text: str) -> Iterable[Tuple[int, str, List[str]]]:
    """Yield (start line, function name, body lines) for each top-level Go function."""
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        match = _GO_FUNC_HEADER.match(lines[index])
        if not match:
            index += 1
            continue
        start = index
        index += 1
        while index < len(lines) and lines[index] != "}":
            index += 1
        yield start + 1, match.group(1), lines[start : index + 1]
        index += 1


def iter_go_files(warp_server: Path) -> Iterable[Path]:
    for root, dirs, files in os.walk(warp_server):
        dirs[:] = [d for d in dirs if d not in SKIPPED_DIRS]
        for name in files:
            if name.endswith(".go") and not name.endswith("_test.go"):
                yield Path(root) / name


def code_matches(warp_server: Path, rollouts: ServerRollouts, term: str) -> List[CodeMatch]:
    needle = normalize(term)
    features_dir = (warp_server / FEATURES_GO).parent
    matches: List[CodeMatch] = []
    for path in iter_go_files(warp_server):
        if path.parent == features_dir:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if needle not in normalize(text) or "features." not in text:
            continue
        for start, function, body in iter_go_functions(text):
            term_lines = [offset for offset, line in enumerate(body) if needle in normalize(line)]
            if not term_lines:
                continue
            seen = set()
            for offset, line in enumerate(body):
                for accessor in _FEATURE_CALL.findall(line):
                    if accessor in seen or accessor not in rollouts.accessors:
                        continue
                    if min(abs(offset - term_line) for term_line in term_lines) > CO_OCCURRENCE_WINDOW:
                        continue
                    seen.add(accessor)
                    matches.append(
                        CodeMatch(
                            path=path.relative_to(warp_server).as_posix(),
                            line=start + offset,
                            function=function,
                            rollout=rollouts.rollout(accessor),
                        )
                    )
    return sorted(matches, key=lambda match: (match.rollout.prod is not False, match.path, match.line))


def name_matches(rollouts: ServerRollouts, term: str) -> List[Rollout]:
    needle = normalize(term)
    return [
        rollout
        for rollout in rollouts.all_rollouts()
        if needle in normalize(rollout.name) or any(needle in normalize(key) for key in rollout.keys)
    ]


def _fmt(value: Optional[bool]) -> str:
    return {True: "on", False: "off", None: "unknown"}[value]


def _describe(rollout: Rollout) -> str:
    keys = f" [{', '.join(rollout.keys)}]" if rollout.keys and rollout.keys != [rollout.name] else ""
    return f"{rollout.name}{keys}: prod={_fmt(rollout.prod)} staging={_fmt(rollout.staging)} -> {rollout.state}"


def cmd_staging_only(rollouts: ServerRollouts, as_json: bool) -> int:
    rows = [rollout for rollout in rollouts.all_rollouts() if rollout.state == "staging-only"]
    if as_json:
        print(json.dumps([row.to_dict() for row in rows], indent=2))
        return 0
    print(f"{len(rows)} flags are on in staging but not in production. Do not document their behavior.")
    print("This list is private. Do not paste it into a public page, PR, or comment.")
    for row in rows:
        print(f"  {_describe(row)}")
    return 0


def cmd_flag(rollouts: ServerRollouts, names: Sequence[str], as_json: bool) -> int:
    results: List[Rollout] = []
    missing = []
    for name in names:
        found = rollouts.find(name)
        if not found:
            missing.append(name)
        results.extend(found)
    if as_json:
        print(json.dumps({"flags": [r.to_dict() for r in results], "unknown_names": missing}, indent=2))
    else:
        for result in results:
            print(_describe(result))
        for name in missing:
            print(f"{name}: no accessor in {FEATURES_GO} and no key in the prod or staging config", file=sys.stderr)
    if missing:
        return 2
    return 1 if any(result.prod is not True for result in results) else 0


def cmd_check(warp_server: Path, rollouts: ServerRollouts, terms: Sequence[str], as_json: bool) -> int:
    report = []
    blocked = False
    for term in terms:
        if len(normalize(term)) < MIN_TERM_LENGTH:
            print(f"Term {term!r} is too short to search reliably; use at least {MIN_TERM_LENGTH} characters.", file=sys.stderr)
            return 2
        by_name = name_matches(rollouts, term)
        by_code = code_matches(warp_server, rollouts, term)
        if any(r.prod is False for r in by_name) or any(m.rollout.prod is False for m in by_code):
            blocked = True
        report.append((term, by_name, by_code))
    if as_json:
        print(
            json.dumps(
                [
                    {
                        "term": term,
                        "name_matches": [r.to_dict() for r in by_name],
                        "code_matches": [
                            {"path": m.path, "line": m.line, "function": m.function, **m.rollout.to_dict()}
                            for m in by_code
                        ],
                    }
                    for term, by_name, by_code in report
                ],
                indent=2,
            )
        )
        return 1 if blocked else 0
    for term, by_name, by_code in report:
        print(f"Term: {term}")
        print("  Flags whose name matches:")
        if not by_name:
            print("    none")
        for rollout in by_name:
            print(f"    {_describe(rollout)}")
        print("  Flags checked by Go functions that mention the term:")
        if not by_code:
            print("    none")
        for match in by_code[:MAX_CODE_MATCHES]:
            print(f"    {match.path}:{match.line} {match.function}() -> {_describe(match.rollout)}")
        if len(by_code) > MAX_CODE_MATCHES:
            print(f"    ... {len(by_code) - MAX_CODE_MATCHES} more (use --json for all)")
    if blocked:
        print(
            "\nAt least one related flag is off in production. Treat the surface as unreleased (Gate 0 deferral)"
            " unless the evidence shows the flag gates something else."
        )
    else:
        print(
            "\nNo related flag is off in production. This does not prove the surface shipped; confirm the"
            " release with the changelog or a production check before documenting it."
        )
    return 1 if blocked else 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("--warp-server", type=Path, default=DEFAULT_WARP_SERVER, help="Path to the warp-server checkout.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("staging-only", help="List flags on in staging but not in production.")
    check = subcommands.add_parser("check", help="Find flags related to user-facing terms.")
    check.add_argument("terms", nargs="+")
    flag = subcommands.add_parser("flag", help="Show the rollout of specific flags.")
    flag.add_argument("names", nargs="+")
    args = parser.parse_args(argv)

    try:
        rollouts = load(args.warp_server)
    except FileNotFoundError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if args.command == "staging-only":
        return cmd_staging_only(rollouts, args.json)
    if args.command == "flag":
        return cmd_flag(rollouts, args.names, args.json)
    return cmd_check(args.warp_server, rollouts, args.terms, args.json)


if __name__ == "__main__":
    sys.exit(main())
