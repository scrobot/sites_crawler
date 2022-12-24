from django.shortcuts import render

from sites_crawler.forms import GrabForm


def home(request):
    context = {}
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GrabForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            context['site_url'] = form.cleaned_data['site_url']

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GrabForm()

    context['form'] = form
    return render(request, 'index.html', context)
