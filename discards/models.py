from django.db import models


class Discard(models.Model):
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=120)
    quantity = models.PositiveIntegerField()
    companies = models.ManyToManyField("companies.Company", related_name="discards")
