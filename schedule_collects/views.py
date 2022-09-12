from django.shortcuts import get_object_or_404, render
from materials.models import Material
from rest_framework import generics
from users.permissions import IsOwnerOrAdmin

from schedule_collects.mixins import SerializerByMethodMixin
from schedule_collects.models import ScheduleCollect
from schedule_collects.permissions import IsOwnerUserOrAdmin
from schedule_collects.serializers import ListScheduleSerializer, ScheduleSerializer


def get_object_by_id(model, **kwargs):
    object = get_object_or_404(model, **kwargs)
    return object


class ScheduleView(SerializerByMethodMixin, generics.ListCreateAPIView):
    queryset = ScheduleCollect.objects.all()
    serializer_map = {
        "GET": ListScheduleSerializer,
        "POST": ScheduleSerializer,
    }
    lookup_url_kwarg = "id"

    def get_queryset(self):
        material_id = self.kwargs["id"]
        material = get_object_by_id(Material, id=material_id)
        schedule = ScheduleCollect.objects.filter(materials=material)
        return schedule

    def perform_create(self, serializer):
        material_id = self.kwargs["id"]
        material = get_object_or_404(Material, id=material_id)
        serializer.save(materials=material)


class ScheduleDetailsView(
    SerializerByMethodMixin, generics.RetrieveUpdateDestroyAPIView
):
    permission_classes = [IsOwnerUserOrAdmin]
    queryset = ScheduleCollect.objects.all()
    serializer_map = {
        "GET": ListScheduleSerializer,
        "PATCH": ScheduleSerializer,
    }
    lookup_url_kwarg = "schedule_id"

    def get_queryset(self):
        material_id = self.kwargs["id"]
        schedule_id = self.kwargs["schedule_id"]
        material = get_object_by_id(Material, id=material_id)

        schedule = ScheduleCollect.objects.filter(materials=material, id=schedule_id)

        return schedule


class ListSchedulesView(generics.ListAPIView):
    queryset = ScheduleCollect.objects.all()
    serializer_class = ListScheduleSerializer


class ListSchedulesDetailsView(generics.ListAPIView):
    queryset = ScheduleCollect.objects.all()
    serializer_class = ListScheduleSerializer

    lookup_url_kwarg = "id"

    def get_queryset(self):
        schedule_id = self.kwargs["id"]

        schedule = ScheduleCollect.objects.filter(id=schedule_id)

        return schedule
