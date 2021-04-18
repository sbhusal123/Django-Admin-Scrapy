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
