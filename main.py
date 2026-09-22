from bs4 import BeautifulSoup, Tag


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


def main():
    print("Hello from web-scraper!")


if __name__ == "__main__":
    main()
