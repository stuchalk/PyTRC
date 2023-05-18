from django.shortcuts import render
from trcconfig.models import *
from datasets.functions import *


def view(request, dsid=None):
    # get the dataset
    dset = Datasets.objects.get(id=dsid)
    refid = dset.reference_id
    # get the reference data
    ref = References.objects.get(id=refid)
    # get the quantity that was measured
    quants = qlist(dsid)

    return render(request, '../templates/datasets/view.html', {'ref': ref, 'quants': quants})
