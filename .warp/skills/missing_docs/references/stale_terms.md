# Stale Terms

Known outdated or incorrect terminology that should be flagged during audits.
The audit script reads this file to check existing docs for stale language.

# Format: `term to search for -> reason it's stale` (one per line within each section).
# Lines starting with `#` are comments. Blank lines are ignored.
# All term matching is case-insensitive.

# Maintenance: when AGENTS.md "Terms to avoid" or "Terminology Standards" changes,
# mirror updates here. Run the audit to verify new terms catch real issues.

## Renamed or removed features

warp ai -> Renamed to Agent Mode
ai command -> Legacy term — now Agent Mode
generate command -> Legacy feature — replaced by Agent Mode
warp terminal -> Prefer 'Warp' unless distinguishing from Oz
natural language command -> Legacy term — now Agent Mode

## Incorrect branding or casing

ai credits -> Use 'credits' without the AI prefix
mac os -> Use 'macOS'

## Deprecated terminology

ozzies -> Use 'Oz agents', 'instances', or 'Oz subagents'
warp agent -> Use 'Agent' or 'Oz agent' depending on context
warp agents -> Use 'Agents' or 'Oz agents' depending on context
agent-mode -> Use 'Agent Mode' (two words, no hyphen)
deploying an oz -> Use 'Deploying an Oz agent'
the oz agent -> Use 'An Oz agent' or 'A parent Oz agent'
oz is running -> Use 'An Oz agent is running' or 'A run is in progress'
