import asyncio
from urllib.parse import urljoin, urlsplit

import aiohttp
from bs4 import BeautifulSoup, Tag


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


class AsyncCrawler:
    def __init__(
        self,
        base_url: str,
        max_concurrency: int = 10,
        max_pages: int = 100,
    ):
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc.lower()
        self.page_data = {}
        self.visited = set()
        self.should_stop = False
        self.all_tasks = set()
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.max_pages = max_pages
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url: str) -> bool:
        async with self.lock:
            if self.should_stop:
                return False
            if len(self.visited) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                return False
            if normalized_url in self.visited:
                return False
            self.visited.add(normalized_url)
            return True

    async def get_html(self, url: str) -> str:
        async with self.session.get(
            url, headers={"User-Agent": "GiuseppeCrawler/1.0"}
        ) as response:
            response.raise_for_status()

            content_type = response.headers.get("content-type", "")
            if not content_type.lower().startswith("text/html"):
                raise ValueError(f"expected text/html content type, got {content_type}")

            return await response.text()

    async def crawl_page(self, current_url: str):
        if self.should_stop:
            return

        current_domain = urlsplit(current_url).netloc.lower()
        if current_domain != self.base_domain:
            return

        normalized_url = normalize_url(current_url)
        if not await self.add_page_visit(normalized_url):
            return

        print(f"crawling {current_url}")
        try:
            async with self.semaphore:
                html = await self.get_html(current_url)
        except Exception as error:
            print(f"Error crawling {current_url}: {error}")
            return

        data = extract_page_data(html, current_url)
        async with self.lock:
            self.page_data[normalized_url] = data

        tasks = []
        for next_url in data["outgoing_links"]:
            task = asyncio.create_task(self._crawl_child(next_url))
            self.all_tasks.add(task)
            tasks.append(task)
        if tasks:
            await asyncio.gather(*tasks)

    async def _crawl_child(self, current_url: str):
        task = asyncio.current_task()
        try:
            await self.crawl_page(current_url)
        finally:
            self.all_tasks.discard(task)

    async def crawl(self) -> dict:
        await self.crawl_page(self.base_url)
        return self.page_data


async def crawl_site_async(
    base_url: str,
    max_concurrency: int = 10,
    max_pages: int = 100,
) -> dict:
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        return await crawler.crawl()
