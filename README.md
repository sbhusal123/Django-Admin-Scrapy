-   [Celery Task Broker](https://docs.celeryproject.org/en/stable/)
-   [RabbitMQ For Task Queue](https://github.com/sbhusal123/RabbitMQ)

**Spin up RabbitMQ server:** `docker run --name rabbitmq -p 5672:5672 rabbitmq`

**Basic integration steps** explained [here](https://github.com/sbhusal123/django-scrapy-integration)

## Customization with admin Panel

**1. Tasks**

```python
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

```

**2. Views**

```python
from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from djscrapyquotes.tasks import task_scrape_all, task_scrape_from_author


def scrape_all_quotes(request):
    if request.user.is_superuser:
        task_scrape_all.delay()
        messages.add_message(request, messages.INFO,
                             'Started crawling all the quotes')
        return HttpResponseRedirect(reverse("admin:index"))
    else:
        return HttpResponseRedirect("../")


def scrape_quotes_from_author(request):
    if request.user.is_superuser:
        author_name = request.POST.get("athr_name")
        task_scrape_from_author.delay(author_name)
        messages.add_message(
            request, messages.INFO, 'Started crawling quotes from {}'.format(author_name))
        return HttpResponseRedirect(reverse("admin:index"))
    else:
        return HttpResponseRedirect("../")
```

**3. Admin Templates**

```html
{% extends 'admin/change_list.html' %} {% load static %} {% block object-tools%}
<div>
    <form action="{% url 'scrape_quotes_from_author' %}" method="POST">
        {% csrf_token %}
        <input type="text" placeholder="Author name" name="athr_name" />
        <button type="submit" class="button" style="padding: 0.5rem">
            Scrape quotes from author
        </button>
    </form>

    <form action="{% url 'scrape_all_quotes' %}" method="POST">
        {% csrf_token %}
        <button type="submit" class="button" style="padding: 0.5rem">
            Scrape All Quotes
        </button>
    </form>
</div>
<br />
{{ block.super }} {% endblock %}
```

**4. Model Admin**

```python
from django.contrib import admin
from .models import Quotes


@admin.register(Quotes)
class QuotesAdmin(admin.ModelAdmin):
    change_list_template = "change_list.html"
```
