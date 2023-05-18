from django.shortcuts import render, redirect
from trcconfig.models import *


def view(request, dsid=None):
    # get the dataset
    dset = Datasets.objects.get(id=dsid)
    refid = dset.reference_id
    # get the reference data
    ref = References.objects.get(id=refid)

    return render(request, '../templates/datasets/view.html', {'ref': ref})
