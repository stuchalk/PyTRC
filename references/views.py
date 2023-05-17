from django.shortcuts import render
from trcconfig.models import *


def index(request):
    """ function to get a list of references """
    refs = References.objects.values('id', 'title', 'year').all().order_by('title', '-year')
    refsbyyear = {}
    for ref in refs:
        if ref.year not in refsbyyear.keys():
            refsbyyear.update({ref.year: []})
        refsbyyear[ref.year].append({'id': ref.id, 'title': ref.title})

    temp = """
    {
        "2019": [
            {
                "id": ??,
                "title": 'title?'
            },
            { another reference...}
        ],
        "2018": []
    }
    """
    render(request, '../templates/references/index.html', {'refs': refsbyyear})
