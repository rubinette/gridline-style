# Content rules

How to fill a Gridline template so the page is honest, consistent and bilingual.

## Placeholders and gaps

- Templates use `{{UPPER_SNAKE}}` placeholders. Replace every one, and delete whole blocks marked `OPTIONAL` rather than leaving them empty or padded (three real features stay three; do not invent a fourth).
- When a fact is missing, write `[DATA NEEDED: what]` in its place and report it. `scripts/check.py` fails on both placeholders and gap markers, so a finished page cannot ship with either.
- Long bodies (post articles, docs pages, release notes) are one placeholder holding prose HTML; write them with the components in `components.md`.

## Facts, numbers, people

- Never invent metrics, benchmark results, prices, customers, logos, testimonials or endorsements. Stats bands and quote grids exist only for real, sourced material; give the source line (`.stats-source`) or attribution.
- A number you cannot verify ships as a gap, never as a precise-looking guess.
- Screenshots: use real ones inside `.window` or `.figure`; otherwise keep the abstract schematic or a `.sketch`. Never imitate another product's interface.
- Sample content uses the fictional product Orbitline and says so (footer note, a callout, or a FAQ answer). Keep that disclosure when you reuse examples as a starting point.

## Voice

- Headings state the point ("Edit together, never wait"); leads are one or two sentences; labels are short nouns.
- Buttons are verbs ("Download", "Read the docs"). One primary button per group.
- Links say where they go; an arrow (→) marks navigation, not emphasis.
- Keep the brand's own name and product terms unchanged across languages.

## Languages

- Ship `en` and `zh-TW` versions of every page unless told otherwise; `<html lang>` is `en` or `zh-Hant-TW`. Interface strings come from `src/i18n/<lang>.json` in the templates; translate every visible string you add, including `aria-label`s and captions.
- Traditional Chinese: full-width punctuation (，。：；「」), no spaces inside dates (`2026年11月10日`), a space between Chinese and Latin words or numbers is optional but consistent, emphasis by `<strong>` or `<em>` (rendered as emphasis dots), never italic.
- English labels set in mono run wider than Chinese; check that rails, buttons and table heads still fit at 1280px and 375px.
