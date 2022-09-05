import uuid
from django.db import models

class Recomendation(models.TextChoices):
    RECICLAVEL = ("Reciclavel",)
    NAORECICLAVEL = ("Não Reciclavel",)
    HOSPITALAR = ("Hospitalar",)
    ORGANICO = ("Orgânico",)
    ELETRONICO =("Eletrônico",)
    AGRICOLA =("Agricola",)
    RADIOTIVO =("Radioativo",)
    INDUSTRIAL = ("Industrial",)

class Material(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True,editable=False)
    name = models.CharField(max_length=120)
    dangerousness = models.BooleanField(default=False)
    category = models.CharField(max_length=40, choices= Recomendation.choices, default=Recomendation.RECICLAVEL)
    infos = models.CharField(max_length=500)
    decomposition = models.PositiveIntegerField()