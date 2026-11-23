# Documentation social previews

## Summary

Generate page-specific 1200×630 previews with stable section labels and complete,
balanced titles. [PR #956](https://github.com/warpdotdev/docs/pull/956) implements
this contract on `factory/dynamic-og-images`.

- Status: approved and implemented.
- Requester: `hongyi-chen`.
- Approval: [gray-label proposal](https://github.com/warpdotdev/docs/blob/0967f2266845e67d8350e7b74e44a6487463ddd4/specs/og-section-headers/SPEC.md),
  approved with “yes go ahead, show me screenshots”.
- Source: [request and typography refinements](https://warpdev.slack.com/archives/C09BVK0PL3Y/p1795414196360039).
  The final dimensions below incorporate the requester's readability,
  Medium-weight, spacing, and smaller balanced-headline decisions.

## Section ownership

1. Show one uppercase section label above the title on recognized section pages.
   Use TERMINAL, AGENTS, FACTORIES, AUTOMATION PLATFORM, CHANGELOG, SUPPORT,
   ENTERPRISE, or GUIDES. Match the existing tab names, including plural AGENTS.
2. Resolve the section from the page's canonical URL family. Do not use the
   referrer, a selected tab, query parameters, an anchor, or navigation order.
3. Apply this mapping to both each listed route and its descendants. Match
   complete path segments, not arbitrary string prefixes.

   | URL family | Section label |
   | --- | --- |
   | `/terminal`, `/code`, `/knowledge-and-collaboration`, `/getting-started` | TERMINAL |
   | `/quickstart` | TERMINAL |
   | `/agents` | AGENTS |
   | `/factories`, `/api` | FACTORIES |
   | `/platform` | AUTOMATION PLATFORM |
   | `/changelog` | CHANGELOG |
   | `/support-and-community` | SUPPORT |
   | `/enterprise` | ENTERPRISE |
   | `/guides` | GUIDES |

4. Omit the section label on `/`, `/404`, and routes outside these families.
   An unlisted page inside a recognized family still receives that family's label.
5. A guide inside `/factories/guides` receives FACTORIES. A factory tutorial
   inside `/guides` receives GUIDES. The label identifies the docs section,
   not every subject mentioned by the page.

Shared billing pages (`credits` and `add-on-credits`) receive SUPPORT.
`/platform/transitioning-from-oz` receives AUTOMATION PLATFORM even when
linked from Factories. A social crawler sees the canonical URL, not the
navigation path. URL-family ownership avoids navigation-order ambiguity
without adding per-page frontmatter or changing tab activation.

## Visual design

| Element | Contract |
| --- | --- |
| Canvas | 1200×630, chrome-blue `#D5DFE2`, 64px outer margins |
| Lockup | Complete black Warp lockup at the upper left |
| Pill | DOCUMENTATION at the upper right, `#1008FF`, black outline, white Azeret SemiMono Medium text, −2% tracking |
| Title | Black uppercase Azeret SemiMono Medium, −5% tracking, 105% leading, maximum rendered size 100px |
| Title bounds | 1072px width, 280px maximum height, left edge x=64px, bottom edge y=566px |
| Section eyebrow | Uppercase Azeret SemiMono Medium, 48px, opaque `#555555`, −2% tracking, 115% leading |
| Eyebrow position | One line within 1072px, x=64px, bottom edge 32px above the rendered title |

The eyebrow moves with the fitted title block. The lockup and pill stay fixed.
Root and unknown routes use the same title layout without an eyebrow.
Do not add ellipses, a subtitle, a divider, or a footer.

Gray keeps the section secondary to the black title. Using linearized-sRGB
luminance, `#555555` against `#D5DFE2` has a contrast ratio of **5.4964:1**.
Keep section text at or above 4.5:1. The reference palette's lighter `#8D8B82`
does not qualify: it produces only **2.5183:1**.

### Title fitting and balancing

1. Find the largest fitting title size from 112px down to 28px in 2px steps,
   using the actual Medium font and the title bounds above.
2. Reduce that fitted size to 90%, rounded down to an even pixel, with a 28px
   floor. This reduces both short headlines and long titles that already
   require smaller type.
3. Measure whole-word lines. Choose the fewest feasible lines, then minimize
   the sum of squared unused widths, including the final line. Preserve word
   order and the complete title.
4. Retain Pango's character wrapping and Unicode fallback for overwide tokens
   or a balanced layout that exceeds the bounds. Use the default image if
   the renderer cannot fit the complete title legibly.

## Build and metadata

- `src/lib/og-image.js` renders the card from the title and optional section.
- `src/lib/social-image.js` owns section resolution, rendered-H1 extraction
  with a document-title fallback, and shared OG/Twitter metadata. Alt text
  includes the section when present, for example
  `Warp Docs — Agents — Skills for agents`.
- `src/integrations/og-images.js` generates previews during production builds,
  not `astro dev`. It resolves routes relative to the output root, normalizes
  `index.html`, `.html`, and trailing slashes, and replaces only head metadata.
  Article HTML stays byte-for-byte intact.
- Equal title-section pairs share a card. Different sections do not reuse the
  wrong card. Asset URLs use PNG-content hashes.
- Untitled pages and render or asset-write failures use `/og-image.png`.
  Brand-font download or checksum failures stop the build rather than
  silently substituting a font.
- Azeret downloads are hash-pinned and cached for offline builds. Decoded fonts
  stay in an OS temporary directory, outside git and deployed output.
  Bundled Inter and Noto fallback fonts retain their licenses and sources in
  `src/assets/og/fonts/`.
- `scripts/validate-og-images.mjs` checks page metadata and referenced PNGs;
  `src/integrations/og-images.test.js` covers rendering and failure behavior.

## Out of scope

- Navigation or information-architecture changes.
- Section-specific colors, multiple labels, breadcrumbs, or new themes.
- Title truncation, title rewrites, or a different font distribution mechanism.
- New runtime image endpoints or changes to third-party unfurl caches.

## Validation criteria

### Automated checks

- Run `npm ci` in the implementation checkout.
- Run `npm run test:og-images`. Its regressions cover:
  - All eight labels, grouped URL families, `/api`, and `/quickstart`.
  - Shared billing → SUPPORT and transition → AUTOMATION PLATFORM.
  - Known-family unlisted pages, root, 404, unknown routes, and segment
    boundaries such as `/agents-extra`.
  - Equivalent nested `index.html`, `.html`, and trailing-slash routes.
  - Equal title-section pairs deduplicate; equal titles in different sections
    produce different PNGs and correct metadata.
  - Every label fits on one line; label, title, logo, and pill do not overlap.
    Preserve 64px margins, title bounds, colors, and full title text.
  - Opaque gray eyebrows, black titles, and at least 4.5:1 text contrast
    calculated from linearized-sRGB relative luminance.
  - Short, long, unbroken, Unicode, and markup-like titles with a section.
  - Smaller type on both short and previously fitted long titles, measured
    balanced word breaks, and complete titles without orphaned final words
    when a more balanced layout fits without adding lines.
  - Existing font-failure, offline-cache, fallback, write-failure, and
    article-body-preservation behavior.
- Run `npm run typecheck` and `npm run test:heading-vars`.
- Run `npm run build`, then `npm run test:og-output`. Record actual page,
  preview, and fallback counts. Require zero unexpected fallbacks.
- Run `npm run test:heading-tocs`, `npm run test:homepage-json-ld`,
  `npm run test:agent-doc-outputs`, `npm run test:docs-markdown`, and
  `npm run test:tracking-routes`.
- Run `npm run lint` and `npm run fmt` checks. Report Trunk as unavailable if
  it is absent; do not count an unavailable check as a pass.
- Check the tracked-file and production-output inventories for proprietary
  Azeret binaries. Neither may contain them.

### Static visual proof

After a successful production build, use computer use to inspect generated
PNGs. Require screenshots, not video, because the deliverable is static.

- Inspect a contact sheet of at least 20 real pages. Include every route in
  this matrix:
  - `/`, `/terminal/windows/tabs`, `/terminal/warpify/ssh-legacy`,
    `/code/code-review`, `/knowledge-and-collaboration/warp-drive`,
    `/getting-started/quickstart/installation-and-setup`.
  - `/agents/capabilities/skills`, `/agents/cli/reference`.
  - `/factories`, `/factories/use-cases/end-to-end-sdlc-automation`, `/api`.
  - `/platform/overview`, `/platform/transitioning-from-oz`,
    `/platform/triggers/scheduled-agents`.
  - `/support-and-community/plans-and-billing/credits`,
    `/support-and-community/plans-and-billing/add-on-credits`.
  - `/enterprise`, `/changelog/2026`.
  - `/guides/external-tools/sqlite-and-stripe-mcp-basic-queries-you-can-make-after-set-up`,
    `/guides/agent-workflows/how-to-run-unattended-agents`.
- Add synthetic Unicode, unbroken-token, and extreme-length fixtures. Mark
  them as fixtures, not published pages.
- Inspect full-size 1200×630 examples of the longest title, longest section
  label, shared billing, `/api`, root, and the Unicode fixture. Inspect reduced
  600×315 versions of the longest title and longest section label.
- Report the visible label, title, wrapping, spacing, and clipping for each
  critical case. Check that reduced images keep the gray label readable and
  visually secondary to the black title.
- Attach the contact sheet and critical screenshots to the existing PR's
  managed proof block. Identify the verified implementation head.
- For requester-facing Slack proof, upload only one or two clean native
  card images directly in the thread. Do not add paths, caption bars, white
  strips, or browser framing to these images. Put context in the surrounding
  message. Do not send the broad contact sheet or gallery links in Slack.
