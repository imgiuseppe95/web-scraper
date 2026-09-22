import sys

from crawl import crawl_page


def main():
    print("Hello, welcome to Giuseppe's web scraper!")
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)

    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)

    print(f"starting crawl of: {sys.argv[1]}")
    try:
        page_data = crawl_page(sys.argv[1])
    except Exception as error:
        print(f"Error crawling URL: {error}")
        sys.exit(1)

    print(f"found {len(page_data)} pages")
    for data in page_data.values():
        print(data)


if __name__ == "__main__":
    main()
