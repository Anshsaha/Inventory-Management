from django.urls import path
from . import views

urlpatterns = [
    path("", views.HealthCheck.as_view(), name="healthcheck"),
    path("register/", views.RegisterUserView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("items/", views.CreateItemView.as_view(), name="create-items"),
    path("items/<str:item_id>/", views.ItemView.as_view(), name="items"),
]
