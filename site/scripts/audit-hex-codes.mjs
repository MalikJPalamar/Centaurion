#!/usr/bin/env node
// QA gate: hex codes must appear ONLY in tokens.css (and asset SVGs in /public).
// Usage: node scripts/audit-hex-codes.mjs
import { readdir, readFile, stat } from "node:fs/promises";
import { join, extname, relative } from "node:path";

const ROOT = new URL("..", import.meta.url).pathname;
const SCAN_DIRS = ["src"];
const SCAN_EXT = new Set([".astro", ".tsx", ".ts", ".css"]);
const ALLOW = new Set([
  "src/styles/tokens.css",
  "src/content/brand-colors.ts",
]);

const HEX = /#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6,8})\b/g;

async function* walk(dir) {
  for (const entry of await readdir(dir)) {
    const full = join(dir, entry);
    const s = await stat(full);
    if (s.isDirectory()) yield* walk(full);
    else yield full;
  }
}

let hits = 0;
for (const d of SCAN_DIRS) {
  const abs = join(ROOT, d);
  for await (const file of walk(abs)) {
    if (!SCAN_EXT.has(extname(file))) continue;
    const rel = relative(ROOT, file);
    if (ALLOW.has(rel)) continue;
    const content = await readFile(file, "utf8");
    const matches = content.match(HEX);
    if (matches) {
      hits += matches.length;
      console.log(`${rel}  →  ${matches.join(", ")}`);
    }
  }
}

if (hits > 0) {
  console.error(`\nFAIL — ${hits} hex code(s) outside tokens.css.`);
  process.exit(1);
}
console.log("PASS — hex codes confined to token layer.");
