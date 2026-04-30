// One-shot script to render public/assets/og/api.png — the social-card image
// (1200×630) used by /api's og:image and twitter:image meta tags.
//
// Run with: node scripts/generate-og-api.mjs
//
// We construct the SVG inline so the Warp wordmark uses the same path data as
// src/assets/warp-logo-dark.svg (no font dependency on the social scraper).
// Sharp rasterizes the SVG to a PNG that's safe to embed everywhere
// (Facebook/Twitter/LinkedIn don't reliably accept SVG og:image).
import { mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const __dirname = dirname(fileURLToPath(import.meta.url));
const outPath = resolve(__dirname, '../public/assets/og/api.png');
mkdirSync(dirname(outPath), { recursive: true });

// Warp wordmark paths copied verbatim from src/assets/warp-logo-dark.svg.
// Two `M…Z` mark paths and one wordmark path. viewBox "91 26 582 135".
const WARP_LOGO = `
  <g fill="#FAF9F6">
    <path d="M170.286 27.5005H227.682C236.973 27.5005 244.505 35.2835 244.505 44.8844V112.374C244.505 121.975 236.973 129.758 227.682 129.758H145.546L170.286 27.5005Z"/>
    <path d="M155.378 46.8732H109.141C99.9291 46.8732 92.4613 54.6562 92.4613 64.257V131.747C92.4613 141.348 99.9291 149.131 109.141 149.131H166.048L168.33 139.618H133.131L155.378 46.8732Z"/>
    <path d="M313.427 129.717L288.122 46.9034H302.418L320.328 110.164L339.717 46.9034H353.19L372.58 110.164L390.325 46.9034H404.949L379.481 129.717H365.843L346.454 66.7853L327.065 129.717H313.427ZM467.986 75.8225C467.986 64.4849 459.935 57.2551 447.776 57.2551C436.438 57.2551 428.387 63.992 427.237 75.1653L414.256 72.7006C416.721 56.2692 430.359 45.5889 447.776 45.5889C467.822 45.5889 481.789 57.4194 481.789 76.6441V129.717H467.986V115.586C463.221 125.117 452.377 131.032 440.382 131.032C423.786 131.032 412.449 120.844 412.449 106.549C412.449 90.6107 425.429 81.9021 451.884 79.2731L467.986 77.4657V75.8225ZM426.415 106.385C426.415 114.108 432.988 119.53 442.518 119.53C458.621 119.53 467.986 108.849 467.986 92.2539V88.3103L451.884 90.1178C435.124 91.9252 426.415 97.6762 426.415 106.385ZM575.81 75.001L561.843 77.63C561.186 65.3065 553.463 58.241 540.975 58.241C525.694 58.241 515.835 72.0433 515.835 94.2256V129.717H501.869V46.9034H515.835V63.1704C521.915 51.3398 532.102 45.5889 544.262 45.5889C562.665 45.5889 575.152 57.0908 575.81 75.001ZM590.697 159.622V46.9034H604.664V58.8982C609.1 51.3398 619.945 45.5889 631.94 45.5889C657.408 45.5889 671.539 63.992 671.539 88.3103C671.539 112.629 657.08 131.032 631.611 131.032C621.095 131.032 610.251 125.774 604.664 118.215V159.622H590.697ZM630.297 118.544C646.728 118.544 657.408 106.549 657.408 88.3103C657.408 70.0716 646.728 58.0767 630.297 58.0767C614.194 58.0767 603.514 70.0716 603.514 88.3103C603.514 106.549 614.194 118.544 630.297 118.544Z"/>
  </g>
`;

// 1200×630 OG card. The logo is centered horizontally, with subtitle text
// rendered as flat <text> using a generic sans-serif that maps reliably across
// scraper-side renderers. Warp's accent blue underlines the wordmark.
const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="#121212"/>
  <!-- subtle grid texture -->
  <g opacity="0.04" fill="none" stroke="#FAF9F6" stroke-width="1">
    <path d="M0 105 L1200 105 M0 210 L1200 210 M0 315 L1200 315 M0 420 L1200 420 M0 525 L1200 525"/>
    <path d="M150 0 L150 630 M300 0 L300 630 M450 0 L450 630 M600 0 L600 630 M750 0 L750 630 M900 0 L900 630 M1050 0 L1050 630"/>
  </g>
  <!-- Warp logo, scaled and centered -->
  <g transform="translate(285, 200) scale(1.08)">
    <svg viewBox="91 26 582 135" width="582" height="135">${WARP_LOGO}</svg>
  </g>
  <!-- Accent rule -->
  <rect x="285" y="395" width="80" height="4" rx="2" fill="hsl(207, 80%, 62%)"/>
  <!-- Wordmark subtitle -->
  <text x="285" y="450" fill="#FAF9F6" font-family="Inter, 'Helvetica Neue', Arial, sans-serif" font-size="46" font-weight="700" letter-spacing="-1">
    Oz Agent API Reference
  </text>
  <text x="285" y="500" fill="hsl(210, 4%, 72%)" font-family="Inter, 'Helvetica Neue', Arial, sans-serif" font-size="26" font-weight="400">
    Create and manage cloud agent runs, schedules, and more.
  </text>
  <text x="285" y="555" fill="hsl(210, 3%, 52%)" font-family="Inter, 'Helvetica Neue', Arial, sans-serif" font-size="22" font-weight="500" letter-spacing="2">
    DOCS.WARP.DEV
  </text>
</svg>
`;

await sharp(Buffer.from(svg)).png().toFile(outPath);
console.log(`Wrote ${outPath}`);
