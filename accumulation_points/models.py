from django.db import models


class AccumulationPoint(models.Model):
    address = models.CharField(max_length=150)
    materials = models.ManyToManyField(
        "materials.Material", related_name="accumulation_points"
    )
