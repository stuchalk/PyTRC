""" datasets views file """
from django.shortcuts import render
from trcconfig.models import *
from datasets.functions import *


def view(request, dsid=None):
    """ function to aggregate data about a dataset """
    # get the dataset
    dset = Datasets.objects.get(id=dsid)
    refid = dset.reference_id
    # get the reference data
    ref = References.objects.get(id=refid)
    # get the quantity(s) that was measured
    quants = qlist(dsid)
    # get the related datasets (from the same paper)
    rellst = Datasets.objects.filter(reference_id=refid).exclude(id=dset.id).values('id', 'setnum').order_by('setnum')
    rels = []
    for rel in rellst:
        rels.append({'id': rel['id'], 'title': 'Dataset ' + str(rel['setnum']) + ' in paper ' + ref.doi})
    # get methodology
    method = dset.sampleprops_set.all()[0].method_name
    # get phase(s)
    cphases = dset.conditions_set.values_list('phase__phasetype__name', flat=True).all().distinct()
    dphases = dset.data_set.values_list('phase__phasetype__name', flat=True).all().distinct()
    phases = []
    for ph in cphases:
        if ph not in phases:
            phases.append(ph)
    for ph in dphases:
        if ph not in phases:
            phases.append(ph)
    phases.sort()
    pstr = "' ".join(phases)
    # get substance(s)

    return render(request, '../templates/datasets/view.html', {'ref': ref, 'quants': quants, 'rels': rels,
                                                               'method': method, 'phases': pstr})
