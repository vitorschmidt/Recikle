from companies.models import Company
from django.db import models
from django.test import TestCase
from info_companies.models import InfoCompany


class InfoCompanyModelTestCase(TestCase):
    
    def setUp(self):
        
        self.company_data = {
            "name": "Company",
            "collect_days": 5,
            "donation": True,
        }
        
        self.company = Company.objects.create(**self.company_data)

        self.info_company_data = {
            "telephone": 12345678,
            "email": "company@email.com",
            "address": "Company's Address",
            "company": self.company
        }
        
        self.info_company = InfoCompany.objects.create(**self.info_company_data)

    # InfoCompany Model Attributes

    def info_company_model_attributes(self):
        
        info_company_model = {
            "id": {
                "instance": models.IntegerField,
                "parameters": {
                    "primary_key": True
                }
            },
            "telephone": {
                "instance": models.IntegerField,
                "parameters": {
                }
            },
            "email": {
                "instance": models.EmailField,
                "parameters": {
                }
            },
            "address": {
                "instance": models.CharField,
                "parameters": {
                    "max_length": 100
                }
            },
            "company": {
                "instance": models.ForeignKey,
                "parameters": {
                }
            },
        }
        
        info_company = InfoCompany.objects.get(id=self.info_company.id)
        for field in info_company_model:
            self.assertIsInstance(info_company._meta.get_field(field), info_company_model[field]["instance"],
                msg=f"1) InfoCompany's {field} field type error")
            for parameter in info_company_model[field]["parameters"]:
                self.assertEquals(getattr(info_company._meta.get_field(field), parameter), info_company_model[field]["parameters"][parameter],
                    msg=f"2) InfoCompany's {field} field {parameter} error")


    def info_company_field_contents(self):
        info_company = InfoCompany.objects.get(id=self.info_company.id)
        for field in self.info_company_data:
            self.assertEquals(getattr(info_company, field), self.info_company_data[field],
                msg=f"1) InfoCompany's {field} content error")
           

