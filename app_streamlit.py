import streamlit as st
import pandas as pd
import numpy as np
import time
import os
import sys
import json
from pathlib import Path

# Add root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.pipeline.orchestrator import NexaSearchPipeline
from src.config.settings import settings

# Page Configurations
st.set_page_config(
    page_title="NexaSearch - Domain Search Engine",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling
st.markdown("""
<style>
    /* CSS for premium look */
    .main {
        background-color: #0e1117;
        color: #c9d1d9;
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3 {
        color: #58a6ff;
        font-family: 'Outfit', sans-serif;
    }
    .stButton>button {
        background-color: #238636;
        color: white;
        border-radius: 6px;
        border: 1px solid rgba(240,246,252,0.1);
        padding: 0.5rem 1rem;
        transition: background-color 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #2ea043;
        border-color: rgba(240,246,252,0.1);
        color: white;
    }
    .card {
        background-color: #161b22;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #30363d;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .card:hover {
        transform: translateY(-2px);
        border-color: #58a6ff;
    }
    .card-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .card-title a {
        color: #58a6ff;
        text-decoration: none;
    }
    .card-title a:hover {
        text-decoration: underline;
    }
    .card-url {
        font-size: 0.85rem;
        color: #8b949e;
        margin-bottom: 0.8rem;
        word-break: break-all;
    }
    .card-meta {
        display: flex;
        gap: 15px;
        font-size: 0.8rem;
        color: #8b949e;
        margin-top: 0.8rem;
    }
    .badge {
        background-color: #21262d;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        border: 1px solid #30363d;
        color: #c9d1d9;
    }
    .badge-score {
        background-color: rgba(88, 166, 255, 0.15);
        color: #58a6ff;
        border: 1px solid rgba(88, 166, 255, 0.3);
    }
    .badge-quality {
        background-color: rgba(46, 160, 67, 0.15);
        color: #56d364;
        border: 1px solid rgba(46, 160, 67, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State pipeline
if "pipeline" not in st.session_state:
    st.session_state.pipeline = NexaSearchPipeline()
if "last_stats" not in st.session_state:
    st.session_state.last_stats = None

pipeline = st.session_state.pipeline
db_stats = pipeline.get_stats()

# Sidebar Navigation
st.sidebar.title("🧬 NexaSearch Panel")
st.sidebar.subheader("Vertical Search Engine")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Go To:",
    ["🏠 Home", "🚀 Build Index", "🔎 Search", "📊 Statistics", "⚙️ Settings"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Index Status")
st.sidebar.metric("Documents", db_stats["document_count"])
st.sidebar.metric("Chunks", db_stats["chunk_count"])

# ----------------- HOME PAGE -----------------
if page == "🏠 Home":
    st.title("🏠 NexaSearch vertical search engine")
    st.subheader("A Search Engine engineered for AI, Research Papers, and Library Documentation")
    
    st.markdown("""
    Welcome to **NexaSearch**, an open-source domain-specific search engine designed to crawl, index, and retrieve knowledge domains with maximum efficiency.
    
    ### 🎯 Target Domains
    - **Research Papers**: ArXiv, OpenReview, papers-with-code, ACL.
    - **Code & API Reference**: Python official docs, PyPI libraries, GitHub repositories.
    - **Technical Documentation**: Hugging Face, LangChain, OpenAI, and Anthropic developer guides.
    
    ### 🏗️ Architecture Stages
    1. **Adaptive BFS Crawling**: Uses playright-powered Crawl4AI to fetch pages.
    2. **Noise Cleaning**: Normalizes whitespace, strips headers/footers, and masks sensitive PII.
    3. **Two-Tier Deduplication**: Removes exact duplicates (SHA256) and filters near-duplicates (MinHash LSH).
    4. **Heuristic Quality Filter**: Flags keyword stuffing, toxicity, and keeps only content-rich pages.
    5. **Semantic Chunker**: Splits articles by headings, keeping section contexts intact.
    6. **Hybrid Inverted Index**: Computes keyword BM25 ranks and semantic vector similarities.
    7. **RRF & Cross-Encoder Reranking**: Merges scores and reranks candidates to serve the top-K.
    """)
    
    st.markdown("### 📁 Storage Information")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**DuckDB Database path:**\n`{db_stats['db_path']}`")
    with col2:
        st.info(f"**Index output directory:**\n`{db_stats['index_dir']}`")

# ----------------- BUILD INDEX PAGE -----------------
elif page == "🚀 Build Index":
    st.title("🚀 Build Search Index")
    st.subheader("Add seed URLs to crawl, clean, deduplicate, chunk, and index")
    
    tab1, tab2 = st.tabs(["🔗 Manual URLs", "📄 Sitemap XML"])
    
    with tab1:
        manual_urls_input = st.text_area(
            "Enter URLs to Crawl (one per line):",
            "https://arxiv.org/abs/1706.03762\nhttps://arxiv.org/abs/2005.14165"
        )
    with tab2:
        sitemap_input = st.text_input(
            "Sitemap XML Path / URL:",
            "data/raw/sitemap/master_seed.xml"
        )
        
    st.markdown("### ⚙️ Pipeline Tuning overrides")
    col1, col2, col3 = st.columns(3)
    with col1:
        max_pages = st.number_input("Max Pages", min_value=1, max_value=500, value=10)
    with col2:
        max_depth = st.number_input("Max BFS Depth", min_value=1, max_value=5, value=2)
    with col3:
        quality_thresh = st.slider("Quality Filter Threshold", 0.0, 1.0, 0.5)

    if st.button("Start Crawling & Indexing 🚀"):
        # Compile URLs
        urls = []
        if manual_urls_input:
            urls = [u.strip() for u in manual_urls_input.split("\n") if u.strip()]
        
        # Load from sitemap if manual is empty or user uses sitemap tab
        if not urls and sitemap_input:
            try:
                if sitemap_input.startswith("http"):
                    import requests
                    resp = requests.get(sitemap_input, timeout=10)
                    root = ET.fromstring(resp.content)
                else:
                    import xml.etree.ElementTree as ET
                    tree = ET.parse(sitemap_input)
                    root = tree.getroot()
                
                urls = [loc.text.strip() for loc in root.findall(".//{*}loc") if loc.text]
            except Exception as e:
                st.error(f"Error loading sitemap: {e}")
        
        if not urls:
            st.error("No valid URLs found to crawl. Please input URLs or verify sitemap.")
        else:
            # Configure pipeline overrides
            pipeline.crawler.max_pages = max_pages
            pipeline.crawler.max_depth = max_depth
            pipeline.quality.threshold = quality_thresh

            # Run pipeline
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("1/6: Crawling pages concurrently...")
            progress_bar.progress(15)
            
            # Since pipeline runs async, we wrap in an event loop runner
            import asyncio
            try:
                t0 = time.time()
                stats = asyncio.run(pipeline.run(urls))
                t_total = time.time() - t0
                
                st.session_state.last_stats = stats
                progress_bar.progress(100)
                status_text.text("Pipeline complete!")
                
                st.success(f"Successfully processed and indexed in {t_total:.2f} seconds!")
                
                # Show summary
                st.subheader("📊 Pipeline Stage breakdown:")
                st.json(stats)
                
                # Force refresh sidebar
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred during indexing: {e}")

# ----------------- SEARCH PAGE -----------------
elif page == "🔎 Search":
    st.title("🔎 NexaSearch Engine")
    st.subheader("Retrieve documents using keyword matching, semantic embeddings, and neural rerankers")
    
    query = st.text_input("Enter your query:", "attention mechanism transformer")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        top_k = st.slider("Top K Results", 1, 50, 10)
    with col2:
        use_vector = st.checkbox("Enable Vector Search", value=True)
    with col3:
        use_rerank = st.checkbox("Enable Cross-Encoder Reranking", value=True)

    if query:
        with st.spinner("Searching index..."):
            t0 = time.time()
            results = pipeline.search(
                query, 
                top_k=top_k, 
                use_vector=use_vector, 
                use_rerank=use_rerank
            )
            t_search = time.time() - t0
        
        st.write(f"Found {len(results)} matches in {t_search * 1000:.1f}ms")
        st.markdown("---")
        
        if not results:
            st.warning("No results found. Build the search index first.")
        else:
            for r in results:
                # Render results cards
                st.markdown(f"""
                <div class="card">
                    <div class="card-title">
                        <a href="{r['url']}" target="_blank">{r['title']}</a>
                    </div>
                    <div class="card-url">{r['url']}</div>
                    <div style="font-style: italic; margin-bottom: 0.8rem;">
                        <strong>{r['heading']}</strong> — {r['snippet']}
                    </div>
                    <div class="card-meta">
                        <span class="badge badge-score">Relevance score: {r['score']}</span>
                        <span class="badge badge-quality">Quality score: {r['quality_score']}</span>
                    </div>
                </div>
                """, unsafe_allowed_html=True)

# ----------------- STATISTICS PAGE -----------------
elif page == "📊 Statistics":
    st.title("📊 Pipeline Analytics")
    st.subheader("Understand execution durations, document filtering, and data quality distributions")
    
    # Check if we have run a pipeline recently
    stats = st.session_state.last_stats
    
    if not stats:
        st.info("No run statistics available. Run the pipeline in **Build Index** tab to collect metrics.")
        
        # Load sample values from db if documents exist
        if db_stats["document_count"] > 0:
            st.markdown("### 🗄️ Database Table Counts")
            st.bar_chart(pd.DataFrame({
                "Count": [db_stats["document_count"], db_stats["chunk_count"]]
            }, index=["Documents", "Chunks"]))
    else:
        st.markdown(f"**Last pipeline execution:** `{stats.get('start_time')}`")
        st.markdown(f"**Total Run time:** `{stats.get('total_time_seconds')}s`")
        
        # Plot run times
        st.markdown("### ⏱️ Stage Execution Durations")
        stage_times = {}
        for stage, info in stats.get("stages", {}).items():
            stage_times[stage] = info.get("time_seconds", 0.0)
        
        st.bar_chart(pd.Series(stage_times, name="Seconds"))

        # Document count reduction
        st.markdown("### 📉 Document Count Reduction Through Pipeline")
        crawled = stats.get("stages", {}).get("crawl", {}).get("crawled_count", 0)
        deduped = stats.get("stages", {}).get("deduplicate", {}).get("output_count", 0)
        passed_quality = stats.get("stages", {}).get("quality_filter", {}).get("output_count", 0)
        
        flow_df = pd.DataFrame({
            "Count": [crawled, deduped, passed_quality]
        }, index=["Crawled", "Deduplicated", "High Quality"])
        
        st.line_chart(flow_df)
        
        # Deduplication breakdown
        st.markdown("### 🛡️ Duplicate Removal Stats")
        exact_dupes = stats.get("stages", {}).get("deduplicate", {}).get("exact_duplicates", 0)
        near_dupes = stats.get("stages", {}).get("deduplicate", {}).get("near_duplicates", 0)
        
        st.write(f"- Exact Duplicates Removed: **{exact_dupes}**")
        st.write(f"- Near Duplicates Removed: **{near_dupes}**")

# ----------------- SETTINGS PAGE -----------------
elif page == "⚙️ Settings":
    st.title("⚙️ System Configuration")
    st.subheader("Displays all environment settings parsed from .env")
    
    # Build dictionary of current configs
    config_dict = {
        "PROJECT_NAME": settings.PROJECT_NAME,
        "DEBUG": settings.DEBUG,
        "DUCKDB_PATH": settings.DUCKDB_PATH,
        "INDEX_DIR": settings.INDEX_DIR,
        "CRAWL_MAX_PAGES": settings.CRAWL_MAX_PAGES,
        "CRAWL_MAX_DEPTH": settings.CRAWL_MAX_DEPTH,
        "CRAWL_CONCURRENT": settings.CRAWL_CONCURRENT,
        "CRAWL_TIMEOUT": settings.CRAWL_TIMEOUT,
        "CRAWL_KEYWORDS": settings.CRAWL_KEYWORDS,
        "QUALITY_THRESHOLD": settings.QUALITY_THRESHOLD,
        "MIN_WORD_COUNT": settings.MIN_WORD_COUNT,
        "MAX_WORD_COUNT": settings.MAX_WORD_COUNT,
        "JACCARD_THRESHOLD": settings.JACCARD_THRESHOLD,
        "CHUNK_SIZE": settings.CHUNK_SIZE,
        "CHUNK_OVERLAP": settings.CHUNK_OVERLAP,
        "EMBEDDING_MODEL_NAME": settings.EMBEDDING_MODEL_NAME,
        "CROSS_ENCODER_MODEL_NAME": settings.CROSS_ENCODER_MODEL_NAME,
        "BM25_WEIGHT": settings.BM25_WEIGHT,
        "VECTOR_WEIGHT": settings.VECTOR_WEIGHT,
        "QUALITY_WEIGHT": settings.QUALITY_WEIGHT,
    }
    
    st.json(config_dict)
    st.info("Note: To change these values, edit the `.env` file in the project root and restart the application.")
