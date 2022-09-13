from companies.models import Company
from django.db import models
from django.test import TestCase


class CompanyModelTestCase(TestCase):
    
    def setUp(self):
        
        self.company_data = {
            "name": "Company",
            "collect_days": 5,
            "donation": True,
        }
        
        self.company = Company.objects.create(**self.company_data)

    # Company Model Attributes

    def company_model_attributes(self):
        
        company_model = {
            "id": {
                "instance": models.IntegerField,
                "parameters": {
                    "primary_key": True
                }
            },
            "name": {
                "instance": models.CharField,
                "parameters": {
                    "max_length": 50
                }
            },
            "collect_days": {
                "instance": models.PositiveIntegerField,
                "parameters": {
                }
            },
            "donation": {
                "instance": models.BooleanField,
                "parameters": {
                    "default": False
                }
            },
            "materials": {
                "instance": models.ManyToManyField,
                "parameters": {
                }
            },
            
        }
        
        company = Company.objects.get(name="Company")
        for field in company_model:
            self.assertIsInstance(company._meta.get_field(field), company_model[field]["instance"],
                msg=f"1) Company's {field} field type error")
            for parameter in company_model[field]["parameters"]:
                self.assertEquals(getattr(company._meta.get_field(field), parameter), company_model[field]["parameters"][parameter],
                    msg=f"2) Company's {field} field {parameter} error")

    def company_field_contents(self):
        company = Company.objects.get(name="Company")
        for field in self.company_data:
            self.assertEquals(getattr(company, field), self.company_data[field],
                msg=f"2) Company's {field} content error")
           

