# Application UI

Use this when applying Gridline to a working web application (workspace, console, dashboard) rather than a page from a template. There is no template: bring the tokens and components into the app's own stylesheet and restyle its existing markup. Keep behaviour, routes and form fields unchanged unless asked.

## Bring the system in

- Copy `assets/css/gridline.css` (every screen module, in cascade order) or just the modules you need from `src/css/` (`tokens`, `base`, `construction`, `components`, plus `prose` for long text). Keep the custom property names so later updates drop in.
- Under a strict CSP (`style-src 'self'`, `script-src 'self'`) keep all CSS in the stylesheet and all JS in files; `assets/js/boot.js` and `site.js` work as external files. Fonts: self-host the sliced files from `src/parts/fonts.<lang>.html` (keep their `unicode-range` rules) or load none; the stacks degrade.
- Everything in `design.md` applies: one accent, `--radius: 0`, hard offsets only, the CJK text rules, 40px controls, 2px focus outlines, light and dark.

## Construction grid: structure sits on grid lines

An app shell can carry a 20px construction grid (`--cell: 20px`) in its outermost layer. Frame edges, header and band rules and any focal card must sit exactly on grid lines; one pixel off reads as a bug.

- Anchor the grid to the page centre: `background-size: var(--cell) var(--cell); background-position: calc(50% + var(--cell) / 2) 0` puts lines at centre ± 20k.
- Make the frame `20n + 1` px wide (e.g. `--frame: 1521px`, `--half: 760px`) and place it with `width: min(100%, var(--frame)); margin-left: max(0px, calc(50% - var(--half)))`, not `margin: auto`: a 1px border occupies the box's first or last pixel, so the extra pixel puts both borders on lines. Apply the same rule to every full-width strip that shares the frame.
- Below the frame width (`@media (max-width: 1520px)` for a 1521px frame) the frame starts at x = 0, so switch the grid to `background-position: 0 0`. Use frame width − 1 as the breakpoint.
- Horizontal rules: with `box-sizing: border-box` and a bottom border, a box whose rule should sit on grid row `y` is `y + 1` px tall when it starts at 0 (header `height: 61px` puts the rule at y = 60).
- Column widths are multiples of the cell (`--rail-left: 240px`, `--rail-right: 380px`); keep them in variables shared by the layout and the markers.
- The grid shows outside the frame and in gutters only. Panels inside the frame are opaque `--canvas` or `--surface`; never put the grid behind text people read.

(Pages from the templates use a different, equivalent rule: grids anchored to each rail with `round` inside the frame; see `design.md` 4.2. Use one approach per surface.)

## Frame, bands and diamonds

- Header content sits inside the frame (`border-inline: 1px solid var(--line)`), with a full-width bottom rule. A 12px hatched band (`.divider`) may follow it.
- Diamonds (`--node`, `--node-fill`, 1px `--line-strong`, `rotate(45deg)`) mark where rules cross the frame and column dividers: one per crossing, centred on the 1px line, above the lines, `aria-hidden`, hidden on mobile where they would crowd.
- Use muted diamonds in app chrome. Reserve accent diamonds for one focal element (a sign-in card's four corners).

## Type and colour

- Headings use `--display` in `--ink` (not accent) at the design weights; supporting text (panel descriptions, metadata) uses `--mono` with `letter-spacing: .02em`; eyebrows are 11px mono uppercase in `--muted`.
- Accent marks the primary action, the current location (selected item, focus ring) and pending items. Status colours appear only on `.state` labels and error text.
- For the mono stack in app chrome put `ui-monospace` before `SFMono-Regular`: Chrome on macOS cannot resolve "SFMono-Regular" by name alone and falls back to a CJK sans.

## Components

- **Buttons**: `.button` (`--surface`, 1px `--line`, 40px), `.button.primary` (solid accent), optional `<kbd>` hint. Secondary navigation buttons end with a muted `→`.
- **Cards, messages, composer**: `--paper` on canvas, 1px line, square, no shadow. Mark a pending or streaming item with a 3px accent left border.
- **Code**: `.code-block` (dark in both themes) with `--shadow-offset`; where the offset would clip, use `outline: 1px dashed var(--line); outline-offset: 4px` instead.
- **Status**: `.state` with `.active` (pending), `.ok` (done), `.warn` (waiting on a person), `.err` (failed).
- **Empty states**: a bordered box with the grid inside, a small bordered icon tile and two short lines.
- **Keyboard hints**: `<kbd class="key">` in mono with a 2px bottom border.
- **Tables**: the prose table style (mono uppercase heads, hairline rows, tabular numerals), wrapped in `.table-wrap`.

## Confirmation dialog for consequential actions

- Native `<dialog>` with `showModal()`, a 3px accent top border, backdrop `rgba(23, 23, 23, .4)` (dark: `rgba(0, 0, 0, .6)`), and an accent-soft callout saying what will happen.
- Show the target, parameters (code block) and a live countdown when the confirmation expires.
- Default focus on the safest choice ("Later"), so Enter and Esc never execute or reject. Offer Later, Reject, Confirm; disable Confirm with a stated reason when the item is no longer actionable.
- If the list behind the dialog re-renders, re-find the live form by id at confirm time.

## Languages

Ship `zh-TW` and `en`, set `<html lang>`, put a compact switch (`EN` / `中文`, mono, bordered, 40px tall) in the header, and translate every visible string including dialog states, empty states, `aria-label`s and server errors.

## Verification

Verify alignment numerically. At widths above and below the frame (e.g. 1886, 1600, 1521, 1520, 1400, 1280) compute each structural edge's distance from the grid origin modulo the cell; every value must be 0:

```js
const W = document.documentElement.clientWidth, ox = W > 1521 ? W / 2 : 0;
const m = v => ((v - ox) % 20 + 20) % 20;
const f = document.querySelector('.workspace').getBoundingClientRect();
[m(f.left), m(f.right - 1), (document.querySelector('header').getBoundingClientRect().bottom - 1) % 20];
```

Then run `scripts/layout.mjs` on the running app's pages (it takes file paths; for a served app, save the page or adapt the URL), inspect a 3× screenshot of a frame corner, and full pages at 1280px and 375px in every language and both themes.
