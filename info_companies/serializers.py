from dataclasses import fields

from companies.models import Company
from rest_framework import serializers
from rest_framework.exceptions import APIException

from info_companies.models import InfoCompany


class InfoCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoCompany
        fields = ["id", "telephone", "email", "address", "company"]

    def create(self, validated_data):
        company_pop = validated_data.pop("company")
        company_save = Company.objects.get(id=company_pop.id)

        validated_data["company"] = company_save

        info_company = InfoCompany.objects.create(**validated_data)

        return info_company


class InfoCompanyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoCompany
        fields = ["id", "telephone", "email", "address"]
