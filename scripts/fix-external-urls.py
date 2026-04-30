#!/usr/bin/env python3
"""Convert hardcoded https://docs.warp.dev/ URLs to internal links."""
import os, re

docs_dir = 'src/content/docs'

# Build valid internal paths
valid_paths = set()
for root, dirs, files in os.walk(docs_dir):
    for f in files:
        if not f.endswith('.mdx'): continue
        rel = os.path.relpath(os.path.join(root, f), docs_dir)
        slug = '/' + rel.replace('.mdx', '/').replace('/index/', '/')
        if slug == '/index/': slug = '/'
        valid_paths.add(slug.rstrip('/'))

# Old gitbook path -> new docs path mapping
PATH_REMAPPING = {
    '/agent-platform/warp-agents/agent-profiles-permissions': '/agent-platform/capabilities/agent-profiles-permissions',
    '/agent-platform/warp-agents/skills': '/agent-platform/capabilities/skills',
    '/agent-platform/warp-agents/planning': '/agent-platform/capabilities/planning',
    '/agent-platform/warp-agents/task-lists': '/agent-platform/capabilities/task-lists',
    '/agent-platform/warp-agents/model-choice': '/agent-platform/capabilities/model-choice',
    '/agent-platform/warp-agents/rules': '/agent-platform/capabilities/rules',
    '/agent-platform/warp-agents/full-terminal-use': '/agent-platform/capabilities/full-terminal-use',
    '/agent-platform/warp-agents/computer-use': '/agent-platform/capabilities/computer-use',
    '/agent-platform/warp-agents/codebase-context': '/agent-platform/capabilities/codebase-context',
    '/agent-platform/warp-agents/web-search': '/agent-platform/capabilities/web-search',
    '/agent-platform/warp-agents/mcp': '/agent-platform/capabilities/mcp',
    '/agent-platform/warp-agents/slash-commands': '/agent-platform/capabilities/slash-commands',
    '/agent-platform/warp-agents/agent-notifications': '/agent-platform/capabilities/agent-notifications',
    '/agent-platform/warp-agents/active-ai': '/agent-platform/local-agents/active-ai',
    '/agent-platform/warp-agents/code-diffs': '/agent-platform/local-agents/code-diffs',
    '/agent-platform/warp-agents/session-sharing': '/agent-platform/local-agents/session-sharing',
    '/agent-platform/warp-agents/cloud-conversations': '/agent-platform/local-agents/cloud-conversations',
    '/agent-platform/warp-agents/interactive-code-review': '/agent-platform/local-agents/interactive-code-review',
    '/agent-platform/warp-agents': '/agent-platform/local-agents/overview',
    '/agent-platform/warp-agents/interacting-with-agents': '/agent-platform/local-agents/interacting-with-agents',
    '/agent-platform/warp-agents/interacting-with-agents/terminal-and-agent-modes': '/agent-platform/local-agents/interacting-with-agents/terminal-and-agent-modes',
    '/agent-platform/local-agents/interacting-with-agents/agent-modality': '/agent-platform/local-agents/interacting-with-agents/terminal-and-agent-modes',
    '/agent-platform/warp-agents/interacting-with-agents/conversation-forking': '/agent-platform/local-agents/interacting-with-agents/conversation-forking',
    '/agent-platform/warp-agents/interacting-with-agents/voice': '/agent-platform/local-agents/interacting-with-agents/voice',
    '/agent-platform/warp-agents/agent-context': '/agent-platform/local-agents/agent-context',
    '/agent-platform/warp-agents/agent-context/blocks-as-context': '/agent-platform/local-agents/agent-context/blocks-as-context',
    '/agent-platform/warp-agents/agent-context/images-as-context': '/agent-platform/local-agents/agent-context/images-as-context',
    '/agent-platform/warp-agents/agent-context/urls-as-context': '/agent-platform/local-agents/agent-context/urls-as-context',
    '/agent-platform/warp-agents/agent-context/selection-as-context': '/agent-platform/local-agents/agent-context/selection-as-context',
    '/agent-platform/warp-agents/agent-context/using-to-add-context': '/agent-platform/local-agents/agent-context/using-to-add-context',
    '/agent-platform/third-party-agents': '/agent-platform/cli-agents/overview',
    '/agent-platform/cloud-agents/cloud-agents-overview': '/agent-platform/cloud-agents/overview',
    '/warp/code/code-review': '/code/code-review',
    '/warp/code/git-worktrees': '/code/git-worktrees',
    '/warp/knowledge-and-collaboration/warp-drive/agent-mode-context': '/knowledge-and-collaboration/warp-drive/agent-mode-context',
    '/warp/terminal/windows/vertical-tabs': '/terminal/windows/vertical-tabs',
    '/guides': '/university',
    '/guides/integrations/how-to-set-up-claude-code': '/university/integrations/how-to-set-up-claude-code',
    '/guides/integrations/how-to-set-up-codex-cli': '/university/integrations/how-to-set-up-codex-cli',
    '/guides/integrations/how-to-set-up-gemini-cli': '/university/integrations/how-to-set-up-gemini-cli',
    '/guides/integrations/how-to-set-up-opencode': '/university/integrations/how-to-set-up-opencode',
    '/knowledge-and-collaboration/rules': '/agent-platform/capabilities/rules',
    '/knowledge-and-collaboration/mcp': '/agent-platform/capabilities/mcp',
    '/code/codebase-context': '/agent-platform/capabilities/codebase-context',
    '/getting-started/installation-and-setup': '/getting-started/quickstart/installation-and-setup',
    '/getting-started/keyboard-shortcuts.md': '/getting-started/keyboard-shortcuts',
    '/support-and-community/plans-and-billing/plans-and-pricing': '/support-and-community/plans-and-billing/plans-pricing-refunds',
    '/reference/api-and-sdk/agent': '/reference/api-and-sdk',
    '/reference/cli/cli': '/reference/cli',
    '/reference/cli/mcp-for-cloud-agents': '/reference/cli/mcp-servers',
    # Additional remappings discovered during the 2026-04-29 sync.
    '/warp/code/code-editor': '/code/code-editor',
    '/warp/code/code-editor/file-tree': '/code/code-editor/file-tree',
    '/warp/code/code-editor/code-editor-vim-keybindings': '/code/code-editor/code-editor-vim-keybindings',
    '/warp/code/code-editor/find-and-replace': '/code/code-editor/find-and-replace',
    '/warp/code/code-editor/language-server-protocol': '/code/code-editor/language-server-protocol',
    '/warp/code/overview': '/code/overview',
    '/warp/code/ssh-feature-support': '/code/ssh-feature-support',
    '/warp/getting-started': '/getting-started/quickstart/installation-and-setup',
    '/warp/getting-started/installation-and-setup': '/getting-started/quickstart/installation-and-setup',
    '/warp/getting-started/coding-in-warp': '/getting-started/quickstart/coding-in-warp',
    '/warp/getting-started/customizing-warp': '/getting-started/quickstart/customizing-warp',
    '/warp/getting-started/migrate-to-warp': '/getting-started/migrate-to-warp',
    '/warp/getting-started/keyboard-shortcuts': '/getting-started/keyboard-shortcuts',
    '/warp/getting-started/supported-shells': '/getting-started/supported-shells',
    '/warp/getting-started/what-is-warp': '/',
    '/warp/getting-started/quickstart': '/quickstart',
    '/warp/terminal/windows/tab-configs': '/terminal/windows/tab-configs',
    '/warp/terminal/windows/configurable-toolbar': '/terminal/windows/configurable-toolbar',
    '/warp/terminal/settings': '/terminal/settings',
    '/warp/terminal/settings/all-settings': '/terminal/settings/all-settings',
    '/warp/knowledge-and-collaboration/admin-panel': '/knowledge-and-collaboration/admin-panel',
    '/warp/knowledge-and-collaboration/warp-drive': '/knowledge-and-collaboration/warp-drive',
    '/agent-platform/cli-agents': '/agent-platform/cli-agents/overview',
    '/guides/mcp-servers/github-mcp-summarizing-open-prs-and-creating-gh-issues': '/university/mcp-servers/github-mcp-summarizing-open-prs-and-creating-gh-issues',
    '/guides/mcp-servers/sentry-mcp-fix-sentry-error-in-empower-website': '/university/mcp-servers/sentry-mcp-fix-sentry-error-in-empower-website',
    '/guides/mcp-servers/linear-mcp-retrieve-issue-data': '/university/mcp-servers/linear-mcp-retrieve-issue-data',
    '/guides/mcp-servers/puppeteer-mcp-scraping-amazon-web-reviews': '/university/mcp-servers/puppeteer-mcp-scraping-amazon-web-reviews',
    '/guides/mcp-servers/context7-mcp-update-astro-project-with-best-practices': '/university/mcp-servers/context7-mcp-update-astro-project-with-best-practices',
}

stats = [0, 0, 0]  # total, converted, remapped

def replace_url(m):
    full_url = m.group(0)
    url_path = m.group(1)
    fragment = m.group(2) or ''
    stats[0] += 1
    
    clean_path = url_path.rstrip('/')
    
    if clean_path in valid_paths:
        stats[1] += 1
        return clean_path + '/' + fragment
    
    new_path = PATH_REMAPPING.get(clean_path)
    if new_path and new_path.rstrip('/') in valid_paths:
        stats[2] += 1
        return new_path + '/' + fragment
    
    return full_url

for root, dirs, files in os.walk(docs_dir):
    for f in files:
        if not f.endswith('.mdx'): continue
        if 'changelog' in root: continue
        
        path = os.path.join(root, f)
        content = open(path).read()
        
        new_content = re.sub(
            r'https://docs\.warp\.dev(/[^)\s"#]*)(#[^)\s"]*)?',
            replace_url,
            content
        )
        
        if new_content != content:
            open(path, 'w').write(new_content)

print(f"Total external URLs found: {stats[0]}")
print(f"Converted (direct match): {stats[1]}")
print(f"Converted (remapped): {stats[2]}")
print(f"Remaining unconverted: {stats[0] - stats[1] - stats[2]}")
