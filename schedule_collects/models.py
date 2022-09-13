import uuid

from django.db import models


class ScheduleCollect(models.Model):
    days = models.IntegerField()
    scheduling = models.DateTimeField()
    materials = models.ManyToManyField("materials.Material", related_name="schedule_collects")
    city = models.CharField(max_length=120)
    user = models.ForeignKey('users.User', on_delete = models.CASCADE, related_name ='schedule_collect')