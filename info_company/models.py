import uuid

from django.db import models


class InfoCompany(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    telephone = models.IntegerField()
    email = models.EmailField()
    address = models.CharField(max_length=100)
    company_id = models.ForeignKey('company.Company', on_delete = models.CASCADE, related_name = 'info_collect')
