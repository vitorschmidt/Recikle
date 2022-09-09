from dataclasses import field
# from materials.serializers import ListMaterialSerializer
from rest_framework import serializers
from rest_framework.exceptions import APIException
from users.serializers import UserSerializer
from schedule_collects.models import ScheduleCollect
from users.serializers import UserSerializer
from materials.models import Material
from users.models import User


class UniqueValidationError(APIException):
    status_code = 422


class ScheduleSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)

    class Meta:
        model = ScheduleCollect
        fields = ["id", "days", "city","scheduling","user"]
        read_only_fields = ["id"]


    def create(self, validated_data):
        user_pop = validated_data.pop("user")
        material_pop = validated_data.pop("materials")
        schedule = ScheduleCollect.objects.get_or_create(**validated_data)[0]
        schedule.materials.add(material_pop)
        return schedule

class ListScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleCollect
        fields = "__all__"
