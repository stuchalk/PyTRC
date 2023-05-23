""" urls for the datasets app """
from django.urls import path
from datasets import views


urlpatterns = [
    path("view/<dsid>", views.view, name='dataset view'),
    path("scidata/<dsid>", views.scidata, name='SciData JSON-LD'),
]
