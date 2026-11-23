// Meme Sprint 3: AI Agent Goes Rogue — entrypoint.
//
// The meme is rendered offline by draw_meme.py (Pillow, build time only)
// and committed next to this file as entry.png. The grader runs this
// program twice with no network and requires both runs to write identical
// bytes, so this file only copies those exact bytes into the output
// directory and verifies the copy. Node 22 standard library only.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = dirname(fileURLToPath(import.meta.url));
const INPUT = join(ROOT, "entry.png");
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const OUTPUT = join(OUTPUT_DIR, "entry.png");

function die(step: string, err: unknown): never {
  const why = err instanceof Error ? err.message : String(err);
  console.error(`meme-sprint-3: ${step}: ${why}`);
  process.exit(1);
}

const sha256 = (buf: Buffer): string =>
  createHash("sha256").update(buf).digest("hex");

let pixels: Buffer;
try {
  pixels = readFileSync(INPUT);
} catch (err) {
  die("cannot read the committed entry.png", err);
}

try {
  mkdirSync(OUTPUT_DIR, { recursive: true });
  writeFileSync(OUTPUT, pixels);
} catch (err) {
  die(`cannot write ${OUTPUT}`, err);
}

let copied: Buffer;
try {
  copied = readFileSync(OUTPUT);
} catch (err) {
  die("cannot read the written entry.png back", err);
}

if (sha256(copied) !== sha256(pixels)) {
  console.error("meme-sprint-3: copy is not byte-identical to entry.png");
  process.exit(1);
}

console.log(
  `meme-sprint-3: wrote ${OUTPUT} (${copied.length} bytes, sha256 ${sha256(copied).slice(0, 12)}...)`,
);
