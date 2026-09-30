"""Static regression checks; run python3 -m unittest discover -s tests."""
import importlib.util
from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("site_build", ROOT / "build.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.elements = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = build.render()
        cls.page = Page(cls.html)

    def test_generated_page_is_current(self):
        self.assertEqual(self.html, (ROOT / "index.html").read_text())

    def test_anchors_and_local_assets(self):
        ids = [attrs['id'] for _, attrs in self.page.elements if 'id' in attrs]
        self.assertEqual(len(ids), len(set(ids)))
        for _, attrs in self.page.elements:
            for key in ('src', 'href'):
                value = attrs.get(key)
                if not value:
                    continue
                if value.startswith('#'):
                    self.assertIn(value[1:], ids)
                elif not urlsplit(value).scheme:
                    self.assertTrue((ROOT / value).is_file(), value)

    def test_resource_placeholders_are_not_links(self):
        for tag, attrs in self.page.elements:
            self.assertNotEqual(attrs.get('href'), '#')
            if attrs.get('aria-disabled') == 'true':
                self.assertNotEqual(tag, 'a')

    def test_images_have_accessibility_and_layout_metadata(self):
        for tag, attrs in self.page.elements:
            if tag == 'img':
                self.assertIn('alt', attrs)
                if attrs.get('id') != 'viewer-image':
                    self.assertGreater(int(attrs['width']), 0)
                    self.assertGreater(int(attrs['height']), 0)

    def test_migration_metadata(self):
        self.assertIn('rel="canonical" href="https://dtdd-proj.github.io/"', self.html)
        self.assertNotIn('qijia-he.github.io/dtdd', self.html)
        self.assertNotIn('${', self.html)
        self.assertIn('static/images/bu_monogram.png', self.html)

    def test_resources_enable_with_real_urls(self):
        self.assertNotIn('href', build.resource('Paper', ''))
        self.assertIn('href="https://example.org/paper"', build.resource('Paper', 'https://example.org/paper'))
        with self.assertRaises(ValueError):
            build.resource('Paper', '#')

    def test_classic_project_layout_and_author_link(self):
        self.assertNotIn('<nav', self.html)
        self.assertNotIn('class="highlights"', self.html)
        self.assertIn('<section id="abstract" class="abstract">', self.html)
        self.assertLess(self.html.index('id="abstract"'), self.html.index('id="method"'))
        self.assertIn('href="https://sites.google.com/site/sugatobasu/">Sugato Basu</a>', self.html)


if __name__ == '__main__':
    unittest.main()
