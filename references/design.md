# Gridline design spec

Read the section for what you are changing. Filling a template needs none of this; the templates already carry every rule. Values live in `tokens.json` and `src/css/`; markup for each component is in `components.md`.

## 1. What Gridline is

A quiet, engineered page: a warm gray-white canvas, hairline construction lines that frame the content, one electric-blue accent, a light serif for display type and a mono face for everything that is furniture (labels, metadata, buttons, code). The construction is visible on purpose — rails, grids, diamond nodes — but it frames content and never competes with it. The page should feel drafted, not decorated, and never like an editor screenshot.

Three habits keep it honest:

1. **Every line encodes structure.** A rail, a band edge, a column divider. No ornamental rules, ticks or side accents.
2. **One accent.** Blue marks the primary action, the current location, links and one small cue per view (the eyebrow). Titles, prices, bullets, avatars and disclosure markers are ink or neutral, so the blue that remains always means something. Status colours label state and nothing else.
3. **Square and flat.** Corners are 0 (`--radius`). Only avatars and status dots are round. Depth is a hard offset in the accent band colour, never a blur.

## 2. Colour

- Light and dark token sets are in `tokens.json` and `src/css/tokens.css`. Dark follows `prefers-color-scheme` unless the page sets `data-theme="light|dark"` on `<html>`; the theme toggle stores the choice in `localStorage["gridline-theme"]` and `boot.js` restores it before paint.
- Light derived colours (`--accent-soft`, `--accent-hover`, `--accent-line`, `--band`) are `color-mix()` of `--accent` inside `@supports`, with hex fallbacks, so changing `--accent` recolours the family. Dark values are explicit hex so they outrank the light derivations; a custom dark accent must set them too.
- Surfaces step up from `--canvas` (page) to `--surface` (content columns) to `--paper` (cards, figures, inputs). Lines: `--grid` (construction grid, faintest), `--line` (rails, borders), `--line-strong` (diamond outlines, table heads).
- Text: `--ink` body, `--ink-2` secondary, `--muted` metadata. Keep body text at or above WCAG AA in both themes; `--muted` is for labels, not paragraphs of reading text.
- Status (`--ok`, `--warn`, `--err` and `-soft`) appear only in `.state` labels, `.callout-warning` / `.callout-caution` and the window sketch's state chips.
- Code surfaces are dark in both themes (`--code`), with a restrained palette in `syntax.css` (Chroma class names, so Hugo output and hand-marked code match).

## 3. Type

- Stacks name the OFL faces IBM Plex Serif, IBM Plex Sans and Lilex first, then platform fonts. The stacks must degrade cleanly: a page reads correctly with none of the faces loaded.
- Traditional Chinese pairs each Latin role with a Chinese face:

  | Role | Latin | Chinese | Fallbacks |
  | --- | --- | --- | --- |
  | `--display` titles, section heads | IBM Plex Serif | Noto Serif TC (Source Han Serif) | Songti TC, PMingLiU |
  | `--body` reading text, interface | IBM Plex Sans | IBM Plex Sans TC | Noto Sans TC, PingFang TC, Microsoft JhengHei |
  | `--mono` labels, metadata; `--code-font` | Lilex | IBM Plex Sans TC (no CJK mono is worth using) | Noto Sans TC, PingFang TC, Heiti TC |

  Song-style serif carries Plex Serif's stroke contrast, so Chinese titles stay in the serif; heavier Song weights crowd, hence 400 (500 for section heads). Plex Sans TC is the Plex family's own Chinese, matching Plex Sans in stroke weight and body proportions in mixed text; Noto Sans TC covers more characters and is installed more widely, so it is the fallback. Mono and code keep Lilex first so Latin and digits align; Chinese in them falls through to Plex Sans TC.
- Web fonts load through the head block in `src/parts/fonts.<lang>.html` (marked OPTIONAL in the templates), never as one whole file per CJK face (5 to 20 MB). Every face is sliced by `unicode-range`: Google Fonts slices Plex Serif and Sans, Lilex and Noto Serif TC; IBM Plex Sans TC is sliced here: `scripts/fonts.py` cuts IBM's complete fonts along Google's frequency-ordered Noto Sans TC slices (`src/fonts/cjk-slices.txt`) into `assets/fonts/ibm-plex-sans-tc/`, which the templates load from jsDelivr pinned to a commit and hugo-gridline serves itself. (IBM's own split files are not ordered by frequency, so an ordinary page touched most of them: 2 to 3 MB, against 0.5 to 0.9 MB now.) After re-running `fonts.py`, commit, then point the jsDelivr URL in `fonts.zh-tw.html` at that commit. A first Chinese page view costs roughly 0.5 to 0.9 MB of Plex Sans TC and about 1 MB of Noto Serif TC; later pages reuse most slices from cache. A page fetches only the slices holding its characters, with `font-display: swap`. English pages load no CJK faces. Weights loaded: Plex Serif 300, 400, 500 and italic 300, 400; Plex Sans 400, 500, 600 and italic 400; Lilex 400 to 600; Noto Serif TC 400 and 500; Plex Sans TC 400, 500, 600. To self-host (strict CSP, no third-party requests), copy the same sliced files and keep the `unicode-range` rules; to go without, delete the block.
- PDFs (`document` templates, WeasyPrint) load no web fonts: install the faces where you render.
- `--display` (serif) for titles and section heads; `--body` (sans) for reading text; `--mono` for labels, buttons, metadata, captions; `--code-font` for code. In Traditional Chinese `--mono` adds CJK faces after the Latin mono so Chinese labels render, while `--code-font` keeps a Latin mono first so code aligns.
- Colour: every title (hero, band, post, docs, CTA, document cover) is `--ink`. The light serif in ink against small accent mono labels is the signature; an accent headline competes with the primary button.
- Weights: Latin display 300 (titles) and 400 (h2, cards); CJK titles 400 and CJK section heads, cards and FAQ 500 (CJK at 300 is too thin, and 500 at title size reads heavy beside Latin 300); emphasis 600, never heavier. Interface emphasis (brand, current nav item) is 600.
- Italic only for an English `<em>`, an English pull quote and English figure captions. CJK never gets synthetic italic: `<em>` in Chinese prose uses emphasis dots (`text-emphasis`), captions and quotes stay upright.
- Every page sets `text-wrap: balance` on headings, `pretty` on paragraphs, tabular numerals on dates, counts, prices and tables, and for Chinese `line-break: strict`, `text-autospace` and `text-spacing-trim: trim-start` on headings. Chinese dates are written without spaces: `2026年11月10日`.
- Measure: prose stays near 70ch (38em in Chinese).

## 4. Construction

The construction is what makes a page Gridline. Its rules come from fixing real misalignments; follow them exactly.

### 4.1 Frame and rails

Every band of the page puts its content in a `.frame`: `width: var(--frame-w)` (1120px, less the gutter on narrow screens), centred, with a 1px `--line` border on each side. Stacked frames read as two continuous rails down the page. The site header, every band, every divider and the footer share the same frame.

### 4.2 Grids

`.grid-bg` draws the construction grid behind a band (hero, stats, CTA). Each side margin's grid is anchored to its rail, and inside the frame `background-repeat: round` fits a whole number of cells between the rails, so **no grid line ever runs a pixel or two beside a rail** (it reads as a doubled rail). Choose `--grid-size` so it divides the 1120px frame and lines land on whole pixels: 20px for heroes, 40px for the CTA and stats bands (16px and 32px below 600px, where `round` keeps them between the rails).

Grids frame heroes and bands. Never put a grid behind body copy people read.

### 4.3 Bands with outer rails

A `.band` (post header, changelog header) adds a second pair of rails up to `--edge` (48px) from the viewport: the margins outside the frame carry a fine grid of half-pixel accent lines (`--fine-cell` 10px, drawn as an SVG mask so it anti-aliases on 1x screens), the strip between the outer and frame rails is plain canvas, and the content inside the frame is clean canvas. `.band.hatch` adds a diagonal hatch inside the frame that fades in toward the right rail.

Below 1264px (`--max` + 2 × `--edge` + 2 × 24px) the outer rails would sit on or within 24px of the frame rails, so they fold into the frame: `--rails` becomes `--frame-w`, and their lines and diamonds stop drawing. Never let two rails run a few pixels apart.

### 4.4 Diamond nodes

Small hollow diamonds (`--node` 7px, `--node-fill`, 1px `--line-strong`) mark where a rail or column divider crosses a horizontal line. Rules:

- **One diamond per crossing.** Two diamonds at the same point (or 1px apart) look like a smudge. When two systems would draw at one crossing (folded outer rails), only one draws.
- **Centred on the 1px line.** A 1px border at the start of a box occupies its first pixel, so its centre is −0.5px from the padding edge: diamonds use `left: -.5px`, `left: calc(100% + .5px)`, `top: -.5px`, `top: calc(100% + .5px)` with `translate(-50%, -50%)`. The element that carries outer-rail diamonds gets the same transparent border box as the elements that draw the rails (`.header-rails`).
- **Drawn by the top layer.** The sticky header draws the diamonds on its bottom border (`.site-header .junction`, plus `.header-rails` on pages with a band); a band sits on its own layer (`z-index: 1`) so the content after it never covers the lower half of its bottom diamonds. Anything that opens over the header (mobile menu) sits above the diamonds.
- Decorative only: `aria-hidden="true"`, `pointer-events: none`.

Markup: an empty `<i class="junction">` inside a box whose two edges are rails; its `::before` and `::after` are the diamonds. A second `<i class="junction">` marks the bottom edge.

### 4.5 Dividers and cells

- `.divider`: a 12px hatched band (`--band` diagonal stripes) between major sections, diamonds on both edges. `.divider.plain`: a single hairline for lighter breaks (hero to value strip, before the footer).
- `.cells` (and `.card-grid`): columns separated by vertical rails, with a diamond at each divider's top and bottom where it meets the lines above and below. Below 880px they stack and the diamonds move to the row ends on the frame rails. `.cells.two`, `.cells.four` set the column count.

## 5. Depth and texture

- `--shadow-offset` (6px both ways, accent band colour) on code blocks, the product window, the featured plan and the mobile menu. `2px 2px 0 var(--band)` on figures and the diagram viewer panel. Nothing blurs.
- Hatches (135°, 3–4px period) are the texture: divider bands, card media frames, feature media, the featured plan, `.row` hover (fading toward the title), `.band.hatch`.
- Print drops shadows (WeasyPrint ignores them) and relies on borders.
- Section heads: title, then a 14px gap and a lead in `--ink-2` at line-height 1.6 (max 520px). Changelog release subheads (h3) are 20px serif without a rule; the card already frames them.
- Lists use neutral square bullets (`--muted`); pull quotes a 1px `--line-strong` rule; callouts a hairline box (`--accent-line` for notes, `--line-strong` for warnings) on their soft wash, never a thick side bar.

## 6. Interaction

- Transitions are `.15s` on colour, border and background only; nothing essential moves. `prefers-reduced-motion` removes them.
- Focus: 2px accent outline, 3px offset (inset on dense controls). Controls are at least 40px tall on every width.
- Hover states: rows gain an accent-line border, a soft accent wash and a fading hatch; cards lift to `--paper` and their title turns accent; buttons darken their border.
- Every page works without JavaScript: navigation, TOC, disclosures (`<details>`), anchors and content are in the document; `site.js` only adds the theme toggle, the menu buttons, copy buttons and TOC highlighting.

## 7. Surfaces

All screen surfaces share the header, footer, frame and tokens. Templates: `assets/templates/<surface>-<lang>.html`.

### Blog index (`blog-index`)
Hero on the 20px grid → divider → three featured `.card-grid` cards → divider → `.index-body`: category and author rail (`.cat-nav`, current item accent) beside the post list grouped by year (`.year` labels, `.row` links with avatars, category badge, date) → pagination → footer. Below 880px the rail becomes a wrapped chip list above the list.

### Post (`post`)
`.band.hatch` header (category eyebrow, title, byline with avatars and roles, date / reading time) → `.post-layout`: `.prose` article beside a 280px aside (sticky on-this-page TOC with the current section highlighted, optional links box) → tags, older / newer post → CTA → footer. Below 1080px the aside hides and an inline `<details>` TOC opens the article. Figures, code blocks, callouts, tables and Mermaid diagrams are prose components (`components.md`).

### Docs (`docs`)
Header with the main nav (Docs current) and a search field → `.docs-layout`: navigation rail of `<details class="docs-group">` sections (current page accent), article (breadcrumbs and edit button on one row, title, full-width lead, prose with steps, states, reference cards, previous / next, last updated), on-this-page rail. Below 1180px the TOC rail folds into the article; below 880px the navigation collapses behind a disclosure button (open by default without JavaScript).

### Changelog (`changelog`)
`.band` header with a centred title → `.release-layout`: rail of channels and version anchors; feed of `.month` labels and `.release` cards (version, latest badge, date, prose notes grouped by h3: features, fixes, breaking changes); pin board with links and the release policy. Below 1180px the pin board moves under the feed; below 880px the rail becomes chips.

### Landing (`landing`)
Optional announcement strip → product hero on the grid (eyebrow category, title, lead, primary button with a key hint, secondary button, platform note) → plain divider → value strip (three `.cells`) → product panel (an abstract `.window` with the offset shadow; replace with a real screenshot inside the window frame, never imitate a real product's UI) → feature rows (`.section-head` with actions, a two-column row with media, a three-column text row) → optional stats band (real, sourced numbers only) → workflow showcase (exclusive `<details name>` accordion beside a figure) → optional plans (one `.featured`) → FAQ → optional latest posts (`.card-grid`) → CTA → footer. Testimonials are allowed only with real, attributable quotes (`.quote-grid`); there is no template slot for invented ones.

### Document (`document`)
A4 pages for WeasyPrint: a cover with one construction `.frame` on the 8mm grid (fixed 240mm high; WeasyPrint places bottom corners from content height otherwise) and a diamond on each corner; content pages with a running label and folio, section heads, cards, callout, table, steps, dark code, pull quote and fine print. Body ≥ 9.5pt, code ≥ 8pt, tables and code never split. Below 820px on screen the pages read as one column.

### Application UI
No template: see `app-ui.md`.

## 8. Usability

Gridline pages should be self-evident: a reader glances, recognises what everything is and what can be clicked, and moves on. These rules come from Steve Krug's *Don't Make Me Think*, the Laws of UX (lawsofux.com), Nielsen's heuristics and WCAG 2.2; each names its source so a trade-off can be argued from it.

- **Site ID and persistent navigation on every page** (Krug, Jakob's law). Every surface, docs included, carries the brand link and the main navigation in the header. Below 820px the navigation folds behind the Menu button; it never disappears. When the brand name is hidden for room, it stays in the link for screen readers so the home link always has a name.
- **"You are here"** (Krug, Nielsen 1). The header link for the current section carries `aria-current="page"` (a post belongs under Blog; a home page that is the blog index belongs under Blog too). Rails mark the current page or filter the same way.
- **Obviously clickable, and nothing else looks clickable** (Krug, law of similarity). Links in text are underlined in the accent line colour; whole-row and card links underline or recolour their title on hover. Badges are labels: no hover state, never a link styled as a badge.
- **One kind of thing per column** (law of similarity, Prägnanz). A list's badge column shows the same kind of label on every row (the category). Status such as "featured" or "newest" belongs where it is the only one of its kind (the featured cards), not mixed into the category column.
- **Labels say where they go** (Krug, Jakob's law). Between posts use "Older post" / "Newer post", not "Previous" / "Next", which readers cannot map to time. Buttons are verbs; arrows mark navigation.
- **Target size** (Fitts's law, WCAG 2.5.8). Controls are at least 40px tall (§6). A link set apart from running text (footer, byline, version rail, chips) is at least 24px tall; links inside a sentence are exempt. `scripts/layout.mjs` checks both.
- **Few choices at a time** (Hick's law, Miller's law). Keep the main navigation to about five items and one primary button per group; longer sets go in the footer or a rail, grouped under labels.
- **One standout per view** (Von Restorff effect). The accent marks one primary action and the current location; a second accent-coloured element competes with it.
- **Omit needless words** (Krug). An eyebrow adds information the title does not (a category, a step), never repeats it ("Blog" above "From the blog"). Leads are one or two sentences.
- **Keyboard and structure** (WCAG 1.3.1, 2.1.1, 4.1.3). Headings do not skip levels (the value strip under the hero is `h2`); scroll boxes that overflow (`.table-wrap`, diagrams) get a tab stop from `site.js`; the copy button announces "Copied" through `aria-live`.

## 9. Responsive and accessibility review

Check every shipped language at 1440 (outer rails shown), 1280, 1000, 375 and 320px, in light and dark (`scripts/layout.mjs`):

- no horizontal scroll; headings wrap deliberately; navigation and CTA groups stack without clipped labels at 320px;
- every control at least 40px tall, every link outside running text at least 24px, with a visible 2px focus outline;
- header navigation present with the current section marked, and the usability rules in §8 hold;
- grid lines meet rails, one diamond per crossing, outer rails folded below 1264px;
- text contrast WCAG AA in both themes, including state labels on their soft backgrounds;
- `<html lang>` matches the content (`en`, `zh-Hant-TW`), and Chinese headings, captions and emphasis stay upright.

## 10. Originality boundary

Gridline's layout vocabulary was informed by looking at zed.dev at a high level (rails, diamond nodes, editorial serif, mono furniture). It is an independent design system: never add Zed's logo, wordmark, screenshots, illustrations, marketing copy or source, and never imply affiliation. Examples use the fictional product Orbitline and say so. Third-party code that ships with a page (Pele for Mermaid) keeps its licence notice.

## 11. Relationship to hugo-gridline

The Hugo theme `hugo-gridline` does not keep its own copy of the system: its `scripts/sync-gridline-style.py` copies `src/css/{tokens,base,construction,components,prose,blog,diagram,syntax}.css` and `src/js/{boot,site,diagram}.js` from this repository, and its templates use the same class names. Change styles here, rebuild, then run the sync in the theme (`--check` reports drift). Rules a Hugo site needs (language switch, large avatars, line-number tables) belong here too, so both stay one system.
