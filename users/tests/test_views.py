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

class UserViewTestCase(TestCase):
    
    def setUp(self):
        
        self.profiles ={
            "Superuser": {
                "username": "superuser",
                "first_name": "Super",
                "last_name": "User",
                "city": "Superuser's City",
                "email": "superuser@kenzie.com",
                "is_company": False,
                "password": "SuperUserPassword123@",
            },
            "Person": {
                "username": "person",
                "first_name": "Person",
                "last_name": "Kenzie",
                "city": "Person's City",
                "email": "person@kenzie.com",
                "is_company": False,
                "password": "PersonPassword123@",
            },
            "Company": {
                "username": "company",
                "first_name": "Company",
                "last_name": "Kenzie",
                "city": "Company's City",
                "email": "company@kenzie.com",
                "is_company": True,
                "password": "CompanyPassword123@",
            }
        }
        self.superuser = User.objects.create_superuser(**self.profiles["Superuser"])
        self.person = User.objects.create_user(**self.profiles["Person"])
        self.company = User.objects.create_user(**self.profiles["Company"])

    # User Login

    def test_user_login(self):
        """Check user login and response tokens"""
        
        route = "/api/login/"
        valid_status_code = status.HTTP_200_OK
        
        for profile in self.profiles:
            body = {"username": self.profiles[profile]["username"], "password": self.profiles[profile]["password"]}
            response = self.client.post(route, body, format='json', HTTP_ACCEPT='application/json')
            content = response.json()
            self.assertEquals(response.status_code, valid_status_code,
                msg=f"User View - POST {route}: {profile} login error {content}")
            for key in ["refresh", "access"]:
                    self.assertTrue(key in content, 
                    msg=f"User View - POST {route}: Key '{key}' not in {profile} response: {content}")   
                
