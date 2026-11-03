""" urls for the temp gb app """
from django.urls import path
from gb import views


urlpatterns = [
    path("", views.index, name='gb index'),
]