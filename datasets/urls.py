""" urls for the datasets app """
from django.urls import path
from datasets import views


urlpatterns = [
    path("", views.index, name='dataset index'),
    path("view/<int:dsid>", views.view, name='dataset view'),
    path("scidata/<int:dsid>", views.scidata, name='SciData JSON-LD'),
]
