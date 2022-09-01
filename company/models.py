import uuid

from django.db import models


class Company(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    collect_days = models.PositiveIntegerField()
    donation = models.BooleanField(default=False)
    materials = models.ManyToManyField("material.Material", related_name="companies")
