from uuid import UUID

from django.db import models
from django.test import Client, TestCase
from materials.models import Material, Recomendation
from rest_framework import status


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test
        
        
class MaterialModelTestCase(TestCase):
    
    def setUp(self):
        
        self.material_data = {
            "name": "Material",
            "dangerousness": False,
            "category": "Category",
            "infos": "Material info",
            "decomposition": 1
        }
        
        self.material = Material.objects.create(**self.material_data)

    # Material Model Attributes

    def material_model_attributes(self, order):
        
        material_model = {
            "id": {
                "instance": models.IntegerField,
                "parameters": {
                    "primary_key": True
                }
            },
            "name": {
                "instance": models.CharField,
                "parameters": {
                    "max_length": 120
                }
            },
            "dangerousness": {
                "instance": models.BooleanField,
                "parameters": {
                    "default": False
                }
            },
            "category": {
                "instance": models.CharField,
                "parameters": {
                    "max_length": 40,
                    "choices": Recomendation.choices,
                    "default": Recomendation.RECICLAVEL
                }
            },
            "infos": {
                "instance": models.CharField,
                "parameters": {
                    "max_length": 500
                }
            },
            "decomposition": {
                "instance": models.PositiveIntegerField,
                "parameters": {
                }
            },
        }
        
        material = Material.objects.get(name="Material")
        for field in material_model:
            self.assertIsInstance(material._meta.get_field(field), material_model[field]["instance"],
                msg=f"{order}.1) Material's {field} field type error")
            for parameter in material_model[field]["parameters"]:
                self.assertEquals(getattr(material._meta.get_field(field), parameter), material_model[field]["parameters"][parameter],
                    msg=f"{order}.2) User's {field} field {parameter} error")


    def material_field_contents(self, order):
        
        material_1 = {
            "name": "Material 1",
            "dangerousness": False,
            "category": "Category 1",
            "infos": "Material 1 info",
            "decomposition": 1
        }
        
        Material.objects.create(**material_1)
        
        material_2 = {
            "name": "Material 2",
            "dangerousness": False,
            "category": "Category 2",
            "infos": "Material 2 info",
            "decomposition": 2
        }

        Material.objects.create(**material_2)

        instance_1 = Material.objects.get(name=material_1["name"])

        for field in material_1:
            self.assertEquals(getattr(instance_1, field), material_1[field],
                msg=f"{order}.1) Material 1's {field} content error")

        instance_2 = Material.objects.get(name=material_2["name"])

        for field in material_2:
            self.assertEquals(getattr(instance_2, field), material_2[field],
                msg=f"{order}.2) Material 2's {field} content error")

''' 
    def test_A(self):
        """A) Check material model attributes"""
        self.material_model_attributes("A") '''

