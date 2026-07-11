# NexaSearch 

A open Source Verticel Search Engine
``` text
Seed Sources
│
├── Official Documentation
├── Wikipedia
├── GitHub
├── Research Papers
├── Blogs
├── News
└── Sitemaps / RSS
        │
        ▼
URL Frontier (Priority Queue)
        │
        ▼
Adaptive / BFS / Best-First Crawling (Crawl4AI)
        │
        ▼
Fetch HTML
        │
        ▼
Main Content Extraction
    ├── Trafilatura
    ├── jusText
    └── BeautifulSoup (optional cleanup)
        │
        ▼
Cleaning Pipeline
    ├── Remove HTML boilerplate
    ├── Remove header/footer/nav
    ├── Remove ads/scripts/styles
    ├── Unicode normalization
    ├── Whitespace normalization
    ├── Empty page removal
    ├── Spam removal
    ├── PII removal (spaCy / Presidio / regex)
    ├── Language detection (fastText)
    └── Metadata extraction
        │
        ▼
Deduplication
    ├── URL Canonicalization
    ├── SHA256 (exact duplicates)
    ├── MinHash
    ├── SimHash
    └── LSH (near duplicates)
        │
        ▼
Quality Filtering
    ├── DistilBERT Quality Classifier
    ├── Readability
    ├── Content length
    ├── Spam classifier
    └── Toxicity filter
        │
        ▼
Chunking
        │
        ▼
Storage
    ├── JSONL / Parquet
    ├── DuckDB
    └── Metadata Database
        │
        ▼
Indexing
    ├── BM25
    ├── Embeddings
    └── Hybrid Index
        │
        ▼
Search / RAG / Fine-tuning
```

# Project Workflow

## 0. Domain
- AI
- Programming
- Research Papers
- Official Documentation

## 1. Seed Collection

Correct.

Add: - Sitemap.xml - RSS Feeds - Previously discovered URLs - Common
Crawl (optional)

------------------------------------------------------------------------

## 2. URL Frontier

Should be a **priority queue**, not just a URL list.

Priority can depend on: - Domain authority - Freshness - Topic
relevance - Crawl depth

------------------------------------------------------------------------

## 3. Crawling

Use Crawl4AI:

-   BFSDeepCrawlStrategy
-   BestFirstDeepCrawlStrategy
-   AdaptiveCrawler

Adaptive crawling is useful for domain-specific search because it spends
more effort on high-quality sections.

------------------------------------------------------------------------

## 4. Content Extraction

Primary choice: - Trafilatura

Alternatives: - jusText - Readability

BeautifulSoup is mainly for additional HTML processing.

------------------------------------------------------------------------

## 5. Cleaning

Recommended order:

1.  Extract article
2.  Remove boilerplate
3.  Remove scripts/styles
4.  Unicode normalization
5.  Remove duplicate lines
6.  Normalize whitespace
7.  PII removal
8.  Language detection
9.  Metadata extraction

------------------------------------------------------------------------

## 6. PII Removal

choices: - Microsoft Presidio - spaCy - Regex

------------------------------------------------------------------------

## 7. Language Detection

Use fastText.

Store language in metadata.

------------------------------------------------------------------------

## 8. Metadata

Store:

-   URL
-   Canonical URL
-   Domain
-   Language
-   Crawl Time
-   Depth
-   Title
-   Hash
-   Word Count

------------------------------------------------------------------------

## 9. Deduplication

### Exact

SHA256

### Near

-   MinHash
-   SimHash
-   LSH

------------------------------------------------------------------------

## 10. Canonicalization

Normalize:

-   http vs https
-   trailing slash
-   index.html
-   URL parameters (where appropriate)

before duplicate checking.

------------------------------------------------------------------------

## 11. Quality Classifier

DistilBERT is a good lightweight choice.

Score pages based on:

-   Readability
-   Grammar
-   Information density
-   Spam
-   Topic relevance

Discard low-quality pages.

------------------------------------------------------------------------

## 12. Indexing

For search:

-   BM25
-   Dense embeddings
-   Hybrid search

------------------------------------------------------------------------

## 13. Search Ranking

Combine:

-   BM25
-   Embedding similarity
-   Freshness
-   Authority
-   LLM reranker

------------------------------------------------------------------------

# Suggested Tech Stack

## Crawling

-   Crawl4AI
-   Playwright

## Extraction

-   Trafilatura
-   jusText

## Cleaning

-   BeautifulSoup
-   spaCy
-   fastText

## Deduplication

-   SHA256
-   datasketch (MinHash)
-   LSH

## Storage

-   DuckDB
-   Parquet
-   JSONL

## Embeddings

-   Nomic
-   E5

## Search

-   BM25
-   FAISS / Qdrant / Milvus

## Final Architecture 

``` bash

                      Seed URLs
                           │
                           ▼
                  URL Normalization
                           │
                           ▼
                    URL Frontier
                           │
                           ▼
                    robots.txt Check
                           │
                           ▼
                 Adaptive Scheduler
                           │
                           ▼
                 URL Hash / Visited DB
                           │
                           ▼
                  Crawl4AI Workers
                           │
                           ▼
                    Raw HTML Store
                           │
            ┌──────────────┴──────────────┐
            ▼                             ▼
     Link Extraction               Trafilatura
            │                             │
            ▼                             ▼
      Link Graph                  Clean Markdown
            │                             │
            └──────────────┬──────────────┘
                           ▼
                 Metadata Extraction
                           │
                           ▼
               FastText Language Detection
                           │
                           ▼
                  PII Detection/Removal
                           │
                           ▼
                  URL Canonicalization
                           │
                           ▼
               SHA-256 Exact Deduplication
                           │
                           ▼
                 MinHash + LSH Near Dedup
                           │
                           ▼
              DistilBERT Quality Classifier
                           │
                           ▼
             Document/Topic Classification
                           │
                           ▼
                     Chunk Generation
                           │
                           ▼
            Chunk Metadata + Document IDs
                           │
                           ▼
                 DuckDB + Parquet Storage
                           │
                           ▼
               Dense Embedding Generation
                           │
                  ┌────────┴────────┐
                  ▼                 ▼
             BM25 Index      Vector Index
                  │                 │
                  └────────┬────────┘
                           ▼
                  Hybrid Retrieval
                           │
                           ▼
                  Cross-Encoder Reranker
                           │
                           ▼
                     LLM Generation
                           │
                           ▼
                    Citation Generator
                           │
                           ▼
                    Final AI Response
```

## Project Structure

``` 
NexaSearch/
├── .venv/
├── .env
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── README.md
├── project_timeline.md
│
├── sources/
│   ├── __init__.py
│   └── sources.py
│
├── src/
│   ├── crawler/
│   │   ├── __init__.py
│   │   ├── crawler.py
│   │   ├── adaptive_crawl.py
│   │   └── sitemap.py
│   │
│   ├── cleaner/
│   │   ├── __init__.py
│   │   └── distil_robert.py
│   │
│   ├── pipeline/
│   │   └── __init__.py
│   │
│   └── utils/
│       └── __init__.py
│
├── data/
│   ├── raw/
│   │   ├── json/
│   │   ├── markdown/
│   │   └── sitemap/
│   │       ├── sitemap_data.xml
│   │       └── sitemap_url.xml
│   │
│   ├── processed/
│   └── cleaned/
│
├── tests/
│   ├── test_crawler.py
│   ├── test_sitemap.py
│   ├── test_cleaner.py
│   └── test_sources.py
│
├── docs/
├── scripts/
└── logs/

```