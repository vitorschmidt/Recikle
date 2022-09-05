from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path("register/", views.RegisterView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("user/<int:user_id>/", views.UpdateUserView.as_view()),
]
