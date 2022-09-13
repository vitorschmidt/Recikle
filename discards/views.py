from companies.models import Company
from companies.permissions import IsCompanyOwnerOrAdmin
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from discards.mixins import SerializerByMethodMixin
from discards.models import Discard
from discards.serializers import DiscardSerializer, ListDiscardSerializer


def get_object_by_id(model, **kwargs):
    object = get_object_or_404(model, **kwargs)
    return object


class DiscardCompanyView(SerializerByMethodMixin, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsCompanyOwnerOrAdmin]

    queryset = Discard.objects.all()
    serializer_map = {
        "GET": ListDiscardSerializer,
        "POST": DiscardSerializer,
    }

    lookup_url_kwarg = "id"

    def get_queryset(self):

        company_id = self.kwargs["id"]
        company = get_object_by_id(Company, id=company_id)
        discards = Discard.objects.filter(companies=company)

        return discards

    def perform_create(self, serializer):

        company_id = self.kwargs["id"]
        company = get_object_or_404(Company, id=company_id)

        serializer.save(companies=company)


class DiscardDetailsView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated, IsCompanyOwnerOrAdmin]

    serializer_class = ListDiscardSerializer
    queryset = Discard.objects.all()

    lookup_url_kwarg = "discard_id"

    def get_queryset(self):
        company_id = self.kwargs["id"]
        company = get_object_by_id(Company, id=company_id)
        discards = Discard.objects.filter(companies=company)

        return discards


class DiscardsView(generics.ListAPIView):
    serializer_class = ListDiscardSerializer
    queryset = Discard.objects.all()
