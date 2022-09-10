from rest_framework import serializers
from rest_framework.exceptions import APIException

from users.models import User


class UniqueValidationError(APIException):
    status_code = 422


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "city",
            "last_name",
            "is_company",
            "date_joined",
            "is_active",
        ]
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
        fields = "__all__"
        read_only_fields = [
            "id",
            "password",
            "username",
            "first_name",
            "last_name",
            "is_company",
        ]


class UserScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "password",
            "username",
            "first_name",
            "last_name",
            "is_company",
            "schedule_collect",
        ]
