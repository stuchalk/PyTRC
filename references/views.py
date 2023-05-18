from django.shortcuts import render
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
    ref = References.objects.get(id=refid)
    dsets = ref.datasets_set.all()
    sets = {}
    for dset in dsets:
        s = {}
        s.update({'points': dset.points})
        s.update({'system': dset.system.name})
        sers = dset.dataseries_set.all()
        pntids = []
        for ser in sers:
            pntids.append(ser.datapoints_set.all().id)
        quants = Data.objects.filter(datapoint_id__in=pntids).values_list('quantity__name', flat=True).distinct('quantity__name')
        s.update({'quantities': quants})
    return render(request, '../templates/references/index.html', {'ref': ref, 'sets': sets})
