from django.shortcuts import render
from config.models import *
from django.db.models.functions import Lower
import re


def home(request):
    user = False
    setcnt = Datasets.objects.all().count()
    keycnt = Keywords.objects.all().count()
    subcnt = Substances.objects.all().count()
    refcnt = References.objects.all().count()
    syscnt = Systems.objects.all().count()
    return render(request, '../templates/home.html', {'user': user, 'setcnt': setcnt,
                                                      'keycnt': keycnt, 'subcnt': subcnt, 'refcnt': refcnt,
                                                      'syscnt': syscnt})


def index(request):
    """ function to get a list of substances """
    subs = Substances.objects.values('name').all().order_by(Lower('name'))
    subsbychar = {}
    for sub in subs:
        temp = re.sub(r'\[\(', '', str(sub['name']))
        if temp[0] not in subsbychar.keys():
            subsbychar.update({temp[0]: []})
        subsbychar[temp[0]].append(sub['name'])
    return render(request, '../templates/substances/index.html', {'subs': subsbychar})


"""
def view(request, refid=None):

    return render(request, '../templates/references/view.html', {})
"""
