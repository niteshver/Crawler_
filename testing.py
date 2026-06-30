import asyncio

from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import (
    BrowserConfig,
    CrawlerRunConfig,
    CacheMode,
    DefaultMarkdownGenerator,
)
from crawl4ai.content_filter_strategy import PruningContentFilter


async def main():
    # ----------------------------
    # Browser Configuration
    # ----------------------------
    browser_config = BrowserConfig(
        headless=True,      # Run browser in background
        verbose=True        # Show logs
    )

    # ----------------------------
    # Markdown Generator
    # ----------------------------
    markdown_generator = DefaultMarkdownGenerator(
        content_filter=PruningContentFilter(
            threshold=0.6
        ),
        options={
            "ignore_links": True
        }
    )

    # ----------------------------
    # Crawl Configuration
    # ----------------------------
    run_config = CrawlerRunConfig(
        markdown_generator=markdown_generator,

        # Ignore tiny text blocks
        word_count_threshold=10,

        # Remove unwanted HTML tags
        excluded_tags=[
            "form",
            "header"
        ],

        # Ignore external links
        exclude_external_links=True,

        # Crawl iframe content
        process_iframes=True,

        # Remove cookie banners/popups
        remove_overlay_elements=True,

        # Use cached pages if available
        cache_mode=CacheMode.ENABLED,
    )

    # ----------------------------
    # Start Browser
    # ----------------------------
    async with AsyncWebCrawler(config=browser_config) as crawler:

        result = await crawler.arun(
            url="https://huggingface.co/docs/transformers/main/en/main_classes/data_collator#transformers.DataCollatorForLanguageModeling",
            config=run_config
        )

        # ----------------------------
        # Success
        # ----------------------------
        if result.success:

            print("=" * 80)
            print("CRAWL SUCCESS")
            print("=" * 80)

            print("\nStatus Code:")
            print(result.status_code)

            print("\nSuccess:")
            print(result.success)

            print("\nRaw HTML (first 500 chars):")
            print(result.html[:500])

            print("\nCleaned HTML (first 500 chars):")
            print(result.cleaned_html[:500])

            print("\nRaw Markdown:")
            print(result.markdown.raw_markdown[:500])

            print("\nFiltered Markdown:")
            print(result.markdown.fit_markdown[:500])

            print("\nImages Found:")
            print("-" * 40)

            for image in result.media.get("images", []):
                print(image)

            print("\nInternal Links:")
            print("-" * 40)

            for link in result.links.get("internal", []):
                print(link)

            print("\nExternal Links:")
            print("-" * 40)

            for link in result.links.get("external", []):
                print(link)

        else:

            print("\nCrawl Failed")
            print(result.error_message)


if __name__ == "__main__":
    asyncio.run(main())