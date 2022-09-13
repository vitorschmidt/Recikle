from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from users.models import User

from companies.models import Company
from companies.permissions import IsCompanyOrAdmin, IsCompanyOwnerOrAdmin
from companies.serializers import CompanySerializer, ListInfoCollectionCompanySerializer


def get_object_by_id(model, **kwargs):
    object = get_object_or_404(model, **kwargs)
    return object


class CompanyView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsCompanyOrAdmin]

    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    def perform_create(self, serializer):
        owner_id = self.request.user.id
        user = get_object_by_id(User, id=owner_id)
        serializer.save(owner_id=user)


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
