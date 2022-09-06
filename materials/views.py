from django.shortcuts import render
from rest_framework import generics

from materials.mixins import SerializerByMethodMixin
from materials.models import Material
from materials.serializers import ListMaterialSerializer,CreateMaterialSerializer

class ListCreateMaterialView(SerializerByMethodMixin,generics.ListCreateAPIView):
    queryset = Material.objects.all()
    serializer_map = {
        "GET": ListMaterialSerializer,
        "POST": CreateMaterialSerializer
    }


class RetrieverUpdateProductView(SerializerByMethodMixin,generics.RetrieveUpdateAPIView):
    queryset = Material.objects.all()
    lookup_url_kwarg = "id"
    serializer_class = ListMaterialSerializer
    serializer_map = {
        "GET": ListMaterialSerializer,
        "PATCH": CreateMaterialSerializer
    }


