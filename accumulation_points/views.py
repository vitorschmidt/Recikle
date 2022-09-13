from companies.permissions import IsCompanyOrAdmin
from django.shortcuts import get_object_or_404
from materials.models import Material
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from accumulation_points.mixins import SerializerByMethodMixin
from accumulation_points.models import AccumulationPoint
from accumulation_points.serializers import (
    AccumulationPointSerializer,
    ListAccumulationPointSerializer,
)


def get_object_by_id(model, **kwargs):
    object = get_object_or_404(model, **kwargs)
    return object


class AccumulationPointView(SerializerByMethodMixin, generics.ListCreateAPIView):
    permission_classes = [IsCompanyOrAdmin]

    queryset = AccumulationPoint.objects.all()
    serializer_map = {
        "GET": ListAccumulationPointSerializer,
        "POST": AccumulationPointSerializer,
    }

    lookup_url_kwarg = "id"

    def get_queryset(self):
        material_id = self.kwargs["id"]
        material = get_object_by_id(Material, id=material_id)
        accumulation = AccumulationPoint.objects.filter(materials=material)

        return accumulation

    def perform_create(self, serializer):
        material_id = self.kwargs["id"]
        material = get_object_or_404(Material, id=material_id)

        serializer.save(materials=material)


class AccumulationPointDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCompanyOrAdmin]

    serializer_class = AccumulationPointSerializer
    queryset = AccumulationPoint.objects.all()

    lookup_url_kwarg = "accumulation_point_id"
