import sys

from crawl import get_html


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
        html = get_html(sys.argv[1])
    except Exception as error:
        print(f"Error fetching URL: {error}")
        sys.exit(1)

    print(html)


if __name__ == "__main__":
    main()
