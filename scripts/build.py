#!/usr/bin/env python3
"""Build Gridline templates and examples from src/.

Sources (edit these):
  src/css/*.css            style modules
  src/js/*.js              behaviour modules
  src/i18n/<lang>.json     interface strings per language
  src/templates/<name>.html one source per surface
  src/parts/<name>.html    shared markup (header, footer, ...)
  src/content/<name>.<lang>.json   example content (placeholder -> value)
  src/content/_shared.<lang>.json  content the parts use (brand, navigation, footer)

Outputs (generated, committed):
  assets/templates/<name>-<lang>.html  self-contained, {{PLACEHOLDERS}} kept
  assets/examples/<name>-<lang>.html   the same with example content filled in
  assets/css/gridline.css, assets/css/print.css, assets/js/*.js  for porting

A template source starts with a directive comment:
  <!-- gridline css="tokens base construction components" -->
and may contain:
  <!--@part:NAME-->  replaced by src/parts/NAME.html (parts may include parts)
  /*@css*/           replaced by the listed CSS modules
  /*@js:NAME*/       replaced by src/js/NAME.js
  [[lang]]           replaced by the language's html lang value
  [[ui:key]]         replaced by the interface string (HTML-escaped)

Usage:
  python3 scripts/build.py           write every output
  python3 scripts/build.py --check   exit 1 if any output is stale or missing
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
ASSETS = ROOT / "assets"

DIRECTIVE = re.compile(r'\A<!--\s*gridline\s+css="([^"]*)"\s*-->\n')
PLACEHOLDER = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
UI = re.compile(r"\[\[ui:([a-z0-9_]+)\]\]")
JS = re.compile(r"/\*@js:([a-z0-9_-]+)\*/")
PART = re.compile(r"<!--@part:([a-z0-9_-]+)-->")
LANGS = ("en", "zh-tw")
# Everything a screen page might use, in cascade order, for assets/css/gridline.css.
SCREEN_MODULES = ("tokens", "base", "construction", "components", "prose", "blog",
                  "docs", "changelog", "landing", "diagram", "syntax")


class BuildError(Exception):
    pass


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def css_bundle(modules: list[str]) -> str:
    parts = []
    for name in modules:
        path = SRC / "css" / f"{name}.css"
        if not path.exists():
            raise BuildError(f"unknown CSS module: {name}")
        parts.append(f"/* ── gridline/{name}.css ── */\n" + read(path).strip() + "\n")
    return "\n".join(parts)


def load_strings(lang: str) -> dict:
    data = json.loads(read(SRC / "i18n" / f"{lang}.json"))
    if "html_lang" not in data or "strings" not in data:
        raise BuildError(f"src/i18n/{lang}.json needs html_lang and strings")
    return data


def render_template(name: str, source: str, lang: str, strings: dict) -> str:
    match = DIRECTIVE.match(source)
    if not match:
        raise BuildError(f"src/templates/{name}.html must start with <!-- gridline css=\"...\" -->")
    body = source[match.end():]

    def part(m: re.Match) -> str:
        path = SRC / "parts" / f"{m.group(1)}.html"
        if not path.exists():
            raise BuildError(f"{name}: unknown part {m.group(1)}")
        return read(path).rstrip("\n")

    for _ in range(5):
        if not PART.search(body):
            break
        body = PART.sub(part, body)
    else:
        raise BuildError(f"{name}: parts nest more than five levels deep")
    modules = match.group(1).split()
    body = body.replace("/*@css*/", css_bundle(modules).strip())

    def js(m: re.Match) -> str:
        path = SRC / "js" / f"{m.group(1)}.js"
        if not path.exists():
            raise BuildError(f"{name}: unknown JS module {m.group(1)}")
        return read(path).strip()

    body = JS.sub(js, body)
    body = body.replace("[[lang]]", strings["html_lang"])

    def ui(m: re.Match) -> str:
        key = m.group(1)
        if key not in strings["strings"]:
            raise BuildError(f"{name}: missing UI string '{key}' in src/i18n/{lang}.json")
        return html.escape(strings["strings"][key], quote=True)

    body = UI.sub(ui, body)
    leftover = re.findall(r"\[\[[^\]]*\]\]", body)
    if leftover:
        raise BuildError(f"{name}: unresolved markers {sorted(set(leftover))}")
    return body


def fill(name: str, lang: str, template: str, content: dict, shared: dict) -> str:
    wanted = set(PLACEHOLDER.findall(template))
    missing = sorted(wanted - set(content) - set(shared))
    unused = sorted(set(content) - wanted)
    clash = sorted(set(content) & set(shared))
    if clash:
        raise BuildError(f"src/content/{name}.{lang}.json repeats shared keys: {', '.join(clash)}")
    if missing:
        raise BuildError(f"src/content/{name}.{lang}.json lacks: {', '.join(missing)}")
    if unused:
        raise BuildError(f"src/content/{name}.{lang}.json has keys the template does not use: {', '.join(unused)}")
    values = {**shared, **content}
    return PLACEHOLDER.sub(lambda m: str(values[m.group(1)]), template)


def outputs() -> dict[Path, str]:
    result: dict[Path, str] = {}
    strings = {lang: load_strings(lang) for lang in LANGS}
    shared = {lang: json.loads(read(SRC / "content" / f"_shared.{lang}.json")) for lang in LANGS}
    for source_path in sorted((SRC / "templates").glob("*.html")):
        name = source_path.stem
        source = read(source_path)
        for lang in LANGS:
            template = render_template(name, source, lang, strings[lang])
            result[ASSETS / "templates" / f"{name}-{lang}.html"] = template
            content_path = SRC / "content" / f"{name}.{lang}.json"
            if not content_path.exists():
                raise BuildError(f"missing example content: {content_path.relative_to(ROOT)}")
            content = json.loads(read(content_path))
            result[ASSETS / "examples" / f"{name}-{lang}.html"] = fill(name, lang, template, content, shared[lang])
    banner = "/* Gridline — generated by scripts/build.py from src/css. Edit the sources, not this file. */\n\n"
    result[ASSETS / "css" / "gridline.css"] = banner + css_bundle(list(SCREEN_MODULES))
    result[ASSETS / "css" / "print.css"] = banner + css_bundle(["print"])
    for name in ("boot", "site", "diagram"):
        result[ASSETS / "js" / f"{name}.js"] = read(SRC / "js" / f"{name}.js")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="report stale outputs instead of writing")
    args = parser.parse_args()
    try:
        built = outputs()
    except BuildError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    expected = set(built)
    generated_dirs = [ASSETS / "templates", ASSETS / "examples"]
    strays = sorted(p for d in generated_dirs if d.exists() for p in d.glob("*.html") if p not in expected)

    if args.check:
        stale = [p for p, text in built.items() if not p.exists() or read(p) != text]
        for path in stale:
            print(f"STALE: {path.relative_to(ROOT)}")
        for path in strays:
            print(f"STRAY: {path.relative_to(ROOT)}")
        if stale or strays:
            print("Run: python3 scripts/build.py")
            return 1
        print(f"OK: {len(built)} outputs up to date")
        return 0

    for path, text in built.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or read(path) != text:
            path.write_text(text, encoding="utf-8")
            print(f"wrote {path.relative_to(ROOT)}")
    for path in strays:
        path.unlink()
        print(f"removed {path.relative_to(ROOT)}")
    print(f"OK: {len(built)} outputs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
