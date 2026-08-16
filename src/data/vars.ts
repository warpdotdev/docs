// src/data/vars.ts
// Single source of truth for product names and key strings.
// To rename: update the value here. Body prose (MDX imports) and
// frontmatter (Vite transform) update automatically on next build.
//
// Key naming rule: keys are stable identifiers, not current brand names.
// Use the future/conceptual name as the key; the value holds the current string.

export const VARS = {
  // Platform — renamed 8/18. The remaining Oz-valued keys below are the
  // deliberate 9/15 holdouts: the `oz` binary and the Oz v1 webapp keep their
  // names until that date, so they are NOT stale, they are pending.
  //
  // IMPORTANT: "Automation Platform" is a common-noun phrase, not a proper
  // noun like "Oz" was. Referential uses need a definite article in the prose
  // ("with the {VARS.WARP_AUTOMATION_PLATFORM}", "The {VARS.…} provides");
  // attributive uses do not ("{{…}} settings", "{{…}}-hosted"). style_lint
  // enforces this. Do not add a bare referential use.
  WARP_AUTOMATION_PLATFORM: "Automation Platform",
  WARP_AGENT_CLI:           "Oz CLI",         // the `oz` binary — holds until 9/15, then "Warp Agent CLI"
  WEB_APP:                  "Oz web app",     // legacy Oz v1 webapp (oz.warp.dev) — holds until 9/15
  WEB_APP_URL:              "https://oz.warp.dev", // holds until 9/15, then "https://app.warp.dev"
  // DASHBOARD and PLATFORM_RUN intentionally held at their Oz values through
  // 9/15 rather than flipped with the platform name. Both name surfaces of the
  // Oz v1 webapp, which keeps its name until then, so flipping them now would
  // make the docs disagree with what the reader sees on screen.
  DASHBOARD:                "Oz dashboard",
  PLATFORM_RUN:             "Oz run",
  API_SDK_NAME:             "Oz API & SDK",   // holds until 9/15, then "Warp API & SDK"

  // Warp Factories web app — a net-new product surface at platform.warp.dev
  // (soft launch ~2026-08-18), separate from the legacy Oz v1 webapp above.
  // Not rename-sensitive: this is a new reference, not a flip of existing
  // Oz-branded text, so it isn't in style_lint.py's RENAME_SENSITIVE_VAR_STRINGS.
  FACTORY_WEB_APP:          "Warp Factories web app",
  FACTORY_WEB_APP_URL:      "https://platform.warp.dev",

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
