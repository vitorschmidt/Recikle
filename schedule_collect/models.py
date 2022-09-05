import uuid

from django.db import models


class ScheduleCollect(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    days = models.IntegerField()
    material = models.ManyToManyField("material.Material", related_name="info_collect")
    city = models.CharField(max_length=128)
    user_id = models.ForeignKey('users.User', on_delete = models.CASCADE, related_name = 'info_collect')