from rest_framework import serializers
from rest_framework.exceptions import APIException
from users.models import User
from users.serializers import UserSerializer

from schedule_collects.models import ScheduleCollect


class UniqueValidationError(APIException):
    status_code = 422


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleCollect
        fields = ["id", "days", "scheduling", "city", "user"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        user_pop = validated_data.pop("user")
        material_pop = validated_data.pop("materials")

        user_save = User.objects.get(id=user_pop.id)

        validated_data["user"] = user_save

        schedule = ScheduleCollect.objects.get_or_create(**validated_data)[0]
        schedule.materials.add(material_pop)
        return schedule


class ListScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleCollect
        fields = "__all__"
