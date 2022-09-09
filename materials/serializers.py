from rest_framework import serializers
from rest_framework.exceptions import APIException

from materials.models import Material


class UniqueValidationError(APIException):
    status_code = 422


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ["id", "name", "dangerousness", "category", "infos", "decomposition"]

    def validate_name(self, value: str):
        if Material.objects.filter(name=value).exists():
            raise UniqueValidationError("material name already registered")

        return value


class MaterialCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = [
            "id",
            "name",
            "dangerousness",
            "category",
            "infos",
            "decomposition",
            "companies",
        ]
        read_only_fields = ["companies"]

    def create(self, validated_data):
        companies_pop = validated_data.pop("companies")

        material = Material.objects.get_or_create(**validated_data)[0]

        material.companies.add(companies_pop)

        return material


class RelationMaterialCompany(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = [
            "id",
            "name",
            "dangerousness",
            "category",
            "infos",
            "decomposition",
            "companies",
        ]
        read_only_fields = [
            "id",
            "dangerousness",
            "category",
            "infos",
            "decomposition",
            "companies",
        ]

    def create(self, validated_data):
        companies_pop = validated_data.pop("companies")

        material = Material.objects.get_or_create(**validated_data)[0]

        material.companies.add(companies_pop)

        return material
