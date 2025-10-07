from django.shortcuts import render
from config.models import *

def index(request):
    """ function to get a list of terms """
    terms = Keywords.objects.values('term', 'id', 'chk').all().order_by('term')
    termsbychar = {}
    for term in terms:
        if term['chk'] is False:
            if str(term['term']).upper()[0] not in termsbychar.keys():
                termsbychar.update({str(term['term']).upper()[0]: {}})
            if str(term['term']) not in termsbychar[str(term['term']).upper()[0]].keys():
                termsbychar[str(term['term']).upper()[0]].update({str(term['term']): []})
            termsbychar[str(term['term']).upper()[0]][str(term['term'])].append(term['id'])
    return render(request, '../templates/keywords/index.html', {'terms': termsbychar})

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