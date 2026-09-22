import requests
from bs4 import BeautifulSoup, Tag
from urllib.parse import urlsplit
from urllib.parse import urljoin


def normalize_url(url: str) -> str:
    parsed = urlsplit(url)  # Parse the raw URL into parts like scheme, netloc, path, and fragment.

    hostname = parsed.netloc.lower()  # Convert the domain to lowercase because hostnames are case-insensitive.
    
    path = parsed.path.rstrip("/")  # Remove a trailing slash from the path to avoid duplicate page URLs.
    if not path:  # If the path is empty, use an empty string so the normalized URL still works.
        path = ""

    return hostname + path  # Join the domain and path into a canonical URL form while keeping the host subdomain.


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


def get_html(url: str) -> str:
    response = requests.get(url, headers={"User-Agent": "GiuseppeCrawler/1.0"})
    response.raise_for_status()

    content_type = response.headers.get("content-type", "")
    if not content_type.lower().startswith("text/html"):
        raise ValueError(f"expected text/html content type, got {content_type}")

    return response.text
