from django.urls import path
from rest_framework.authtoken import views as auth_view

from . import views

urlpatterns = [
    path("users/register/", views.UserRegister.as_view()),
    path("users/", views.UserView.as_view()),
    path("users/<int:user_id>/", views.UserViewUnique.as_view()),
    path("users/login/", auth_view.obtain_auth_token),
]
