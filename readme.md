# 🌐 Search Engine - Data Collection Pipeline

> A modular data collection pipeline for a search engine. This project focuses on crawling, extracting, cleaning, deduplicating, and preparing high-quality web data for future indexing and ranking.

![Python](https://img.shields.io/badge/Python-3.12+-blue)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

# 📖 Project Summary

This repository contains the **Data Collection** module of my search engine.

The primary objective is to collect **high-quality web pages**, remove unnecessary content, eliminate duplicate pages, detect language, extract metadata, and prepare a clean dataset for future indexing.

> **Current Progress:** Approximately **50% of the Data Collection pipeline** has been completed.

The project is inspired by the data pipelines used in modern search engines and large-scale datasets such as Google Search, Common Crawl, FineWeb, RefinedWeb, and Meta's Llama data pipeline.

---

# 🎯 Current Scope

The current focus is only on **Data Collection**.

Implemented / Planned:

- Seed URL Collection
- URL Frontier
- Web Crawling
- HTML Collection
- Content Extraction
- Metadata Extraction
- Language Detection
- Duplicate Detection
- Quality Filtering

The following modules are **not part of this repository yet**:

- Indexing
- Ranking
- Search API
- Query Processing

---

# 🏗 Pipeline Architecture

```text
                Seed Collection
        (Wikipedia, GitHub, Official Sites)
                         │
                         ▼
                  URL Frontier
                  (Priority Queue)
                         │
                         ▼
                 Robots.txt Checker
                         │
                         ▼
             Downloader (Crawl4AI)
                         │
                         ▼
                 Raw HTML Storage
                         │
                         ▼
              Trafilatura Extraction
                         │
                         ▼
                 Clean Main Content
                         │
                         ▼
               Metadata Extraction
                         │
                         ▼
          Language Detection (FastText)
                         │
                         ▼
        Exact Duplicate Detection (SHA256)
                         │
                         ▼
      Near Duplicate Detection (MinHash + LSH)
                         │
                         ▼
     Quality Filtering (DistilRoBERTa)
                         │
                         ▼
              Clean Dataset Storage
```

---

# 📂 Project Structure

```text
search-engine/

│
├── crawler/
│   ├── downloader.py
│   ├── frontier.py
│   ├── scheduler.py
│   └── robots.py
│
├── parser/
│   ├── extractor.py
│   ├── metadata.py
│   └── links.py
│
├── deduplication/
│   ├── sha256.py
│   ├── minhash.py
│   └── lsh.py
│
├── quality/
│   ├── language.py
│   ├── classifier.py
│   └── filters.py
│
├── storage/
│   ├── raw_html/
│   ├── cleaned_text/
│   └── metadata/
│
├── requirements.txt
│
├── .gitignore
│
├── LICENSE
│
└── README.md
```

---

# 🔄 Data Collection Workflow

### 1. Seed Collection

The crawler starts with trusted sources such as

- Wikipedia
- GitHub
- Official Websites
- Government Websites
- Technical Blogs

---

### 2. URL Frontier

Responsible for

- URL Queue
- URL Priority
- Visited URLs
- Crawl Scheduling

---

### 3. Downloader

Downloads HTML pages using

- Crawl4AI
- Async Crawling

Stores

- HTML
- Status Code
- Response Headers
- Crawl Time

---

### 4. Content Extraction

Uses **Trafilatura** to remove

- Navigation
- Footer
- Sidebar
- Advertisements
- Scripts

Extracts

- Main Content
- Title
- Author
- Date

---

### 5. Metadata Extraction

Stores

- URL
- Canonical URL
- Domain
- Title
- Language
- Publish Date
- Crawl Date
- Word Count

---

### 6. Language Detection

Uses **FastText** to identify document language.

---

### 7. Duplicate Detection

#### Exact Duplicate

- SHA256

#### Near Duplicate

- MinHash
- Locality Sensitive Hashing (LSH)

---

### 8. Quality Filtering

Uses DistilRoBERTa to remove

- Spam
- Empty Pages
- Low-quality Content
- Very Short Documents

---

# 🛠 Libraries Used

| Category | Library |
|----------|----------|
| Crawling | Crawl4AI |
| HTML Parsing | lxml |
| Content Extraction | Trafilatura |
| Language Detection | FastText |
| NLP | spaCy |
| Duplicate Detection | datasketch |
| Hashing | hashlib |
| Machine Learning | Transformers |
| Quality Classification | DistilRoBERTa |
| Async Programming | asyncio |
| Storage | DuckDB / SQLite |
| Logging | loguru |

---

# 📦 requirements.txt

```text
crawl4ai
trafilatura
lxml
httpx
playwright
beautifulsoup4

fasttext-wheel
spacy

transformers
torch

datasketch

duckdb
sqlite-utils

loguru

tqdm

pandas
numpy

aiofiles
asyncio

python-dotenv

orjson
```

---

# 🚀 Current Progress

## Completed

- [x] Project Architecture
- [x] Seed Collection Design
- [x] URL Frontier Design
- [x] Metadata Schema
- [x] Duplicate Detection Planning
- [x] Quality Filter Planning

---

## In Progress

- [ ] Downloader
- [ ] Async Crawling
- [ ] Trafilatura Integration
- [ ] Metadata Extraction
- [ ] Language Detection
- [ ] Duplicate Detection

---

## Overall Progress

```text
██████████░░░░░░░░░░ 50%
```

The current repository focuses only on the **Data Collection** stage of the search engine.

---

# 🎯 Future Work

After completing the data collection module, the next stages will include:

- Index Construction
- Inverted Index
- BM25 Ranking
- Semantic Search
- Query Processing
- Search API
- Web Interface

---

# 🤝 Contributing

Contributions are welcome.

## Getting Started

1. Fork the repository

```bash
git clone https://github.com/yourusername/search-engine.git
```

2. Create a new branch

```bash
git checkout -b feature/new-feature
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Commit your changes

```bash
git commit -m "Add new feature"
```

5. Push your branch

```bash
git push origin feature/new-feature
```

6. Open a Pull Request

---

## Contribution Guidelines

Please ensure that:

- Code follows PEP 8.
- Functions include type hints where appropriate.
- New modules include comments or docstrings.
- Pull requests are focused on a single feature or bug fix.

---

# 📜 License

This project is licensed under the MIT License.

---

⭐ If you find this project useful, consider starring the repository.