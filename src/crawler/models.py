from datetime import datetime
from typing import Any

from pydantic import BaseModel, HttpUrl


class RawDocument(BaseModel):

    url: HttpUrl

    status_code: int

    html: str

    cleaned_html: str

    markdown: str

    metadata: dict[str, Any]

    internal_links: list[str]

    external_links: list[str]

    images: list[str]

    crawled_at: datetime