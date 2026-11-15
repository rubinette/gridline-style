import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from check import check_file, style_warnings


def write(root: Path, name: str, text: str) -> Path:
    path = root / name
    path.write_text(text, encoding="utf-8")
    return path


class CheckFileTest(TestCase):
    def test_valid_document_passes(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            write(root, "asset.svg", "<svg xmlns='http://www.w3.org/2000/svg'/>")
            good = write(root, "good.html", "<html lang='en'><main id='start'><a href='#start'>Top</a><img src='asset.svg'></main></html>")
            self.assertEqual(([], []), check_file(good))

    def test_template_placeholders_are_allowed_on_request(self) -> None:
        with TemporaryDirectory() as directory:
            template = write(Path(directory), "template.html", "<html lang='en'><a href='{{TARGET}}'>{{LABEL}}</a></html>")
            self.assertEqual([], check_file(template, allow_placeholders=True)[0])
            self.assertTrue(check_file(template)[0])

    def test_broken_document_reports_each_problem(self) -> None:
        with TemporaryDirectory() as directory:
            broken = write(Path(directory), "broken.html",
                           "<html><main id='same'><p id='same'>{{TITLE}} [[ui:menu]]</p><a href='#lost'>Lost</a><img src='missing.svg'></main></html>")
            errors = check_file(broken)[0]
            for fragment in ("placeholder", "build marker", "missing <html lang>", "duplicate id", "missing anchor", "broken local"):
                self.assertTrue(any(fragment in error for error in errors), fragment)

    def test_data_needed_marker_is_unresolved(self) -> None:
        with TemporaryDirectory() as directory:
            page = write(Path(directory), "page.html", "<html lang='en'><p>[DATA NEEDED: monthly users]</p></html>")
            self.assertTrue(any("DATA NEEDED" in error for error in check_file(page)[0]))


class StyleWarningTest(TestCase):
    def test_square_corners_and_round_avatars_pass(self) -> None:
        self.assertEqual([], style_warnings(".a{border-radius:0}.b{border-radius:50%}.c{border-radius:var(--radius)}"))

    def test_rounded_corners_warn(self) -> None:
        self.assertTrue(style_warnings(".card{border-radius:8px}"))

    def test_hard_offsets_pass_and_blur_warns(self) -> None:
        self.assertEqual([], style_warnings(".a{box-shadow:6px 6px 0 var(--band),-6px -6px 0 var(--band)}"))
        self.assertEqual([], style_warnings(".a{box-shadow:0 0 0 2px var(--surface)}"))
        self.assertTrue(style_warnings(".a{box-shadow:0 4px 12px rgba(0,0,0,.2)}"))

    def test_remote_fonts_warn(self) -> None:
        self.assertTrue(style_warnings("@import url('https://fonts.googleapis.com/css2?family=Inter');"))

    def test_only_the_sliced_font_block_may_link_out(self) -> None:
        head = '<!doctype html><html lang="en"><head><title>t</title>{}</head><body></body></html>'
        fonts = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lilex&amp;display=swap">'
                 '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@ibm/plex-sans-tc@1.1.1/fonts/split/woff2/hinted/IBMPlexSansTC-Regular.css">')
        other = '<link rel="stylesheet" href="https://example.com/fonts.css">'
        with TemporaryDirectory() as tmp:
            ok = write(Path(tmp), "ok.html", head.format(fonts))
            bad = write(Path(tmp), "bad.html", head.format(other))
            self.assertEqual([], check_file(ok)[1])
            self.assertTrue(check_file(bad)[1])
