from django.shortcuts import render, redirect
from config.models import *
from django.db.models.functions import Lower


def index(request):
    """ function to get a list of quantities """
    qnts = Quantities.objects.all().order_by(Lower('name'))
    return render(request, '../templates/quantities/index.html', {'qnts': qnts})

def view(request, qntid=None):
    if not qntid:
        return redirect('/quantities')
    qnt = Quantities.objects.get(id=qntid)
    return render(request, '../templates/systems/view.html', {'qnt': qnt})
