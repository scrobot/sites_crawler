from typing import Optional

from app.crawler.dtos import CrawlJobDto
from app.crawler.models import CrawlJob


class CrawlerService:

    @staticmethod
    def create_job(url: str, session: Optional[str] = None) -> CrawlJobDto:
        # create a new job in the database
        job = CrawlJob.objects.create(url=url, session=session)
        # return the job as a dto
        return CrawlJobDto.from_model(job)
