from material.serializers import ListMaterialSerializer
from rest_framework import serializers
from rest_framework.exceptions import APIException
from users.serializers import UserSerializer
from schedule_collect.models import ScheduleCollect
from users.serializers import UserSerializer


class UniqueValidationError(APIException):
    status_code = 422


class InfoCollectSerializer(serializers.ModelSerializer):
    materials = ListMaterialSerializer(read_only=True)
    user_id = UserSerializer(read_only=True)
    
    class Meta:
        model = ScheduleCollect
        fields = ["id", "days", "material", "city", "user_id"]
        read_only_fields = ["id","user_id","material"]


    def create(self, validated_data):
        info_collect = ScheduleCollect.objects.create(**validated_data)

        return info_collect
