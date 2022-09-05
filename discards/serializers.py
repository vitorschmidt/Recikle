from company.models import Company
from company.serializers import CompanySerializer
from rest_framework import serializers
from rest_framework.exceptions import APIException

from discards.models import Discard


class UniqueValidationError(APIException):
    status_code = 422


class DiscardSerializer(serializers.ModelSerializer):
    # companies = CompanySerializer(read_only=True)

    class Meta:
        model = Discard
        fields = ["id", "address", "city", "quantity", "companies"]
        read_only_fields = ["id", "companies"]

    def validate_address(self, value: str):
        if Discard.objects.filter(address=value).exists():
            raise UniqueValidationError("address already registered")

        return value

    def create(self, validated_data):

        companies_pop = validated_data.pop("companies")

        discard = Discard.objects.create(**validated_data)
        company_id = companies_pop
        # import ipdb

        # ipdb.set_trace()
        teste = Company.objects.filter(id=company_id)
       
        discard.companies.add(teste)

        return discard
