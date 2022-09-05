from companies.models import Company
from django.shortcuts import get_object_or_404
from rest_framework import generics

from discards.models import Discard
from discards.serializers import DiscardSerializer


def get_object_by_id(model, **kwargs):
    object = get_object_or_404(model, **kwargs)
    return object


class DiscardCompanyView(generics.ListCreateAPIView):
    queryset = Discard.objects.all()
    serializer_class = DiscardSerializer

    lookup_url_kwarg = "id"

    # def get_queryset(self):
    #     company_id = self.kwargs["id"]
    #     company = get_object_by_id(Company, id=company_id)
    #     discards = Discard.objects.filter(companies=company)

    #     return discards

    def perform_create(self, serializer):
        company_id = self.kwargs["id"]
        company = get_object_or_404(Company, id=company_id)

        # teste = self.request.data
        # # import ipdb

        # # ipdb.set_trace()
        teste = company.id
        serializer.save(companies=teste)


class DiscardDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DiscardSerializer
    queryset = Discard.objects.all()

    lookup_url_kwarg = "discard_id"
