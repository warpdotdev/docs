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
  // Renamed per HYC (8/17), same shape as PLATFORM_RUN below: a plain
  // platform-level term, with "factory dashboard" written directly on pages
  // that are specifically about a factory. Lowercase: "Warp Factories" is the
  // product, a "factory" is an instance, and a bare capitalized "Factory" is
  // never a proper noun (AGENTS.md -> Warp Factories terminology).
  //
  // "Runs page" was the other candidate and reads better in isolation, but it
  // names a single page in the web app. This surface is defined as unified
  // across the Warp app and web, and its Warp-app half is the Agent Management
  // Panel, not a Runs page. The descriptive term keeps that meaning.
  //
  // Lowercase common noun, so capitalize only at the start of a sentence or
  // bullet -- which the variable cannot do, so avoid putting it there.
  DASHBOARD:                "cloud agent dashboard",
  // Renamed per HYC (8/17): the platform-level default is the plain
  // descriptive phrase, not a branded one. Factory-specific pages should write
  // "factory run" directly rather than reaching for this variable.
  //
  // Kept singular so `{VARS.PLATFORM_RUN}s` pluralizes correctly at the call
  // sites that do that.
  PLATFORM_RUN:             "cloud agent run",
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
