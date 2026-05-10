from django.shortcuts import render, redirect
from config.models import *
from django.db.models.functions import Lower
import re


def index(request):
    """ function to get a list of systems """
    syss = Systems.objects.all().order_by(Lower('name')).values('id', 'name', 'composition')
    sysbychar = {}
    for sys in syss:
        temp = re.sub(r'^[\[(+\-)/]+', '', str(sys['name'].upper()))
        if temp[0] not in sysbychar.keys():
            sysbychar.update({temp[0]: []})
        sysbychar[temp[0]].append(sys)
    syss = dict(sorted(sysbychar.items()))
    return render(request, '../templates/systems/index.html', {'syss': syss})


def view(request, sysid=None):
    if not sysid:
        return redirect('/systems')
    sys = Systems.objects.get(id=sysid)
    return render(request, '../templates/systems/view.html', {'sys': sys})
