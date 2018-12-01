from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.auth_register, name="register"),
    path("logout", views.auth_logout, name="logout"),
    path("add_item", views.add_item, name="add_item"),
    path("edit_quantity", views.edit_quantity, name="edit_quantity"),
    path("remove_item", views.remove_item, name="remove_item"),
    path("update_progress", views.update_progress, name="update_progress"),
    path("orders", views.orders, name="orders"),
    path("submit_order", views.submit_order, name="submit_order"),
    path("cart", views.cart, name="cart"),
    path("login", views.auth_login, name="login")
]
