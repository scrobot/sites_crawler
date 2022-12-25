from typing import Optional
from django_cron import CronJobBase, Schedule
from app.crawler.dtos import CrawlJobDto
from app.crawler.models import CrawlJob


class CrawlerTaskService:

    @staticmethod
    def create_job(url: str, session: Optional[str] = None) -> CrawlJobDto:
        # create a new job in the database
        job = CrawlJob.objects.create(url=url, session=session)
        # return the job as a dto
        return CrawlJobDto.from_model(job)


class CrawlerJobService(CronJobBase):
    RUN_EVERY_MINS = 1  # every 1 minute

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'  # a unique code

    def do(self):
        print("I'm a test cron job!")
        pass  # do your thing here
