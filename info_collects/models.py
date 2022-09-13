from django.db import models

class InfoCollect(models.Model):
    user_id = models.ManyToManyField("users.User", related_name="info_collect")
    cep = models.IntegerField()
    address = models.CharField(max_length=150)
    reference_point = models.CharField(max_length=120)
    materials = models.ManyToManyField("materials.Material", related_name="info_collects")
    company = models.ForeignKey('companies.Company', on_delete = models.CASCADE, related_name = 'info_collect')
