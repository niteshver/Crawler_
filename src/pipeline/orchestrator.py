import time
from typing import List, Dict, Any, Optional
from src.config.settings import settings
from src.crawler.logger import logger
from src.crawler.crawler import CrawlerManager
from src.processing.cleaner import TextCleaner
from src.processing.deduplication import DeduplicationPipeline
from src.quality.quality_filter import QualityFilter
from src.chunking.chunker import DocumentChunker
from src.storage.duckdb_store import DuckDBStore
from src.search.engine import SearchEngine

class NexaSearchPipeline:
    def __init__(self):
        self.crawler = CrawlerManager()
        self.cleaner = TextCleaner()
        self.dedup = DeduplicationPipeline()
        self.quality = QualityFilter()
        self.chunker = DocumentChunker()
        self.store = DuckDBStore()
        self.engine = SearchEngine()
        
        self.pipeline_stats: Dict[str, Any] = {}

    async def run(self, urls: List[str]) -> Dict[str, Any]:
        """
        Run the complete crawl-to-index pipeline.
        """
        start_time = time.time()
        logger.info("=" * 60)
        logger.info("Starting NexaSearch Crawl & Index Pipeline")
        logger.info("=" * 60)
        
        self.pipeline_stats = {
            "start_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "stages": {}
        }

        # --- STAGE 1: CRAWLING ---
        t0 = time.time()
        raw_docs = await self.crawler.crawl(urls)
        crawl_time = time.time() - t0
        self.pipeline_stats["stages"]["crawl"] = {
            "time_seconds": round(crawl_time, 2),
            "input_urls": len(urls),
            "crawled_count": len(raw_docs)
        }
        
        if not raw_docs:
            logger.warning("Pipeline aborted: No documents crawled.")
            self.pipeline_stats["status"] = "Aborted (No docs crawled)"
            return self.pipeline_stats

        # --- STAGE 2: CLEANING ---
        t0 = time.time()
        cleaned_docs = []
        for doc in raw_docs:
            text = doc.get("markdown", "")
            url = doc.get("url", "")
            clean_res = self.cleaner.clean(text, url)
            
            cleaned_doc = {
                **doc,
                "text": clean_res["text"],
                "metadata": {
                    **doc.get("metadata", {}),
                    **clean_res["metadata"]
                }
            }
            cleaned_docs.append(cleaned_doc)
            
        clean_time = time.time() - t0
        self.pipeline_stats["stages"]["clean"] = {
            "time_seconds": round(clean_time, 2),
            "processed_count": len(cleaned_docs)
        }

        # --- STAGE 3: DEDUPLICATION ---
        t0 = time.time()
        unique_docs, dedup_stats = self.dedup.deduplicate_batch(cleaned_docs)
        dedup_time = time.time() - t0
        self.pipeline_stats["stages"]["deduplicate"] = {
            "time_seconds": round(dedup_time, 2),
            **dedup_stats
        }

        if not unique_docs:
            logger.warning("Pipeline aborted: All documents were duplicates.")
            self.pipeline_stats["status"] = "Aborted (All duplicates)"
            return self.pipeline_stats

        # --- STAGE 4: QUALITY FILTERING ---
        t0 = time.time()
        filtered_docs, quality_stats = self.quality.filter_documents(unique_docs)
        quality_time = time.time() - t0
        self.pipeline_stats["stages"]["quality_filter"] = {
            "time_seconds": round(quality_time, 2),
            **quality_stats
        }

        if not filtered_docs:
            logger.warning("Pipeline aborted: All documents failed quality filter.")
            self.pipeline_stats["status"] = "Aborted (Failed quality checks)"
            return self.pipeline_stats

        # --- STAGE 5: SAVE DOCUMENTS TO DUCKDB ---
        self.store.save_documents(filtered_docs)

        # --- STAGE 6: CHUNKING ---
        t0 = time.time()
        chunks = self.chunker.chunk_batch(filtered_docs)
        chunk_time = time.time() - t0
        self.pipeline_stats["stages"]["chunking"] = {
            "time_seconds": round(chunk_time, 2),
            "input_docs": len(filtered_docs),
            "generated_chunks": len(chunks)
        }

        # --- STAGE 7: SAVE CHUNKS TO DUCKDB ---
        self.store.save_chunks(chunks)

        # --- STAGE 8: INDEXING ---
        t0 = time.time()
        # Retrieve all chunks from storage to build/update index
        all_stored_chunks = self.store.get_all_chunks()
        self.engine.index(all_stored_chunks)
        index_time = time.time() - t0
        self.pipeline_stats["stages"]["indexing"] = {
            "time_seconds": round(index_time, 2),
            "indexed_chunks": len(all_stored_chunks)
        }

        total_time = time.time() - start_time
        self.pipeline_stats["total_time_seconds"] = round(total_time, 2)
        self.pipeline_stats["status"] = "Success"
        
        logger.info("=" * 60)
        logger.info(f"Pipeline finished successfully in {self.pipeline_stats['total_time_seconds']} seconds.")
        logger.info(f"Indexed {len(filtered_docs)} unique docs into {len(chunks)} chunks.")
        logger.info("=" * 60)

        return self.pipeline_stats

    def search(self, query: str, top_k: int = 10, use_vector: bool = True, use_rerank: bool = True) -> List[Dict[str, Any]]:
        """Query the search engine index."""
        return self.engine.search(query, top_k, use_vector, use_rerank)

    def get_stats(self) -> Dict[str, Any]:
        """Get stats about database and index size."""
        return {
            "document_count": self.store.get_document_count(),
            "chunk_count": self.store.get_chunk_count(),
            "db_path": self.store.db_path,
            "index_dir": str(settings.absolute_index_dir)
        }
