from django.shortcuts import render
from rest_framework import generics
from django.shortcuts import get_object_or_404
from schedule_collects.mixins import SerializerByMethodMixin
from schedule_collects.models import ScheduleCollect
from schedule_collects.serializers import ScheduleSerializer,ListScheduleSerializer
from materials.models import Material

def get_object_by_id(model, **kwargs):
    object= get_object_or_404(model,**kwargs)
    return object

class ScheduleView(SerializerByMethodMixin,generics.ListCreateAPIView):
    queryset=ScheduleCollect.objects.all()
    serializer_map = {"GET":ListScheduleSerializer,"POST":ScheduleSerializer}
    lookup_url_kwarg="id"

    def get_queryset(self):
        material_id = self.kwargs["id"]
        material = get_object_by_id(Material, id=material_id)
        schedule = ScheduleCollect.objects.filter(materials=material)
        return schedule

    def perform_create(self, serializer):
        material_id = self.kwargs["id"]
        material=get_object_or_404(Material, id=material_id)
        serializer.save(materials=material)

class ScheduleDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleSerializer
    queryset = ScheduleCollect.objects.all()

    lookup_url_kwarg="schedule_id"