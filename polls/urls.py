from django.urls import include, path
from . import admin, views

urlpatterns = [
    path("", views.index, name="index"),
]