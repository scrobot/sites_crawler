from dataclasses import dataclass
from typing import Optional

from app.crawler.models import CrawlJob


@dataclass
class SitemapDto:
    map: dict


@dataclass
class CrawlRequestDto:
    url: str
    session_key: Optional[str]


@dataclass
class CrawlJobDto:
    id: int
    url: str
    created_at: str
    status: str

    @staticmethod
    def from_model(model: CrawlJob):
        return CrawlJobDto(
            id=model.id,
            url=model.url,
            created_at=model.created_at.__str__(),
            status=model.status
        )
