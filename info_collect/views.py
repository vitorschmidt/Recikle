from django.shortcuts import render

from rest_framework import generics
from info_collect.serializers import InfoCollectSerializer
from info_collect.models import InfoCollect

class InfoCollectView(generics.ListCreateAPIView):

    queryset = InfoCollect.objects.all()
    serializer_class = InfoCollectSerializer
