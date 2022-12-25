import json
from typing import Optional
from bs4 import BeautifulSoup
from django.db import transaction
from django_cron import CronJobBase, Schedule
from app.crawler.dtos import CrawlJobDto, SitemapDto
from app.crawler.models import CrawlJob, WebsiteData

import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque


class CrawlerTaskService:

    @staticmethod
    def create_job(url: str, session: Optional[str] = None) -> CrawlJobDto:
        # create a new job in the database
        job = CrawlJob.objects.create(url=url, session=session)
        # return the job as a dto
        return CrawlJobDto.from_model(job)

    @staticmethod
    def get_job(job_id):
        try:
            # get the job from the database
            job = CrawlJob.objects.get(id=job_id)
            job_dto = CrawlJobDto.from_model(job)
            # get the sitemap from the database
            website = WebsiteData.objects.get(url=job.url)
            sitemap = json.loads(website.data)

            return job_dto, sitemap
        except CrawlJob.DoesNotExist:
            return None, None
        except WebsiteData.DoesNotExist:
            return job_dto, None

    def handle_chunk_jobs(self):
        # TODO: check, maybe the best way will be to wrap handling in `select_for_update()`
        # get all jobs that are not complete
        jobs = CrawlJob.objects.filter(status__in=[CrawlJob.PENDING, CrawlJob.PROCESS])[0:10]
        # iterate over all jobs
        for job in jobs:
            try:
                # if the job is pending, start processing it
                if job.status == CrawlJob.PENDING:
                    self.update_job(job, status=CrawlJob.PROCESS)
                # if the job is in process, continue processing it
                if job.status == CrawlJob.PROCESS:
                    with transaction.atomic():
                        scrapped_data = WebsiteScrapper(job.url).get_all_website_links()
                        self.update_job(job, status=CrawlJob.COMPLETE)
                        self.save_website_links(job.url, scrapped_data)
            except Exception as e:
                print(e)
                self.update_job(job, status=CrawlJob.ERROR)

    @staticmethod
    def update_job(job: CrawlJob, status: str):
        job.status = status
        job.save()

    @staticmethod
    def save_website_links(url: str, sitemap: SitemapDto):
        query = WebsiteData.objects.filter(url=url)
        if query.exists():
            query.update(data=sitemap.to_json())
        else:
            WebsiteData.objects.create(
                url=url,
                data=sitemap.to_json()
            )


class WebsiteScrapper:
    url: str

    def __init__(self, url: str):
        self.url = url

    # TODO: make scrapper asynchronous for better performance
    # TODO: refactor this method to separate methods for better readability
    def get_all_website_links(self) -> SitemapDto:
        # a queue of urls to be crawled
        urls = deque([self.url])

        # a set of urls that we have already been processed
        processed_urls = set()
        # a set of domains inside the target website
        local_urls = set()
        # a set of domains outside the target website
        foreign_urls = set()
        # a set of broken urls
        broken_urls = set()

        # process urls one by one until we exhaust the queue
        while len(urls):
            # move next url from the queue to the set of processed urls
            url = urls.popleft()
            processed_urls.add(url)
            # get url's content
            print("Processing %s" % url)
            try:
                response = requests.get(url)
            except (requests.exceptions.MissingSchema,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.InvalidURL,
                    requests.exceptions.InvalidSchema):
                # add broken urls to its own set, then continue
                broken_urls.add(url)
                continue

            # extract base url to resolve relative links
            parts = urlsplit(url)
            base = "{0.netloc}".format(parts)
            strip_base = base.replace("www.", "")
            base_url = "{0.scheme}://{0.netloc}".format(parts)
            path = url[:url.rfind('/') + 1] if '/' in parts.path else url

            # create a beutiful soup for the html document
            soup = BeautifulSoup(response.text, "lxml")

            for link in soup.find_all('a'):
                # extract link url from the anchor
                anchor = link.attrs["href"] if "href" in link.attrs else ''

                if anchor.startswith('/'):
                    local_link = base_url + anchor
                    local_urls.add(local_link)
                elif strip_base in anchor:
                    local_urls.add(anchor)
                elif not anchor.startswith('http'):
                    local_link = path + anchor
                    local_urls.add(local_link)
                else:
                    foreign_urls.add(anchor)

                [urls.append(i) for i in local_urls if not i in urls and not i in processed_urls]

        return SitemapDto(urls=processed_urls, foreign_urls=foreign_urls, broken_urls=broken_urls)


class CrawlerJobService(CronJobBase):
    RUN_EVERY_MINS = 1  # every 1 minute

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'scrap_url'  # a unique code

    @transaction.non_atomic_requests
    def do(self):
        CrawlerTaskService().handle_chunk_jobs()
