#!/usr/bin/env python3
"""Check finished (or template) Gridline HTML files without a browser.

Errors (exit 1):
  unresolved {{PLACEHOLDER}} or [DATA NEEDED: ...] (unless --allow-placeholders)
  leftover build markers ([[ui:...]], [[lang]], /*@css*/, <!--@part:...-->)
  missing <html lang>, duplicate ids, broken local links, missing #anchors
Warnings (exit 1 only with --strict): departures from the Gridline style
  rounded corners other than 0 / 50% / var(--radius)
  blurred box-shadows (the system uses hard offsets only)
  remote stylesheets other than the sliced web-font block (src/parts/fonts.*.html)
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

PLACEHOLDER = re.compile(r"{{[^{}]+}}|\[DATA NEEDED:[^\]]+\]")
MARKER = re.compile(r"\[\[(?:ui:[a-z0-9_]+|lang)\]\]|/\*@(?:css|js:[a-z0-9_-]+)\*/|<!--@part:[a-z0-9_-]+-->")
REMOTE_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript"}
RADIUS = re.compile(r"border-radius\s*:\s*([^;}]+)")
SHADOW = re.compile(r"box-shadow\s*:\s*([^;}]+)")
LENGTH = re.compile(r"-?\d*\.?\d+(?:px|rem|em|pt|mm)?")


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.refs: list[tuple[str, str]] = []
        self.html_lang: str | None = None
        self.stylesheets: list[str] = []
        self.styles: list[str] = []
        self._in_style = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.html_lang = values.get("lang") or ""
        if tag == "style":
            self._in_style = True
        if tag == "link" and (values.get("rel") or "").lower() == "stylesheet":
            self.stylesheets.append(values.get("href") or "")
        if values.get("id"):
            self.ids.append(values["id"] or "")
        for key in ("href", "src", "poster"):
            if values.get(key):
                self.refs.append((key, values[key] or ""))
        if values.get("style"):
            self.styles.append(values["style"] or "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "style":
            self._in_style = False

    def handle_data(self, data: str) -> None:
        if self._in_style:
            self.styles.append(data)


def split_shadows(value: str) -> list[str]:
    parts, depth, current = [], 0, ""
    for char in value:
        depth += char == "("
        depth -= char == ")"
        if char == "," and depth == 0:
            parts.append(current)
            current = ""
        else:
            current += char
    parts.append(current)
    return parts


# The web-font block (src/parts/fonts.*.html) loads faces sliced by
# unicode-range; any other remote stylesheet is a departure.
FONT_SOURCES = (
    "https://fonts.googleapis.com/css2?",
    "https://cdn.jsdelivr.net/gh/rubinette/gridline-style@",
)


def style_warnings(css: str) -> list[str]:
    warnings: list[str] = []
    for value in RADIUS.findall(css):
        v = value.strip().replace("!important", "").strip()
        if v in {"0", "0px", "50%", "var(--radius)"} or v.startswith("var(--pele-radius"):
            continue
        warnings.append(f"rounded corners: border-radius: {v}")
    for value in SHADOW.findall(css):
        for shadow in split_shadows(value):
            s = re.sub(r"[a-z-]+\([^()]*(?:\([^()]*\))*[^()]*\)", " ", shadow)  # drop var(), rgba(), color-mix()
            s = s.replace("inset", " ")
            lengths = LENGTH.findall(s)
            if len(lengths) >= 3 and float(re.sub(r"[a-z]+$", "", lengths[2]) or 0) != 0:
                warnings.append(f"blurred shadow: box-shadow: {shadow.strip()}")
    if re.search(r"@import\s+url\(\s*['\"]?https?:", css) or "@font-face" in css and re.search(r"src\s*:[^;]*url\(\s*['\"]?https?:", css):
        warnings.append("remote font or stylesheet in CSS")
    return sorted(set(warnings))


def check_file(path: Path, allow_placeholders: bool = False) -> tuple[list[str], list[str]]:
    text = path.read_text(encoding="utf-8")
    parser = DocumentParser()
    parser.feed(text)
    errors: list[str] = []

    if not allow_placeholders:
        for token in sorted(set(PLACEHOLDER.findall(text))):
            errors.append(f"unresolved placeholder: {token}")
    for token in sorted(set(MARKER.findall(text))):
        errors.append(f"leftover build marker: {token}")
    if "<html" in text and not parser.html_lang:
        errors.append("missing <html lang>")

    for value, count in Counter(parser.ids).items():
        if count > 1:
            errors.append(f"duplicate id: {value}")

    known_ids = set(parser.ids)
    for attr, ref in parser.refs:
        if allow_placeholders and PLACEHOLDER.search(ref):
            continue
        parsed = urlsplit(ref)
        if parsed.scheme.lower() in REMOTE_SCHEMES or ref.startswith("//"):
            continue
        if parsed.path:
            target = (path.parent / unquote(parsed.path)).resolve()
            if not target.exists():
                errors.append(f"broken local {attr}: {ref}")
        if parsed.fragment and (not parsed.path or Path(unquote(parsed.path)).name == path.name):
            if unquote(parsed.fragment) not in known_ids:
                errors.append(f"missing anchor target: #{unquote(parsed.fragment)}")

    warnings = style_warnings("\n".join(parser.styles))
    for href in parser.stylesheets:
        if href.startswith(("http:", "https:", "//")) and not href.startswith(FONT_SOURCES):
            warnings.append(f"remote stylesheet: {href} (only the sliced web-font block may link out)")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--allow-placeholders", action="store_true", help="for template files")
    parser.add_argument("--strict", action="store_true", help="fail on style warnings too")
    args = parser.parse_args()
    failed = False
    for path in args.paths:
        errors, warnings = check_file(path, args.allow_placeholders)
        for error in errors:
            print(f"ERROR: {path}: {error}")
        for warning in warnings:
            print(f"WARN:  {path}: {warning}")
        if errors or (args.strict and warnings):
            failed = True
        elif not warnings:
            print(f"OK:    {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
