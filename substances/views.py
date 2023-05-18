from django.shortcuts import render, redirect
from trcconfig.models import *


def index(request):
    """ function to get a list of references """
    refs = References.objects.values('id', 'title', 'year').all().order_by('-year', 'title')
    refsbyyear = {}
    for ref in refs:
        if ref['year'] not in refsbyyear.keys():
            refsbyyear.update({ref['year']: []})
        refsbyyear[ref['year']].append({'id': ref['id'], 'title': ref['title']})
    return render(request, '../templates/references/index.html', {'refs': refsbyyear})


def view(request, refid=None):

    return render(request, '../templates/references/view.html', {})
