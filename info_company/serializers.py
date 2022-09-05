from rest_framework import serializers
from rest_framework.exceptions import APIException
from company.serializers import CompanySerializer
from info_company.models import InfoCompany



class UniqueValidationError(APIException):
    status_code = 422


class InfoCompanySerializer(serializers.ModelSerializer):
    company_id = CompanySerializer(read_only=True)
    class Meta:
        model = InfoCompany
        fields = ["id", "telephone", "email", "address", "company_id"]
        read_only_fields = ["id","company_id"]


    def create(self, validated_data):
        info_company = InfoCompany.objects.create(**validated_data)

        return info_company

