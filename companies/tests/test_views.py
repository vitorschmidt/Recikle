import random
from uuid import UUID

from companies.models import Company
from discards.models import Discard
from django.db import models
from django.test import Client, TestCase
from info_collects.models import InfoCollect
from info_companies.models import InfoCompany
from materials.models import Material, Recomendation
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
        self.random_company = []
        self.random_discard = []
        self.random_material = []
        self.random_infocompany = []
        self.random_infocollect = []

        try:
            for i in range(1,11):
                self.random_company.append(Company.objects.create(**{
                    "name": f"Random Company {i}",
                    "collect_days": i,
                    "donation": (i % 2 == 0),
                }))
                self.random_discard.append(Discard.objects.create(**{
                    "address": f"Random Company {i} Discard's Address",
                    "city": f"Random Company {i} Discard's City",
                    "quantity": i,
                }))
                self.random_discard[i-1].companies.sets = self.random_company[i-1]
                self.random_material.append(Material.objects.create(**{
                    "name": f"Random Company {i} Material",
                    "dangerousness": False,
                    "category": Recomendation.RECICLAVEL,
                    "infos": f"Random Company {i} Material's info",
                    "decomposition": i
                }))
                self.random_company[i-1].materials.sets = self.random_material[i-1]
                self.random_infocompany.append(InfoCompany.objects.create(**{
                    "telephone": 12345678,
                    "email": f"randomcompany{i}@email.com",
                    "address": f"Random Company {i} InfoCompany's Address",
                    "company": self.random_company[i-1]
                }))
                self.random_infocollect.append(InfoCollect.objects.create(**{
                    "cep": 10000000,
                    "address": f"Random Company {i} InfoCollect's Address",
                    "reference_point": f"Random Company {i} InfoCollect's Address",
                    "company": self.random_company[i-1]
                }))
                self.random_infocollect[i-1].materials.sets = self.random_material[i-1]
        except Exception as e:
            print(e)

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
            
        valid_status_code = status.HTTP_200_OK
        route = f"/api/companies/{self.random_company[random.randint(0, 9)].id}/" 
        
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
            
        valid_status_code = status.HTTP_200_OK
        route = f"/api/companies/{self.random_company[random.randint(0, 9)].id}/" 
                
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']
        
        body = {
        "name": "Superuser's Company Patch",
        "collect_days": 99,
        "donation": True,
        #"materials": []
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
        for key in ["name", "collect_days", "donation"]:
            self.assertEquals(body[key], content[key], 
                msg=f"3) PATCH {route} error (superuser credentials): content doesn't match; {content}")   
                

    def superuser_patch_duplicate_company_id(self):
        
        valid_status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        route = f"/api/companies/{self.random_company[random.randint(0, 9)].id}/" 
                
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']
        
        body = {
        "name": self.company.name,
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

    def superuser_get_company_discards(self):
        
        route = f"/api/companies/{self.random_company[random.randint(0, 9)].id}/discards/"
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


    def superuser_post_company_discard(self):
        
        route = f"/api/companies/{self.random_company[random.randint(0, 9)].id}/discards/"
        valid_status_code = status.HTTP_201_CREATED
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']

        body = {
            "address": "Discard's Address",
            "city": "Discard's City",
            "quantity": 5,
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
        for key in ["id", "address", "city", "quantity"]:
                self.assertTrue(key in content, 
                msg=f"2) POST {route} error (superuser credentials): Key '{key}' not in response; {content}")   
         
         
    # PATH /api/companies/<int:id>/discards/<int:discard_id>/

    def superuser_get_company_discard_id(self):

        random_id = random.randint(0, 9)
        route = f"/api/companies/{self.random_company[random_id].id}/discards/{self.random_discard[random_id].id}/"
        valid_status_code = status.HTTP_200_OK
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']

        response = self.client.get(
            route,
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (superuser credentials): {content}")
        for key in ["id", "address", "city", "quantity", "companies"]:
                self.assertTrue(key in content, 
                msg=f"2) GET {route} error (superuser credentials): Key '{key}' not in response; {content}")   
         
         
    def superuser_patch_company_discard_id(self):
        
        random_id = random.randint(0, 9)
        route = f"/api/companies/{self.random_company[random_id].id}/discards/{self.random_discard[random_id].id}/"
        valid_status_code = status.HTTP_200_OK
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']

        body = {
            "address": "PATCH Discard's Address",
            "city": "PATCH Discard's City",
            "quantity": 99,
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
        for key in ["id", "address", "city", "quantity", "companies"]:
            self.assertTrue(key in content, 
                msg=f"2) PATCH {route} error (superuser credentials): Key '{key}' not in response; {content}")   
        for key in ["address", "city", "quantity"]:
            self.assertEquals(body[key], content[key], 
                msg=f"3) PATCH {route} error (superuser credentials): '{key}' field doesn't match; {content}")   
         

# PATH /api/companies/<int:id>/materials/

    def superuser_get_company_materials(self):
        
        route = f"/api/companies/{self.random_company[random.randint(0, 9)].id}/materials/"
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


    def superuser_post_company_material(self):
        
        route = f"/api/companies/{self.random_company[random.randint(0, 9)].id}/materials/"
        valid_status_code = status.HTTP_201_CREATED
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']

        body = {
            "name": "POST Random Company Material",
            "dangerousness": False,
            "category": Recomendation.NAORECICLAVEL,
            "infos": "POST Random Company Material's info",
            "decomposition": 99
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
        for key in ["id", "name", "dangerousness", "category", "infos", "decomposition", "companies"]:
            self.assertTrue(key in content, 
                msg=f"2) POST {route} error (superuser credentials): Key '{key}' not in response; {content}")   
        for key in ["name", "dangerousness", "category", "infos", "decomposition",]:
            self.assertEquals(body[key], content[key], 
                msg=f"3) POST {route} error (superuser credentials): '{key}' field doesn't match; {content}")   


# PATH /api/companies/<int:id>/materials/<int:material_id>/

    def superuser_get_company_material_id(self):
    
        random_id = random.randint(0, 9)
        route = f"/api/companies/{self.random_company[random_id].id}/materials/{self.random_material[random_id].id}/"
        valid_status_code = status.HTTP_200_OK
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']

        response = self.client.get(
            route,
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (superuser credentials): {content}")
        for key in ["id", "name", "dangerousness", "category", "infos", "decomposition", "companies"]:
            self.assertTrue(key in content, 
                msg=f"2) GET {route} error (superuser credentials): Key '{key}' not in response; {content}")   
        for key in ["name", "dangerousness", "category", "infos", "decomposition",]:
            self.assertEquals(self.random_material[random_id].key, content[key], 
                msg=f"3) GET {route} error (superuser credentials): '{key}' field doesn't match; {content}")   


    def superuser_patch_company_material_id(self):

        random_id = random.randint(0, 9)
        route = f"/api/companies/{self.random_company[random_id].id}/materials/{self.random_material[random_id].id}/"
        valid_status_code = status.HTTP_201_CREATED
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']

        body = {
            "name": "PATCH Random Company Material",
            "dangerousness": False,
            "category": Recomendation.NAORECICLAVEL,
            "infos": "PATCH Random Company Material's info",
            "decomposition": 99
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
        for key in ["id", "name", "dangerousness", "category", "infos", "decomposition", "companies"]:
            self.assertTrue(key in content, 
                msg=f"2) PATCH {route} error (superuser credentials): Key '{key}' not in response; {content}")   
        for key in ["name", "dangerousness", "category", "infos", "decomposition",]:
            self.assertEquals(body[key], content[key], 
                msg=f"3) PATCH {route} error (superuser credentials): '{key}' field doesn't match; {content}")   

  
# PATH /api/companies/<int:id>/info_collection/

    def superuser_get_company_infocollection(self):
        
        route = f"/api/companies/{self.random_company[random.randint(0, 9)].id}/info_collection/"
        valid_status_code = status.HTTP_200_OK
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']

        response = self.client.get(
            route,
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (superuser credentials): {content}")
        self.assertIsInstance(content["results"], list,
            msg=f"2) GET {route} error (superuser credentials); response is not list: {content}")


# PATH /api/companies/<int:id>/info_company/

    def superuser_get_company_infocompany(self):
        
        route = f"/api/companies/{self.random_company[random.randint(0, 9)].id}/info_company/"
        valid_status_code = status.HTTP_200_OK
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']

        response = self.client.get(
            route,
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (superuser credentials): {content}")
        self.assertIsInstance(content["results"], list,
            msg=f"2) GET {route} error (superuser credentials); response is not list: {content}")

