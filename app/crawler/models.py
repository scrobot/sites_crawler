from django.db import models


class CrawlJob(models.Model):
    PENDING = 'pending'
    PROCESS = 'process'
    COMPLETE = 'complete'
    ERROR = 'error'

    Statuses = (
        (PENDING, 'Pending'),
        (PROCESS, 'In process'),
        (COMPLETE, 'Completed'),
        (ERROR, 'Error'),
    )

    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=Statuses, default='pending', max_length=50)
    session = models.CharField(null=True, blank=True, max_length=100)


# TODO: Create a relation many-to-many between CrawlJob and WebsiteData if needed
class WebsiteData(models.Model):
    url = models.CharField(max_length=255)
    data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
