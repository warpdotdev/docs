#!/usr/bin/env python3
"""
Add missing redirect entries to vercel.json identified by audit_redirects.py.
Covers 52 paths from the GitBook → Astro migration audit, plus 2 known gaps
from the traffic analysis (BYOK and model-choice).

Usage:
    python3 scripts/add_missing_redirects.py [--dry-run]
"""

import json
import argparse
from pathlib import Path

# Old source path (no leading slash) → new destination URL
MAPPINGS = {
    # Agent platform section root ----------------------------------------
    "agent-platform/warp-agents": "/agent-platform/",

    # guides/developer-workflows/backend ---------------------------------
    "guides/developer-workflows/backend/how-to-create-priority-matrix-for-database-optimization":
        "/guides/devops/how-to-create-priority-matrix-for-database-optimization/",
    "guides/developer-workflows/backend/how-to-write-sql-commands-inside-a-postgres-repl":
        "/guides/devops/how-to-write-sql-commands-inside-a-postgres-repl/",

    # guides/developer-workflows/beginner --------------------------------
    "guides/developer-workflows/beginner/10-coding-features-you-should-know":
        "/guides/getting-started/10-coding-features-you-should-know/",
    "guides/developer-workflows/beginner/how-to-create-project-rules-for-an-existing-project-astro-+-typescript-+-tailwind":
        "/guides/configuration/how-to-create-project-rules-for-an-existing-project-astro-typescript-tailwind/",
    "guides/developer-workflows/beginner/how-to-customize-warps-appearance":
        "/guides/getting-started/how-to-customize-warps-appearance/",
    "guides/developer-workflows/beginner/how-to-explain-your-codebase-using-warp-rust-codebase":
        "/guides/agent-workflows/how-to-explain-your-codebase-using-warp-rust-codebase/",
    "guides/developer-workflows/beginner/how-to-make-warps-ui-more-minimal":
        "/guides/getting-started/how-to-make-warps-ui-more-minimal/",
    "guides/developer-workflows/beginner/how-to-master-warps-code-review-panel":
        "/guides/getting-started/how-to-master-warps-code-review-panel/",
    "guides/developer-workflows/beginner/trigger-reusable-actions-with-saved-prompts":
        "/guides/configuration/trigger-reusable-actions-with-saved-prompts/",
    "guides/developer-workflows/beginner/welcome-to-warp":
        "/guides/getting-started/welcome-to-warp/",

    # guides/developer-workflows/devops ----------------------------------
    "guides/developer-workflows/devops/how-to-analyze-cloud-run-logs-gcloud":
        "/guides/devops/how-to-analyze-cloud-run-logs-gcloud/",
    "guides/developer-workflows/devops/how-to-create-a-production-ready-docker-setup":
        "/guides/devops/how-to-create-a-production-ready-docker-setup/",

    # guides/developer-workflows/frontend-ui ----------------------------
    "guides/developer-workflows/frontend-ui/how-to-actually-code-ui-that-matches-your-mockup-react-+-tailwind":
        "/guides/frontend/how-to-actually-code-ui-that-matches-your-mockup-react-tailwind/",
    "guides/developer-workflows/frontend-ui/how-to-replace-a-ui-element-in-warp-rust-codebase":
        "/guides/frontend/how-to-replace-a-ui-element-in-warp-rust-codebase/",

    # guides/developer-workflows (top-level) ----------------------------
    "guides/developer-workflows/how-to-review-ai-generated-code":
        "/guides/agent-workflows/how-to-review-ai-generated-code/",
    "guides/developer-workflows/how-to-run-multiple-ai-coding-agents":
        "/guides/agent-workflows/how-to-run-multiple-ai-coding-agents/",
    "guides/developer-workflows/how-to-use-voice-and-images-to-prompt-coding-agents":
        "/guides/agent-workflows/how-to-use-voice-and-images-to-prompt-coding-agents/",
    "guides/developer-workflows/warp-for-product-managers":
        "/guides/agent-workflows/warp-for-product-managers/",

    # guides/developer-workflows/power-user -----------------------------
    "guides/developer-workflows/power-user/how-to-configure-yolo-and-strategic-agent-profiles":
        "/guides/configuration/how-to-configure-yolo-and-strategic-agent-profiles/",
    "guides/developer-workflows/power-user/how-to-edit-agent-code-in-warp":
        "/guides/agent-workflows/how-to-edit-agent-code-in-warp/",
    "guides/developer-workflows/power-user/how-to-review-prs-like-a-senior-dev":
        "/guides/agent-workflows/how-to-review-prs-like-a-senior-dev/",
    "guides/developer-workflows/power-user/how-to-run-3-agents-in-parallel-summarize-logs-+-analyze-pr-+-modify-ui":
        "/guides/agent-workflows/how-to-run-3-agents-in-parallel-summarize-logs-analyze-pr-modify-ui/",
    "guides/developer-workflows/power-user/how-to-set-coding-best-practices":
        "/guides/configuration/how-to-set-coding-best-practices/",
    "guides/developer-workflows/power-user/how-to-set-coding-preferences-with-rules":
        "/guides/configuration/how-to-set-coding-preferences-with-rules/",
    "guides/developer-workflows/power-user/how-to-set-tech-stack-preferences-with-rules":
        "/guides/configuration/how-to-set-tech-stack-preferences-with-rules/",
    "guides/developer-workflows/power-user/how-to-set-up-self-serve-data-analytics-with-skills":
        "/guides/configuration/how-to-set-up-self-serve-data-analytics-with-skills/",
    "guides/developer-workflows/power-user/how-to-sync-your-monorepos":
        "/guides/configuration/how-to-sync-your-monorepos/",
    "guides/developer-workflows/power-user/how-to-use-agent-profiles-efficiently":
        "/guides/configuration/how-to-use-agent-profiles-efficiently/",

    # guides/developer-workflows/testing-and-security -------------------
    "guides/developer-workflows/testing-and-security/how-to-generate-unit-and-security-tests-to-debug-faster":
        "/guides/devops/how-to-generate-unit-and-security-tests-to-debug-faster/",
    "guides/developer-workflows/testing-and-security/how-to-prevent-secrets-from-leaking":
        "/guides/devops/how-to-prevent-secrets-from-leaking/",

    # guides/end-to-end-builds ------------------------------------------
    "guides/end-to-end-builds/building-a-chrome-extension-d3.js-+-javascript-+-html-+-css":
        "/guides/build-an-app-in-warp/building-a-chrome-extension-d3js-javascript-html-css/",
    "guides/end-to-end-builds/building-a-real-time-chat-app-github-mcp-+-railway":
        "/guides/build-an-app-in-warp/building-a-real-time-chat-app-github-mcp-railway/",

    # guides/how-warp-uses-warp -----------------------------------------
    "guides/how-warp-uses-warp/building-warps-input-with-warp":
        "/guides/build-an-app-in-warp/building-warps-input-with-warp/",
    "guides/how-warp-uses-warp/creating-rules-for-agents":
        "/guides/configuration/creating-rules-for-agents/",
    "guides/how-warp-uses-warp/running-multiple-agents-at-once-with-warp":
        "/guides/agent-workflows/running-multiple-agents-at-once-with-warp/",
    "guides/how-warp-uses-warp/understanding-your-codebase":
        "/guides/agent-workflows/understanding-your-codebase/",
    "guides/how-warp-uses-warp/using-images-as-context-with-warp":
        "/guides/agent-workflows/using-images-as-context-with-warp/",
    "guides/how-warp-uses-warp/using-mcp-servers-with-warp":
        "/guides/external-tools/using-mcp-servers-with-warp/",

    # guides/integrations -----------------------------------------------
    "guides/integrations/how-to-set-up-codex-cli":
        "/guides/external-tools/how-to-set-up-codex-cli/",
    "guides/integrations/how-to-set-up-gemini-cli":
        "/guides/external-tools/how-to-set-up-gemini-cli/",
    "guides/integrations/how-to-set-up-ollama":
        "/guides/external-tools/how-to-set-up-ollama/",

    # guides/mcp-servers ------------------------------------------------
    "guides/mcp-servers/context7-mcp-update-astro-project-with-best-practices":
        "/guides/external-tools/context7-mcp-update-astro-project-with-best-practices/",
    "guides/mcp-servers/figma-remote-mcp-create-a-website-from-a-figma-file-from-scratch":
        "/guides/external-tools/figma-remote-mcp-create-a-website-from-a-figma-file-from-scratch/",
    "guides/mcp-servers/github-mcp-summarizing-open-prs-and-creating-gh-issues":
        "/guides/external-tools/github-mcp-summarizing-open-prs-and-creating-gh-issues/",
    "guides/mcp-servers/linear-mcp-retrieve-issue-data":
        "/guides/external-tools/linear-mcp-retrieve-issue-data/",
    "guides/mcp-servers/linear-mcp-updating-tickets-with-a-lean-build-approach":
        "/guides/external-tools/linear-mcp-updating-tickets-with-a-lean-build-approach/",
    "guides/mcp-servers/puppeteer-mcp-scraping-amazon-web-reviews":
        "/guides/external-tools/puppeteer-mcp-scraping-amazon-web-reviews/",
    "guides/mcp-servers/sentry-mcp-fix-sentry-error-in-empower-website":
        "/guides/external-tools/sentry-mcp-fix-sentry-error-in-empower-website/",
    "guides/mcp-servers/sqlite-and-stripe-mcp-basic-queries-you-can-make-after-set-up":
        "/guides/external-tools/sqlite-and-stripe-mcp-basic-queries-you-can-make-after-set-up/",

    # guides/terminal-command-line-tips ---------------------------------
    "guides/terminal-command-line-tips/improve-your-kubernetes-workflow-kubectl-+-helm":
        "/guides/devops/improve-your-kubernetes-workflow-kubectl-helm/",

    # guides/warp-runtime (page removed, send to guides landing) --------
    "guides/warp-runtime/building-a-slackbot": "/guides/",

    # Known traffic gaps from earlier data analysis ---------------------
    "support-and-community/plans-and-billing/bring-your-own-api-key":
        "/agent-platform/inference/bring-your-own-api-key/",
    "agent-platform/capabilities/model-choice":
        "/agent-platform/inference/model-choice/",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true",
                        help="Print entries without writing to vercel.json")
    args = parser.parse_args()

    vercel_path = Path(__file__).parent.parent / "vercel.json"
    with open(vercel_path) as f:
        vercel = json.load(f)

    existing = {
        r["source"].lower().rstrip("/").split("#")[0]
        for r in vercel.get("redirects", [])
    }

    new_entries = []
    skipped = []
    for old, dest in MAPPINGS.items():
        source = f"/{old}"
        if source.lower().rstrip("/") in existing:
            skipped.append(source)
            continue
        new_entries.append({"source": source, "destination": dest, "statusCode": 308})

    print(f"New entries: {len(new_entries)}  |  Already covered: {len(skipped)}")
    for e in new_entries:
        print(f"  {e['source']}")
        print(f"    → {e['destination']}")

    if args.dry_run:
        print("\n[DRY RUN] vercel.json not modified.")
        return

    vercel["redirects"].extend(new_entries)
    with open(vercel_path, "w") as f:
        json.dump(vercel, f, indent=2)
        f.write("\n")

    print(f"\nWrote {len(new_entries)} new redirects to {vercel_path.name}.")


if __name__ == "__main__":
    main()
