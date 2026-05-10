""" urls for the substances app """
from django.urls import path
from quantities import views


urlpatterns = [
    path("", views.index, name='quantities index'),
    # path("substances/view/<subid>", views.view, name='substance view'),
]
