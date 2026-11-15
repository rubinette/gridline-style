# Gridline brand guidelines

**English** · [繁體中文](BRAND.zh-TW.md)

> Status: v0.2 (Nov 15, 2026).

This document says what the Gridline brand is, how it looks and how it speaks. It is for anyone who introduces, promotes or extends Gridline: writing a README, making screenshots or cover art, mentioning Gridline elsewhere, or dressing their own product in Gridline. Implementation values and component markup are not repeated here; see [`references/design.md`](references/design.md), [`references/tokens.json`](references/tokens.json) and [`references/components.md`](references/components.md).

## 1. What the brand is

### 1.1 In one sentence

**Gridline is a design system that draws its construction lines: a gray-white canvas, hairline rails, diamond nodes and one electric blue, so technical content reads like a precise drawing rather than a decorated page.**

### 1.2 Brand architecture

| Name | What it is | How to write it |
| --- | --- | --- |
| **Gridline** | The brand and the visual system | Capital G, one word, no space or hyphen |
| **gridline-style** | The design-system repository and Claude skill (spec, CSS, JS, templates) | Lower case, in code type; only when you mean the repository or skill |
| **hugo-gridline** | The Hugo blog theme built on gridline-style | Lower case, in code type; its display name in the Hugo theme directory is "Gridline" |
| **Orbitline** | The **fictional** product used in sample content | Every appearance must have a "fictional" disclosure nearby |

- When you mean the look, say "Gridline style" or "a page made with Gridline", not "gridline-style style".
- Do not translate the brand name: Chinese text keeps "Gridline".
- gridline-style replaces the earlier zed-style. Do not use the zed-style name publicly except in migration notes.

### 1.3 Personality

| Is | Is not |
| --- | --- |
| Precise: every line lands on a pixel | Showy: animation, gradients, glow |
| Quiet: construction frames the content | Cold: it is still a readable, warm gray-white |
| Honest: numbers are sourced, samples say they are fictional | Inflated: an unsourced "10× faster" |
| Equally bilingual: English and Traditional Chinese ship together | Translated as an afterthought |

The three habits that never change (design.md §1): **every line encodes structure**, **one accent**, **square and flat**.

## 2. Mark

### 2.1 The Gridline mark

The mark comes from hugo-gridline's [`static/favicon.svg`](https://github.com/rubinette/hugo-gridline/blob/main/static/favicon.svg): a square frame on a 32 × 32 grid, a faint cross of construction lines through it, and a hollow diamond at the centre; standalone files are listed in §2.4. It condenses the brand's three elements: frame, grid and node.

| Part | Spec |
| --- | --- |
| Frame | 27 × 27, 2-unit stroke in the accent, filled with `--canvas` |
| Cross | 1-unit stroke in the accent at 45% opacity |
| Diamond | 11-unit diagonal, 2-unit stroke in the accent, no fill |
| Dark | Fill becomes the dark `--canvas` (`#111216`), strokes the dark accent (`#7e9bff`) |

Rules:

- **Minimum size** 16 px (favicon). Below 24 px the cross may be dropped.
- **Clear space** at least one diamond's width (about a third of the frame) on every side.
- **Two colourways only**: light (blue frame on gray-white) and dark (light blue on near-black). Where only one colour is possible, stroke everything in `--ink`.
- **Never** round the corners, add a shadow or gradient, fill the diamond, rotate the mark, recolour it outside the accent, or swap the diamond for a dot.

### 2.2 Wordmark

The header lockup is mark + name: the name in the body sans (`--body`, IBM Plex Sans first), weight 600, letter-spacing −0.01em, colour `--ink`, 10 px from the mark. The name is always "Gridline": no all caps, no attached slogan.

### 2.3 Monogram

When Gridline dresses **another** product, the header, card placeholders and CTA show that product's monogram (`.brand-mark`): a 26 px square, 1 px accent border, mono 500, upper case.

- The letter comes from the product's own name (Hugo: `params.monogram`, defaulting to the first character of the site title).
- A product with a Chinese name may use one Han character; check it reads clearly at 26 px.
- The monogram is the **adopter's** mark, not Gridline's; an adopter with its own logo can replace it.

### 2.4 Mark files

Everything is in [`brand/`](brand/). The SVGs are the source; PNGs come from `node scripts/brand.mjs` (run `npm install --prefix scripts` first; set `GRIDLINE_CHROME` to a Chromium path if Chrome is not installed).

| File | Use |
| --- | --- |
| `mark.svg`, `mark-dark.svg` | The mark, fixed light / dark |
| `mark-auto.svg` | Favicon; follows the system theme (contains a `<style>`, so use it only as a standalone file, never inline it in a page) |
| `mark-small.svg` | Below 24 px; no cross |
| `mark-mono.svg` | Single colour, stroked with `currentColor` |
| `lockup.svg`, `lockup-dark.svg` | Horizontal mark + wordmark for READMEs and document headers |
| `og.svg`, `og-zh-tw.svg`, `og-dark.svg` | Social previews, 1200 × 630 |
| `png/` | Mark at 16–512 px, dark mark, lockups at 2x, social previews |

Social preview layout: a 1040 px frame (26 cells of 40 px) between two band lines, one diamond at each of the four crossings, a 40 px construction grid inside the frame, the mark at 80 px top left, then "Gridline" as a large accent serif and one mono line of description, with repository names and the licence below the frame. For another project's preview, keep the layout and swap the mark, name and line.

The wordmark and previews name font stacks rather than embedding fonts, so the PNGs use whatever faces the rendering machine has. Regenerate them on a machine with IBM Plex and Lilex installed before a public release.

## 3. Colour

The full light and dark palettes are in [`tokens.json`](references/tokens.json). At brand level, remember these:

| Role | Light | Dark | Where |
| --- | --- | --- | --- |
| Canvas | `#f5f5f0` | `#111216` | Page background, warm gray-white / near-black |
| Ink | `#171717` | `#ececea` | Body text and headings |
| Line | `#d9d9d2` | `#2c2d33` | Rails, borders |
| **Accent** | **`#315cf4`** | **`#7e9bff`** | Primary action, current location, links, one key idea per view |
| Code | `#16171a` | `#0c0d10` | Code blocks are dark in both themes |

**Proportion**: a view is roughly 90% neutrals (canvas, surface, lines, ink) and under 10% accent. When there is too much blue, remove decorative blue first, never the primary button.

**Status colours** (green ok, amber warn, red err) appear only on state labels and warning callouts. They are not a second accent.

**Contrast** (computed, WCAG):

| Pair | Ratio |
| --- | --- |
| Accent `#315cf4` text on canvas `#f5f5f0` | 4.84:1 (AA) |
| White text on the accent button | 5.29:1 (AA) |
| `--muted` text on the light canvas | 5.20:1 (AA) |
| Dark accent `#7e9bff` on the dark canvas | 7.15:1 (AAA) |
| Dark button text `#0b0d14` on `#7e9bff` | 7.41:1 (AAA) |

When you change the accent, the light derived colours follow (`color-mix()`); the dark ones must be set by hand. Recheck this table in both themes.

## 4. Type

| Role | Faces (in fallback order) | Use |
| --- | --- | --- |
| Display | IBM Plex Serif → platform serif; Chinese: **Noto Serif TC** → Songti | Titles, section heads |
| Body | IBM Plex Sans → platform sans; Chinese: **IBM Plex Sans TC** → Noto Sans TC → PingFang, Microsoft JhengHei | Reading text, interface, wordmark |
| Mono | Lilex → IBM Plex Mono → platform mono; Chinese falls back to IBM Plex Sans TC → Noto Sans TC | Labels, buttons, dates, metadata, code |

- All OFL faces, free to embed. Chinese titles stay in a Song-style serif because it carries Plex Serif's stroke contrast; Chinese text uses Plex Sans TC, the Plex family's own Chinese, so mixed text keeps one stroke weight and body size. There is no Chinese mono worth using: Latin and digits stay in Lilex and Chinese falls back to Plex Sans TC.
- On the web, load fonts **sliced by `unicode-range`** so a page downloads only the characters it uses; **never a whole Chinese font file**. Pages must still read correctly with no web fonts at all.
- Titles are set in ink, never the accent. Latin display 300 (titles) and 400 (sections); CJK titles 400 and section heads 500 (heavier Song weights crowd); emphasis 600 and **nothing heavier**.
- Italic only for English `<em>`, quotes and captions. Chinese is **never italic**; emphasis uses emphasis dots (`text-emphasis`).
- The contrast of a light serif headline against small mono labels is the most recognisable type trait. Keep it in every piece.

## 5. Construction vocabulary

This is what sets Gridline apart from other minimal styles. Brand-level principles:

1. **Rails**: content sits in a 1120 px frame with 1 px lines on both sides, forming two continuous lines down the page.
2. **Grids**: only behind framing bands (hero, stats, CTA), **never behind reading text**.
3. **Diamonds**: 7 px hollow diamonds only where lines cross, one per crossing.
4. **Hatch**: a fine 135° hatch is the only texture, on divider bands and media frames.
5. **Depth**: a hard 6 px offset in the pale accent band colour only; **no blurred shadows, glows or glass**.

The page is drafted, not decorated: if a line cannot say what structure it encodes, remove it. Pixel-level rules are in design.md §4 and [`anti-patterns.md`](references/anti-patterns.md).

## 6. Illustration, diagrams and screenshots

### 6.1 Covers and schematic illustration

Follow the hugo-gridline example site's `exampleSite/assets/covers/*.svg`:

- An 800 × 500 canvas over a faint 50-unit grid (`#8f8f88` at about 22% opacity).
- Objects are **abstract wireframe schematics**: boxes, columns, bars standing for text; mostly neutral gray `#8f8f88`, with **one** accent element marking the point.
- 1.5–2 strokes, square caps (`stroke-linecap: square`), fills only at very low opacity (6–8%).
- Text labels in mono, small and few.
- No people, photo collage, 3D or gradients.

### 6.2 Diagrams

Mermaid diagrams render with Pele and follow the theme's colours and type; see [`references/mermaid.md`](references/mermaid.md). Data visualisation sits on neutrals with the accent marking one key series.

### 6.3 Product screenshots

- Use **real** screenshots only, inside a `.window` or `.figure` frame (square, 2 px hard offset).
- Without one, use an abstract schematic (`.sketch`). **Never imitate a real product's interface.**
- README screenshots should represent light and dark, English and Chinese; hugo-gridline has `images/screenshot.png`, `screenshot-zh-tw.png` and `tn.png` today.

## 7. Voice and copy

### 7.1 Principles

- **Headings state the point**: "Edit together, never wait", not "Explore the endless possibilities of collaboration".
- **Leads are one or two sentences**; labels are short nouns; buttons are verbs ("Download", "Read the docs"), one primary per group.
- **Links say where they go**; an arrow (→) marks navigation, not emphasis.
- **No inflation**: a number without a source ships as `[DATA NEEDED: …]`, never as a precise-looking guess.
- **Never invent** customers, logos, testimonials or reviews.

### 7.2 English and Chinese

| Item | English | Traditional Chinese |
| --- | --- | --- |
| Dates | `Nov 10, 2026` | `2026年11月10日` (no spaces) |
| Punctuation | Half-width | Full-width (，。：；「」) |
| Emphasis | Italic `<em>` or bold | Bold or emphasis dots, never italic |
| Brand and product names | As is | As is, untranslated |
| Space between CJK and Latin | — | Optional, but consistent within a document |

Every page ships in `en` and `zh-TW`; `<html lang>` is `en` or `zh-Hant-TW`.

### 7.3 Standard descriptions of Gridline

- **One line (en)**: A grid-led design system: hairline construction lines, serif display type, mono metadata and one electric-blue accent, in light and dark.
- **One line (zh)**：以構造線為骨架的設計系統：細線導軌、襯線標題、等寬中繼資料與單一電光藍，支援淺色與深色。
- **Hugo theme (en, as in `theme.toml`)**: A grid-led editorial blog theme: hairline construction lines, serif display type, mono metadata, one electric-blue accent.

## 8. Originality and attribution

Gridline's layout vocabulary was informed by zed.dev at a high level (rails, diamond nodes, editorial serif, mono labels), but it is an independent design system:

- **Never use** Zed's logo, wordmark, screenshots, illustrations, marketing copy or code, and **never imply** partnership or endorsement.
- In public descriptions you may say "page structure inspired by zed.dev; design and code are original", together with "not affiliated with Zed Industries".
- Samples always use the fictional Orbitline and say so (footer, callout or FAQ).
- Third-party code shipped with a page (Pele for Mermaid, MIT) keeps its licence notice.
- gridline-style and hugo-gridline are MIT licensed, © 2026 rubinette.

## 9. For adopters: dressing your product in Gridline

When you build your own site or document with Gridline:

- **Replace**: the product name, monogram or logo, navigation, footer, all sample content and the Orbitline disclosure.
- **You may adjust**: the accent (in dark mode set the derived colours by hand and recheck contrast) and which landing sections you keep.
- **Keep**: one accent, square corners, hard offsets, the rail and diamond construction rules, the bilingual type rules, and pages that work without JavaScript.
- **No credit is required** on the page, but a footer or README note linking back to the repository is welcome.
- A site with its own accent and logo is **your brand** using the Gridline system; do not call it "Gridline".

## 10. Quick checklist

Before publishing anything that carries Gridline's name or look:

- [ ] Names written correctly (Gridline / `gridline-style` / `hugo-gridline`)
- [ ] One accent; status colours only for state
- [ ] Square corners; no blurred shadows or gradients
- [ ] Serif headings, mono labels, no Chinese italic
- [ ] Checked in light and dark; text contrast at AA
- [ ] English and Traditional Chinese both done, with each language's date and punctuation rules
- [ ] No invented numbers, customers or quotes; samples marked fictional
- [ ] No Zed marks or assets, no implied affiliation
