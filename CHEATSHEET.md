# Gridline · cheatsheet

One page to scan before filling a template or nudging a detail. Full spec: `references/design.md`.

## Eleven invariants

1. Gray-white canvas `#f5f5f0`, content columns `#fbfbf8`, cards `#ffffff`; dark mode mirrors every token.
2. One accent, electric blue `#315cf4` (dark `#7e9bff`): primary action, current location, links, the eyebrow. Titles stay ink.
3. Status colours (ok / warn / err) only on `.state` labels and warning / caution callouts.
4. Square corners (`--radius: 0`); only avatars and status dots are round.
5. Depth is a hard offset in the band colour (`--shadow-offset`, figures `2px 2px 0`), never a blur.
6. Serif display in ink (Latin 300/400, CJK titles 400 and section heads 500), sans body, mono for every label, button and caption; emphasis 600 max. Chinese: Noto Serif TC titles, IBM Plex Sans TC text and interface (Noto Sans TC fallback), Lilex for Latin in mono with Chinese falling back to Plex Sans TC; web fonts sliced by `unicode-range`, never a whole CJK file.
7. Every line encodes structure: rails, band edges, column dividers; a diamond marks each crossing, once, centred.
8. Grids are anchored to rails and frame heroes and bands, never reading text.
9. 40px minimum controls (24px for links outside running text), 2px accent focus outline, works without JavaScript.
10. Never invent facts; `[DATA NEEDED: …]` instead. Fictional examples say they are fictional.
11. Don't make readers think (`design.md` §8): header nav on every page with the current section marked, one kind of label per column, "Older / Newer post", no eyebrow that repeats the title.

## Core tokens

| Token | Light | Dark | Use |
| --- | --- | --- | --- |
| `--canvas` | `#f5f5f0` | `#111216` | page |
| `--surface` | `#fbfbf8` | `#15161a` | content columns, buttons |
| `--paper` | `#ffffff` | `#1a1b20` | cards, figures, inputs |
| `--ink` / `--ink-2` / `--muted` | `#171717` / `#3e3e3c` / `#676762` | `#ececea` / `#c9c9c5` / `#9a9a94` | text |
| `--line` / `--line-strong` / `--grid` | `#d9d9d2` / `#c5c5bd` / `#e8e8e2` | `#2c2d33` / `#3a3b42` / `#1c1d22` | rails, diamonds, grid |
| `--accent` | `#315cf4` | `#7e9bff` | the one accent |
| `--accent-soft` / `--accent-line` | derived | `#1b2240` / `#34406e` | washes, underlines |
| `--band` | accent 6% | accent 8% | hatches, offsets |
| `--code` | `#16171a` | `#0c0d10` | code (dark in both) |
| `--node-fill` | `#ffffff` | `#07080b` | diamond fill |

## Construction

| | Value |
| --- | --- |
| Frame | `--frame-w` = min(1120px, 100% − 2 × 24px); 16px gutter ≤ 600px |
| Outer rails | `--edge` 48px from the viewport; fold into the frame ≤ 1264px |
| Grid | hero 20px, bands 40px (16 / 32 ≤ 600px); band margins: 10px half-pixel accent lines |
| Diamonds | `--node` 7px, 1px `--line-strong`, `--node-fill`, centred on the line (±0.5px) |
| Dividers | 12px hatched band (diamonds both edges) or 1px plain |
| Header | 64px, sticky, draws the diamonds on its bottom edge |
| Breakpoints | 1264 fold · 1180 docs/changelog rails · 1080 post aside · 880 stack · 820 menu · 600 phone · 360 |

## Templates (`assets/templates/<name>-en.html`, `-zh-tw.html`)

| Name | Surface |
| --- | --- |
| `landing` | product page: hero, value strip, panel, features, stats, showcase, plans, FAQ, posts, CTA |
| `docs` | documentation page: nav rail, article, on-this-page |
| `changelog` | release notes: version rail, release cards, pin board |
| `blog-index` | blog home: hero, featured cards, category rail + rows |
| `post` | article: band header, prose, TOC aside, tags, CTA |
| `document` | A4 technical brief → PDF |

## Class quick list

`frame` `grid-bg` `divider` `divider plain` `junction` `band` `band hatch` `band-rails` `cells` `two` `four` · `hero` `hero-inner center|left` `section-head` `cta` `announce` · `button` `primary` `ghost` `icon-btn` `eyebrow` `nav-label` `lead` `badge` `accent` `state active|ok|warn|err` `avatars` · `card-grid` `card` `card-link` `card-media` `card-placeholder` · `prose` `callout callout-note|tip|important|warning|caution` `code-block` `figure` `figure diagram` `table-wrap` `steps` `sketch` · `toc toc-aside` `toc-inline` `links-box` `tag-list` `post-nav` `pagination`

## Commands (run from the skill directory)

```bash
python3 scripts/check.py page.html                 # finished page: must pass
python3 scripts/check.py --allow-placeholders tpl.html
node scripts/layout.mjs page.html --shots out/     # widths × light/dark (npm install --prefix scripts once)
uv run --no-project --with weasyprint --with pymupdf python scripts/render.py brief.html brief.pdf --png pages/
python3 scripts/build.py && python3 -m unittest discover -s scripts/tests   # after editing src/
```
