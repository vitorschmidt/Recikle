from django.db import models


class AccumulationPoint(models.Model):
    address = models.CharField(max_length=256)
    materials = models.ManyToManyField(
        "material.Material", related_name="accumulation_points"
    )
