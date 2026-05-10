""" urls for the systems app """
from django.urls import path
from systems import views


urlpatterns = [
    path("", views.index, name='system index'),
    path("view/<int:sysid>", views.view, name='system view'),
]
