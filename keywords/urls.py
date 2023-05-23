""" urls for the keywords app """
from django.urls import path
from keywords import views


urlpatterns = [
    path("", views.index, name='keywords index'),
    # path("view/<kwid>", views.view, name='keywords view'),
]
