/**
 * Generates public/openapi.json from developers/agent-api-openapi.yaml.
 *
 * Run automatically via the `prebuild` / `predev` npm scripts.
 * Also runnable directly: node scripts/generate-openapi-json.mjs
 *
 * The JSON copy in public/ is what gets served at docs.warp.dev/openapi.json.
 * The YAML source is the source of truth — update that file when the API changes
 * and this script picks it up at the next build.
 */

import fs from 'node:fs';
import { parse } from 'yaml';

const src = 'developers/agent-api-openapi.yaml';
const dst = 'public/openapi.json';

const yaml = fs.readFileSync(src, 'utf-8');
const obj = parse(yaml);
fs.writeFileSync(dst, JSON.stringify(obj, null, 2));

const bytes = fs.statSync(dst).size;
console.log(`Generated ${dst} (${(bytes / 1024).toFixed(1)} KB) from ${src}`);
