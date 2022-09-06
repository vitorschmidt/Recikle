from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("user/<user_id>/", views.UpdateUserView.as_view()),
    path("users/", views.ListUsersView.as_view()),
]
