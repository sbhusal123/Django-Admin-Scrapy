from __future__ import absolute_import, unicode_literals

from celery import shared_task

import os
from pathlib import Path


@shared_task
def task_scrape_all():
    """Scrape all the quptes"""
    django_path = Path(__file__).resolve().parent.parent
    os.chdir(str(django_path)+"/scraper")
    os.system("scrapy crawl quotes")


@shared_task
def task_scrape_from_author(author_name):
    """Scrape quotes from author"""
    django_path = Path(__file__).resolve().parent.parent
    os.chdir(str(django_path)+"/scraper")
    os.system(
        "scrapy crawl some-quotes -a author='{}'".format(author_name))
