#!/usr/bin/env node
// QA gate: scan content directories for forbidden buzzwords.
// Usage: node scripts/audit-forbidden-words.mjs
import { readdir, readFile, stat } from "node:fs/promises";
import { join, extname } from "node:path";

const ROOT = new URL("..", import.meta.url).pathname;
const SCAN_DIRS = ["src", "copy", "public"];
const SCAN_EXT = new Set([".astro", ".tsx", ".ts", ".md", ".html", ".js", ".mjs"]);

const FORBIDDEN = [
  "empower", "unlock", "leverage", "synergy", "transform",
  "journey", "ecosystem", "holistic", "cutting-edge",
  "next-generation", "revolutionary", "game-chang",
  "ai-powered", "world-class", "best-in-class", "end-to-end",
  "seamlessly", "robust solution",
];

// Negative lookbehind excludes CSS/SVG attribute names like `text-transform`,
// `border-transform`, etc. — we only flag real prose usage.
const RE = new RegExp(`(?<![-_a-z0-9])(${FORBIDDEN.join("|")})`, "gi");

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
  try {
    for await (const file of walk(abs)) {
      if (!SCAN_EXT.has(extname(file))) continue;
      const content = await readFile(file, "utf8");
      const lines = content.split(/\r?\n/);
      lines.forEach((line, i) => {
        const m = line.match(RE);
        if (m) {
          hits++;
          console.log(`${file}:${i + 1}  ${m.join(", ")}  →  ${line.trim().slice(0, 120)}`);
        }
      });
    }
  } catch {}
}

if (hits > 0) {
  console.error(`\nFAIL — ${hits} forbidden-word hit(s).`);
  process.exit(1);
}
console.log("PASS — no forbidden words.");
