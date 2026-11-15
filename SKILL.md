---
name: gridline-style
description: Create or refine pages in the Gridline style — a gray-white canvas framed by hairline construction rails with diamond nodes, one electric-blue accent, serif display type and mono metadata, in light and dark. Templates for product landing pages, documentation, changelogs, blog indexes, blog posts and A4 technical briefs (HTML to PDF), in English and Traditional Chinese, plus guidance for restyling web application UI. Use when asked for a Gridline / hugo-gridline page, a precise grid-led technical site or document, or anything previously made with zed-style. Not for copying Zed or any other brand's marks, screenshots or copy.
---

# Gridline style

A design system for quiet, engineered pages: content framed by visible construction (rails, grids, diamond nodes), one accent, editorial serif headings, mono furniture. It is the system behind the hugo-gridline Hugo theme and replaces zed-style.

Paths below are relative to this skill's directory. Keep the user's files in their working directory and call scripts by full path.

## 1 · Lock the contract

Infer, then state in one line before building: **surface**, **languages** (default both `en` and `zh-TW` when the user writes Chinese, otherwise the user's language), **outputs** (HTML; plus PDF for a document), **length**, and **gaps** (facts or images the input lacks). Ask at most one compact question, and only when two surfaces would produce materially different results.

## 2 · Choose the surface

| The user wants | Template | Notes |
| --- | --- | --- |
| product / landing / home page, pricing, launch page | `landing` | sections are optional; delete what the material does not support |
| documentation, help or how-to page | `docs` | nav rail, article, on-this-page |
| changelog, release notes page | `changelog` | version rail, release cards, pin board |
| blog home or post list | `blog-index` | featured cards, category rail, year rows |
| blog post, article, engineering note | `post` | band header, prose body, TOC aside |
| technical brief, white paper, report, one-pager to print | `document` | A4 pages → PDF via `scripts/render.py` |
| restyle an existing web app (workspace, console, dashboard) | none | read `references/app-ui.md`; bring in `assets/css/gridline.css` |
| a Hugo site | none | use the hugo-gridline theme; this skill's rules still apply |

Templates: `assets/templates/<name>-en.html` and `<name>-zh-tw.html`, self-contained (CSS and JS inline). Filled examples for judging density and tone: `assets/examples/`.

## 3 · Read the right amount

| Task | Read |
| --- | --- |
| Fill a template | the template + `CHEATSHEET.md` + `references/content.md` |
| Add a component a template lacks | `references/components.md` |
| Diagrams | `references/mermaid.md` |
| Change layout, construction or visual behaviour | `references/design.md` (and `anti-patterns.md`) |
| Application UI | `references/app-ui.md` + `references/design.md` |
| Review a page | `references/anti-patterns.md` |
| Name, mark, voice, cover art or attribution | `BRAND.md` |

## 4 · Fill the template

1. Copy the template(s) for the chosen surface and languages into the working directory. Never write the page from scratch, and leave the inline CSS alone during a content fill.
2. Replace every `{{PLACEHOLDER}}`. Long bodies (`BODY_HTML`, `ARTICLE_HTML`, release notes) are prose HTML built from `references/components.md`.
3. Delete blocks marked `OPTIONAL` that the material does not support, and add repeated items (rows, releases, nav groups) by copying the existing markup.
4. Mark the current navigation link with `aria-current="page"`; keep ids unique and anchors resolvable.
5. Follow `references/content.md`: no invented numbers, quotes, logos or screenshots; `[DATA NEEDED: what]` for gaps; translate every visible string in each language.
6. A brand accent: override `--accent` on `:root` (light) and the dark blocks' `--accent`, `--accent-hover`, `--accent-soft`, `--accent-line`, `--band`; check contrast in both themes.

## 5 · Verify

```bash
python3 scripts/check.py page-en.html page-zh-tw.html          # must print OK (no placeholders, gaps, broken links)
node scripts/layout.mjs page-en.html page-zh-tw.html --widths 1440,1280,375,320 --shots shots/ --full
uv run --no-project --with weasyprint --with pymupdf python scripts/render.py brief.html brief.pdf --png pages/   # documents
```

`layout.mjs` needs `npm install --prefix <skill>/scripts` once and Google Chrome. Then open the screenshots (or page PNGs) and check, in every language and both themes:

- rails continuous, one diamond per crossing, grid lines meeting rails, outer rails folded below 1264px;
- headings wrap deliberately, Chinese text upright, no clipped labels at 320px, no horizontal scroll;
- one accent, no blurred shadows or rounded corners, nothing invented;
- documents: page count, folios, no split tables or code, CJK glyphs present.

Fix the most visible defects, re-run, and stop after three rounds; report what remains.

## 6 · Done means

The closing message lists every file produced (each language, each format), the `check.py` and `layout.mjs` results, the PDF page count for documents, every `[DATA NEEDED]` gap and assumption, and an honest visual verdict ("checked at 1440/375 in light and dark" or "build verified, visuals not inspected").

## Visual feedback

When the user rejects how something looks, inspect the render first, name the concrete defect (surface, width, theme, what is off), change the smallest thing that fixes it, and re-verify the affected matrix — the width it was seen at, its neighbours, both themes and both languages. After two unsuccessful rounds on the same element, show 2–3 labelled variants side by side instead of nudging again.

## Changing the system

Sources are in `src/` (CSS modules, JS, i18n, parts, templates, example content). After editing:

```bash
python3 scripts/build.py                      # regenerate assets/
python3 -m unittest discover -s scripts/tests # tests include "outputs are up to date"
node scripts/layout.mjs assets/examples/*.html
```

Update `references/design.md` and `tokens.json` with any rule or value change. hugo-gridline uses these CSS and JS modules directly: run its `python3 scripts/sync-gridline-style.py` after a change (and check its example site) so the theme follows.

## When not to use

A different design language (Material, a Tailwind default), saturated multi-colour palettes, decorative illustration styles, or reproducing another brand's site.
