from django.shortcuts import get_object_or_404
from rest_framework import generics

from companies.models import Company
from companies.serializers import CompanySerializer, ListInfoCollectionCompanySerializer


def get_object_by_id(model, **kwargs):
    object = get_object_or_404(model, **kwargs)
    return object


class CompanyView(generics.ListCreateAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class CompanyDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    lookup_url_kwarg = "id"


class ListInfoCollectionCompany(generics.ListAPIView):
    serializer_class = ListInfoCollectionCompanySerializer
    queryset = Company.objects.all()

    lookup_url_kwarg = "id"

    def get_queryset(self):
        company_id = self.kwargs["id"]

        company = Company.objects.filter(id=company_id)

        return company
