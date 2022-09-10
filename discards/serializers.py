from rest_framework import serializers
from rest_framework.exceptions import APIException

from discards.models import Discard


class UniqueValidationError(APIException):
    status_code = 422


class DiscardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discard
        fields = ["id", "address", "city", "quantity"]

    def create(self, validated_data):

        companies_pop = validated_data.pop("companies")

        discard = Discard.objects.get_or_create(**validated_data)[0]

        discard.companies.add(companies_pop)

        return discard


class ListDiscardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discard
        fields = "__all__"
