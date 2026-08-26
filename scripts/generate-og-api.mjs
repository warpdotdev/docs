// Renders public/assets/og/api.png (npm run og:api) — the 1200x630 social
// card used by /api's og:image and twitter:image meta tags. Reads the
// wordmark from src/assets/warp-logo-dark.svg so the raster card can't drift
// from the canonical asset, then rasterizes to PNG since scrapers don't
// reliably accept SVG og:image.
import { mkdirSync, readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const __dirname = dirname(fileURLToPath(import.meta.url));
const outPath = resolve(__dirname, '../public/assets/og/api.png');
mkdirSync(dirname(outPath), { recursive: true });

// The source asset has no root width/height, so a nested <svg> would default
// to 100% of its parent; add the native 598x209 dimensions explicitly.
const wordmarkSvg = readFileSync(resolve(__dirname, '../src/assets/warp-logo-dark.svg'), 'utf-8')
  .trim()
  .replace('<svg ', '<svg width="598" height="209" ');

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
  <g transform="translate(285, 150) scale(1.05)">
    ${wordmarkSvg}
  </g>
  <!-- Accent rule -->
  <rect x="285" y="395" width="80" height="4" rx="2" fill="hsl(207, 80%, 62%)"/>
  <!-- Wordmark subtitle -->
  <text x="285" y="450" fill="#FAF9F6" font-family="Inter, 'Helvetica Neue', Arial, sans-serif" font-size="46" font-weight="700" letter-spacing="-1">
    Agent API Reference
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
