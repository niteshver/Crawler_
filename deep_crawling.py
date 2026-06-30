from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.async_configs import BrowserConfig, CacheMode, CrawlerRunConfig, DefaultMarkdownGenerator
import asyncio
from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer
from crawl4ai import AsyncWebCrawler
import os
import json
import hashlib


def select_markdown_text(result):
    """Prefer filtered markdown, then cited markdown, then raw markdown."""
    if not result.markdown:
        return ""

    candidates = [
        result.markdown.fit_markdown,
        result.markdown.markdown_with_citations,
        result.markdown.raw_markdown,
    ]
    for candidate in candidates:
        if candidate and candidate.strip():
            return candidate
    return ""


def has_crawl_error(result, markdown_text):
    error_markers = [
        result.error_message or "",
        result.cleaned_html or "",
        markdown_text or "",
    ]
    return any("Crawl4AI Error:" in marker for marker in error_markers)

async def main():
    browser_config = BrowserConfig(
        headless=True,
        verbose=True
    )

    markdown_generator = DefaultMarkdownGenerator(
        # content_filter=PruningContentFilter(
        #     threshold=0.6
        # ),
        # options={
        #     "ignore_links" : True
        # }
    )

    urls1 = [

        "https://www.geeksforgeeks.org/artificial-intelligence/agent-based-modelling/",
        "https://www.geeksforgeeks.org/courses/category/dsa-placements",
        "https://www.anylogic.com/use-of-simulation/agent-based-modeling/",
    ]
    score = KeywordRelevanceScorer(
        keywords = ["Agent", "agent", "system"],
        weight=0.7
    )

    

    strategy = BFSDeepCrawlStrategy(
        max_depth= 2,
        include_external=False,
        url_scorer=score,
        max_pages=25

    )

    config_run = CrawlerRunConfig(
        markdown_generator=markdown_generator,
        deep_crawl_strategy=strategy,
        stream=True,
        word_count_threshold=10,
        exclude_external_links=True,
        exclude_social_media_links=True,
        process_iframes=True,
        remove_forms=True,
        cache_mode=CacheMode.BYPASS,
        magic=True,
        
    )

    os.makedirs("markdown", exist_ok=True)
    os.makedirs("json", exist_ok=True)

    async with AsyncWebCrawler(config=browser_config) as crawler:
        async for result in await crawler.arun_many(
            urls=urls1,
            config = config_run
        ):
            metadata = result.metadata or {}
            markdown_text = select_markdown_text(result)

            if not result.success:
                print(f"result failed {result.url}")
                print(result.error_message)
                continue

            if has_crawl_error(result, markdown_text):
                print(f"Skipping unsupported page for {result.url}")
                print(markdown_text[:300])
                continue

            print("*" * 80)
            print(result.url)
            print(result.status_code)
            print("=" * 50)
            print("HTML Length:", len(result.html))
            print("Clean HTML Length:", len(result.cleaned_html or ""))
            print("Markdown Length:", len(result.markdown.raw_markdown))
            print("Fit Markdown Length:", len(result.markdown.fit_markdown))
            print("Saved Markdown Length:", len(markdown_text))


            filename = hashlib.md5(

                result.url.encode()
            ).hexdigest()

            

            # ---------------------------
            # Save Markdown
            # ---------------------------
            with open(
                f"markdown/{filename}.md",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(markdown_text)

            # ---------------------------
            # Save JSON
            # ---------------------------
            document = {
                "url": result.url,
                "title": metadata.get("title"),
                "status": result.status_code,
                "markdown": markdown_text,
                "internal_links": result.links.get("internal", []),
                "external_links": result.links.get("external", []),
                "images": result.media.get("images", []),
                "metadata": metadata,
            }

            with open(
                f"json/{filename}.json",
                "w",
                encoding="utf-8",
            ) as f:
                json.dump(
                    document,
                    f,
                    indent=4,
                    ensure_ascii=False,
                )

            print("Saved Markdown")
            print("Saved JSON")
            print(
                "Content Preview:\n",
                markdown_text[:300],
            )


if __name__ == "__main__":
    asyncio.run(main())



    
