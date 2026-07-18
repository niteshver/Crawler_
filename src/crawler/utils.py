import hashlib


def sha256(text: str) -> str:

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

TRACKING_PARAMS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "gclid",
    "fbclid",
}


def canonicalize_url(url: str) -> str:
    """
    Normalize URLs so equivalent URLs map to one canonical form.
    """
    parts = urlsplit(url)

    scheme = parts.scheme.lower()
    netloc = parts.netloc.lower()

    if netloc.endswith(":80") and scheme == "http":
        netloc = netloc[:-3]

    if netloc.endswith(":443") and scheme == "https":
        netloc = netloc[:-4]

    path = parts.path or "/"

    if path != "/" and path.endswith("/"):
        path = path[:-1]

    query = urlencode(
        sorted(
            (k, v)
            for k, v in parse_qsl(parts.query, keep_blank_values=True)
            if k not in TRACKING_PARAMS
        )
    )

    return urlunsplit((scheme, netloc, path, query, ""))

from crawler.config import settings

for directory in [
    settings.DATA_DIR,
    settings.RAW_HTML_DIR,
    settings.MARKDOWN_DIR,
    settings.JSON_DIR,
    settings.LOG_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)