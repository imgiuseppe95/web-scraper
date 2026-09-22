import unittest

from crawl import (
    get_first_paragraph_from_html,
    get_heading_from_html,
    get_images_from_html,
    get_urls_from_html,
    extract_page_data,
)


class TestHtmlContent(unittest.TestCase):
    def test_get_heading_from_html_returns_h1(self):
        html = "<html><body><h1>Welcome</h1></body></html>"
        self.assertEqual(get_heading_from_html(html), "Welcome")

    def test_get_heading_from_html_returns_h2_when_h1_missing(self):
        html = "<html><body><h2>Secondary heading</h2></body></html>"
        self.assertEqual(get_heading_from_html(html), "Secondary heading")

    def test_get_heading_from_html_returns_empty_string_when_no_heading_exists(self):
        html = "<html><body><p>Just text</p></body></html>"
        self.assertEqual(get_heading_from_html(html), "")

    def test_get_first_paragraph_from_html_returns_first_p(self):
        html = "<html><body><p>First paragraph</p><p>Second paragraph</p></body></html>"
        self.assertEqual(get_first_paragraph_from_html(html), "First paragraph")

    def test_get_first_paragraph_from_html_returns_empty_string_when_no_p_exists(self):
        html = "<html><body><h1>Title</h1></body></html>"
        self.assertEqual(get_first_paragraph_from_html(html), "")

    def test_get_urls_from_html_returns_absolute_urls(self):
        base_url = "https://crawler-test.com"
        html = '<html><body><a href="/about">About</a></body></html>'
        self.assertEqual(
            get_urls_from_html(html, base_url),
            ["https://crawler-test.com/about"],
        )

    def test_get_urls_from_html_returns_all_anchor_urls(self):
        base_url = "https://crawler-test.com"
        html = (
            '<html><body><a href="/first">First</a>'
            '<a href="https://example.com">Second</a></body></html>'
        )
        self.assertEqual(
            get_urls_from_html(html, base_url),
            ["https://crawler-test.com/first", "https://example.com"],
        )

    def test_get_images_from_html_returns_relative_url_as_absolute(self):
        base_url = "https://crawler-test.com"
        html = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        self.assertEqual(
            get_images_from_html(html, base_url),
            ["https://crawler-test.com/logo.png"],
        )

    def test_get_images_from_html_returns_absolute_url(self):
        base_url = "https://crawler-test.com"
        html = '<html><body><img src="https://example.com/logo.png"></body></html>'
        self.assertEqual(
            get_images_from_html(html, base_url),
            ["https://example.com/logo.png"],
        )

    def test_get_images_from_html_skips_image_without_src(self):
        base_url = "https://crawler-test.com"
        html = '<html><body><img alt="Missing source"></body></html>'
        self.assertEqual(get_images_from_html(html, base_url), [])

    def test_extract_page_data_basic(self):
        page_url = "https://crawler-test.com"
        html = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(extract_page_data(html, page_url), expected)


if __name__ == "__main__":
    unittest.main()
