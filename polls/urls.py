from django.urls import include, path
from . import admin, views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("all", views.AllView.as_view(), name="all"),
    path("<int:pk>/frequency/", views.FrequencyView.as_view(), name="frequency"),
    path('statistics', views.statistics, name='statistics'),
    path('add/', views.add, name='add'),
    path('confirm_add/', views.confirm_add, name='confirm_add'),
]