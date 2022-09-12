from companies.models import Company
from companies.permissions import IsOnlyCompanyDono
from companies.serializers import InfoCompanyListSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from info_companies.models import InfoCompany
from info_companies.serializers import InfoCompanySerializer


class InfoCompanyView(generics.ListCreateAPIView):
    permission_classes = [IsOnlyCompanyDono]

    queryset = InfoCompany.objects.all()
    serializer_class = InfoCompanySerializer


class InfoCompanyDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InfoCompany.objects.all()
    serializer_class = InfoCompanySerializer

    lookup_url_kwarg = "id"


class CompanyInfosView(generics.ListAPIView):
    serializer_class = InfoCompanyListSerializer
    queryset = Company.objects.all()

    lookup_url_kwarg = "id"

    def get_queryset(self):
        company_id = self.kwargs["id"]

        company = Company.objects.filter(id=company_id)

        return company
