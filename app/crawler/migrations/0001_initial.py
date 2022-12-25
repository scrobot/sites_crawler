# Generated by Django 4.1.4 on 2022-12-25 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CrawlJob",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.URLField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("process", "In process"),
                            ("complete", "Completed"),
                            ("error", "Error"),
                        ],
                        default="pending",
                        max_length=50,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WebsiteData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("website", models.CharField(max_length=255)),
                ("data", models.JSONField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("session", models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
