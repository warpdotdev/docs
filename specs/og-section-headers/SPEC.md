# Section labels for documentation social previews

## Summary

Add a section label above each documentation preview title. Keep the accepted
design in [PR #956](https://github.com/warpdotdev/docs/pull/956). Use one stable
section per URL, even when several navigation tabs link to that URL.

- Status: approved and implemented; section size revised for readability on 2026-11-23.
- Requester: `hongyi-chen`.
- Implementation baseline: `86309f7e8700339e7fa542f5a09fad36a477594a`.
- Reuse PR #956 and branch `factory/dynamic-og-images`.
- Do not implement the header until the requester approves this specification.

## Requester decisions

The requester replied, “go for it, let’s try it”, to this direction:

- Keep DOCUMENTATION and add a small section label above the title.
- Use existing tab names.
- Label shared billing pages SUPPORT.
- Label Transitioning from Oz AUTOMATION PLATFORM.
- Do not choose the label from the first matching navigation tab.
- Keep root and unknown pages generic.
- Preserve full titles.

This reply aligns the design direction. It does not approve an unwritten spec
or waive approval. The dimensions and resolver details below are proposed
implementation choices, not pixel-level requester decisions.

On the committed proposal, the requester replied:

> sure, does it have to be black, should it be a different color, like grey perhaps?

Use a neutral gray eyebrow in response to this feedback. The recommended
`#555555` value below is a design choice, not a hex value selected by the
requester. The requester approved the committed gray-label proposal with
“yes go ahead, show me screenshots”.

The requester also asked for “just 1-2 images directly in this slack thread”.
Keep broad coverage in internal and PR proof. Send only one or two clean
images directly in Slack, without paths or gallery caption bars.

### Readability revision

After seeing the implemented gray labels, the requester asked, “Maybe a bit
bigger? It's hard to read”. The section eyebrow increased from 24px to 32px.
After seeing those cards, the requester asked, “Maybe a bit bigger? Still small”.
Increase the eyebrow to 48px: 24px at 600×315 and 12.8px at 320×168,
compared with 16px and 8.5px for the 32px version.
This explicit sizing revision supersedes only the section type size.
Keep the gray color, Medium weight, tracking, line height, 24px title gap,
title fitting, margins, pill, and section ownership unchanged.

## Product behavior

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
   Keep the existing generic layout on those pages. An unlisted page inside a
   recognized family still receives that family's label.
5. A guide inside `/factories/guides` receives FACTORIES. A factory tutorial
   inside `/guides` receives GUIDES. The label identifies the docs section,
   not every subject mentioned by the page.
6. Preserve the complete title and its existing wrapping and shrinking policy.
   Do not add ellipses, a subtitle, a divider, or a footer.
7. Keep production-build generation and existing fallback behavior. This work
   does not add dynamic previews to `astro dev`.

### Why one URL can appear in several sections

These are navigation links to the same canonical page, not duplicate content:

| Page | Navigation locations | Source at the baseline |
| --- | --- | --- |
| [Usage and billing](https://docs.warp.dev/support-and-community/plans-and-billing/credits/) | Factories → Plans & support; Support → Plans & billing | `src/sidebar.ts:582,807` |
| [Purchasing additional usage](https://docs.warp.dev/support-and-community/plans-and-billing/add-on-credits/) | Factories → Plans & support; Support → Plans & billing | `src/sidebar.ts:583,808` |
| [Transitioning from Oz](https://docs.warp.dev/platform/transitioning-from-oz/) | Factories → Plans & support; Automation Platform → Overview | `src/sidebar.ts:585,654` |

A social crawler sees the shared URL, not the navigation path. The comment at
`src/sidebar.ts:652–653` records that the transition URL currently activates
Factories. Its preview will intentionally say AUTOMATION PLATFORM.

## Visual design

Preserve the accepted 1200×630 canvas:

- Chrome-blue background: `#D5DFE2`.
- Complete black Warp lockup at the upper left.
- Terminal-blue `#1008FF` DOCUMENTATION pill at the upper right, with a black
  outline and white text.
- Outer margins: 64px.
- Bottom-aligned black uppercase title in Azeret SemiMono Regular.
- Title tracking: −5%. Line height: 115%.
- Pill font: Azeret SemiMono Medium. Tracking: −2%.

Add the section as an eyebrow, not another badge:

- Font: Azeret SemiMono Medium, 48px, uppercase.
- Color: neutral gray `#555555`, fully opaque. Keep the page title black.
- Tracking: −2%. Line height: 115%.
- Left edge: x=64px.
- Bottom edge: 24px above the rendered title's top edge.
- Keep the label on one line within the existing 1072px content width.
- Keep the title inside its existing 280px maximum height. Keep the title's
  bottom edge at y=566px.
- Move the eyebrow with the fitted title block. Do not move the lockup or pill.

This layout leaves the title's full width available. The longest proposed
label, AUTOMATION PLATFORM, does not compete with the logo or pill.

The gray makes the section secondary to the black title without adding
another accent color. Using WCAG linearized-sRGB relative luminance,
`#555555` against `#D5DFE2` has a contrast ratio of **5.4964:1**. Keep section
text at or above 4.5:1. Do not use the reference palette's lighter `#8D8B82`
for this text: it produces only **2.5183:1** on the accepted background.

## Technical design

References below use the implementation baseline.

- `src/lib/og-image.js:73,86`: extend `renderOgImage` with an optional section.
  Measure the title with the existing algorithm. Render the section above the
  measured title. An omitted section preserves the existing generic rendering.
- `src/lib/social-image.js:3,12`: add one shared section resolver for the URL
  mapping. Keep title extraction from rendered H1 and document-title fallback.
  Include the section in image alt text when present, for example
  `Warp Docs — Agents — Skills for agents`. Preserve existing alt text for
  generic cards.
- `src/integrations/og-images.js:21,26`: derive each page route from its path
  relative to the output root. Normalize root `index.html`, nested
  `index.html`, `.html`, and trailing slashes before resolution. Pass title and
  section to the renderer.
- Cache generated previews by both title and section. Equal titles in
  different sections must not share the wrong card. Equal title-section pairs
  may share a card. Keep PNG-content hashing for asset URLs.
- `scripts/validate-og-images.mjs`: resolve the expected section for each
  generated page. Validate section-aware metadata and all referenced PNGs.
- `src/integrations/og-images.test.js:31,59`: extend the existing geometry,
  design, deduplication, fallback, and metadata tests.
- Preserve the hash-pinned build-only Azeret downloads and font cache.
  Keep proprietary fonts out of git and deployed output.
- Do not edit navigation, article titles, content frontmatter, or redirects.

## Decisions and alternatives

| Decision | Selected option and reason | Alternative and trade-off |
| --- | --- | --- |
| Ownership | Stable URL-family mapping. Shared billing and transition pages keep the agreed home labels. | First navigation match follows current tab activation but changes when navigation is reordered. |
| Label vocabulary | Existing eight tab names. This names the section readers can find. | Product-only labels omit Support, Enterprise, Changelog, and Guides. Singular AGENT diverges from navigation. |
| Placement | Section eyebrow above the title. Keep the accepted DOCUMENTATION pill. | Replacing the pill removes its existing role. A second badge adds competing chrome. |
| Eyebrow color | Neutral gray `#555555` makes the section secondary and provides 5.4964:1 contrast. | Black has stronger contrast but competes with the title. Palette gray `#8D8B82` is softer but fails the 4.5:1 text threshold at 2.5183:1. |
| Generic pages | Omit the eyebrow on root and unknown routes. | Guessing from the title or current tab can assign the wrong product. |
| Maintenance | One path-family resolver, with tests for cross-linked and unlisted pages. | Per-page frontmatter adds authoring work. Parsing navigation retains shared-page ambiguity and couples preview ownership to tab order. |

## Assumptions

- Assumption: matching existing names means all eight tabs, with AGENTS plural.
  The requester agreed to existing tab names but did not enumerate them.
- Assumption: the URL-family table, `/api` exception, and known-family
  inheritance implement the agreed stable-home direction. They do not assign
  new ownership in site navigation.
- The original 24px eyebrow increased to 32px, then 48px after further feedback.
  Verify the revised size at native and reduced preview sizes while keeping
  the approved 24px title gap.
- Assumption: `#555555` is the neutral gray to try in response to the
  requester's color feedback. The requester did not select this exact value.
- Assumption: section-aware alt text preserves the information added visually.

## Out of scope

- Navigation or information-architecture changes.
- Section-specific colors, multiple labels, breadcrumbs, or new themes.
- Title truncation, title rewrites, or a different font distribution mechanism.
- New runtime image endpoints or changes to third-party unfurl caches.

## Validation criteria

### Automated checks

- Run `npm ci` in the implementation checkout.
- Run `npm run test:og-images`. Add named regressions for:
  - All eight labels, grouped URL families, `/api`, and `/quickstart`.
  - Shared billing → SUPPORT and transition → AUTOMATION PLATFORM.
  - Known-family unlisted pages, root, 404, unknown routes, and segment
    boundaries such as `/agents-extra`.
  - Equivalent nested `index.html`, `.html`, and trailing-slash routes.
  - Equal title-section pairs deduplicate; equal titles in different sections
    produce different PNGs and correct metadata.
  - Every label fits on one line; label, title, logo, and pill do not overlap.
    Preserve 64px margins, title bounds, colors, and full title text.
  - The eyebrow uses opaque `#555555`; the title remains black. Calculate
    text/background contrast from linearized-sRGB relative luminance and
    assert a ratio of at least 4.5:1 for `#555555` against `#D5DFE2`.
  - Short, long, unbroken, Unicode, and markup-like titles with a section.
  - Existing font-failure, offline-cache, fallback, write-failure, and
    article-body-preservation behavior.
- Run `npm run typecheck` and `npm run test:heading-vars`.
- Run `npm run build`, then `npm run test:og-output`. Record actual page,
  preview, and fallback counts. Require zero unexpected fallbacks.
- Run `npm run test:heading-tocs`, `npm run test:homepage-json-ld`,
  `npm run test:agent-doc-outputs`, and `npm run test:tracking-routes`.
- Run `npm run lint` and `npm run fmt` checks. Report Trunk as unavailable if
  it is absent; do not count an unavailable check as a pass.
- Check `git diff --name-only 86309f7..HEAD` for new font binaries. Inspect the
  production output inventory to confirm the build-only Azeret files remain
  absent. Record these checks with the implementation evidence.

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
  managed proof block. Identify the verified implementation head. Do not
  present the baseline screenshots as proof of the new section labels.
- For requester-facing Slack proof, upload only one or two clean native
  card images directly in the thread. Do not add paths, caption bars, white
  strips, or browser framing to these images. Put context in the surrounding
  message. Do not send the broad contact sheet or gallery links in Slack.
