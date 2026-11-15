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

    def test_demo_form_does_not_store_messages(self):
        contacts = (SITE / "contacts.html").read_text(encoding="utf-8")
        script = (SITE / "assets" / "js" / "app.js").read_text(encoding="utf-8")
        self.assertNotIn('name="email"', contacts)
        self.assertNotIn('name="name"', contacts)
        self.assertNotIn("gym4-messages", script)
        self.assertIn("не сохранены", script)

if __name__ == "__main__":
    unittest.main()
