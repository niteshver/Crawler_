import asyncio
import hashlib
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from crawl4ai import AsyncUrlSeeder, SeedingConfig


ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.crawler.sitemap import SOURCES


OUTPUT_XML = "data/raw/sitemap/master_seed.xml"


# -----------------------------
# URL Filters
# -----------------------------

IGNORE = [
    "/login",
    "/logout",
    "/signup",
    "/signin",
    "/register",
    "/pricing",
    "/about",
    "/privacy",
    "/terms",
    "/contact",
    "/cookies",
    "/favicon",
    ".css",
    ".js",
    ".png",
    ".jpg",
    ".jpeg",
    ".svg",
    ".gif",
]


KEYWORDS = [
    "tutorial",
    "guide",
    "documentation",
    "docs",
    "reference",
    "api",
    "project",
    "paper",
    "research",
    "model",
    "dataset",
]


def url_hash(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()


def is_relevant(url: str, title: str = "") -> bool:

    url = url.lower()
    title = title.lower()

    for item in IGNORE:
        if item in url:
            return False

    if any(word in url for word in KEYWORDS):
        return True

    if any(word in title for word in KEYWORDS):
        return True

    return False


async def discover_urls():

    all_urls = {}
    seeder = AsyncUrlSeeder()

    async with seeder:

        for source_name, domains in SOURCES.items():

            config = SeedingConfig(
                source="sitemap",
                pattern="*",
                filter_nonsense_urls=True,
            )

            for domain in domains:

                print(f"\nDiscovering: {domain}")

                try:
                    pages = await seeder.urls(
                        domain,
                        config=config,
                    )

                except Exception as e:
                    print(f"Failed to discover {domain}: {e}")
                    continue

                print(f"Found {len(pages)} URLs")

                kept = 0

                for page in pages:

                    # Crawl4AI versions differ:
                    # sometimes page is a string,
                    # sometimes it's a dictionary.

                    if isinstance(page, dict):
                        url = page.get("url", "")
                        head = page.get("head_data", {}) or {}
                        title = head.get("title", "")
                    else:
                        url = str(page)
                        title = ""

                    if not url:
                        continue

                    if not is_relevant(url, title):
                        continue

                    h = url_hash(url)

                    if h in all_urls:
                        continue

                    all_urls[h] = {
                        "url": url,
                        "domain": domain,
                        "source": source_name,
                    }

                    kept += 1

                print(f"Kept {kept}")

    return list(all_urls.values())


def generate_xml(urls):

    root = ET.Element(
        "urlset",
        xmlns="http://www.sitemaps.org/schemas/sitemap/0.9",
    )

    today = datetime.now().strftime("%Y-%m-%d")

    for page in sorted(urls, key=lambda x: x["url"]):

        url = ET.SubElement(root, "url")

        loc = ET.SubElement(url, "loc")
        loc.text = page["url"]

        lastmod = ET.SubElement(url, "lastmod")
        lastmod.text = today

        if page["source"] == "research":
            change = "daily"
            priority = "1.0"

        elif page["source"] in ["python", "pypi"]:
            change = "weekly"
            priority = "0.9"

        else:
            change = "weekly"
            priority = "0.8"

        ET.SubElement(url, "changefreq").text = change
        ET.SubElement(url, "priority").text = priority

    tree = ET.ElementTree(root)

    ET.indent(tree)

    Path(OUTPUT_XML).parent.mkdir(parents=True, exist_ok=True)

    tree.write(
        OUTPUT_XML,
        encoding="utf-8",
        xml_declaration=True,
    )

    print("\n" + "=" * 60)
    print(f"Saved {len(urls)} URLs")
    print(OUTPUT_XML)
    print("=" * 60)


async def main():

    urls = await discover_urls()

    generate_xml(urls)


if __name__ == "__main__":
    asyncio.run(main())