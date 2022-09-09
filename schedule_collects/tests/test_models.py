from datetime import datetime

from django.db import models
from django.test import TestCase
from django.utils.timezone import make_aware
from schedule_collects.models import ScheduleCollect
from users.models import User


class ScheduleCollectModelTestCase(TestCase):
    
    def setUp(self):
        
        self.superuser_data = {
            "username": "superuser",
            "first_name": "Super",
            "last_name": "User",
            "city": "Superuser's City",
            "email": "superuser@kenzie.com",
            "is_company": False,
            "password": "SuperUserPassword123@",
            }
        
        self.user = User.objects.create_superuser(**self.superuser_data)

        self.schedule_collect_data = {
            "days": 5,
            "scheduling": make_aware(datetime.now()),
            "city": "Address",
            "user": self.user
        }
        
        self.schedule_collect = ScheduleCollect.objects.create(**self.schedule_collect_data)

    # ScheduleCollect Model Attributes

    def schedule_collect_model_attributes(self):
        
        schedule_collect_model = {
            "id": {
                "instance": models.IntegerField,
                "parameters": {
                    "primary_key": True
                }
            },
            "days": {
                "instance": models.IntegerField,
                "parameters": {
                }
            },
            "scheduling": {
                "instance": models.DateTimeField,
                "parameters": {
                }
            },
            "materials": {
                "instance": models.ManyToManyField,
                "parameters": {
                }
            },
            "city": {
                "instance": models.CharField,
                "parameters": {
                    "max_length": 128
                }
            },
            "user": {
                "instance": models.ForeignKey,
                "parameters": {
                }
            },
        }
        
        schedule_collect = ScheduleCollect.objects.get(id=self.schedule_collect.id)
        for field in schedule_collect_model:
            self.assertIsInstance(schedule_collect._meta.get_field(field), schedule_collect_model[field]["instance"],
                msg=f"1) ScheduleCollect's {field} field type error")
            for parameter in schedule_collect_model[field]["parameters"]:
                self.assertEquals(getattr(schedule_collect._meta.get_field(field), parameter), schedule_collect_model[field]["parameters"][parameter],
                    msg=f"2) ScheduleCollect's {field} field {parameter} error")


    def schedule_collect_field_contents(self):
        schedule_collect = ScheduleCollect.objects.get(id=self.schedule_collect.id)
        for field in self.schedule_collect_data:
            self.assertEquals(getattr(schedule_collect, field), self.schedule_collect_data[field],
                msg=f"1) ScheduleCollect's {field} content error")
           

