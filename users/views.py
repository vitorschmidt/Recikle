from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from users.mixins import SerializerByMethodMixin
from users.models import User
from users.permissions import IsOwnerOrAdmin
from users.serializers import (
    UpdateUserSerializer,
    UserScheduleSerializer,
    UserSerializer,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UpdateUserView(SerializerByMethodMixin, generics.RetrieveUpdateAPIView):

    permission_classes = [IsOwnerOrAdmin, IsAuthenticated]

    lookup_url_kwarg = "user_id"

    queryset = User.objects.all()

    serializer_map = {
        "PATCH": UpdateUserSerializer,
        "GET": UserSerializer,
    }


class ListUsersView(SerializerByMethodMixin, generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = User.objects.all()

    serializer_map = {"GET": UserSerializer}


class UserSchedulesView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserScheduleSerializer

    lookup_url_kwarg = "id"
