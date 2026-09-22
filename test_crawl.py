import unittest
from crawl import normalize_url


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_removes_trailing_slash(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_removes_www_prefix(self):
        input_url = "https://www.boot.dev"
        actual = normalize_url(input_url)
        expected = "boot.dev"
        self.assertEqual(actual, expected)

    def test_normalize_url_lowercases_hostname(self):
        input_url = "https://BOOT.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "boot.dev/blog/path"
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()