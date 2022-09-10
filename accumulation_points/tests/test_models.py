from accumulation_points.models import AccumulationPoint
from django.db import models
from django.test import TestCase


class AccumulationPointModelTestCase(TestCase):
    
    def setUp(self):
        
        self.accumulation_point_data = {
            "address": "Accumulation Point Address",
            #"materials": None,
        }
        
        self.accumulation_point = AccumulationPoint.objects.create(**self.accumulation_point_data)

    # AcuumulationPoint Model Attributes

    def accumulation_point_model_attributes(self):
        
        accumulation_point_model = {
            "id": {
                "instance": models.IntegerField,
                "parameters": {
                    "primary_key": True
                }
            },
            "address": {
                "instance": models.CharField,
                "parameters": {
                    "max_length": 256
                }
            },
            "materials": {
                "instance": models.ManyToManyField,
                "parameters": {
                }
            },
        }
        
        accumulation_point = AccumulationPoint.objects.get(id=self.accumulation_point.id)
        for field in accumulation_point_model:
            self.assertIsInstance(accumulation_point._meta.get_field(field), accumulation_point_model[field]["instance"],
                msg=f"1) AccumulationPoint's {field} field type error")
            for parameter in accumulation_point_model[field]["parameters"]:
                self.assertEquals(getattr(accumulation_point._meta.get_field(field), parameter), accumulation_point_model[field]["parameters"][parameter],
                    msg=f"2) AccumulationPoint's {field} field {parameter} error")


    def accumulation_point_field_contents(self):
        accumulation_point = AccumulationPoint.objects.get(id=self.accumulation_point.id)
        for field in self.accumulation_point_data:
            self.assertEquals(getattr(accumulation_point, field), self.accumulation_point_data[field],
                msg=f"1) AccumulationPoint's {field} content error")
           

