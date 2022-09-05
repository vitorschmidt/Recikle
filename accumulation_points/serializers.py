from rest_framework import serializers
from rest_framework.exceptions import APIException

from accumulation_points.models import AccumulationPoint


class UniqueValidationError(APIException):
    status_code = 422


class AccumulationPointSerializer(serializers.ModelField):
    class Meta:
        model = AccumulationPoint
        fields = ["id", "address", "materials"]

    def validate_address(self, value: str):
        if AccumulationPoint.objects.filter(address=value).exists():
            raise UniqueValidationError("address already registered")

        return value

    def create(self, validated_data):
        accumulation_point = AccumulationPoint.objects.create(**validated_data)

        return accumulation_point
