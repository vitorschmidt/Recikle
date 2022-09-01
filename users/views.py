from rest_framework import generics
from users.models import User
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import  UserSerializer

class RegisterView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
