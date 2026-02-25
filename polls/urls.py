from django.urls import include, path
from . import admin, views

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    path("specifics/<int:question_id>/detail", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]