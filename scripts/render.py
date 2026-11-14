#!/usr/bin/env python3
"""Render one self-contained HTML document to PDF with WeasyPrint.

  python3 scripts/render.py brief.html brief.pdf [--png pages/]

--png writes one PNG per page (needs PyMuPDF) for the visual pass. When the
packages are not installed, run through uv:
  uv run --no-project --with weasyprint --with pymupdf python scripts/render.py ...
"""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path


def configure_macos_libraries() -> None:
    if sys.platform != "darwin":
        return
    cache = Path(tempfile.gettempdir()) / "gridline-style-fontconfig-cache"
    cache.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("XDG_CACHE_HOME", str(cache))
    candidates = [Path("/opt/homebrew/lib"), Path("/usr/local/lib")]
    existing = [Path(value) for value in os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "").split(":") if value]
    paths = [path for path in candidates if (path / "libgobject-2.0.dylib").exists()]
    os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = ":".join(map(str, [*paths, *existing]))


def export_pages(pdf: Path, out_dir: Path, scale: float = 1.5) -> int:
    try:
        import pymupdf as fitz
    except ImportError:
        try:
            import fitz  # PyMuPDF before 1.24
        except ImportError:
            fitz = None
    if fitz is None:
        print("ERROR: --png needs PyMuPDF. Try: uv run --no-project --with weasyprint --with pymupdf python scripts/render.py ...", file=sys.stderr)
        return 2
    out_dir.mkdir(parents=True, exist_ok=True)
    with fitz.open(pdf) as document:
        for index, page in enumerate(document, start=1):
            target = out_dir / f"{pdf.stem}-p{index}.png"
            page.get_pixmap(matrix=fitz.Matrix(scale, scale)).save(target)
            print(f"OK: wrote {target}")
        print(f"pages: {document.page_count}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--png", type=Path, metavar="DIR", help="also write one PNG per page into DIR")
    args = parser.parse_args()
    configure_macos_libraries()
    try:
        from weasyprint import HTML
    except (ImportError, OSError) as error:
        print(f"ERROR: WeasyPrint is unavailable ({error}). Try: uv run --no-project --with weasyprint python scripts/render.py INPUT OUTPUT", file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    source = args.input.resolve()
    HTML(filename=str(source), base_url=str(source.parent)).write_pdf(str(args.output.resolve()))
    print(f"OK: wrote {args.output}")
    if args.png:
        return export_pages(args.output, args.png)
    return 0


if __name__ == "__main__":
    sys.exit(main())
