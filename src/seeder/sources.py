from crawl4ai import SeedingConfig

SOURCES = {
    "python": {
        "domains": [
            "docs.python.org",
            "python.org",
            "pypi.org",
            
        ],
        "config": SeedingConfig(
            source="sitemap",
            pattern="*/3/*",
            filter_nonsense_urls=True,
            extract_head=True,
            max_urls=50000,
        ),
    },

    "pypi": {
        "domains": [
            "pypi.org",
        ],
        "config": SeedingConfig(
            source="sitemap",
            pattern="*/project/*",
            filter_nonsense_urls=True,
            extract_head=True,
            max_urls=100000,
        ),
    },

    "ai": {
        "domains": [
            "huggingface.co",
            "python.langchain.com",
            "openai.com",
            "anthropic.com",
        ],
        "config": SeedingConfig(
            source="sitemap",
            pattern="*",
            filter_nonsense_urls=True,
            extract_head=True,
            max_urls=50000,
        ),
    },

    "research": {
        "domains": [
            "arxiv.org",
            "paperswithcode.com",
            "openreview.net",
            "aclanthology.org",
        ],
        "config": SeedingConfig(
            source="sitemap+cc",
            pattern="*/abs/*",
            filter_nonsense_urls=True,
            extract_head=True,
            max_urls=100000,
        ),
    },
}