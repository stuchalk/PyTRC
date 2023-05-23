from django.shortcuts import render
from trcconfig.models import *


def index(request):
    """ function to get a list of substances """
    subs = Substances.objects.values('name').all().order_by('name')
    subsbychar = {}
    for sub in subs:
        if str(sub['name']).upper()[0] not in subsbychar.keys():
            subsbychar.update({str(sub['name']).upper()[0]: []})
        subsbychar[str(sub['name']).upper()[0]].append(sub['name'])
    return render(request, '../templates/substances/index.html', {'subs': subsbychar})


"""
def view(request, refid=None):

    return render(request, '../templates/references/view.html', {})
"""
