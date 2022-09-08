from rest_framework import serializers
from rest_framework.exceptions import APIException
from users.serializers import UserSerializer
from schedule_collects.models import ScheduleCollect
from users.serializers import UserSerializer


class UniqueValidationError(APIException):
    status_code = 422


class ScheduleSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)

    class Meta:
        model = ScheduleCollect
        fields = ["id", "days", "city", "user_id"]
        read_only_fields = ["id"]


    def create(self, validated_data):
        material_pop = validated_data.pop("materials")
        schedule = ScheduleCollect.objects.get_or_create(**validated_data)[0]
        schedule.materials.add(material_pop)
        return schedule

class ListScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleCollect
        fields = "__all__"
