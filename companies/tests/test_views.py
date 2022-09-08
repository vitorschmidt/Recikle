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

class CompanyViewTestCase(TestCase):
    
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

    # PATH /api/companies/

    def post_company(self, order):
        
        route = "/api/companies/"
        valid_status_code = status.HTTP_201_CREATED
        
        for profile in self.profiles:
            body = {
            "name": f"{profile}'s Company",
            "collect_days": 5,
            "donation": True,
            "materials": []
            }
            response = self.client.post(route, body, format='json', HTTP_ACCEPT='application/json')
            content = response.json()
            self.assertEquals(response.status_code, valid_status_code,
                msg=f"{order}.1) POST {route}: {profile} credentials error {content}")
            for key in ["id", "name", "collect_days", "donation", "materials"]:
                    self.assertTrue(key in content, 
                    msg=f"{order}.2) POST {route}: Key '{key}' not in response ({profile} credentials): {content}")   
                
    
    
    def get_company(self, order):
        
        route = "/api/companies/"
        valid_status_code = status.HTTP_200_OK
        
        for profile in self.profiles:
            body = {
            "name": f"{profile}'s Company",
            "collect_days": 5,
            "donation": True,
            "materials": []
            }
            self.client.post(route, body, format='json', HTTP_ACCEPT='application/json')
            response = self.client.get(route, HTTP_ACCEPT='application/json')
            content = response.json()
            self.assertEquals(response.status_code, valid_status_code,
                msg=f"{order}.1) GET {route}: {profile} credentials error {content}")
            self.assertIsInstance(content["results"], list,
                msg=f"{order}.2) GET {route}: {profile} credentials error; response is not list: {content}")
                
    
    def get_company_id(self, order):
            
        valid_status_code = status.HTTP_200_OK
        route = "/api/companies/"
        
        for profile in self.profiles:
            body = {
            "name": f"{profile}'s Company",
            "collect_days": 5,
            "donation": True,
            "materials": []
            }
            id = self.client.post(route, body, format='json', HTTP_ACCEPT='application/json').json().id
            response = self.client.get(route + id, HTTP_ACCEPT='application/json')
            content = response.json()
            self.assertEquals(response.status_code, valid_status_code,
                msg=f"{order}.1) GET {route+id}: {profile} credentials error {content}")
            self.assertIsInstance(content, list,
                msg=f"{order}.2) GET {route+id}: {profile} credentials error; response is not list: {content}")
            for key in ["id", "name", "collect_days", "donation", "materials"]:
                    self.assertTrue(key in content[0], 
                    msg=f"{order}.3) GET {route+id}: Key '{key}' not in response ({profile} credentials): {content}")   
                
    