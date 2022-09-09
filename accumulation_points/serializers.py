from rest_framework import serializers
from rest_framework.exceptions import APIException

from accumulation_points.models import AccumulationPoint


class UniqueValidationError(APIException):
    status_code = 422


class AccumulationPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccumulationPoint
        fields = ["id", "address"]

    def create(self, validated_data):
        material_pop = validated_data.pop("materials")
        accumulation_point= AccumulationPoint.objects.get_or_create(**validated_data)[0]
        accumulation_point.materials.add(material_pop)

        return accumulation_point

class ListAccumulationPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccumulationPoint
        fields = "__all__"
