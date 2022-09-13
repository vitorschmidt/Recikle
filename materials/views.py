from companies.models import Company
from companies.permissions import IsCompanyOwnerOrAdmin
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from materials.mixins import SerializerByMethodMixin
from materials.models import Material
from materials.permissions import IsOnlyAdmin
from materials.serializers import (
    MaterialCompanySerializer,
    MaterialSerializer,
    RelationMaterialCompany,
)


def get_object_by_id(model, **kwargs):
    object = get_object_or_404(model, **kwargs)
    return object


class ListCreateMaterialView(generics.ListCreateAPIView):
    permission_classes = [IsOnlyAdmin]
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class RetrieverUpdateProductView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOnlyAdmin]

    queryset = Material.objects.all()
    lookup_url_kwarg = "id"
    serializer_class = MaterialSerializer


class CompanyMaterialsView(SerializerByMethodMixin, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsCompanyOwnerOrAdmin]

    queryset = Material.objects.all()
    lookup_url_kwarg = "id"
    serializer_map = {
        "GET": MaterialCompanySerializer,
        "POST": RelationMaterialCompany,
    }

    def get_queryset(self):
        company_id = self.kwargs["id"]
        company = get_object_by_id(Company, id=company_id)
        materials = Material.objects.filter(companies=company)

        return materials

    def perform_create(self, serializer):

        company_id = self.kwargs["id"]

        company = get_object_or_404(Company, id=company_id)

        serializer.save(companies=company)


class CompanyMaterialsDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsCompanyOwnerOrAdmin]

    serializer_class = MaterialCompanySerializer
    queryset = Material.objects.all()

    lookup_url_kwarg = "material_id"

    def get_queryset(self):
        company_id = self.kwargs["id"]
        company = get_object_by_id(Company, id=company_id)
        materials = Material.objects.filter(companies=company)

        return materials
