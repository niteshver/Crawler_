
import asyncio
from datetime import datetime
import xml.etree.ElementTree as ET

from crawl4ai import AsyncUrlSeeder, SeedingConfig


# -------------------------------------
# Websites
# -------------------------------------

SOURCES = {

    "python": [
        "docs.python.org",
        "pypi.org",
    ],

    "ai": [
        "huggingface.co",
        "python.langchain.com",
        "openai.com",
        "anthropic.com",
    ],

    "research": [
        "arxiv.org",
        "paperswithcode.com",
        "openreview.net",
        "aclanthology.org",
    ],

}


# -------------------------------------
# Discover URLs
# -------------------------------------

async def discover_urls():

    config = SeedingConfig(
        source="sitemap+cc",
        extract_head=False,
        filter_nonsense_urls=True,
        max_urls=-1,
        concurrency=20,
    )

    all_urls = []

    async with AsyncUrlSeeder() as seeder:

        for category, domains in SOURCES.items():

            print(f"\nDiscovering {category} websites...")

            results = await seeder.many_urls(
                domains,
                config
            )

            for domain, pages in results.items():

                print(f"{domain}: {len(pages)} URLs")

                for page in pages:

                    all_urls.append({

                        "url": page["url"],

                        "source": category,

                        "domain": domain,

                    })

    return all_urls


# -------------------------------------
# Generate XML
# -------------------------------------

def build_xml(urls):

    unique = {}

    for page in urls:
        unique[page["url"]] = page

    root = ET.Element(
        "urlset",
        xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
    )

    today = datetime.now().strftime("%Y-%m-%d")

    for page in sorted(unique.values(), key=lambda x: x["url"]):

        url = ET.SubElement(root, "url")

        loc = ET.SubElement(url, "loc")
        loc.text = page["url"]

        lastmod = ET.SubElement(url, "lastmod")
        lastmod.text = today

        changefreq = ET.SubElement(url, "changefreq")
        changefreq.text = "weekly"

        priority = ET.SubElement(url, "priority")

        if page["source"] == "research":
            priority.text = "1.0"

        elif page["source"] == "python":
            priority.text = "0.9"

        else:
            priority.text = "0.8"

    tree = ET.ElementTree(root)

    ET.indent(tree)

    tree.write(
        "master_seed.xml",
        encoding="utf-8",
        xml_declaration=True
    )

    print("\nmaster_seed.xml created!")


# -------------------------------------
# Main
# -------------------------------------

async def main():

    urls = await discover_urls()

    print(f"\nTotal URLs: {len(urls)}")

    build_xml(urls)


if __name__ == "__main__":
    asyncio.run(main())