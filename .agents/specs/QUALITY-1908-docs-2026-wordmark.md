# Spec: Update the docs site to the 2026 Warp wordmark

## Product

### Summary

Replace the Warp wordmark rendered by the docs site with the requester-supplied 2026 artwork. The Starlight header and standalone `/api` topbar must use explicit white and dark SVG variants, preserve the existing theme-switching behavior, and size the new proportions optically rather than retaining the old raw CSS dimensions. The generated Agent API social card must use the same white variant. The site favicon and Apple touch icon must use the separately supplied icon-only glyph on a durable dark background.

### Key design choices

- Keep the existing `warp-logo-dark.svg` and `warp-logo-light.svg` asset paths and theme contracts so all current consumers continue to share one pair of assets.
- Use explicit SVG variants: white artwork for dark backgrounds and `#121212` artwork for light backgrounds. Do not use `currentColor` or theme-dependent CSS inside the SVGs.
- Increase both header logo boxes from `1.25rem` to `1.625rem` high. The new viewBox has substantially more vertical space around its painted paths, so this preserves the existing approximately 20px painted height instead of making the new wordmark appear smaller.
- Regenerate the Agent API social card from the white SVG file rather than maintaining another copy of the path data in the generator.
- Build the favicon family from one canonical `800×800` white icon source on a `#121212` background. Keep explicit SVG and PNG link declarations; do not add an ICO-only dependency or theme-responsive transparent glyph.
- Do not change the generic no-logo social card.

### Behavior

1. Every Starlight docs page renders the complete 2026 icon-and-wordmark artwork in its site-title link.
2. The standalone `/api` page renders the same complete artwork in its topbar.
3. Light mode renders the dark-fill asset, and dark mode renders the white-fill asset, with exactly one visible logo in each theme.
4. At the default 16px root font size, both page headers allocate a `1.625rem` (26px) high responsive SVG box with `width: auto`. The new paths occupy about 20px of that box, matching the current wordmark's painted height while producing an approximately 74px-wide mark.
5. The wordmark stays unclipped and does not overlap header navigation, the mobile menu, breadcrumbs, or theme controls at desktop and mobile widths.
6. The Agent API Open Graph/Twitter image remains 1200×630, contains the new white 2026 artwork at a comparable visual weight to the current wordmark, and preserves the surrounding title, subtitle, accent rule, background, and grid treatment produced by the current generator.
7. Browser tabs render the new icon-only glyph on a solid dark rounded-square background that remains visible against both light and dark browser chrome, independent of the page theme.
8. PNG favicon fallbacks render the same composition at 16×16 and 32×32, and the Apple touch icon renders a full-bleed dark background with the centered white glyph at 180×180. The icon stays recognizable at every required size.
9. Other tracked files whose names contain “Warp” remain unchanged unless they are one of the actual brand-wordmark or favicon consumers enumerated in this spec.

## Tech

### Context

The implementation is based on commit `977bbed52043268a4a126b78a3e4b4f077e5f289`.

- `src/assets/warp-logo-dark.svg:1-5` and `src/assets/warp-logo-light.svg:1-5` contain the current white and dark wordmark variants. Their `592×135` viewBox has an aspect ratio of about 4.39.
- `src/components/CustomSiteTitle.astro:20-21` imports both assets as raw SVG. Its existing Starlight theme utilities show the white asset on dark backgrounds and the dark asset on light backgrounds. `src/components/CustomSiteTitle.astro:77` currently fixes the SVG box at `1.25rem` high.
- `src/components/WarpTopbar.astro:15-16` imports the same files for the standalone `/api` header. Its body-class theme selectors already map the correct variant to `.dark-mode` and `.light-mode`; `src/components/WarpTopbar.astro:152` also fixes the SVG box at `1.25rem` high.
- `astro.config.mjs:84-86` points Starlight's logo configuration at the same two assets. `astro.config.mjs:170` configures `/apple-touch-icon.png`; that existing icon link is now in scope and must be joined by explicit SVG and PNG favicon links.
- `src/components/CustomHeader.astro:27` renders Starlight's `SiteTitle` on desktop and mobile. The horizontal topic navigation and right-side controls are hidden below the existing Starlight breakpoint, while the title remains visible.
- `src/pages/api.astro:199` renders `WarpTopbar`; its `/favicon.svg` reference at `src/pages/api.astro:58` is in scope and must expose the same SVG/PNG/touch-icon family as Starlight pages.
- `scripts/generate-og-api.mjs:16-21` duplicates the current wordmark paths, and `scripts/generate-og-api.mjs:41` scales them into `public/assets/og/api.png`. `src/pages/api.astro:49,57` publishes that generated PNG as the API page's Open Graph and Twitter image.
- `src/routeData.ts:35` points ordinary Starlight pages at `public/og-image.png`. That 1200×630 image is an abstract collage with no Warp logo or wordmark, so it is not a logo consumer.

### Design alternatives

- **Theme handling:** A single `currentColor` SVG would reduce asset duplication, but generated/rasterized social images cannot inherit site CSS and the requester explicitly chose separate variants. Keep two files with identical geometry and explicit fills.
- **Asset paths:** Adding new `*-2026.svg` filenames would make the refresh visible in the filesystem, but it would require changing every consumer and create parallel generations of the same role. Replace the contents of the existing theme assets so the repository retains one canonical pair.
- **Header sizing:** Keeping `height: 1.25rem` would shrink the painted artwork because the supplied `598×209` viewBox uses only about 160 vertical units for visible paths. At `1.625rem`, the painted height is approximately `160 / 209 × 26 = 19.9px`, matching the current artwork's approximately `132 / 135 × 20 = 19.6px`. Use `1.625rem` in both header components.
- **API card source:** Copying the new paths into `generate-og-api.mjs` would preserve the current implementation shape but create a third source of truth. Read and embed `src/assets/warp-logo-dark.svg` in the generator so subsequent wordmark changes cannot leave the raster output stale.
- **Favicon contrast:** A transparent white glyph with `prefers-color-scheme` styling would disappear on light browser chrome and make visibility depend on browser SVG/CSS support. Put the white glyph on a fixed `#121212` background for all favicon outputs.
- **Favicon formats:** An SVG-only favicon is sufficient for modern browsers but lacks a deterministic fallback and does not produce the Apple touch image. Generate 16×16 and 32×32 PNG fallbacks and a 180×180 Apple touch icon with the repository's existing `sharp` dependency. Do not add a `.ico` encoder or a new dependency because all owned pages declare the SVG/PNG family explicitly.
- **Generic social card:** Adding the wordmark to `public/og-image.png` would be a new card redesign, not a replacement of an existing logo. Keep it unchanged.

### Proposed changes

#### Theme SVG assets

Update `src/assets/warp-logo-dark.svg` and `src/assets/warp-logo-light.svg` with the exact geometry in the source asset at the end of this spec.

- Both files use `viewBox="0 0 598 209"` and contain identical path data.
- Omit fixed root `width` and `height` attributes so each consumer owns presentation sizing.
- `warp-logo-dark.svg` uses `fill="#FFFFFF"` on all three paths for dark backgrounds.
- `warp-logo-light.svg` uses `fill="#121212"` on all three paths for light backgrounds.
- Preserve the existing filename meaning: the suffix names the background theme, not the artwork color.

#### Starlight and API headers

Update the SVG sizing rule in both `src/components/CustomSiteTitle.astro` and `src/components/WarpTopbar.astro`:

- `height: 1.625rem`
- `width: auto`
- `max-width: 100%`
- `display: block`

Do not change the current raw-SVG imports, theme utility classes, body-class theme selectors, link destinations, accessibility labels, or screen-reader-only site title. Do not introduce separate desktop/mobile dimensions; the 26px box fits the existing 64px desktop and 56px mobile header heights.

Keep `astro.config.mjs` pointed at the same two files and verify that `light` still maps to `warp-logo-light.svg` and `dark` still maps to `warp-logo-dark.svg`.

#### Agent API social card

Update `scripts/generate-og-api.mjs` to read `src/assets/warp-logo-dark.svg` and embed that SVG in the 1200×630 card instead of keeping a `WARP_LOGO` path-data duplicate.

Render the `598×209` SVG with `translate(285, 150) scale(1.05)`. This produces an approximately 628×219 outer box centered within the card; the painted paths run from about y=200 to y=369, leaving a deliberate gap above the accent rule at y=395.

Preserve the generator's existing background, grid, accent rule, text styles, title, subtitle, and output path. Run `npm run og:api` and commit the regenerated `public/assets/og/api.png`.

#### Favicon and Apple touch icon

Add `src/assets/warp-icon-white.svg` as the canonical icon-only source, using the exact `800×800` geometry at the end of this spec. Keep its two paths white and omit presentation styling.

Add `scripts/generate-favicons.mjs`, using the existing `sharp` dependency, and expose it as `npm run favicon:generate`. The generator must:

- Read `src/assets/warp-icon-white.svg`; do not duplicate its paths in the script.
- Compose `public/favicon.svg` as an `800×800` SVG with a full-canvas `#121212` background rectangle using `rx="144"` and the unchanged white glyph above it.
- Rasterize the rounded-square composition to `public/favicon-16x16.png` and `public/favicon-32x32.png`.
- Rasterize a touch-icon composition to `public/apple-touch-icon.png` at 180×180. Its `#121212` background is full bleed with no pre-rounded transparent corners because Apple applies the platform mask; the glyph uses the source viewBox's built-in safe area.
- Produce deterministic outputs from the same source asset in one command.

Update the Starlight `head` entries in `astro.config.mjs` and the standalone `<head>` in `src/pages/api.astro` to declare the same ordered icon family:

1. SVG primary: `/favicon.svg`, `type="image/svg+xml"`.
2. 32×32 PNG fallback: `/favicon-32x32.png`, `type="image/png"`, `sizes="32x32"`.
3. 16×16 PNG fallback: `/favicon-16x16.png`, `type="image/png"`, `sizes="16x16"`.
4. Apple touch icon: `/apple-touch-icon.png`, `sizes="180x180"`.

Retain the existing icon link semantics where practical, but remove duplicate link declarations so each page emits exactly one link for each size/role. Do not create PWA 192×192/512×512 icons or a web manifest; the repository has no current PWA icon pipeline.

#### Explicit exclusions

Do not modify:

- `public/og-image.png`
- `src/routeData.ts`
- The screenshot and demo-media inventory below

### Warp-named files and assets that are not brand-wordmark sources

The audit found no unrelated standalone SVG icon named for Warp. The other matching tracked assets are product screenshots or demo media and must not be edited as logo sources:

- `src/assets/agent-platform/cloud-agent-harness-selector-warp-app.png` — screenshot of the cloud-agent harness selector.
- `src/assets/agent-platform/delete-warpy.png` — screenshot of the Warpy Slack app details.
- `src/assets/agent-platform/linear-warp-on-web.png` — screenshot of a Warp web session launched from an integration flow.
- `src/assets/agent-platform/plans-in-warp-drive-side-panel.png` — screenshot of plans in the Warp Drive side panel.
- `src/assets/terminal/Open_Warp_Drive.png` — screenshot of the Warp Drive launcher.
- `src/assets/terminal/Warp_Drive_Zero_State.png` — Warp Drive empty-state screenshot.
- `src/assets/terminal/Warp_Drive_with_Team.png` — Warp Drive team-state screenshot.
- `src/assets/terminal/migrate-to-warp.png` — screenshot of the settings-profile import flow.
- `src/assets/terminal/warp-ai-permissions.png` — screenshot of an agent command permission prompt.
- `src/assets/terminal/warp-ai-viewing-commands.png` — screenshot of command details in an agent conversation.
- `src/assets/terminal/warp-dark.png` — dark-theme product screenshot.
- `src/assets/terminal/warp-light.png` — light-theme product screenshot.
- `src/assets/terminal/warp-factories-welcome.png` — product welcome page screenshot for Warp and Warp Factories.
- `src/assets/terminal/warp_drive_nav1.png` — Warp Drive navigation screenshot.
- `src/assets/terminal/warp_drive_nav2.png` — Warp Drive navigation and side-panel screenshot.
- `src/assets/terminal/warp_drive_offline.png` — Warp Drive offline-state screenshot.
- `src/assets/terminal/warpify_ssh_auto_script.png` — Warpify SSH auto-script screenshot.
- `src/assets/terminal/warpify_ssh_prompt.png` — Warpify SSH prompt screenshot.
- `public/assets/support-and-community/open-warp-mac.mp4` and `open-warp-mac.poster.jpg` — macOS app-opening demonstration and poster frame.
- `public/assets/terminal/warp-custom-prompt-demo.mp4` and `warp-custom-prompt-demo.poster.jpg` — custom-prompt demonstration and poster frame.

Other Warp-named non-asset files are also out of scope:

- `src/components/WarpTopicNav.astro` — top-level documentation topic navigation and its generic topic icons.
- `src/styles/warp-components.css` — shared docs component styling.
- `.agents/skills/release_updates/scripts/update_warp_app.py` — release automation that downloads the Warp application.
- `.warp/references/settings-schema.json` — generated/reference Warp settings schema.

### Open questions resolved

- **Favicon treatment:** The requester superseded the earlier exclusion and supplied a separate icon-only asset. Use it on a fixed dark background for the SVG, PNG fallbacks, and Apple touch icon.
- **Light-mode implementation:** Use separate explicit SVG variants, not `currentColor`.
- **Preview breadth:** Capture desktop and mobile Starlight headers and `/api` topbars in both themes, the generated API social card, and browser-tab/direct-size proof for the new favicon family.
- **Warp-named matches:** Change only actual live brand-wordmark sources. Leave product screenshots, videos, navigation icons, styles, tooling, and settings references unchanged.
- **Ordinary-page social card:** Leave the generic no-logo collage unchanged; the in-scope generated social card is the Agent API card.

### Risks and blast radius

- The new viewBox is much taller relative to its width. A naive content replacement would make the painted logo too small; the paired CSS size updates mitigate this.
- The larger CSS box could crowd controls at narrow widths. Mobile captures at 390px and a boundary check at 320px mitigate this.
- Theme filename semantics are easy to invert because `warp-logo-dark.svg` contains white artwork. Deterministic DOM/theme checks and paired screenshots mitigate this.
- Leaving path data copied in the social-card generator would allow the header and raster card to drift. Reading the canonical white asset mitigates this.
- Generated PNG output can change independently of source text. Regenerating it with the repository command and reviewing the resulting 1200×630 artifact mitigates this.
- A transparent white favicon glyph would disappear against light browser chrome, while an overly padded composition would become illegible at 16px. The fixed dark background, supplied square viewBox, standard-size rasters, and browser-tab previews mitigate this.
- Apple applies its own mask to touch icons. A full-bleed square touch source avoids double-rounded transparent margins while the browser favicon keeps intentional rounded corners.
- Historical screenshots can contain older Warp marks as part of captured product UI. Editing those pixels would misrepresent the documented state; they are explicitly excluded.

## Validation and verification criteria

All criteria must pass before merge.

1. **Wordmark geometry and fills:** Parse both theme SVGs and confirm they use `viewBox="0 0 598 209"`, contain the same three path `d` values as the wordmark source asset below, and differ only in explicit fill color (`#FFFFFF` versus `#121212`). Neither file contains theme CSS, `currentColor`, or fixed root dimensions.
2. **Favicon source and composition:** Confirm `src/assets/warp-icon-white.svg` uses the supplied `800×800` viewBox and exact two white path values. Confirm `public/favicon.svg` adds only the required `#121212` rounded background and preserves the source paths unchanged.
3. **Generated favicon dimensions:** Run `npm run favicon:generate`, then use `sharp(...).metadata()` or an equivalent deterministic image inspection to confirm `favicon-16x16.png` is 16×16, `favicon-32x32.png` is 32×32, and `apple-touch-icon.png` is 180×180. Re-running the command without source changes produces no Git diff.
4. **Icon link coverage:** Inspect a built representative Starlight page and `/api`. Each emits one SVG favicon link, one 32×32 PNG link, one 16×16 PNG link, and one 180×180 Apple touch link with the specified paths, types, and sizes. No duplicate role/size declarations remain.
5. **Consumer audit:** Search for `warp-logo-dark.svg`, `warp-logo-light.svg`, `warp-icon-white.svg`, and the old path anchor `M170.286`. The new sources are consumed only through the specified headers, generators, and icon links, and the old path anchor is absent from tracked text sources after the favicon replacement.
6. **Header sizing:** Inspect the built output or browser DOM for a representative Starlight page and `/api`. Each visible wordmark SVG has a 26px CSS height at the default root size, automatic width of approximately 74px, preserved `598:209` aspect ratio, and no clipping.
7. **Starlight light/dark previews:** After a successful build, run the docs site and use computer use to capture screenshots of a representative Starlight page at 1440px and 390px viewport widths in both light and dark mode. The light screenshots show the dark-fill logo, the dark screenshots show the white-fill logo, exactly one logo is visible, and header navigation/menu controls do not overlap it.
8. **API light/dark previews:** In the same running build, capture `/api` at 1440px and 390px in both themes. Verify the correct variant, one visible logo, preserved breadcrumb/theme-control alignment on desktop, and an unclipped logo with the narrow-screen rules applied on mobile.
9. **Narrow boundary:** Exercise both the Starlight page and `/api` at 320px width in both themes. No screenshot is required if the 390px captures already demonstrate the state, but record that the logo, menu/theme controls, and available text do not overlap or cause horizontal scrolling.
10. **Theme persistence:** Select light and dark modes from both the Starlight theme control and the `/api` theme control, reload, and navigate between a Starlight route and `/api`. The correct logo variant appears on first paint without a double-logo frame or a contrasting-theme flash.
11. **Favicon visual proof:** Capture the real browser tab for a Starlight page and `/api` against both light and dark browser chrome where the available runner permits. Also capture or compose a proof sheet showing the generated 16×16, 32×32, and 180×180 outputs at native scale and enlarged nearest-neighbor scale. The white glyph remains recognizable, centered, unclipped, and contrasted at every size.
12. **Social-card generation:** Run `npm run og:api`. Confirm `public/assets/og/api.png` is 1200×630, uses the new 2026 white wordmark centered at the specified scale, preserves the existing card composition and current generator text, and contains no clipping or collision. Include the regenerated image in the requester's preview set.
13. **Explicit exclusions:** Verify `git diff -- public/og-image.png src/routeData.ts` is empty and none of the screenshot/demo files listed above changed.
14. **Accessibility:** Verify the header brand links keep their current accessible names and destinations, the decorative inline wordmark SVGs remain hidden from assistive technology, and the screen-reader site title remains present. Favicon link updates must not change document titles or accessible page content.
15. **Repository checks:** Run `npm run typecheck`, `npm run build`, and `npm run lint`. Run the repository's documented formatter (`npm run fmt`) and confirm the final diff contains only intended files.
16. **Automated-test exemption:** Do not add a regression test. This is a requester-approved pure asset/visual refresh; an assertion over literal SVG paths, CSS dimensions, or generated pixels would be tautological. Deterministic generator/dimension checks, typecheck, production build, lint/format gates, and running-UI visual proof are the required verification.
17. **Proof publication:** Attach the light/dark desktop and mobile header screenshots, favicon/browser-tab proof, and generated API card preview to the Linear task and implementation PR. Preview media is evidence and must not be committed; the favicon rasters and `public/assets/og/api.png` are committed product assets.

## Requester-supplied source asset

The implementation must derive both theme variants from this exact geometry:

```svg
<svg width="598" height="209" viewBox="0 0 598 209" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M88.8106 50.3347C89.0987 49.1413 90.1667 48.3005 91.3943 48.3005H155.163C165.824 48.3005 174.467 57.2314 174.467 68.2481L174.236 146.903C174.236 157.92 165.593 166.851 154.932 166.851H64.0584C62.3382 166.851 61.0711 165.242 61.4748 163.569L88.8106 50.3347Z" fill="white"/>
<path d="M71.4281 70.7031C71.8197 69.035 70.554 67.4376 68.8405 67.4376H19.1396C8.56908 67.4376 0 76.3685 0 87.3851L0 166.272C0 177.288 8.61333 186.883 19.1838 186.883H82.3876C83.6167 186.883 84.6855 186.04 84.9722 184.845L86.3156 179.245C86.7165 177.573 85.4497 175.967 83.731 175.967H50.0656C48.3521 175.967 47.0864 174.369 47.4781 172.701L71.4281 70.7031Z" fill="white"/>
<path d="M342.372 87.296L301.864 171.592L278.74 120.916L255.452 171.592L215.108 87.296H235.608L256.928 134.692L279.232 84.344L301.536 134.692L322.528 87.296H342.372ZM408.753 87.296H428.105V167H408.753V155.356C403.833 163.392 393.337 168.968 382.513 168.968C360.373 168.968 342.825 150.6 342.825 127.148C342.825 103.696 360.373 85.328 382.513 85.328C393.337 85.328 403.833 90.904 408.753 98.94V87.296ZM362.013 127.148C362.013 141.252 372.345 151.912 385.793 151.912C399.405 151.912 409.737 141.252 409.737 127.148C409.737 113.044 399.405 102.384 385.793 102.384C372.345 102.384 362.013 113.044 362.013 127.148ZM497.466 87.46V107.14C494.35 105.5 491.07 104.844 487.298 104.844C475.654 104.844 467.618 113.372 467.618 126.328V167H448.266V87.296H467.618V99.76C471.554 91.888 479.59 85.82 489.594 85.82C493.366 85.82 495.498 86.476 497.466 87.46ZM528.08 87.296V98.94C533.164 90.904 543.66 85.328 554.484 85.328C576.624 85.328 594.172 103.696 594.172 127.148C594.172 150.6 576.624 168.968 554.484 168.968C543.66 168.968 533.164 163.392 528.08 155.356V208.492H508.728V87.296H528.08ZM574.984 127.148C574.984 113.044 564.652 102.384 551.04 102.384C537.592 102.384 527.26 113.044 527.26 127.148C527.26 141.252 537.592 151.912 551.04 151.912C564.652 151.912 574.984 141.252 574.984 127.148Z" fill="white"/>
</svg>
```

The favicon family must derive from this exact requester-supplied icon-only geometry:

```svg
<svg width="800" height="800" viewBox="0 0 800 800" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M405.928 222.034L594.677 222.034C625.231 222.034 650 244.972 650 273.267L649.338 475.283C649.338 503.579 624.569 526.516 594.016 526.516H323.909L405.928 222.034Z" fill="white"/>
<path d="M356.901 271.185H204.852C174.558 271.185 150 294.123 150 322.418L150 525.028C150 553.324 174.685 577.966 204.978 577.966H392.119L399.623 549.929H283.869L356.901 271.185Z" fill="white"/>
</svg>
```
