from django.shortcuts import render
from config.models import *
from django.db.models.functions import Lower
import re


def index(request):
    """ function to get a list of quantities """
    qnts = Quantities.objects.all().order_by(Lower('name'))
    return render(request, '../templates/quantities/index.html', {'qnts': qnts})
