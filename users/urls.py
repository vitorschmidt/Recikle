from django.urls import path
from info_collects.views import UserInfoCollectionDetailsView, UserInfoCollectionView
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("user/<user_id>/", views.UpdateUserView.as_view()),
    path("users/", views.ListUsersView.as_view()),
    path("users/<id>/info_collection/", UserInfoCollectionView.as_view()),
    path(
        "users/<id>/info_collection/<info_id>/",
        UserInfoCollectionDetailsView.as_view(),
    ),
    path("users/<id>/schedules/", views.UserSchedulesView.as_view()),
]
