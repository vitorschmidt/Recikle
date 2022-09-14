from companies.models import Company
from django.db import models
from django.test import TestCase
from info_collects.models import InfoCollect
from users.models import User


class InfoCollectModelTestCase(TestCase):
    
    def setUp(self):
        
        self.superuser = User.objects.create_superuser(**{
                "username": "superuser",
                "first_name": "Super",
                "last_name": "User",
                "city": "Superuser's City",
                "email": "superuser@kenzie.com",
                "is_company": False,
                "password": "SuperUserPassword123@",
        })
        
        self.company = Company.objects.create(**{
            "name": "Company",
            "collect_days": 5,
            "donation": True,
            "owner_id": self.superuser
        })

        self.info_collect_data = {
            "cep": 10000000,
            "address": "Company's Address",
            "reference_point": "Company's Address",
            "company": self.company
        }
        
        self.info_collect = InfoCollect.objects.create(**self.info_collect_data)

    # InfoCollect Model Attributes

    def info_collect_model_attributes(self):
        
        info_collect_model = {
            "id": {
                "instance": models.IntegerField,
                "parameters": {
                    "primary_key": True
                }
            },
            "user_id": {
                "instance": models.ManyToManyField,
                "parameters": {
                }
            },
            "cep": {
                "instance": models.IntegerField,
                "parameters": {
                }
            },
            "address": {
                "instance": models.CharField,
                "parameters": {
                    "max_length": 150
                }
            },
            "reference_point": {
                "instance": models.CharField,
                "parameters": {
                    "max_length": 120
                }
            },
            "materials": {
                "instance": models.ManyToManyField,
                "parameters": {
                }
            },
            "company": {
                "instance": models.ForeignKey,
                "parameters": {
                }
            },
        }
        
        info_collect = InfoCollect.objects.get(id=self.info_collect.id)
        for field in info_collect_model:
            self.assertIsInstance(info_collect._meta.get_field(field), info_collect_model[field]["instance"],
                msg=f"1) InfoCollect's {field} field type error")
            for parameter in info_collect_model[field]["parameters"]:
                self.assertEquals(getattr(info_collect._meta.get_field(field), parameter), info_collect_model[field]["parameters"][parameter],
                    msg=f"2) InfoCollect's {field} field {parameter} error")


    def info_collect_field_contents(self):
        info_collect = InfoCollect.objects.get(id=self.info_collect.id)
        for field in self.info_collect_data:
            self.assertEquals(getattr(info_collect, field), self.info_collect_data[field],
                msg=f"1) InfoCollect's {field} content error")
           

