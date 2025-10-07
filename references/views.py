from django.shortcuts import render, redirect
from config.models import *
from datasets.functions import *


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
    # get the data
    try:
        ref = References.objects.get(id=refid)
    except References.DoesNotExist:
        return redirect('/references/')

    dsets = ref.datasets_set.all()
    sets = []
    for dset in dsets:
        s = {}
        s.update({'points': dset.points})
        s.update({'numsers': dset.dataseries_set.all().count()})
        s.update({'system': dset.system.name})
        s.update({'quantities': qlist(dset.id)})
        descstr = str(s['points']) + " datapoints in " + str(s['numsers']) + " series, <b>quantities:</b> "
        descstr += s['quantities'] + ", <b>system:</b> " + s['system']
        sets.append({'id': dset.id, 'desc': descstr})
    return render(request, '../templates/references/view.html', {'ref': ref, 'sets': sets})


def rdr(request, bad=None):
    return redirect('/references/')
