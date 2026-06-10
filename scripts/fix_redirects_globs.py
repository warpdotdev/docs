#!/usr/bin/env python3
"""
Apply two improvements to the new redirects in vercel.json:
1. Replace 13 individual rules with 3 glob patterns (Petra's suggestion)
2. Add %2B-encoded duplicates for the 6 source paths containing literal '+'
"""
import json
from pathlib import Path

vercel_path = Path(__file__).parent.parent / "vercel.json"

# 1. Rules to remove (will be replaced by globs)
REMOVE = {
    "/guides/integrations/how-to-set-up-codex-cli",
    "/guides/integrations/how-to-set-up-gemini-cli",
    "/guides/integrations/how-to-set-up-ollama",
    "/guides/mcp-servers/context7-mcp-update-astro-project-with-best-practices",
    "/guides/mcp-servers/figma-remote-mcp-create-a-website-from-a-figma-file-from-scratch",
    "/guides/mcp-servers/github-mcp-summarizing-open-prs-and-creating-gh-issues",
    "/guides/mcp-servers/linear-mcp-retrieve-issue-data",
    "/guides/mcp-servers/linear-mcp-updating-tickets-with-a-lean-build-approach",
    "/guides/mcp-servers/puppeteer-mcp-scraping-amazon-web-reviews",
    "/guides/mcp-servers/sentry-mcp-fix-sentry-error-in-empower-website",
    "/guides/mcp-servers/sqlite-and-stripe-mcp-basic-queries-you-can-make-after-set-up",
    "/guides/developer-workflows/devops/how-to-analyze-cloud-run-logs-gcloud",
    "/guides/developer-workflows/devops/how-to-create-a-production-ready-docker-setup",
}

# 2. Paths with literal '+' that need %2B-encoded duplicates
PLUS_PATHS = [
    (
        "/guides/developer-workflows/beginner/how-to-create-project-rules-for-an-existing-project-astro-+-typescript-+-tailwind",
        "/guides/configuration/how-to-create-project-rules-for-an-existing-project-astro-typescript-tailwind/",
    ),
    (
        "/guides/developer-workflows/frontend-ui/how-to-actually-code-ui-that-matches-your-mockup-react-+-tailwind",
        "/guides/frontend/how-to-actually-code-ui-that-matches-your-mockup-react-tailwind/",
    ),
    (
        "/guides/developer-workflows/power-user/how-to-run-3-agents-in-parallel-summarize-logs-+-analyze-pr-+-modify-ui",
        "/guides/agent-workflows/how-to-run-3-agents-in-parallel-summarize-logs-analyze-pr-modify-ui/",
    ),
    (
        "/guides/end-to-end-builds/building-a-chrome-extension-d3.js-+-javascript-+-html-+-css",
        "/guides/build-an-app-in-warp/building-a-chrome-extension-d3js-javascript-html-css/",
    ),
    (
        "/guides/end-to-end-builds/building-a-real-time-chat-app-github-mcp-+-railway",
        "/guides/build-an-app-in-warp/building-a-real-time-chat-app-github-mcp-railway/",
    ),
    (
        "/guides/terminal-command-line-tips/improve-your-kubernetes-workflow-kubectl-+-helm",
        "/guides/devops/improve-your-kubernetes-workflow-kubectl-helm/",
    ),
]

with open(vercel_path) as f:
    vercel = json.load(f)

redirects = vercel["redirects"]
before = len(redirects)

# Remove individual rules being replaced by globs
redirects = [r for r in redirects if r["source"] not in REMOVE]
removed = before - len(redirects)
print(f"Removed {removed} individual rules")

existing_sources = {r["source"].lower() for r in redirects}
new_entries = []

# Add glob rules
new_entries.append({
    "source": "/guides/integrations/:slug*",
    "destination": "/guides/external-tools/:slug/",
    "statusCode": 308,
})
new_entries.append({
    "source": "/guides/mcp-servers/:slug*",
    "destination": "/guides/external-tools/:slug/",
    "statusCode": 308,
})
new_entries.append({
    "source": "/guides/developer-workflows/devops/:slug*",
    "destination": "/guides/devops/:slug/",
    "statusCode": 308,
})
print("Added 3 glob rules")

# Add %2B-encoded duplicates for + paths
for src_plus, dest in PLUS_PATHS:
    encoded = src_plus.replace("+", "%2B")
    if encoded.lower() not in existing_sources:
        new_entries.append({"source": encoded, "destination": dest, "statusCode": 308})
        print(f"  %2B variant: {encoded[:70]}...")

redirects.extend(new_entries)
vercel["redirects"] = redirects

with open(vercel_path, "w") as f:
    json.dump(vercel, f, indent=2)
    f.write("\n")

after = len(redirects)
print(f"\nDone. Redirects: {before} → {after} ({after - before:+d})")
print(f"  Removed {removed}, added {len(new_entries)} (3 globs + 6 %2B variants)")
