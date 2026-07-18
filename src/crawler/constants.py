from enum import Enum


class CrawlStatus(str, Enum):

    PENDING = "pending"

    RUNNING = "running"

    SUCCESS = "success"

    FAILED = "failed"

    SKIPPED = "skipped"


class StorageType(str, Enum):

    RAW_HTML = "raw_html"

    MARKDOWN = "markdown"

    JSON = "json"