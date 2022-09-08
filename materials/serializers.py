from dataclasses import fields

from companies.models import Company
from rest_framework import serializers

from materials.models import Material


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ["id", "name", "dangerousness", "category", "infos", "decomposition"]


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
