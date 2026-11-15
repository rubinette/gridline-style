#!/usr/bin/env python3
"""Slice IBM Plex Sans TC into small web-font files by unicode-range.

IBM publishes Plex Sans TC already split, but its slices are not ordered by
how often characters occur, so an ordinary Chinese page touches most of them
(about 3 MB per page in testing). This script re-slices the complete fonts
along src/fonts/cjk-slices.txt, the frequency-ordered slicing Google Fonts
uses for Noto Sans TC, so a page fetches a handful of slices instead.

Outputs (generated, committed):
  assets/fonts/ibm-plex-sans-tc/IBMPlexSansTC-<Weight>-<id>.woff2
  assets/fonts/ibm-plex-sans-tc/plex-sans-tc.css   @font-face rules, relative URLs
  assets/fonts/ibm-plex-sans-tc/LICENSE.txt        SIL Open Font License 1.1

Usage:
  python3 scripts/fonts.py                 # fetches @ibm/plex-sans-tc with npm pack
  python3 scripts/fonts.py --source DIR    # DIR holds IBMPlexSansTC-<Weight>.woff2

Needs fontTools and brotli (pip install fonttools brotli).
"""

from __future__ import annotations

import argparse
import io
import os
import subprocess
import sys
import tarfile
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLICES = ROOT / "src" / "fonts" / "cjk-slices.txt"
OUT = ROOT / "assets" / "fonts" / "ibm-plex-sans-tc"
PACKAGE = "@ibm/plex-sans-tc@1.1.1"
WEIGHTS = {"Regular": 400, "Medium": 500, "SemiBold": 600}
FAMILY = "IBM Plex Sans TC"


def parse_ranges(text: str) -> set[int]:
    points: set[int] = set()
    for part in text.split(","):
        part = part.strip().upper().removeprefix("U+")
        if not part:
            continue
        if "-" in part:
            lo, hi = part.split("-")
            points.update(range(int(lo, 16), int(hi, 16) + 1))
        else:
            points.add(int(part, 16))
    return points


def format_ranges(points: set[int]) -> str:
    out, ordered = [], sorted(points)
    i = 0
    while i < len(ordered):
        j = i
        while j + 1 < len(ordered) and ordered[j + 1] == ordered[j] + 1:
            j += 1
        a, b = ordered[i], ordered[j]
        out.append(f"U+{a:x}" if a == b else f"U+{a:x}-{b:x}")
        i = j + 1
    return ", ".join(out)


def load_slices() -> list[tuple[str, set[int]]]:
    slices = []
    for line in SLICES.read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            sid, ranges = line.split("\t")
            slices.append((sid, parse_ranges(ranges)))
    return slices


def fetch_source(tmp: Path) -> Path:
    subprocess.run(["npm", "pack", "-q", PACKAGE], cwd=tmp, check=True, stdout=subprocess.DEVNULL)
    tgz = next(tmp.glob("*.tgz"))
    with tarfile.open(tgz) as tar:
        members = [m for m in tar.getmembers() if "/complete/woff2/hinted/" in m.name]
        tar.extractall(tmp, members=members, filter="data")
    return tmp / "package" / "fonts" / "complete" / "woff2" / "hinted"


def cut(job: tuple[bytes, str, int, str, set[int]]) -> str:
    from fontTools import subset
    from fontTools.ttLib import TTFont

    data, weight, value, sid, points = job
    name = f"IBMPlexSansTC-{weight}-{sid}.woff2"
    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = ["*"]
    options.name_IDs = ["*"]
    options.notdef_outline = True
    font = TTFont(io.BytesIO(data))
    sub = subset.Subsetter(options)
    sub.populate(unicodes=points)
    sub.subset(font)
    font.flavor = "woff2"
    font.save(OUT / name)
    return (
        "@font-face {\n"
        f"  font-family: \"{FAMILY}\";\n"
        "  font-style: normal;\n"
        f"  font-weight: {value};\n"
        "  font-display: swap;\n"
        f"  src: url(\"{name}\") format(\"woff2\");\n"
        f"  unicode-range: {format_ranges(points)};\n"
        "}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--source", type=Path, help="folder with IBMPlexSansTC-<Weight>.woff2")
    args = parser.parse_args()
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        print("needs fontTools and brotli: pip install fonttools brotli", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory() as tmpdir:
        source = args.source or fetch_source(Path(tmpdir))
        slices = load_slices()
        OUT.mkdir(parents=True, exist_ok=True)
        for old in OUT.glob("*.woff2"):
            old.unlink()
        jobs = []
        for weight, value in WEIGHTS.items():
            path = source / f"IBMPlexSansTC-{weight}.woff2"
            font = TTFont(path)
            cmap = set(font.getBestCmap())
            # Decode the WOFF2 once; each slice then loads the plain TrueType bytes.
            font.flavor = None
            buf = io.BytesIO()
            font.save(buf)
            data = buf.getvalue()
            # Characters the font has that no slice names go in one last slice.
            rest = cmap - set().union(*(s for _, s in slices))
            for sid, points in [*slices, ("rest", rest)]:
                points = points & cmap
                if points:
                    jobs.append((data, weight, value, sid, points))
        with ProcessPoolExecutor(max_workers=os.cpu_count()) as pool:
            rules = list(pool.map(cut, jobs, chunksize=4))
        header = (
            "/* IBM Plex Sans TC (SIL OFL 1.1, LICENSE.txt), sliced by unicode-range\n"
            "   along Google Fonts' frequency-ordered Noto Sans TC slices.\n"
            "   Generated by gridline-style scripts/fonts.py; do not edit. */\n"
        )
        (OUT / "plex-sans-tc.css").write_text(header + "".join(rules), encoding="utf-8")
        license_src = source / "license.txt"
        if license_src.exists():
            (OUT / "LICENSE.txt").write_text(license_src.read_text(encoding="utf-8"), encoding="utf-8")
    total = sum(p.stat().st_size for p in OUT.glob("*.woff2"))
    print(f"OK: {len(list(OUT.glob('*.woff2')))} files, {total / 1e6:.1f} MB in {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
