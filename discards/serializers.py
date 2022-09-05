from companies.models import Company
from companies.serializers import CompanySerializer
from rest_framework import serializers
from rest_framework.exceptions import APIException

from discards.models import Discard


class UniqueValidationError(APIException):
    status_code = 422


class DiscardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discard
        fields = ["id", "address", "city", "quantity"]

    def validate_address(self, value: str):
        if Discard.objects.filter(address=value).exists():
            raise UniqueValidationError("address already registered")

        return value

    def create(self, validated_data):

        companies_pop = validated_data.pop("companies")

        discard = Discard.objects.create(**validated_data)

        discard.companies.add(companies_pop)

        return discard


class ListDiscardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discard
        fields = "__all__"
