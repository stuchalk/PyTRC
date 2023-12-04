""" urls for the substances app """
from django.urls import path
from substances import views


urlpatterns = [
    path("", views.home, name='website homepage'),
    path("substances/", views.index, name='substances index'),
    # path("substances/view/<subid>", views.view, name='substance view'),
]
