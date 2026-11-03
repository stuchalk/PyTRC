""" temp gb file """
import json
import os
from django.shortcuts import render
from django.conf import settings


def index(request):
    # Open the file and load the data
    file_path = os.path.join(settings.BASE_DIR, 'gb', 'gbterms.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    terms = data['terms']['list']
    return render(request, '../templates/gb/index.html', {'terms': terms})
