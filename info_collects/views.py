from django.shortcuts import get_object_or_404
from materials.mixins import SerializerByMethodMixin
from materials.models import Material
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from users.models import User
from users.permissions import IsOwnerOrAdmin

from info_collects.models import InfoCollect
from info_collects.serializers import (
    InfoCollectMaterialSerializer,
    InfoCollectSerializer,
    ListInfoCollectSerializer,
)


def get_object_by_id(model, **kwargs):
    object = get_object_or_404(model, **kwargs)
    return object


class UserInfoCollectionView(SerializerByMethodMixin, generics.ListCreateAPIView):
    queryset = InfoCollect.objects.all()
    serializer_map = {"GET": ListInfoCollectSerializer, "POST": InfoCollectSerializer}

    lookup_url_kwarg = "id"

    def get_queryset(self):
        user_id = self.kwargs["id"]
        user = get_object_by_id(User, id=user_id)
        info_collect = InfoCollect.objects.filter(user_id=user)

        return info_collect

    def perform_create(self, serializer):
        user_id = self.kwargs["id"]
        user = get_object_by_id(User, id=user_id)

        serializer.save(user_id=user)


class UserInfoCollectionDetailsView(
    SerializerByMethodMixin, generics.RetrieveUpdateDestroyAPIView
):
    queryset = InfoCollect.objects.all()
    serializer_map = {
        "GET": ListInfoCollectSerializer,
        "PATCH": InfoCollectSerializer,
    }

    lookup_url_kwarg = "info_id"

    def get_queryset(self):
        user_id = self.kwargs["id"]
        info_id = self.kwargs["info_id"]
        user = get_object_by_id(User, id=user_id)

        infos = InfoCollect.objects.filter(user_id=user, id=info_id)

        return infos


class MaterialInfoCollectionView(SerializerByMethodMixin, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = InfoCollect.objects.all()
    serializer_map = {
        "GET": ListInfoCollectSerializer,
        "POST": InfoCollectMaterialSerializer,
    }

    def get_queryset(self):
        material_id = self.kwargs["id"]
        material = get_object_by_id(Material, id=material_id)

        info_collect = InfoCollect.objects.filter(materials=material)

        return info_collect

    def perform_create(self, serializer):
        material_id = self.kwargs["id"]
        material = get_object_by_id(Material, id=material_id)

        serializer.save(materials=material)


class MaterialInfoCollectionDetailsView(
    SerializerByMethodMixin, generics.RetrieveUpdateDestroyAPIView
):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]
    queryset = InfoCollect.objects.all()
    serializer_map = {
        "GET": ListInfoCollectSerializer,
        "PATCH": InfoCollectMaterialSerializer,
    }

    lookup_url_kwarg = "info_id"

    def get_queryset(self):
        material_id = self.kwargs["id"]
        info_id = self.kwargs["info_id"]
        material = get_object_by_id(Material, id=material_id)

        infos = InfoCollect.objects.filter(materials=material, id=info_id)

        return infos
