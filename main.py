import asyncio
import sys

from crawl import crawl_site_async
from json_report import write_json_report


async def main():
    print("Hello, welcome to Giuseppe's web scraper!")
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)

    try:
        base_url = sys.argv[1]
        max_concurrency = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        max_pages = int(sys.argv[3]) if len(sys.argv) > 3 else 100
        if len(sys.argv) > 4:
            raise ValueError
    except ValueError:
        print("usage: uv run main.py BASE_URL [MAX_CONCURRENCY] [MAX_PAGES]")
        sys.exit(1)

    if max_concurrency < 1 or max_pages < 1:
        print("MAX_CONCURRENCY and MAX_PAGES must be positive integers")
        sys.exit(1)

    print(f"starting crawl of: {base_url}")
    try:
        page_data = await crawl_site_async(base_url, max_concurrency, max_pages)
    except Exception as error:
        print(f"Error crawling URL: {error}")
        sys.exit(1)

    print(f"found {len(page_data)} pages")
    write_json_report(page_data)


if __name__ == "__main__":
    asyncio.run(main())
