from uuid import UUID

from django.db import models
from django.test import Client, TestCase
from rest_framework import status
from users.models import User


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test
        
        
class UserModelTestCase(TestCase):
    
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
        
        self.person_data = {
            "username": "person",
            "first_name": "Person",
            "last_name": "Kenzie",
            "city": "Person's City",
            "email": "person@kenzie.com",
            "is_company": False,
            "password": "PersonPassword123@",
            }
        
        self.company_data = {
            "username": "company",
            "first_name": "Company",
            "last_name": "Kenzie",
            "city": "Company's City",
            "email": "company@kenzie.com",
            "is_company": True,
            "password": "CompanyPassword123@",
            }
        
        self.superuser = User.objects.create_superuser(**self.superuser_data)
        self.person = User.objects.create_user(**self.person_data)
        self.company = User.objects.create_user(**self.company_data)

    # User Model Attributes

    def user_model_attributes(self, order):
        
        user_model = {
            "id": {
                "instance": models.UUIDField,
                "parameters": {
                    "primary_key": True
                }
            },
            "username": {
                "instance": models.CharField,
                "parameters": {
                    "max_length": 200
                }
            },
            "first_name": {
                "instance": models.CharField,
                "parameters": {
                    "max_length": 50
                }
            },
            "last_name": {
                "instance": models.CharField,
                "parameters": {
                    "max_length": 50
                }
            },
            "city": {
                "instance": models.CharField,
                "parameters": {
                    "max_length": 120
                }
            },
            "email": {
                "instance": models.EmailField,
                "parameters": {
                    "max_length": 150
                }
            },
            "is_company": {
                "instance": models.BooleanField,
                "parameters": {
                    "default": False
                }
            },
            "date_joined": {
                "instance": models.DateTimeField,
                "parameters": {
                }
            },
        }
        
        user = User.objects.get(username="superuser")
        for field in user_model:
            self.assertIsInstance(user._meta.get_field(field), user_model[field]["instance"],
                msg=f"{order}.1) User's {field} field type error")
            for parameter in user_model[field]["parameters"]:
                self.assertEquals(getattr(user._meta.get_field(field), parameter), user_model[field]["parameters"][parameter],
                    msg=f"{order}.2) User's {field} field {parameter} error")
                
    # User Levels and UUID
    
    def user_type(self, order):
        
        user_levels = {
            "superuser": {
                "is_superuser": True,
                "is_company": False
            },
            "person": {
                "is_superuser": False,
                "is_company": False
            },
            "company": {
                "is_superuser": False,
                "is_company": True
            }
        }
            
        for level in user_levels:
            user = User.objects.get(username=level)
            self.assertTrue(getattr(user, "id"),
                msg=f"{order}.1) Invalid {level}.id (UUID)")
            for attribute in user_levels[level]:
                self.assertEqual(getattr(user, attribute), user_levels[level][attribute],
                    msg=f"{order}.2) '{level}.{attribute}' must be {user_levels[level][attribute]}")
''' 
    def test_A(self):
        """A) Check user model attributes"""
        self.user_model_attributes("A")

    def test_B(self):
        """B) Check user type"""
        self.user_type("B")
 '''
