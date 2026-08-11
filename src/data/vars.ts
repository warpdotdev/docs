// src/data/vars.ts
// Single source of truth for product names and key strings.
// To rename: update the value here. Body prose (MDX imports) and
// frontmatter (Vite transform) update automatically on next build.
//
// Key naming rule: keys are stable identifiers, not current brand names.
// Use the future/conceptual name as the key; the value holds the current string.

export const VARS = {
  // Platform — keys named for upcoming Warp branding; values are current Oz names
  WARP_AUTOMATION_PLATFORM: "Oz",             // value → "Warp Automation Platform" at rename
  WARP_AGENT_CLI:           "Oz CLI",         // value → "Warp Agent CLI" at rename
  WEB_APP:                  "Oz web app",     // future name TBD
  WEB_APP_URL:              "https://oz.warp.dev", // value → "https://app.warp.dev" at rename
  DASHBOARD:                "Oz dashboard",   // future name TBD
  PLATFORM_RUN:             "Oz run",         // future name TBD

  // Warp Agent CLI — the standalone terminal front-end (the `warp` binary).
  // Launch name confirmed via the launch blog draft (2026-07-28).
  //
  // NOTE: the WARP_AGENT_CLI key above was reserved for renaming the Oz CLI to
  // this same name. That overlap is now resolved by product direction: at the
  // next launch (approximately 2026-08-18) the Oz CLI is retired and wrapped
  // into the Warp Agent CLI, leaving a single CLI. The two keys are expected to
  // collapse into one at that point. Keeping them separate until the
  // convergence ships, since merging them now would rewrite prose across both
  // CLI doc surfaces.
  WARP_CLI:                 "Warp Agent CLI",

  // Feature names (stable — keys and values expected to remain unchanged)
  AGENT_MODE:               "Agent Mode",
  WARP_DRIVE:               "Warp Drive",
  WARP_TERMINAL:            "Warp Terminal",

  // Billing (stable)
  CREDITS:                  "credits",
  ADD_ON_CREDITS:           "Add-on Credits",

  // URLs
  CONTACT_SALES_URL:        "https://www.warp.dev/contact-sales",
} as const;
