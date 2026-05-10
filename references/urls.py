""" urls for the references app """
from django.urls import path
from references import views


urlpatterns = [
    path("", views.index, name='reference index'),
    path("view/<int:refid>", views.view, name='reference view'),
]
