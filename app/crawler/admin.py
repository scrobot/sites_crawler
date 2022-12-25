from app.crawler.models import CrawlJob, WebsiteData
from django.contrib import admin


@admin.register(CrawlJob)
class CrawlJobAdmin(admin.ModelAdmin):
    list_display = ['url', 'created_at', 'status', 'session']


@admin.register(WebsiteData)
class CrawlJobAdmin(admin.ModelAdmin):
    list_display = ['url', 'created_at']
