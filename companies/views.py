from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from companies.models import Company
from companies.permissions import IsCompanyOrAdmin, IsCompanyOwnerOrAdmin
from companies.serializers import CompanySerializer, ListInfoCollectionCompanySerializer


def get_object_by_id(model, **kwargs):
    object = get_object_or_404(model, **kwargs)
    return object


class CompanyView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsCompanyOrAdmin]

    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class CompanyDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsCompanyOwnerOrAdmin]

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
