from dataclasses import dataclass
from typing import Optional
from dataclasses_json import dataclass_json
from app.crawler.models import CrawlJob


@dataclass_json
@dataclass
class SitemapDto:
    urls: set
    foreign_urls: set
    broken_urls: set


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
    def from_model(model: CrawlJob) -> 'CrawlJobDto':
        return CrawlJobDto(
            id=model.id,
            url=model.url,
            created_at=model.created_at.__str__(),
            status=model.status
        )
