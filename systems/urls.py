""" urls for the systems app """
from django.urls import path
from systems import views


urlpatterns = [
    path("", views.index, name='systems index'),
    # path("view/<kwid>", views.view, name='keywords view'),
]
