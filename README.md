# Web Scraper

An asynchronous web crawler that collects headings, paragraphs, links, and image URLs from pages on the same domain.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

Install the project dependencies with:

```bash
uv sync
```

## Usage

Run the crawler with a starting URL:

```bash
uv run main.py BASE_URL [MAX_CONCURRENCY] [MAX_PAGES]
```

For example:

```bash
uv run main.py https://learnwebscraping.dev/practice/ecommerce/ 3 25
```

`MAX_CONCURRENCY` defaults to `10`, and `MAX_PAGES` defaults to `100`. Both values must be positive integers.

The crawler follows links on the starting domain, avoids duplicate pages, and writes the collected page data to `report.json` sorted by URL.

## Testing

Run the test suite with:

```bash
uv run python -m unittest discover
```
