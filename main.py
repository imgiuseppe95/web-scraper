import sys

from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin


def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    h1_tag = soup.find("h1")
    if isinstance(h1_tag, Tag):
        return h1_tag.get_text(strip=True)

    h2_tag = soup.find("h2")
    if isinstance(h2_tag, Tag):
        return h2_tag.get_text(strip=True)

    return ""


def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    paragraph = soup.find("p")
    if isinstance(paragraph, Tag):
        return paragraph.get_text(strip=True)

    return ""


def get_urls_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for anchor in soup.find_all("a"):
        href = anchor.get("href")
        if href is not None:
            urls.append(urljoin(base_url, href))
    return urls


def get_images_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    image_urls = []
    for image in soup.find_all("img"):
        src = image.get("src")
        if src is not None:
            image_urls.append(urljoin(base_url, src))
    return image_urls


def extract_page_data(html: str, page_url: str) -> dict:
    return {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }


def main():
    print("Hello, welcome to Giuseppe's web scraper!")
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)

    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)

    print(f"starting crawl of: {sys.argv[1]}")


if __name__ == "__main__":
    main()
