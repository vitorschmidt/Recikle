from companies.models import Company
from companies.serializers import CompanySerializer
from materials.serializers import MaterialSerializer
from rest_framework import serializers
from rest_framework.exceptions import APIException
from users.serializers import UserSerializer

from info_collects.models import InfoCollect


class UniqueValidationError(APIException):
    status_code = 422


class InfoCollectSerializer(serializers.ModelSerializer):
    # materials = MaterialSerializer(read_only=True)
    # user_id = UserSerializer(read_only=True)
    # company_id = CompanySerializer(read_only=True)

    class Meta:
        model = InfoCollect
        fields = ["id", "cep", "address", "reference_point", "company"]

    def create(self, validated_data):

        user_pop = validated_data.pop("user_id")
        company_pop = validated_data.pop("company")
        company_save = Company.objects.get(id=company_pop.id)

        validated_data["company"] = company_save

        info_collect = InfoCollect.objects.get_or_create(**validated_data)[0]

        info_collect.user_id.add(user_pop)

        return info_collect


class ListInfoCollectSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoCollect
        fields = "__all__"
