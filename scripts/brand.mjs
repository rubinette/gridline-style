// Render brand/*.svg to PNG: mark at 16–512px, lockups at 2x, social previews at 1200x630.
// Usage: node scripts/brand.mjs   (npm install --prefix scripts first; set GRIDLINE_CHROME to a Chromium path if Chrome is not installed)
import { readFileSync, mkdirSync } from "node:fs";
import { resolve } from "node:path";

const { chromium } = await import("playwright-core");
const dir = resolve(import.meta.dirname, "../brand");
const out = resolve(dir, "png");
mkdirSync(out, { recursive: true });

const jobs = [
  ...[16, 32, 48, 64, 128, 180, 256, 512].map((s) => ({ src: s < 24 ? "mark-small.svg" : "mark.svg", w: s, h: s, name: `mark-${s}.png` })),
  ...[64, 128, 256, 512].map((s) => ({ src: "mark-dark.svg", w: s, h: s, name: `mark-dark-${s}.png` })),
  { src: "lockup.svg", w: 264, h: 64, scale: 2, name: "lockup.png" },
  { src: "lockup-dark.svg", w: 264, h: 64, scale: 2, name: "lockup-dark.png" },
  { src: "og.svg", w: 1200, h: 630, name: "og.png" },
  { src: "og-zh-tw.svg", w: 1200, h: 630, name: "og-zh-tw.png" },
  { src: "og-dark.svg", w: 1200, h: 630, name: "og-dark.png" },
];

const launch = process.env.GRIDLINE_CHROME ? { executablePath: process.env.GRIDLINE_CHROME } : { channel: "chrome" };
const browser = await chromium.launch(launch);
for (const j of jobs) {
  const page = await browser.newPage({ viewport: { width: j.w, height: j.h }, deviceScaleFactor: j.scale ?? 1 });
  const svg = readFileSync(resolve(dir, j.src), "utf8");
  await page.setContent(`<!doctype html><style>html,body{margin:0;background:transparent}svg{display:block;width:${j.w}px;height:${j.h}px}</style>${svg}`);
  await page.screenshot({ path: resolve(out, j.name), omitBackground: true });
  await page.close();
  console.log("brand/png/" + j.name);
}
await browser.close();
