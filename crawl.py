from urllib.parse import urlsplit


def normalize_url(url: str) -> str:
    parsed = urlsplit(url)  # Parse the raw URL into parts like scheme, netloc, path, and fragment.

    hostname = parsed.netloc.lower()  # Convert the domain to lowercase because hostnames are case-insensitive.
    if hostname.startswith("www."):  # Remove the common www. prefix when present.
        hostname = hostname[4:]

    path = parsed.path.rstrip("/")  # Remove a trailing slash from the path to avoid duplicate page URLs.
    if not path:  # If the path is empty, use an empty string so the normalized URL still works.
        path = ""

    return hostname + path  # Join the domain and path into a canonical URL form.
