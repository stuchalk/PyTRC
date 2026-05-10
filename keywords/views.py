from django.shortcuts import render
from config.models import *
from django.db.models.functions import Lower
import re


def index(request):
    """ function to get a list of terms """
    terms = Keywords.objects.all().order_by(Lower('term'))
    termsbychar = {}
    for term in terms:
        if not term.chk:
            temp = re.sub(r'^[\[(+\-)/]+', '', str(term.term.upper()))
            if temp[0] not in termsbychar.keys():
                termsbychar.update({temp[0]: []})
            termsbychar[temp[0]].append(term)
    terms = dict(sorted(termsbychar.items()))
    return render(request, '../templates/keywords/index.html', {'terms': terms})

"""
def view(request, refid=None):
    if not refid:
        return redirect('/references')
    ref = References.objects.get(id=refid)
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
    return render(request, '../templates/references/view.html', {'ref': ref, 'sets': sets})mplates/keywords/index.html', {})
    """