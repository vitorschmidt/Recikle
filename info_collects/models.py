
import uuid

from django.db import models


class InfoCollect(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user_id = models.ManyToManyField("users.User", related_name="info_collect")
    localization = models.CharField(max_length=128)
    materials = models.ManyToManyField("materials.Material", related_name="info_collects")
    company_id = models.ForeignKey('companies.Company', on_delete = models.CASCADE, related_name = 'info_collect')
