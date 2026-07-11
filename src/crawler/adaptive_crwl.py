# from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
# from crawl4ai.async_configs import BrowserConfig, CacheMode, CrawlerRunConfig, DefaultMarkdownGenerator
# import asyncio
# from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer
# from crawl4ai import AsyncWebCrawler, AdaptiveCrawler
# from crawl4ai.content_filter_strategy import PruningContentFilter
# import os
# import json
# import hashlib
# import xml.etree.ElementTree as ET
# import asyncio


# async def main():
#     browser_config = BrowserConfig(
#         headless=True,
#         verbose=True
#     )



#     async with AsyncWebCrawler(config=browser_config) as crawler:

#         adaptive = AdaptiveCrawler(crawler)

#         result = await adaptive.digest(
#             start_url="https://docs.langchain.com",
#             query="LangGraph agents"
#         )

#         adaptive.print_stats()

#         print(result.crawled_urls)
#         if result is exit:
            


# if __name__ == "__main__":


#     asyncio.run(main())