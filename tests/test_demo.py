from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "demo" / "site"

class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ("href", "src"):
            value = attrs.get(key, "")
            if value and not value.startswith(("#", "https://", "http://", "mailto:", "tel:", "data:")):
                self.refs.append(value.split("#", 1)[0].split("?", 1)[0])

class DemoBuildTests(unittest.TestCase):
    def test_expected_pages_exist(self):
        expected = {
            "index.html", "sveden.html", "parents.html", "students.html",
            "news.html", "contacts.html", "priem.html", "styleguide.html", "404.html",
        }
        self.assertTrue(SITE.is_dir(), "Run demo/build_demo.py before tests")
        self.assertTrue(expected.issubset({p.name for p in SITE.glob("*.html")}))

    def test_local_references_resolve(self):
        for page in SITE.glob("*.html"):
            parser = AssetParser()
            parser.feed(page.read_text(encoding="utf-8"))
            for ref in parser.refs:
                if ref:
                    target = (page.parent / ref).resolve()
                    self.assertTrue(target.exists(), f"{page.name}: broken local reference {ref}")

    def test_standalone_assets_are_copied(self):
        source = ROOT / "demo" / "assets"
        self.assertEqual((source / "css" / "style.css").read_bytes(), (SITE / "assets" / "css" / "style.css").read_bytes())
        self.assertEqual((source / "js" / "app.js").read_bytes(), (SITE / "assets" / "js" / "app.js").read_bytes())

    def test_every_page_has_shared_shell(self):
        for page in SITE.glob("*.html"):
            html = page.read_text(encoding="utf-8")
            self.assertIn('id="siteHeader"', html, page.name)
            self.assertIn('class="footer-grid"', html, page.name)
            self.assertIn('class="skip-link"', html, page.name)

    def test_inner_pages_have_editor_placeholders(self):
        pages = ["sveden.html", "parents.html", "students.html", "news.html", "priem.html", "contacts.html", "styleguide.html"]
        for name in pages:
            html = (SITE / name).read_text(encoding="utf-8")
            self.assertIn("ЗАГЛУШКА ДЛЯ ЗАПОЛНЕНИЯ", html, name)
            self.assertIn("Демонстрационный макет", html, name)
            self.assertIn('id="nav"', html, name)

    def test_demo_contains_no_old_contact_claims(self):
        for page in SITE.glob("*.html"):
            html = page.read_text(encoding="utf-8")
            self.assertNotIn("+78512500567", html, page.name)
            self.assertNotIn("gimn4@obr.astrobl.ru", html, page.name)
            self.assertNotIn("ул. Б. Хмельницкого, 16", html, page.name)

    def test_demo_form_does_not_store_messages(self):
        contacts = (SITE / "contacts.html").read_text(encoding="utf-8")
        script = (SITE / "assets" / "js" / "app.js").read_text(encoding="utf-8")
        self.assertNotIn('name="email"', contacts)
        self.assertNotIn('name="name"', contacts)
        self.assertNotIn("gym4-messages", script)
        self.assertIn("не сохранены", script)

if __name__ == "__main__":
    unittest.main()
