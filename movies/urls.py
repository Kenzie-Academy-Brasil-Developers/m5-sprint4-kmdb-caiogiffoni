from django.urls import path
from rest_framework.authtoken import views as auth_view

from . import views

urlpatterns = [
    path("movies/", views.MoviesView.as_view(), name="movie-view"),
    path("movies/<int:movie_id>/", views.MoviesDetailView.as_view()),
]
