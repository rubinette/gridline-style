#!/usr/bin/env node
// Browser check for finished Gridline pages: every file × width × colour scheme.
// Reports horizontal overflow, controls under 40px tall, console errors and
// broken images; optionally saves full-page screenshots for the visual pass.
//
//   npm install --prefix <skill>/scripts        # once: playwright-core
//   node <skill>/scripts/layout.mjs page.html [more.html] [--widths 1280,375,320]
//        [--schemes light,dark] [--shots out/] [--full]
//
// Uses the installed Google Chrome (channel "chrome"); set GRIDLINE_CHROME to
// an executable path to use another Chromium.
import { pathToFileURL } from "node:url";
import { resolve, basename } from "node:path";
import { mkdirSync } from "node:fs";

let chromium;
try {
  ({ chromium } = await import("playwright-core"));
} catch {
  console.error("playwright-core is missing. Run: npm install --prefix " + resolve(import.meta.dirname));
  process.exit(2);
}

const args = process.argv.slice(2);
const opt = (name, fallback) => {
  const i = args.indexOf(name);
  if (i === -1) return fallback;
  const value = args[i + 1];
  args.splice(i, 2);
  return value;
};
const flag = (name) => {
  const i = args.indexOf(name);
  if (i === -1) return false;
  args.splice(i, 1);
  return true;
};
const widths = opt("--widths", "1280,375,320").split(",").map(Number);
const schemes = opt("--schemes", "light,dark").split(",");
const shots = opt("--shots", null);
const full = flag("--full");
const files = args;
if (!files.length) {
  console.error("usage: node layout.mjs page.html [...] [--widths 1280,375,320] [--schemes light,dark] [--shots dir] [--full]");
  process.exit(2);
}
if (shots) mkdirSync(shots, { recursive: true });

const launch = process.env.GRIDLINE_CHROME ? { executablePath: process.env.GRIDLINE_CHROME } : { channel: "chrome" };
const browser = await chromium.launch(launch);
let problems = 0;

for (const file of files) {
  const url = pathToFileURL(resolve(file)).href;
  for (const width of widths) {
    for (const scheme of schemes) {
      const context = await browser.newContext({ viewport: { width, height: 900 }, colorScheme: scheme, deviceScaleFactor: width < 600 ? 2 : 1 });
      const page = await context.newPage();
      const errors = [];
      page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
      page.on("pageerror", (e) => errors.push(String(e)));
      await page.goto(url, { waitUntil: "networkidle" });
      await page.waitForTimeout(300);
      const report = await page.evaluate(() => {
        const vw = document.documentElement.clientWidth;
        const scrollers = (el) => {
          for (let a = el.parentElement; a; a = a.parentElement) {
            const o = getComputedStyle(a).overflowX;
            if (o === "auto" || o === "scroll" || o === "hidden" || o === "clip") return true;
          }
          return false;
        };
        const label = (el) => el.tagName.toLowerCase() + (el.className && typeof el.className === "string" ? "." + el.className.trim().split(/\s+/).join(".") : "");
        const wide = [...document.querySelectorAll("body *")]
          .filter((el) => {
            const b = el.getBoundingClientRect();
            if (!b.width || getComputedStyle(el).position === "fixed") return false;
            return (b.right > vw + 1 || b.left < -1) && !scrollers(el);
          })
          .slice(0, 5)
          .map((el) => `${label(el)} → ${Math.round(el.getBoundingClientRect().right)}px`);
        const small = [...document.querySelectorAll("a.button, button, .icon-btn, input:not([type=hidden]), select, summary")]
          .filter((el) => el.offsetParent && !el.closest("[hidden], .sr-only, .skip-link"))
          .filter((el) => el.getBoundingClientRect().height < 39.5)
          .slice(0, 5)
          .map((el) => `${label(el)} ${Math.round(el.getBoundingClientRect().height)}px`);
        const images = [...document.images].filter((img) => img.complete && img.naturalWidth === 0).map((img) => img.getAttribute("src"));
        return { overflow: document.documentElement.scrollWidth - vw, wide, small, images };
      });
      const issues = [];
      if (report.overflow > 0) issues.push(`horizontal scroll ${report.overflow}px`);
      if (report.wide.length) issues.push(`outside viewport: ${report.wide.join(", ")}`);
      if (report.small.length) issues.push(`controls under 40px: ${report.small.join(", ")}`);
      if (report.images.length) issues.push(`broken images: ${report.images.join(", ")}`);
      if (errors.length) issues.push(`console: ${errors.slice(0, 3).join(" | ")}`);
      const tag = `${basename(file)} @ ${width} ${scheme}`;
      if (issues.length) {
        problems += 1;
        console.log(`ISSUE ${tag}\n  - ${issues.join("\n  - ")}`);
      } else {
        console.log(`OK    ${tag}`);
      }
      if (shots) {
        await page.screenshot({ path: `${shots}/${basename(file, ".html")}-${width}-${scheme}.png`, fullPage: full });
      }
      await context.close();
    }
  }
}
await browser.close();
process.exit(problems ? 1 : 0);
