from django.shortcuts import render
from config.models import *
from django.db.models.functions import Lower


def index(request):
    """ function to get a list of systems """
    syss = Systems.objects.values('name', 'id').all().order_by(Lower('name'))
    sysbychar = {}
    for sys in syss:
        if str(sys['name']).upper()[0] not in sysbychar.keys():
            sysbychar.update({str(sys['name']).upper()[0]: {}})
        if str(sys['name']) not in sysbychar[str(sys['name']).upper()[0]].keys():
            sysbychar[str(sys['name']).upper()[0]].update({str(sys['name']): []})
        sysbychar[str(sys['name']).upper()[0]][str(sys['name'])].append(sys['id'])
    return render(request, '../templates/systems/index.html', {'syss': sysbychar, 'app': 'Systems'})

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