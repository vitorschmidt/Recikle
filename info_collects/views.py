from django.shortcuts import get_object_or_404
from materials.mixins import SerializerByMethodMixin
from rest_framework import generics
from users.models import User

from info_collects.models import InfoCollect
from info_collects.serializers import InfoCollectSerializer, ListInfoCollectSerializer


def get_object_by_id(model, **kwargs):
    object = get_object_or_404(model, **kwargs)
    return object


# class InfoCollectView(generics.ListCreateAPIView):

#     queryset = InfoCollect.objects.all()
#     serializer_class = InfoCollectSerializer


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


class UserInfoCollectionDetailsView(generics.RetrieveUpdateDestroyAPIView):
    ...
