from rest_framework import generics
from info_companies.serializers import InfoCompanySerializer
from info_companies.models import InfoCompany

class InfoCompanyView(generics.ListCreateAPIView):

    queryset = InfoCompany.objects.all()
    serializer_class = InfoCompanySerializer

class InfoCompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = InfoCompany.objects.all()
    serializer_class = InfoCompanySerializer

