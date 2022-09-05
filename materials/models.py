import uuid
from django.db import models

class Material(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True,editable=False)
    name = models.CharField(max_length=120)
    dangerousness = models.BooleanField(default=False)
    category = models.CharField(max_length=120)
    infos = models.CharField(max_length=500)
    decomposition = models.PositiveIntegerField()