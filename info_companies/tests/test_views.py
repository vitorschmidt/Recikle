import random
import string
from uuid import UUID

from companies.models import Company
from django.db import models
from django.test import Client, TestCase
from info_companies.models import InfoCompany
from rest_framework import status
from users.models import User


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test

class InfoCompanyViewTestCase(TestCase):
    
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

        self.info_company_data = {
            "telephone": 12345678,
            "email": "company@email.com",
            "address": "Company's Address",
            "company": self.company
        }
        
        self.info_company = InfoCompany.objects.create(**self.info_company_data)


    # PATH /api/info_company/

    def superuser_get_infocompany(self):
        
        route = "/api/info_company/"
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


    def person_get_infocompany(self):
        
        route = "/api/info_company/"
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


    def company_get_infocompany(self):
        
        route = "/api/info_company/"
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


    def superuser_post_infocompany(self):
        
        route = "/api/info_company/"
        valid_status_code = status.HTTP_201_CREATED
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']
        
        body = {
            "telephone": 12345678,
            "email": "company@email.com",
            "address": "Company's Address",
            "company": self.company.id
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
        for key in ["id", "telephone", "email", "address", "company"]:
            self.assertTrue(key in content, 
                msg=f"2) POST {route} error (superuser credentials): Key '{key}' not in response; {content}")   
        for key in ["telephone", "email", "address", "company"]:
            self.assertEquals(body[key], content[key], 
                msg=f"3) POST {route} error (superuser credentials): content doesn't match; {content}")   


    def person_post_infocompany(self):
        
        route = "/api/info_company/"
        valid_status_code = status.HTTP_201_CREATED
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Person"]["username"], 'password': self.profiles["Person"]["password"]},
            format='json'
        ).json()['access']
        
        body = {
            "telephone": 12345678,
            "email": "company@email.com",
            "address": "Company's Address",
            "company": self.company.id
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
        for key in ["id", "telephone", "email", "address", "company"]:
            self.assertTrue(key in content, 
                msg=f"2) POST {route} error (person credentials): Key '{key}' not in response; {content}")   
        for key in ["telephone", "email", "address", "company"]:
            self.assertEquals(body[key], content[key], 
                msg=f"3) POST {route} error (person credentials): content doesn't match; {content}")   
   

    def company_post_infocompany(self):
        
        route = "/api/info_company/"
        valid_status_code = status.HTTP_201_CREATED
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Company"]["username"], 'password': self.profiles["Company"]["password"]},
            format='json'
        ).json()['access']
        
        body = {
            "telephone": 12345678,
            "email": "company@email.com",
            "address": "Company's Address",
            "company": self.company.id
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
        for key in ["id", "telephone", "email", "address", "company"]:
            self.assertTrue(key in content, 
                msg=f"2) POST {route} error (company credentials): Key '{key}' not in response; {content}")   
        for key in ["telephone", "email", "address", "company"]:
            self.assertEquals(body[key], content[key], 
                msg=f"3) POST {route} error (company credentials): content doesn't match; {content}")   
   
   
    # PATH info_company/<int:id>/

    def superuser_get_infocompany_id(self):
        company = []
        infocompany = []
        for i in range(1,11):
            company.append(Company.objects.create(
            **{"name": f"Random Company {i}",
               "collect_days": i,
               "donation": (i % 2 == 0),
            }))
            infocompany.append(InfoCompany.objects.create(
            **{
                "telephone": 12345678,
                "email": f"company{i}@email.com",
                "address": f"Company{i}'s Address",
                "company": company[i-1]
            }))
        
        valid_status_code = status.HTTP_200_OK
        route = f"/api/info_company/{infocompany[random.randint(0, 9)].id}/" 
        
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
        for key in ["id", "telephone", "email", "address", "company"]:
            self.assertTrue(key in content, 
                msg=f"2) POST {route} error (company credentials): Key '{key}' not in response; {content}")   


    def superuser_patch_infocompany_id(self):
        
        company = []
        infocompany = []
        for i in range(1,11):
            company.append(Company.objects.create(
            **{"name": f"Random Company {i}",
               "collect_days": i,
               "donation": (i % 2 == 0),
            }))
            infocompany.append(InfoCompany.objects.create(
            **{
                "telephone": 12345678,
                "email": f"company{i}@email.com",
                "address": f"Company{i}'s Address",
                "company": company[i-1]
            }))
            
        selection = random.randint(0, 9)    
        valid_status_code = status.HTTP_200_OK
        route = f"/api/info_company/{infocompany[selection].id}/" 
                
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']
        
        body = {
            "telephone": 12345678+random.randint(0, 9),
            "email": f"company{random.randint(100, 200)}@email.com",
            "address": f"{random.randint(500, 800)} Street",
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
        for key in ["id", "telephone", "email", "address", "company"]:
            self.assertTrue(key in content, 
                msg=f"2) PATCH {route} error (superuser credentials): Key '{key}' not in response; {content}")   
        for key in ["telephone", "email", "address"]:
            self.assertEquals(body[key], content[key], 
                msg=f"3) PATCH {route} error (superuser credentials): content doesn't match; {content}")   
                

    def superuser_patch_invalid_body_infocompany_id(self):
        
        company = []
        infocompany = []
        for i in range(1,11):
            company.append(Company.objects.create(
            **{"name": f"Random Company {i}",
               "collect_days": i,
               "donation": (i % 2 == 0),
            }))
            infocompany.append(InfoCompany.objects.create(
            **{
                "telephone": 12345678,
                "email": f"company{i}@email.com",
                "address": f"Company{i}'s Address",
                "company": company[i-1]
            }))
            
        selection = random.randint(0, 9)    
        valid_status_code = status.HTTP_400_BAD_REQUEST
        route = f"/api/info_company/{infocompany[selection].id}/" 
                
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']
        
        body = {
            "telephone": 12345678+random.randint(0, 9),
            "email": f"company{random.randint(100, 200)}@email.com",
            "address": ''.join(random.choices(string.ascii_uppercase +string.digits, k=150)),
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
            msg=f"1) PATCH {route} invalid body error (superuser credentials): {content}")
                



