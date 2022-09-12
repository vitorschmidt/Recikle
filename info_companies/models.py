from django.db import models

class InfoCompany(models.Model):
    telephone = models.IntegerField()
    email = models.EmailField()
    address = models.CharField(max_length=150)
    company = models.ForeignKey('companies.Company', on_delete = models.CASCADE, related_name = 'info_company')
