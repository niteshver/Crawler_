from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    ####################
    # Project
    ####################

    PROJECT_NAME: str = "NexaCrawler"

    DEBUG: bool = True

    ####################
    # Paths
    ####################

    BASE_DIR: Path = Path(__file__).resolve().parents[1]

    DATA_DIR: Path = BASE_DIR / "data"

    RAW_HTML_DIR: Path = DATA_DIR / "raw_html"

    MARKDOWN_DIR: Path = DATA_DIR / "markdown"

    JSON_DIR: Path = DATA_DIR / "json"

    LOG_DIR: Path = DATA_DIR / "logs"

    ####################
    # Crawling
    ####################

    MAX_DEPTH: int = 2

    MAX_PAGES: int = 500

    CONCURRENT_REQUESTS: int = 10

    MAX_RETRIES: int = 3

    REQUEST_TIMEOUT: int = 30

    USER_AGENT: str = (
        "NexaCrawler/1.0 (+https://github.com/your-repo)"
    )

    ####################
    # Browser
    ####################

    HEADLESS: bool = True

    WAIT_UNTIL: str = "load"

    ####################
    # Markdown
    ####################

    PRUNING_THRESHOLD: float = 0.6

    WORD_COUNT_THRESHOLD: int = 10

    ####################
    # Logging
    ####################

    LOG_LEVEL: str = "INFO"

    ####################
    # Environment
    ####################

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()