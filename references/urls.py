""" urls for the references app """
from django.urls import path
from references import views


urlpatterns = [
    path("", views.index, name='ref index'),
    path("view/", views.rdr, name='ref view'),
    path("view/<int:refid>", views.view, name='ref view'),
    path("view/<bad>", views.rdr, name='ref view'),
]
