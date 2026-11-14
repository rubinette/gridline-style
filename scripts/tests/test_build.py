import sys
from pathlib import Path
from unittest import TestCase

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build
from check import check_file

ROOT = Path(__file__).resolve().parents[2]


class BuildTest(TestCase):
    def test_outputs_are_up_to_date(self) -> None:
        built = build.outputs()
        stale = [str(p.relative_to(ROOT)) for p, text in built.items() if not p.exists() or p.read_text(encoding="utf-8") != text]
        self.assertEqual([], stale, "run python3 scripts/build.py")

    def test_every_surface_ships_in_both_languages(self) -> None:
        surfaces = sorted(p.stem for p in (ROOT / "src" / "templates").glob("*.html"))
        self.assertTrue(surfaces)
        for name in surfaces:
            for lang in build.LANGS:
                self.assertTrue((ROOT / "assets" / "templates" / f"{name}-{lang}.html").exists(), f"{name}-{lang}")
                self.assertTrue((ROOT / "assets" / "examples" / f"{name}-{lang}.html").exists(), f"{name}-{lang}")

    def test_examples_and_templates_pass_the_checker(self) -> None:
        for path in sorted((ROOT / "assets" / "examples").glob("*.html")):
            self.assertEqual(([], []), check_file(path), path.name)
        for path in sorted((ROOT / "assets" / "templates").glob("*.html")):
            self.assertEqual(([], []), check_file(path, allow_placeholders=True), path.name)

    def test_fill_rejects_missing_unused_and_shared_keys(self) -> None:
        with self.assertRaises(build.BuildError):
            build.fill("x", "en", "{{A}}{{B}}", {"A": "1"}, {})
        with self.assertRaises(build.BuildError):
            build.fill("x", "en", "{{A}}", {"A": "1", "EXTRA": "2"}, {})
        with self.assertRaises(build.BuildError):
            build.fill("x", "en", "{{A}}", {"A": "1"}, {"A": "shared"})
        self.assertEqual("1-s", build.fill("x", "en", "{{A}}-{{S}}", {"A": "1"}, {"S": "s"}))

    def test_unknown_ui_string_fails(self) -> None:
        strings = {"html_lang": "en", "strings": {}}
        with self.assertRaises(build.BuildError):
            build.render_template("x", '<!-- gridline css="tokens" -->\n[[ui:nope]]', "en", strings)
