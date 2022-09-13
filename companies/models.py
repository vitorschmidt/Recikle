from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=120)
    collect_days = models.PositiveIntegerField()
    donation = models.BooleanField(default=False)
    materials = models.ManyToManyField("materials.Material", related_name="companies")
    owner_id = models.ForeignKey(
        "users.User", related_name="company", on_delete=models.CASCADE
    )
