# Mermaid diagrams

Gridline renders Mermaid text with [Pele](https://github.com/obsidianmd/pele) (MIT, © kepano): a small renderer that outputs themeable SVG. The `post` and `docs` templates include it; copy the pieces below into other pages.

## Markup

```html
<figure class="figure diagram">
  <div class="figure-frame">
    <pre class="mermaid">sequenceDiagram
    A->>B: hello</pre>
  </div>
  <figcaption>Figure 2: what the diagram shows.</figcaption>
</figure>
```

Escape `<`, `>` and `&` inside the `<pre>`. The caption also becomes the title of the full-window viewer.

## Loader

The `diagram-script` part (`src/parts/diagram-script.html`) is one module script with `src/js/diagram.js` inline:

```html
<script type="module"
  data-pele="https://cdn.jsdelivr.net/npm/pele@1.13.0/dist/esm/lazy.js"
  data-zoom-in="Zoom in" data-zoom-out="Zoom out" data-zoom-reset="Reset zoom"
  data-expand="Expand to window" data-close="Close">/* diagram.js */</script>
```

- Pin the version. The lazy entry imports only the diagram types a page uses (10–20 small chunks).
- To self-host (no CDN, strict CSP): copy the package's `dist/esm/lazy.js` and `chunks/` beside the page, keep its `LICENSE`, and point `data-pele` at your copy. hugo-gridline vendors it this way.
- With JavaScript off, offline, or if Pele fails to load, the source stays visible as a quiet code block (`pre.mermaid` styles). Syntax errors are drawn in place by Pele.
- Pages without a `pre.mermaid` never fetch Pele; delete the script anyway when a page has no diagrams.

## Behaviour

- Pele lays the diagram out for the column width. When it has to scale a wide diagram down, it shows zoom controls; Gridline restyles them as a 40px toolbar on the bottom edge (`.pele-zoom`, `!important` because Pele sets inline styles).
- `diagram.js` adds an **expand-to-window** button in the bottom-right corner of every rendered diagram (the zoom toolbar docks to its left). It sits beside the Pele host, not inside it, because Pele rewrites the host on every render.
- The viewer is one shared `<dialog>`: a framed panel over the grid, caption in the bar, close button; Esc, the button or a click outside the panel closes it, focus returns to the expand button, and the page behind does not scroll. It shows a copy of the SVG at its natural viewBox, fitted to the canvas with container-query units, with Pele's zoom always on (up to 8× natural size, drag to pan).

## Colours

Every `--pele-*` variable maps to a Gridline token on `.mermaid-diagram, .diagram-viewer-canvas` (`src/css/diagram.css`), so diagrams follow light and dark and a custom accent without re-rendering, and corners stay square (`--pele-radius: 0px`). Chart series alternate the accent and neutrals, all mixed toward `--ink` (Pele draws in-slice labels in the background colour), which keeps each series at least 4.2:1 against the page in both themes. Do not add a second hue.
