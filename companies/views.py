from rest_framework import generics

from companies.models import Company
from companies.serializers import CompanySerializer


class CompanyView(generics.ListCreateAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class CompanyDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    lookup_url_kwarg = "id"
