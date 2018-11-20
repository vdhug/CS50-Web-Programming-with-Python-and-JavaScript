from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.auth_register, name="register"),
    path("logout", views.auth_logout, name="logout"),
    path("login", views.auth_login, name="login")
]
