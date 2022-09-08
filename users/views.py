from rest_framework import generics
from users.mixins import SerializerByMethodMixin
from users.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from users.permissions import IsOwnerOrAdmin
from users.serializers import  UpdateUserSerializer, UserSerializer

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

    serializer_map = {
        "GET": UserSerializer
    }
