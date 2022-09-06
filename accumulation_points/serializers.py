from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from rest_framework.exceptions import APIException

from accumulation_points.models import AccumulationPoint


class UniqueValidationError(APIException):
    status_code = 422


class AccumulationPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccumulationPoint
        fields = ["id", "address", "materials"]

    def validate_address(self, value: str):
        if AccumulationPoint.objects.filter(address=value).exists():
            raise UniqueValidationError("address already registered")

        return value

    def get(self, validated_data):
        material_pop = validated_data.pop("materials")
        accumulation_point = AccumulationPoint.objects.create(**validated_data)
        accumulation_point.materials.add(material_pop)

        return accumulation_point

class ListAccumulationPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccumulationPoint
        fields = "__all__"
