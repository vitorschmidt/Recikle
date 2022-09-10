import random
from uuid import UUID

from companies.models import Company
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

        self.company_data = {
            "name": "Company",
            "collect_days": 5,
            "donation": True,
        }
        
        self.company = Company.objects.create(**self.company_data)


    # PATH /api/companies/

    def superuser_get_company(self):
        
        route = "/api/companies/"
        valid_status_code = status.HTTP_200_OK
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']

        response = self.client.get(
            route,
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (superuser credentials): {content}")
        self.assertIsInstance(content["results"], list,
            msg=f"2) GET {route} error (superuser credentials); response is not list: {content}")


    def person_get_company(self):
        
        route = "/api/companies/"
        valid_status_code = status.HTTP_200_OK
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Person"]["username"], 'password': self.profiles["Person"]["password"]},
            format='json'
        ).json()['access']

        response = self.client.get(
            route,
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (person credentials): {content}")
        self.assertIsInstance(content["results"], list,
            msg=f"2) GET {route} error (person credentials); response is not list: {content}")


    def company_get_company(self):
        
        route = "/api/companies/"
        valid_status_code = status.HTTP_200_OK
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Company"]["username"], 'password': self.profiles["Company"]["password"]},
            format='json'
        ).json()['access']

        response = self.client.get(
            route,
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (company credentials): {content}")
        self.assertIsInstance(content["results"], list,
            msg=f"2) GET {route} error (company credentials); response is not list: {content}")


    def superuser_post_company(self):
        
        route = "/api/companies/"
        valid_status_code = status.HTTP_201_CREATED
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']
        
        body = {
        "name": "Superuser's Company",
        "collect_days": 5,
        "donation": True,
        "materials": []
        }
        response = self.client.post(
            route,
            body,
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) POST {route} error (superuser credentials): {content}")
        for key in ["id", "name", "collect_days", "donation", "materials"]:
                self.assertTrue(key in content, 
                msg=f"2) POST {route} error (superuser credentials): Key '{key}' not in response; {content}")   
                

    def person_post_company(self):
        
        route = "/api/companies/"
        valid_status_code = status.HTTP_201_CREATED
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Person"]["username"], 'password': self.profiles["Person"]["password"]},
            format='json'
        ).json()['access']
        
        body = {
        "name": "Person's Company",
        "collect_days": 5,
        "donation": True,
        "materials": []
        }
        response = self.client.post(
            route,
            body,
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) POST {route} error (person credentials): {content}")
        for key in ["id", "name", "collect_days", "donation", "materials"]:
                self.assertTrue(key in content, 
                msg=f"2) POST {route} error (person credentials): Key '{key}' not in response; {content}")   
                

    def company_post_company(self):
        
        route = "/api/companies/"
        valid_status_code = status.HTTP_201_CREATED
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Company"]["username"], 'password': self.profiles["Company"]["password"]},
            format='json'
        ).json()['access']
        
        body = {
        "name": "Company's Company",
        "collect_days": 5,
        "donation": True,
        "materials": []
        }
        response = self.client.post(
            route,
            body,
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) POST {route} error (company credentials): {content}")
        for key in ["id", "name", "collect_days", "donation", "materials"]:
                self.assertTrue(key in content, 
                msg=f"2) POST {route} error (company credentials): Key '{key}' not in response; {content}")   


    def superuser_post_duplicate_company(self):
        
        route = "/api/companies/"
        valid_status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']
        
        body = {
        "name": "Company",
        "collect_days": 5,
        "donation": True,
        "materials": []
        }
        response = self.client.post(
            route,
            body,
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) POST {route} duplicate error (superuser credentials): {content}")
        self.assertEquals(content, {'detail': 'name already registered'},
            msg=f"2) POST {route} duplicate error (superuser credentials): {content}")   


    def superuser_post_invalid_company(self):
        
        route = "/api/companies/"
        valid_status_code = status.HTTP_400_BAD_REQUEST
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']
        
        body = {}
        response = self.client.post(
            route,
            body,
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) POST {route} invalid body error (superuser credentials): {content}")
        self.assertEquals(content, {'name': ['This field is required.'], 'collect_days': ['This field is required.']},
            msg=f"2) POST {route} invalid body error (superuser credentials): {content}")   


    # PATH /api/companies/<int:id>/
    
    def superuser_get_company_id(self):
        company = []
        for i in range(1,11):
            company.append(Company.objects.create(
            **{"name": f"Random Company {i}",
               "collect_days": i,
               "donation": (i % 2 == 0),
            }))
            
        valid_status_code = status.HTTP_200_OK
        route = f"/api/companies/{company[random.randint(0, 9)].id}/" 
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']

        response = self.client.get(
            route,
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (superuser credentials): {content}")
        for key in ["id", "name", "collect_days", "donation", "materials"]:
            self.assertTrue(key in content, 
            msg=f"2) GET {route} error (superuser credentials): Key '{key}' not in response; {content}")   
    

    def superuser_patch_company_id(self):
        
        company = []
        for i in range(1,11):
            company.append(Company.objects.create(
            **{"name": f"Random Company {i}",
               "collect_days": i,
               "donation": (i % 2 == 0),
            }))
            
        valid_status_code = status.HTTP_200_OK
        route = f"/api/companies/{company[random.randint(0, 9)].id}/" 
                
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']
        
        body = {
        "name": "Superuser's Company Patch",
        "collect_days": 99,
        "donation": True,
        "materials": []
        }
        response = self.client.patch(
            route,
            body,
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) PATCH {route} error (superuser credentials): {content}")
        for key in ["name", "collect_days", "donation", "materials"]:
            self.assertTrue(key in content, 
            msg=f"2) PATCH {route} error (superuser credentials): Key '{key}' not in response; {content}")   
            self.assertEquals(body[key], content[key], 
            msg=f"2) PATCH {route} error (superuser credentials): content doesn't match; {content}")   
                

    def superuser_patch_duplicate_company_id(self):
        
        company = []
        for i in range(1,11):
            company.append(Company.objects.create(
            **{"name": f"Random Company {i}",
               "collect_days": i,
               "donation": (i % 2 == 0),
            }))
            
        valid_status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        route = f"/api/companies/{company[random.randint(0, 9)].id}/" 
                
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']
        
        body = {
        "name": "Company",
        "collect_days": 99,
        "donation": True,
        "materials": []
        }
        response = self.client.patch(
            route,
            body,
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) POST {route} duplicate error (superuser credentials): {content}")
        self.assertEquals(content, {'detail': 'name already registered'},
            msg=f"2) POST {route} duplicate error (superuser credentials): {content}")   
                

# PATH /api/companies/<int:id>/discards/
# PATH /api/companies/<int:id>/discards/<int:discard_id>/
# PATH /api/companies/<int:id>/materials/
# PATH /api/companies/<int:id>/materials/<int:material_id>/
# PATH /api/companies/<int:id>/info_collection/
# PATH /api/companies/<int:id>/info_company/
