import random
from datetime import datetime
from uuid import UUID

from accumulation_points.models import AccumulationPoint
from companies.models import Company
from discards.models import Discard
from django.db import models
from django.test import Client, TestCase
from django.utils.timezone import make_aware
from info_collects.models import InfoCollect
from info_companies.models import InfoCompany
from materials.models import Material, Recomendation
from rest_framework import status
from schedule_collects.models import ScheduleCollect
from users.models import User


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test

class MaterialViewTestCase(TestCase):
    
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


        self.random_usercompany = []
        self.random_company = []
        self.random_discard = []
        self.random_material = []
        self.random_infocompany = []
        self.random_infocollect = []
        self.random_accumulationpoint = []
        self.random_schedulecollect = []

        for i in range(1,11):
            self.random_usercompany.append(User.objects.create_user(**{
                "username": f"usercompany{i}",
                "first_name": f"Company {i}",
                "last_name": "Kenzie",
                "city": f"Company {i}'s City",
                "email": f"usercompany{i}@kenzie.com",
                "is_company": True,
                "password": f"UserCompany{i}Password123@",
            }))
            self.random_company.append(Company.objects.create(**{
                "name": f"Random Company {i}",
                "collect_days": i,
                "donation": (i % 2 == 0),
                "owner_id": self.random_usercompany[i-1]
            }))
            self.random_discard.append(Discard.objects.create(**{
                "address": f"Random Company {i} Discard's Address",
                "city": f"Random Company {i} Discard's City",
                "quantity": i,
            }))
            self.random_discard[i-1].companies.sets = self.random_company[i-1]
            self.random_material.append(Material.objects.create(**{
                "name": f"Random Company {i} Material",
                "decomposition": 2,
                "dangerousness": False,
                "category": Recomendation.RECICLAVEL,
                "infos": f"Random Company {i} Material's info",
            }))
            self.random_company[i-1].materials.sets = self.random_material[i-1]
            self.random_infocompany.append(InfoCompany.objects.create(**{
                "telephone": 12345678+i,
                "email": f"randomcompany{i}@email.com",
                "address": f"Random Company {i} InfoCompany's Address",
                "company": self.random_company[i-1]
            }))
            self.random_infocollect.append(InfoCollect.objects.create(**{
                "cep": 10000000+i,
                "address": f"Random Company {i} InfoCollect's Address",
                "reference_point": f"Random Company {i} InfoCollect's Reference Point",
                "company": self.random_company[i-1]
            }))
            self.random_infocollect[i-1].materials.sets = self.random_material[i-1]
            self.random_infocollect[i-1].user_id.sets = self.random_usercompany[i-1]
            self.random_accumulationpoint.append(AccumulationPoint.objects.create(**{
                "address": f"Random Company {i} Accumulation Point's Address"
            }))
            self.random_accumulationpoint[i-1].materials.sets = self.random_material[i-1]
            self.random_schedulecollect.append(ScheduleCollect.objects.create(**{
                "days": 3,
                "scheduling": make_aware(datetime.now()),
                "city": f"Random Company {i} Schedule Collect's City",
                "user": self.random_usercompany[i-1]
            }))
            self.random_schedulecollect[i-1].materials.sets = self.random_material[i-1]
                
            
        self.materials = {
            "reciclável": {
                "name": "Reciclável",
                "dangerousness": False,
                "category": "Reciclavel",
                "infos": "Material info",
                "decomposition": 1
            },
            "não reciclável": {
                "name": "Não Reciclável",
                "dangerousness": False,
                "category": "Não Reciclavel",
                "infos": "Material info",
                "decomposition": 1
            },
            "hospitalar": {
                "name": "Hospitalar",
                "dangerousness": True,
                "category": "Hospitalar",
                "infos": "Material info",
                "decomposition": 1
            },
            "orgânico": {
                "name": "Orgânico",
                "dangerousness": False,
                "category": "Orgânico",
                "infos": "Material info",
                "decomposition": 1
            },
            "eletrônico": {
                "name": "Eletrônico",
                "dangerousness": True,
                "category": "Eletrônico",
                "infos": "Material info",
                "decomposition": 1
            },
            "agrícola": {
                "name": "Agrícola",
                "dangerousness": True,
                "category": "Agricola",
                "infos": "Material info",
                "decomposition": 1
            },
            "radioativo": {
                "name": "Radioativo",
                "dangerousness": True,
                "category": "Radioativo",
                "infos": "Material info",
                "decomposition": 1
            },
            "industrial": {
                "name": "Industrial",
                "dangerousness": True,
                "category": "Industrial",
                "infos": "Material info",
                "decomposition": 1
            }
        }

    # PATH /api/materials/

    def superuser_get_materials(self):

        route = "/api/materials/"
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


    def person_get_materials(self):

        route = "/api/materials/"
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
            msg=f"1) GET {route} error (superuser credentials): {content}")
        self.assertIsInstance(content["results"], list,
            msg=f"2) GET {route} error (superuser credentials); response is not list: {content}")


    def superuser_post_material(self):
        
        route = "/api/materials/"
        valid_status_code = status.HTTP_201_CREATED
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']
        
        body = {
            "name": "POST Random Material",
            "dangerousness": False,
            "category": Recomendation.NAORECICLAVEL,
            "infos": "POST Random Material's info",
            "decomposition": 88
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
        for key in ["id", "name", "dangerousness", "category", "infos", "decomposition"]:
            self.assertTrue(key in content, 
                msg=f"2) POST {route} error (superuser credentials): Key '{key}' not in response; {content}")   
                

# PATH /api/materials/<int:id>/

    def superuser_get_materials_id(self):
        
        route = f"/api/materials/{self.random_material[random.randint(0, 9)].id}/"
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
        for key in ["id", "name", "dangerousness", "category", "infos", "decomposition"]:
            self.assertTrue(key in content, 
                msg=f"2) POST {route} error (superuser credentials): Key '{key}' not in response; {content}")   


    def superuser_patch_material_id(self):

        random_id = random.randint(0, 9)
        route = f"/api/materials/{self.random_material[random_id].id}/"
        valid_status_code = status.HTTP_200_OK
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']
        
        body = {
            "name": "PATCH Random Material",
            "dangerousness": True,
            "category": Recomendation.NAORECICLAVEL,
            "infos": "PATCH Random Material's info",
            "decomposition": 88
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
        for key in ["id", "name", "dangerousness", "category", "infos", "decomposition"]:
            self.assertTrue(key in content, 
                msg=f"2) PATCH {route} error (superuser credentials): Key '{key}' not in response; {content}")   
        for key in ["name", "dangerousness", "category", "infos", "decomposition"]:
            self.assertEquals(self.random_material[random_id].key, content[key], 
                msg=f"3) PATCH {route} error (superuser credentials): '{key}' field doesn't match; {content}")   

                         
# PATH /api/materials/<int:id>/accumulation_point/

    def superuser_get_material_accumulationpoint(self):

        random_id = random.randint(0, 9)
        route = f"/api/materials/{self.random_material[random_id].id}/accumulation_point/"

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


    def superuser_post_material_accumulationpoint(self):
        
        random_id = random.randint(0, 9)
        route = f"/api/materials/{self.random_material[random_id].id}/accumulation_point/"
        valid_status_code = status.HTTP_201_CREATED
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']
        
        body = {
            "address": "POST Random Accumulation Point",
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
        for key in ["id", "address"]:
            self.assertTrue(key in content, 
                msg=f"2) POST {route} error (superuser credentials): Key '{key}' not in response; {content}")   
                

# PATH /api/materials/<int:id>/accumulation_point/<int:accumulation_point_id>/

    def superuser_get_material_accumulationpoint_id(self):

        random_id = random.randint(0, 9)
        route = f"/api/materials/{self.random_material[random_id].id}/accumulation_point/{self.random_accumulationpoint[random_id].id}/"

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
        for key in ["id", "address"]:
            self.assertTrue(key in content, 
                msg=f"2) GET {route} error (superuser credentials): Key '{key}' not in response; {content}")   


    def superuser_patch_material_accumulationpoint_id(self):

        random_id = random.randint(0, 9)
        route = f"/api/materials/{self.random_material[random_id].id}/accumulation_point/{self.random_accumulationpoint[random_id].id}/"

        valid_status_code = status.HTTP_200_OK

        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']

        body = {
            "address": "PATCH Random Accumulation Point",
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
        for key in ["id", "address"]:
            self.assertTrue(key in content, 
                msg=f"2) PATCH {route} error (superuser credentials): Key '{key}' not in response; {content}")   
        for key in ["address"]:
            self.assertEquals(getattr(self.random_material[random_id], key), content[key], 
                msg=f"3) PATCH {route} error (superuser credentials): '{key}' field doesn't match; {content}")   


# PATH /api/materials/<int:id>/info_collection/


    def superuser_get_material_infocollection(self):

        random_id = random.randint(0, 9)
        route = f"/api/materials/{self.random_material[random_id].id}/info_collection/"

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


    def superuser_post_material_infocollection(self):
        
        random_id = random.randint(0, 9)
        route = f"/api/materials/{self.random_material[random_id].id}/info_collection/"
        valid_status_code = status.HTTP_201_CREATED
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']
        
        body = {
            "cep": 99999999,
            "address": f"Random InfoCollect's Address",
            "reference_point": f"Random InfoCollect's Reference Point",        }
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
        for key in ["id", "cep", "address", "reference_point"]:
            self.assertTrue(key in content, 
                msg=f"2) POST {route} error (superuser credentials): Key '{key}' not in response; {content}")   
                

# PATH /api/materials/<int:id>/info_collection/<int:info_id>/

    def superuser_get_material_infocollection_id(self):

        random_id = random.randint(0, 9)
        route = f"/api/materials/{self.random_material[random_id].id}/info_collection/{self.random_infocollect[random_id].id}/"

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
        for key in ["id", "address"]:
            self.assertTrue(key in content, 
                msg=f"2) GET {route} error (superuser credentials): Key '{key}' not in response; {content}")   


    def superuser_patch_material_infocollection_id(self):

        random_id = random.randint(0, 9)
        route = f"/api/materials/{self.random_material[random_id].id}/info_collection/{self.random_infocollect[random_id].id}/"

        valid_status_code = status.HTTP_200_OK

        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']

        body = {
            "cep": 88888888,
            "address": f"PATCH Random InfoCollect's Address",
            "reference_point": f"PATCH Random InfoCollect's Reference Point",
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
        for key in ["id", "address"]:
            self.assertTrue(key in content, 
                msg=f"2) PATCH {route} error (superuser credentials): Key '{key}' not in response; {content}")   
        for key in ["cep", "address", "reference_point"]:
            self.assertEquals(self.random_infocollect[random_id].key, content[key], 
                msg=f"3) PATCH {route} error (superuser credentials): '{key}' field doesn't match; {content}")   






    def material_register(self, order):
        
        route = "/api/materials/"
        valid_status_code = status.HTTP_201_CREATED
        self.client = Client()
        for item in self.materials:
            body = self.materials[item]
            response = self.client.post(
                route,
                body,
                format='json',
                content_type='application/json',
                HTTP_ACCEPT='application/json')
            content = response.json()
            self.assertEquals(response.status_code, valid_status_code,
                msg=f"{order}.1) Material creation error: {content}")

    def duplicate_material_register(self, order):
        
        route = "/api/materials/"
        body = self.materials["reciclável"]
        response_1 = self.client.post(
            route,
            body,
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json')
        content_1 = response_1.json()
        response_2 = self.client.post(
            route,
            body,
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json')
        content_2 = response_2.json()
        self.assertEquals(response_1.status_code, status.HTTP_201_CREATED,
            msg=f"{order}.1) Material creation error (first instance): {content_1}")
        self.assertEquals(response_2.status_code, status.HTTP_401_UNAUTHORIZED,
            msg=f"{order}.2) Duplicate material creation error: {content_2}")

    # GET /api/materials/

    def material_list(self, order):
        
        route = "/api/materials/"
        response = self.client.get(
            route,
            HTTP_ACCEPT='application/json')
        content = response.json()
        self.assertEquals(response.status_code, status.HTTP_200_OK,
            msg=f"{order}.1) Material list error: {content}")







