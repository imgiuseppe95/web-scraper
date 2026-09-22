import unittest

from main import get_first_paragraph_from_html, get_heading_from_html


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


if __name__ == "__main__":
    unittest.main()
