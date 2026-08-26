// One-shot script to generate the docs site's favicon family from the
// canonical icon-only source asset.
//
// Run with: node scripts/generate-favicons.mjs
//
// Composes src/assets/warp-icon-white.svg onto a fixed #121212 background so
// the glyph stays visible against both light and dark browser chrome,
// independent of the page's own theme. Rasterizes that composition to the
// PNG fallback sizes browsers and Apple require, using the repository's
// existing sharp dependency (no new image-encoding dependency).
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const __dirname = dirname(fileURLToPath(import.meta.url));
const publicDir = resolve(__dirname, '../public');
mkdirSync(publicDir, { recursive: true });

const sourceSvg = readFileSync(resolve(__dirname, '../src/assets/warp-icon-white.svg'), 'utf-8');
const innerMarkup = sourceSvg.match(/<svg[^>]*>([\s\S]*)<\/svg>/)?.[1]?.trim();
if (!innerMarkup) {
  throw new Error('Could not read glyph markup from src/assets/warp-icon-white.svg');
}

const BACKGROUND = '#121212';

// Browser favicon: rounded-square background so the icon reads as an app
// icon in browser tabs and bookmark bars, with the source glyph unchanged
// on top.
const faviconSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800">
  <rect width="800" height="800" rx="144" fill="${BACKGROUND}"/>
  ${innerMarkup}
</svg>
`;

// Apple touch icon: full-bleed background with no pre-rounded corners.
// iOS/iPadOS apply their own rounded-square mask to whatever square image
// they're given, so a source with its own rounding would double up.
const touchIconSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800">
  <rect width="800" height="800" fill="${BACKGROUND}"/>
  ${innerMarkup}
</svg>
`;

const faviconSvgPath = resolve(publicDir, 'favicon.svg');
writeFileSync(faviconSvgPath, faviconSvg);

const favicon16Path = resolve(publicDir, 'favicon-16x16.png');
const favicon32Path = resolve(publicDir, 'favicon-32x32.png');
const touchIconPath = resolve(publicDir, 'apple-touch-icon.png');

await sharp(Buffer.from(faviconSvg)).resize(16, 16).png().toFile(favicon16Path);
await sharp(Buffer.from(faviconSvg)).resize(32, 32).png().toFile(favicon32Path);
await sharp(Buffer.from(touchIconSvg)).resize(180, 180).png().toFile(touchIconPath);

for (const outPath of [faviconSvgPath, favicon16Path, favicon32Path, touchIconPath]) {
  console.log(`Wrote ${outPath}`);
}
