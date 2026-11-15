# Anti-patterns

Mistakes that break the Gridline look, most of them seen in real fixes. Each line says what goes wrong and what to do instead.

## Construction

1. **A grid line a few pixels beside a rail.** Reads as a doubled rail. Anchor grids to rails (`.grid-bg` does) and pick a cell size that divides the frame (20 / 40 for 1120px).
2. **Two diamonds at one crossing, or 1px apart.** Looks like a smudge. One element draws each crossing; fold outer rails into the frame below 1264px.
3. **Diamonds off the line.** Centre on the 1px border: −0.5px from the padding edge, and give the element that carries outer-rail diamonds the same border box as the elements drawing the rails.
4. **Half a diamond.** The next section paints over the bottom half, or the sticky header over the top half. Give the band its own layer (`z-index: 1`) and let the header draw the diamonds on its own bottom edge.
5. **Rails a few pixels apart.** Two parallel rails closer than ~24px read as an error, not structure.
6. **Grid behind reading text.** Grids frame heroes and bands; prose sits on `--surface`.
7. **Tinted margins.** The fine grid in a band's margins is lines on the canvas, not a coloured fill.
8. **Half-pixel gradient lines.** A `.5px` gradient stop renders nothing on 1x screens; use an SVG mask (as `.band` does) or 1px lines.

## Colour and depth

9. **A second accent.** Green buttons, purple badges, gradient headings. One blue; status colours only on state labels.
10. **Blurred shadows, glows, glassmorphism.** Use the hard offset in the band colour, or a border.
11. **Rounded corners.** `--radius` is 0; only avatars and status dots are round.
12. **Hard-coded hex in a component.** Use tokens so dark mode and a custom accent follow.
13. **Light-only fixes.** Every change is checked in dark too (diamond fill, fine-grid mix, code surfaces).

## Type

14. **Bold display headings.** Latin display is 300/400; CJK 500; nothing above 600.
15. **Synthetic CJK italic.** Chinese emphasis uses emphasis dots; captions and quotes stay upright.
16. **Latin-only mono for Chinese labels.** Mono labels need CJK fallbacks (and in print every stack does).
17. **Spaced Chinese dates in mono** (`2026 年 11 月 10 日`). Write `2026年11月10日`.
18. **Linked web fonts.** Name the stacks; do not link or embed fonts.

## Components and content

19. **Ornamental lines.** Short accent rules under headings, side bars on cards. Every line encodes structure, state or grouping.
20. **Controls under 40px.** Including summaries and search inputs (make the input itself the 40px control).
21. **`<style>` inside an inline SVG.** It applies to the whole page. Use the `.sketch` classes.
22. **Imitating a real product UI** in the product panel, or Zed's marks anywhere. Keep the schematic abstract.
23. **Invented numbers, logos, quotes.** Use `[DATA NEEDED: …]` and report the gap.
24. **Hiding content on small screens.** Move it (pin board under the feed, rail into chips), do not drop it.
25. **Placeholders or OPTIONAL blocks left in a finished page.** Fill or delete; `scripts/check.py` must pass without `--allow-placeholders`.

## Usability

26. **A page without the main navigation** (docs headers, landing variants). Keep the header nav on every page; fold it behind Menu on small screens.
27. **No "you are here".** Mark the current section with `aria-current="page"` in the header and the current item in any rail.
28. **Mixed labels in one column** ("Featured" next to "Engineering"). One kind of badge per column; flag status elsewhere.
29. **"Previous" / "Next" between dated posts.** Say "Older post" / "Newer post".
30. **Eyebrow repeating the title.** Drop it, or use it for information the title lacks.
31. **Tiny utility links** (footer legal links, author names at line height). At least 24px tall.
32. **Skipped heading levels** (an `h3` right under the `h1`) and scroll boxes the keyboard cannot reach.

