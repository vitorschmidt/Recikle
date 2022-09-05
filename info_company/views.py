
from rest_framework import generics
from info_company.serializers import InfoCompanySerializer
from info_company.models import InfoCompany

class InfoCompanyView(generics.ListCreateAPIView):

    queryset = InfoCompany.objects.all()
    serializer_class = InfoCompanySerializer

class InfoCompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = InfoCompany.objects.all()
    serializer_class = InfoCompanySerializer

