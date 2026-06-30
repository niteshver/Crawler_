from crawl4ai.async_configs import CacheMode,BrowserConfig,CrawlerRunConfig,DefaultMarkdownGenerator, LLMConfig
from crawl4ai.content_filter_strategy import PruningContentFilter, BM25ContentFilter, LLMContentFilter
from crawl4ai import AsyncWebCrawler
import asyncio

async def main():
    browser_config = BrowserConfig(
        headless=True,
        verbose=True
    )
    urls = [
        "https://en.wikipedia.org/wiki/A.I._Artificial_Intelligence",
        "https://en.wikipedia.org/wiki/A.I._Artificial_Intelligence#Pre-production"
    ]

    # llm_filter = LLMContentFilter(
    #     llm_config=LLMConfig(provider="ollama/Ishita21:latest"),
    #      instruction="""
    #     You are an information extraction engine.

    #     Your task is to extract the MAIN CONTENT from the webpage, not to rewrite or summarize it.

    #     Rules:

    #     1. Extract ONLY content that already exists in the webpage.
    #     2. Do NOT generate new text.
    #     3. Do NOT invent headings, examples, tables, code, or explanations.
    #     4. Do NOT use placeholders such as "[Describe...]" or "[Add...]".
    #     5. Preserve the original wording whenever possible.
    #     6. Preserve the original heading hierarchy.
    #     7. Preserve code blocks exactly as they appear.
    #     8. Preserve lists, tables, and important formatting.
    #     9. Remove:
    #     - Navigation menus
    #     - Headers
    #     - Footers
    #     - Sidebars
    #     - Advertisements
    #     - Cookie banners
    #     - Related articles
    #     - Social sharing buttons
    #     - Comments
    #     - Newsletter prompts
    #     - Login prompts
    #     10. Keep only the main article or documentation content.

    #     Output requirements:

    #     - Return ONLY valid Markdown.
    #     - Do NOT wrap the output in markdown code fences.
    #     - Do NOT add introductions or conclusions.
    #     - Do NOT explain what you did.
    #     - If no meaningful article exists, return an empty string.
    #     """,
    #     chunk_token_threshold=1024,
    #     verbose=True   
    # )

    markdown_generator = DefaultMarkdownGenerator(
        # BM25ContentFilter(

        #     bm25_threshold=0.6,
        #     user_query="machine learning",
        #     language="english"
        # ),
        content_filter=PruningContentFilter(
            threshold=0.6,
    
        ),
    
        options = {
            "ignore_links" : True
        }
    )

    run_config = CrawlerRunConfig(
        markdown_generator=markdown_generator,
        word_count_threshold=10,
        flatten_shadow_dom=True,
        wait_until="load",
        delay_before_return_html=0.3,
        excluded_tags=[
            "form",
            "header",
            "footer",
            "nav",
            "aside",
        ],
        exclude_external_links=True,
        # exclude_all_images=True,
        process_iframes=True,
        remove_consent_popups=True,
        remove_overlay_elements=True,
        # only_text=True,
        remove_forms=True,
        cache_mode=CacheMode.ENABLED
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        results = await crawler.arun_many(
    urls=urls,
    config=run_config
)
        
        

        for result in results:

            if not result.success:
                print(result.url)
                print(result.error_message)
                continue

            print("=" * 80)
            print(result.url)
            print(result.status_code)

            print(result.markdown.fit_markdown[:500])

if __name__ == "__main__":
    asyncio.run(main())


