from discards.models import Discard
from django.db import models
from django.test import TestCase


class DiscardModelTestCase(TestCase):
    
    def setUp(self):
        
        self.discard_data = {
            "address": "Discard's Address",
            "city": "Discard's City",
            "quantity": 5,
        }
        
        self.discard = Discard.objects.create(**self.discard_data)

    # Discard Model Attributes

    def discard_model_attributes(self):
        
        discard_model = {
            "id": {
                "instance": models.IntegerField,
                "parameters": {
                    "primary_key": True
                }
            },
            "address": {
                "instance": models.CharField,
                "parameters": {
                    "max_length": 150
                }
            },
            "city": {
                "instance": models.CharField,
                "parameters": {
                    "max_length": 50
                }
            },
            "quantity": {
                "instance": models.PositiveIntegerField,
                "parameters": {
                }
            },
            "companies": {
                "instance": models.ManyToManyField,
                "parameters": {
                }
            },
        }
        
        discard = Discard.objects.get(id=self.discard.id)
        for field in discard_model:
            self.assertIsInstance(discard._meta.get_field(field), discard_model[field]["instance"],
                msg=f"1) Discard's {field} field type error")
            for parameter in discard_model[field]["parameters"]:
                self.assertEquals(getattr(discard._meta.get_field(field), parameter), discard_model[field]["parameters"][parameter],
                    msg=f"2) Discard's {field} field {parameter} error")


    def discard_field_contents(self):
        discard = Discard.objects.get(id=self.discard.id)
        for field in self.discard_data:
            self.assertEquals(getattr(discard, field), self.discard_data[field],
                msg=f"1) Discard's {field} content error")
           

