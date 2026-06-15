# Vercel Firewall challenge blocks the AFDocs audit

When every AFDocs check fails or the audit reports a "SPA shell" with content
past 50%, the most likely cause is **not** a docs regression — it's that
`docs.warp.dev` is sitting behind a **Vercel Firewall bot challenge**. The
`afdocs` crawler is a non-browser HTTP client, so it can't solve the
JavaScript challenge and never reaches real content. Every check becomes a
false positive.

The audit script (`scripts/afdocs_audit.mjs`) now detects this up front and
aborts with an `invalid` status (exit code `2`) instead of publishing a
misleading score.

## How to confirm

```bash
curl -sS -D - -o /dev/null https://docs.warp.dev/llms.txt
```

You are blocked by a challenge if the response shows **any** of:

- `HTTP/2 429`
- `x-vercel-mitigated: challenge`
- an `x-vercel-challenge-token:` header
- `server: Vercel` serving an HTML "Vercel Security Checkpoint" body

A spoofed browser `User-Agent` does **not** help — Vercel's Bot Protection
specifically flags non-browser clients that claim to be a browser (e.g. a
`curl`/`fetch` request identifying as Chrome).

## Root cause

The 429 + `x-vercel-mitigated: challenge` signal comes from one of two
Vercel Firewall features on the project that serves `docs.warp.dev`:

- **Attack Challenge Mode** (Firewall → Bot Management → Attack Mode). Usually
  toggled on temporarily during a DDoS attack. If left on, it challenges all
  traffic that isn't a Vercel-*verified* bot.
- **Bot Protection managed ruleset** in **challenge** mode, which serves a
  JavaScript challenge to all non-browser traffic.

In both modes Vercel auto-allows its directory of *verified* bots (Googlebot,
verified webhook providers, etc.), but the `afdocs` audit runner is not a
verified bot, so it is challenged and blocked.

> This is a platform/firewall configuration, not a docs-repo bug. The repo
> already implements every AFDocs remediation (llms.txt, `.md` variants,
> `src/middleware.ts` content negotiation, in-page llms directives, and
> `.well-known/mcp.json`).

## Remediation

The `afdocs` CLI cannot send a custom header or User-Agent
(`npx afdocs check --help` exposes no such flag), so a header-based WAF bypass
is not possible through the audit tool. Use one of the following Vercel-side
fixes (requires Firewall permissions on the `docs.warp.dev` project).

### Option A — Disable Attack Mode (if it was left on)

Vercel's automatic DDoS mitigation stays active without Attack Mode, so this
is safe once the targeted attack is over.

- Dashboard: project → **Firewall** → **Bot Management** → **Attack Mode** →
  **Disable**.
- CLI: `vercel firewall attack-mode disable` (applies immediately).

Verify with the `curl` command above — a healthy response is `HTTP 200` with
no `x-vercel-mitigated` header.

### Option B — Switch Bot Protection to Log mode

If the Bot Protection managed ruleset is in **challenge** mode, switch it to
**log** mode (project → **Firewall** → **Bot Management**) so non-browser
agents — including AI doc consumers — aren't challenged.

### Option C — Allow the audit runner through (keep protection on)

Add a **System Bypass rule** or a **WAF custom rule with a `bypass` action**
that matches the audit runner's egress IP, so the runner gets a valid score
while the rest of the site stays protected.

```bash
# Example: bypass the firewall for a known runner IP
vercel firewall rules add "AFDocs audit bypass" \
  --condition '{"type":"ip_address","op":"eq","value":"RUNNER_IP"}' \
  --action bypass --yes
vercel firewall publish
```

Because the audit tool can't send a secret header, prefer an IP match. If the
runner has no stable egress IP, run the audit from an allowlisted network, or
use Option A/B around the audit window.

## Why this also matters beyond the audit

Challenge mode blocks **all** non-browser clients that aren't Vercel-verified
bots, not just the audit runner. That can defeat the purpose of the
agent-friendly docs work: AI agents and crawlers that aren't in Vercel's
verified directory may also be unable to fetch `llms.txt` or `.md` content.
Keeping Attack/Challenge mode off (relying on Vercel's always-on DDoS
mitigation) is the agent-friendly default; reserve challenge mode for active
attacks.
