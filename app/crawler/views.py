from django.shortcuts import render

from app.crawler.forms import GrabForm
from app.crawler.services import CrawlerTaskService


def home(request):
    context = {}
    # if this is a POST request we need to process the form data
    match request.method:
        case "POST":
            # create a form instance and populate it with data from the request:
            form = GrabForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                context['job'] = CrawlerTaskService.create_job(form.cleaned_data['site_url'])
        case "GET":
            form = GrabForm()

    context['form'] = form

    return render(request, 'index.html', context)


def job(request, job_id: str):
    context = {}
    # if this is a POST request we need to process the form data
    match request.method:
        case "GET":
            (job_info, sitemap) = CrawlerTaskService.get_job(job_id)

            if job_info is None:
                return render(request, '404.html', context)

            context['job'] = job_info
            context['sitemap'] = sitemap

    return render(request, 'job.html', context)
