""" urls for the datasets app """
from django.urls import path
from datasets import views


urlpatterns = [
    path("view/<refid>", views.view, name='ref view'),
]
