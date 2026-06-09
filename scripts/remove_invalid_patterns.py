#!/usr/bin/env python3
"""Remove source patterns that contain regex metacharacters (+ and .) invalid in path-to-regexp v6."""
import json
from pathlib import Path

REMOVE = {
    "/guides/developer-workflows/beginner/how-to-create-project-rules-for-an-existing-project-astro-+-typescript-+-tailwind",
    "/guides/developer-workflows/frontend-ui/how-to-actually-code-ui-that-matches-your-mockup-react-+-tailwind",
    "/guides/developer-workflows/power-user/how-to-run-3-agents-in-parallel-summarize-logs-+-analyze-pr-+-modify-ui",
    "/guides/end-to-end-builds/building-a-real-time-chat-app-github-mcp-+-railway",
    "/guides/terminal-command-line-tips/improve-your-kubernetes-workflow-kubectl-+-helm",
    "/guides/end-to-end-builds/building-a-chrome-extension-d3.js-+-javascript-+-html-+-css",
}

vercel_path = Path(__file__).parent.parent / "vercel.json"
with open(vercel_path) as f:
    vercel = json.load(f)

before = len(vercel["redirects"])
vercel["redirects"] = [r for r in vercel["redirects"] if r.get("source") not in REMOVE]
removed = before - len(vercel["redirects"])

with open(vercel_path, "w") as f:
    json.dump(vercel, f, indent=2)
    f.write("\n")

print(f"Removed {removed} invalid patterns. Redirects: {before} → {len(vercel['redirects'])}")
