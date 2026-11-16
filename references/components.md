# Components

Markup for every Gridline component. Styles live in `src/css/` (module named in brackets); a template only includes the modules it needs, so copy a component into a page whose template already carries its module, or add the module to the template's directive and rebuild.

Decorative construction (`.junction`, `.band-rails`, `.header-rails`, `.divider`, sketches) is always `aria-hidden="true"`.

## Page skeleton [base]

```html
<html lang="en" class="no-js">          <!-- zh-Hant-TW for Traditional Chinese -->
<head> … boot.js inline (restores the theme, swaps no-js → js) … </head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">…</header>
  <main id="main">…</main>
  <div class="divider plain" aria-hidden="true"><div class="frame"><i class="junction"></i></div></div>
  <footer class="site-footer">…</footer>
  <script>/* site.js */</script>
</body>
```

## Construction [construction]

```html
<!-- Hatched divider band between major sections: diamonds on both edges. -->
<div class="divider" aria-hidden="true"><div class="frame"><i class="junction"></i><i class="junction"></i></div></div>

<!-- Plain hairline. -->
<div class="divider plain" aria-hidden="true"><div class="frame"><i class="junction"></i></div></div>

<!-- A section on the construction grid (20px for heroes, 40px for other bands). -->
<section class="grid-bg"><div class="frame">…</div></section>

<!-- Band with outer rails (page header). .hatch adds the fading diagonal hatch. -->
<header class="band hatch">
  <div class="band-rails" aria-hidden="true"><i class="junction"></i></div>
  <div class="frame band-inner"><i class="junction" aria-hidden="true"></i>
    <p class="eyebrow">Category</p>
    <h1 class="band-title">Title</h1>          <!-- .post-title in a post -->
    <p class="lead">Lead</p>
  </div>
</header>
```

## Site header [components]

```html
<header class="site-header">
  <div class="header-rails" aria-hidden="true"><i class="junction"></i></div>  <!-- shows only on pages with a .band -->
  <div class="frame header-inner">
    <i class="junction" aria-hidden="true"></i>
    <a class="brand" href="/"><span class="brand-mark" aria-hidden="true">O</span><span class="brand-name">Orbitline</span></a>
    <nav class="nav-links" id="site-nav" aria-label="Main">
      <a href="/docs/" aria-current="page">Docs</a> …
    </nav>
    <div class="header-actions">
      <button class="icon-btn theme-toggle" type="button" aria-label="Toggle dark mode" aria-pressed="false" hidden>…sun / moon svgs…</button>
      <a class="button primary header-button" href="#">Download</a>
      <button class="icon-btn menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" hidden>Menu</button>
    </div>
  </div>
</header>
```

Docs keep the main nav (Docs marked current) and add a search field after it: `<form class="search" role="search">` with an icon `<svg>`, `<input type="search" aria-label="…">` and `<kbd>/</kbd>`.

Announcement strip under the header: `<div class="announce"><div class="frame"><strong>New:</strong> text <a href="#">Link →</a></div></div>`.

## Hero and section heads [components]

```html
<section class="hero grid-bg" aria-labelledby="t">
  <div class="frame hero-inner center">            <!-- .left for a left-aligned hero -->
    <p class="eyebrow">Category</p>
    <h1 id="t">Title</h1>
    <p class="lead">One or two sentences.</p>
    <div class="actions">
      <a class="button primary" href="#">Download <kbd>D</kbd></a>
      <a class="button" href="#">Read the docs <span class="arrow" aria-hidden="true">→</span></a>
    </div>
  </div>
</section>

<div class="section-head">
  <div><h2>Section title</h2><p>Short lead.</p></div>
  <div class="actions"><a class="button ghost" href="#">Secondary <span class="arrow" aria-hidden="true">→</span></a></div>
</div>
```

Closing CTA: `<section class="cta grid-bg"><div class="frame cta-inner"><p class="eyebrow">…</p><h2>…</h2><p>…</p><div class="actions">…</div></div></section>`, preceded by a hatched divider.

## Buttons, labels, states [components]

| Markup | Use |
| --- | --- |
| `<a class="button primary">` | the one primary action in a group |
| `<a class="button">` | secondary |
| `<a class="button ghost">` | tertiary, inside section heads |
| `<kbd>K</kbd>` inside a button | keyboard hint (hidden below 820px) |
| `<span class="arrow" aria-hidden="true">→</span>` | navigation buttons |
| `<button class="icon-btn">` | square 40px icon button |
| `<p class="eyebrow">` | accent mono overline |
| `<p class="nav-label">` | muted mono label above a list |
| `<span class="badge">` / `.badge.accent` | category; "Latest" only where the order does not already show it (a version rail) |
| `<span class="state">` `.active` `.ok` `.warn` `.err` | state labels, the only status colour |
| `<span class="avatars sm|md"><span class="avatar">L</span></span>` | people (round) |
| `<kbd class="key">⌘</kbd>` | a key outside prose |

## Cells and cards [components]

```html
<section class="frame cells">                      <!-- .two, .four; .no-nodes drops the diamonds -->
  <div class="value"><h2>Title</h2><p>Text</p></div> …
</section>

<section class="frame card-grid">
  <article class="card"><a class="card-link" href="#">
    <div class="card-media"><img src="cover.png" alt=""></div>   <!-- or <svg class="sketch">, or .card-placeholder -->
    <div class="card-body">
      <h2 class="card-title">Title</h2>
      <p class="card-excerpt">Two-line excerpt.</p>
      <div class="card-meta"><span class="card-authors">Name</span><time datetime="2026-11-10">Nov 10, 2026</time></div>
    </div>
  </a></article> …
</section>
```

Place cells and card grids between two horizontal lines (dividers, a section head's border) so their diamonds land on lines.

## Prose [prose]

Inside `<div class="prose">`:

- Headings: `<h2 id="slug">Text<a class="anchor" href="#slug" aria-label="Link to this section">#</a></h2>`; h3 sans 600; h4 mono overline.
- Lists (neutral square bullets), `ol.steps` (numbered steps with a rail), `blockquote` (pull quote), `hr` (hatched band), `kbd`, `mark`, inline `code`, footnotes (`.footnotes`).
- Tables: wrap in `<div class="table-wrap">` for horizontal scroll.
- Callout: `<div class="callout callout-note" role="note"><p class="callout-title">Note</p><p>…</p></div>`; `callout-tip`, `callout-important` look like note; `callout-warning` and `callout-caution` use the status colours.

### Code block [components + syntax]

```html
<figure class="code-block">
  <figcaption class="code-head"><span class="code-label">buffer/src/id.rs</span>
    <button class="copy" type="button" data-done="Copied" hidden>Copy</button></figcaption>
  <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-rust">…</code></pre></div>
</figure>
```

Highlight with Chroma class names (`.k` keyword, `.s` string, `.c1` comment, `.nf` function, `.gp` prompt, `.go` output…) or leave it monochrome.

### Figure [components]

```html
<figure class="figure">
  <div class="figure-frame"><img src="diagram.png" alt="What it shows"></div>
  <figcaption>Figure 1: caption.</figcaption>
</figure>
```

Image runs edge to edge inside a hairline frame with a 2px offset; the caption shares the frame. For an illustration without an image, draw an inline `<svg class="sketch" role="img" aria-label="…">` with the sketch classes: `.grid` (construction lines), `.ln` (lines), `.box`, `.hi` (accent box), `.hi-ln`, `.node` (diamond), `.dot`, text with `.tx` (ink) or `.ac` (accent); `.sketch.lg` for 14px labels. Never put a `<style>` inside an inline SVG: it applies to the whole page.

### Mermaid diagram [diagram]

`<figure class="figure diagram"><div class="figure-frame"><pre class="mermaid">flowchart LR …</pre></div><figcaption>…</figcaption></figure>` plus the diagram script. See `mermaid.md`.

## Navigation pieces [components]

```html
<details class="toc toc-inline"><summary>On this page</summary><ul>…</ul></details>   <!-- shows below 1080px -->
<nav class="toc toc-aside" aria-label="On this page"><p class="nav-label">On this page</p><ul><li><a href="#a">…</a><ul>…</ul></li></ul></nav>
<div class="links-box"><p class="nav-label">See also</p><ul><li><a href="#">Link <span aria-hidden="true">→</span></a></li></ul></div>
<ul class="tag-list"><li><a href="#">#tag</a></li></ul>
<nav class="post-nav"><a class="prev" href="#"><span class="nav-label">← Older post</span><span class="post-nav-title">…</span></a><a class="next" href="#">…</a></nav>
<nav class="pagination"><span class="page-of">Page 1 of 2</span><a class="button" href="#">Older →</a></nav>
```

## Blog pieces [blog]

`.index-body` > `.cat-nav` (`.cat-nav-inner` with `.nav-label` + `<ul>` of `<a><span>Name</span><span class="count">3</span></a>`, current `aria-current="page"`) + `.post-list` (`<h2 class="year"><span>2026</span></h2>` + `<ol class="rows">` of `<a class="row">` with `.row-title` > `.row-text` + avatars, and `.row-meta` > `.badge` + `<time>`). Post header byline: `<ul class="byline"><li class="author">avatars + <span class="author-text"><a>Name</a><span class="author-role">Role</span></span></li></ul>`, then `<p class="post-meta"><time>…</time><span>4 min read</span></p>`. Taxonomy grid: `.term-grid` of `<a class="term"><span class="term-name">…</span><span class="term-desc">…</span><span class="term-count">…</span></a>`.

## Docs pieces [docs]

`.docs-layout` > `nav.docs-nav` (`.docs-nav-toggle` button + `#docs-nav-list` of `<details class="docs-group" open><summary>Section</summary><ul>…</ul></details>`), `article.docs-main` (`.docs-head` with `.docs-head-bar` (`ol.breadcrumbs.eyebrow` + edit button), then `h1.docs-title` and `.lead`; prose; `.docs-footer` with `.post-nav` and `.docs-updated`), `aside.docs-toc`. Reference cards: `<div class="ref-grid"><a class="ref-card" href="#"><strong>Title</strong><span>Text</span></a></div>`.

## Changelog pieces [changelog]

`.release-layout` > `nav.release-rail` (channels and version anchors), `.release-feed` (`<h2 class="month">`, `<article class="release" id="v1-2-0">` with `.release-head` > `a.version` (+ `.badge.accent`) + `<time>`, and `.release-body.prose` notes), `aside.pinboard` (links, `.pin-note`).

## Landing pieces [landing]

| Class | What it is |
| --- | --- |
| `.product-hero` on `.hero-inner` | product hero; `.hero-note` platform line |
| `.value-strip.cells` > `.value` | three short claims |
| `.panel-stage` > `.window` | abstract product window: `.window-bar` (three squares + title), `.window-body` (`.window-side` items with `.state`, `.window-main` with `.window-task`, `.window-steps`, `.window-lines`), `.window-status` |
| `.feature-rows` > `.cells` > `.feature` | features; optional `.feature-media` with an image or sketch |
| `.grid-bg` > `.stats-inner` | stats band: `.stats-cells.cells.four` > `.stat` (`.stat-value`, `.stat-label`) + `.stats-source` |
| `.showcase` | `.showcase-list` of `<details class="showcase-item" name="group">` beside `.showcase-figure` |
| `.plans-stage` > `.plans` > `.plan` | `.plan-name`, `.price` (`strong` + unit), `.plan-desc`, `ul.checks`, button; `.plan.featured` |
| `.faq-stage` > `.faq` | `<details><summary>Question</summary><div><p>Answer</p></div></details>` |
| `.quote-grid.cells` > `figure.quote` | real quotes only: `blockquote` + `figcaption` (avatar, name, `span` role) |
