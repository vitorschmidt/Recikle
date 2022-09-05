from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User

class UniqueValidationError(APIException):
    status_code = 422


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "city","last_name", "is_company", "date_joined"]
        read_only_fields = ["id"]

    def validate_username(self, value: int):
        if User.objects.filter(username=value).exists():
            raise UniqueValidationError("username already registered")

        return value

    def validate_email(self, value: int):
        if User.objects.filter(email=value).exists():
            raise UniqueValidationError("email already registered")

        return value

    def create(self, validated_data):
        account = User.objects.create_user(**validated_data)

        return account    

class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "city"]
        read_only_fields = ["id", "password", "username", "first_name", "last_name", "is_company"]       