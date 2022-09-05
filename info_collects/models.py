
from django.db import models


class InfoCollect(models.Model):
    user_id = models.ManyToManyField("users.User", related_name="info_collect")
    localization = models.CharField(max_length=128)
    materials = models.ManyToManyField("materials.Material", related_name="info_collects")
    company = models.ForeignKey('companies.Company', on_delete = models.CASCADE, related_name = 'info_collect')
