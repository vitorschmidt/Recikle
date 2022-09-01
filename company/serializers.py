from material.serializers import CreateMaterialSerializer
from rest_framework import serializers
from rest_framework.exceptions import APIException

from company.models import Company


class UniqueValidationError(APIException):
    status_code = 422


class CompanySerializer(serializers.ModelSerializer):


    class Meta:
        model = Company
        fields = ["id", "name", "collect_days", "donation", "materials"]
        read_only_fields = ["id", "materials"]

    def validate_name(self, value: str):
        if Company.objects.filter(name=value).exists():
            raise UniqueValidationError("name already registered")

        return value

    def create(self, validated_data):
        company = Company.objects.create(**validated_data)

        return company
