from django.urls import path
from rest_framework.authtoken import views as auth_view

from . import views

urlpatterns = [
    path("account/", views.UserView.as_view()),
    path("token-auth/", auth_view.obtain_auth_token),
]
