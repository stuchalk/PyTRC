""" urls for the references app """
from django.urls import path
from substances import views


urlpatterns = [
    path("", views.index, name='ref index'),
    path("view/<refid>", views.view, name='ref view'),
]
