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

        # self.company_data = {
        #     "name": "Company",
        #     "collect_days": 5,
        #     "donation": True,
        # }
        
        # self.company = Company.objects.create(**self.company_data)

        self.superuser_company = Company.objects.create(**{
            "name": "Superuser Company's Name",
            "collect_days": 5,
            "donation": True,
            "owner_id": self.superuser
        })
        self.superuser_discard = Discard.objects.create(**{
            "address": "Superuser Discard's Address",
            "city": "Superuser Discard's City",
            "quantity": 4,
        })
        self.superuser_discard.companies.sets = self.superuser_company
        self.superuser_material = Material.objects.create(**{
            "name": "Superuser Material's Name",
            "dangerousness": False,
            "category": Recomendation.RECICLAVEL,
            "infos": "Superuser Material's Infos",
            "decomposition": 2
        })
        self.superuser_company.materials.sets = self.superuser_material
        self.superuser_infocompany = InfoCompany.objects.create(**{
            "telephone": 12345678,
            "email": "superuser@company.com",
            "address": "Superuser InfoCompany's Address",
            "company": self.superuser_company
        })
        self.superuser_infocollect = InfoCollect.objects.create(**{
            "cep": 10000000,
            "address": "Superuser InfoCollect's Address",
            "reference_point": "Superuser InfoCollect's Reference Point",
            "company": self.superuser_company
        })
        self.superuser_infocollect.materials.sets = self.superuser_material
        self.superuser_infocollect.user_id.sets = self.superuser
        self.superuser_accumulationpoint = AccumulationPoint.objects.create(**{
            "address": "Superuser Accumulation Point's Address"
        })
        self.superuser_accumulationpoint.materials.sets = self.superuser_material
        self.superuser_schedulecollect = ScheduleCollect.objects.create(**{
            "days": 5,
            "scheduling": make_aware(datetime.now()),
            "city": "Superuser Schedule Collect's City",
            "user": self.superuser
        })
        self.superuser_schedulecollect.materials.sets = self.superuser_material


        self.default_company = Company.objects.create(**{
            "name": "Default Company's Name",
            "collect_days": 5,
            "donation": True,
            "owner_id": self.company
        })
        self.default_discard = Discard.objects.create(**{
            "address": "Default Discard's Address",
            "city": "Default Discard's City",
            "quantity": 5,
        })
        self.default_discard.companies.sets = self.default_company
        self.default_material = Material.objects.create(**{
            "name": "Default Material's Name",
            "dangerousness": False,
            "category": Recomendation.RECICLAVEL,
            "infos": "Default Material's Infos",
            "decomposition": 3
        })
        self.default_company.materials.sets = self.default_material
        self.default_infocompany = InfoCompany.objects.create(**{
            "telephone": 12345678,
            "email": "default@infocompany.com",
            "address": "Default InfoCompany's Address",
            "company": self.default_company
        })
        self.default_infocollect = InfoCollect.objects.create(**{
            "cep": 20000000,
            "address": "Default InfoCollect's Address",
            "reference_point": "Default InfoCollect's Reference Point",
            "company": self.default_company
        })
        self.default_infocollect.materials.sets = self.default_material
        self.default_infocollect.user_id.sets = self.company
        self.default_accumulationpoint = AccumulationPoint.objects.create(**{
            "address": "Default Accumulation Point's Address"
        })
        self.default_accumulationpoint.materials.sets = self.default_material
        self.default_schedulecollect = ScheduleCollect.objects.create(**{
            "days": 3,
            "scheduling": make_aware(datetime.now()),
            "city": "Default Schedule Collect's City",
            "user": self.company
        })
        self.default_schedulecollect.materials.sets = self.default_material

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
                "dangerousness": False,
                "category": Recomendation.RECICLAVEL,
                "infos": f"Random Company {i} Material's info",
                "decomposition": i
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

    # PATH /api/companies/

    def superuser_get_companies(self):
        
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


    def person_get_companies(self):
        
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


    def company_get_companies(self):
        
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


    def anonymous_get_companies(self):
        
        route = "/api/companies/"
        valid_status_code = status.HTTP_401_UNAUTHORIZED

        response = self.client.get(
            route,
            HTTP_ACCEPT='application/json',
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (company credentials): {content}")


    def invalid_get_companies(self):
        
        route = "/api/companies/"
        valid_status_code = status.HTTP_401_UNAUTHORIZED
        
        response = self.client.get(
            route,
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer INVALID' 
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (company credentials): {content}")


    def superuser_post_company(self):
        
        route = "/api/companies/"
        valid_status_code = status.HTTP_201_CREATED
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']
        
        body = {
        "name": "New Superuser's Company",
        "collect_days": 5,
        "donation": True,
        #"materials": []
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
        for key in ["owner_id"]:
            self.assertFalse(key in content, 
                msg=f"2) POST {route} error (superuser credentials): Key '{key}' in response: {content}")   
                

    def person_post_company(self):
        
        route = "/api/companies/"
        valid_status_code = status.HTTP_403_FORBIDDEN
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Person"]["username"], 'password': self.profiles["Person"]["password"]},
            format='json'
        ).json()['access']
        
        body = {
        "name": "New Person's Company",
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


    def anonymous_post_company(self):
        
        route = "/api/companies/"
        valid_status_code = status.HTTP_401_UNAUTHORIZED
        
        body = {
        "name": "Anonymous's Company",
        "collect_days": 5,
        "donation": True,
        "materials": []
        }
        response = self.client.post(
            route,
            body,
            content_type='application/json',
            HTTP_ACCEPT='application/json',
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) POST {route} error (anonymous): {content}")


    def invalid_post_company(self):
        
        route = "/api/companies/"
        valid_status_code = status.HTTP_401_UNAUTHORIZED
        
        body = {
        "name": "Invalid Company",
        "collect_days": 5,
        "donation": True,
        "materials": []
        }
        response = self.client.post(
            route,
            body,
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer INVALID'
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) POST {route} error (invalid credentials): {content}")


    def superuser_post_duplicate_company(self):
        
        route = "/api/companies/"
        valid_status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']
        
        body = {
        "name": self.superuser_company.name,
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
    
    def superuser_get_own_companyid(self):
            
        valid_status_code = status.HTTP_200_OK
        route = f"/api/companies/{self.superuser_company.id}/" 
        
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
    

    def superuser_get_others_companyid(self):
            
        valid_status_code = status.HTTP_200_OK
        route = f"/api/companies/{self.default_company.id}/" 
        
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
    
    
    def company_get_own_companyid(self):
            
        valid_status_code = status.HTTP_200_OK
        route = f"/api/companies/{self.default_company.id}/" 
        
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
        for key in ["id", "name", "collect_days", "donation", "materials"]:
            self.assertTrue(key in content, 
            msg=f"2) GET {route} error (company credentials): Key '{key}' not in response; {content}")   
    

    def person_get_companyid(self):
            
        valid_status_code = status.HTTP_403_FORBIDDEN
        route = f"/api/companies/{self.default_company.id}/" 
        
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
    

    def invalid_get_companyid(self):
            
        valid_status_code = status.HTTP_401_UNAUTHORIZED
        route = f"/api/companies/{self.default_company.id}/" 
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Person"]["username"], 'password': self.profiles["Person"]["password"]},
            format='json'
        ).json()['access']

        response = self.client.get(
            route,
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer INVALID'
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (invalid credentials): {content}")
    

    def anonymous_get_companyid(self):
            
        valid_status_code = status.HTTP_403_FORBIDDEN
        route = f"/api/companies/{self.default_company.id}/" 
        
        response = self.client.get(
            route,
            HTTP_ACCEPT='application/json',
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (anonymous): {content}")
        

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
        "name": self.default_company.name,
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


    def random_usercompany_patch_company_id(self):

        random_id = random.randint(0, 9)
        valid_status_code = status.HTTP_200_OK
        route = f"/api/companies/{self.random_company[random_id].id}/" 
                
        token = self.client.post(
            '/api/login/',
            {'username': f"usercompany{random_id+1}", 'password': f"UserCompany{random_id+1}Password123@"},
            format='json'
        ).json()['access']
        
        body = {
        "name": "PATCH Random Company's Name",
        "collect_days": 99,
        "donation": True,
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
            msg=f"1) PATCH {route} error (company credentials): {content}")
        for key in ["name", "collect_days", "donation", "materials"]:
            self.assertTrue(key in content, 
                msg=f"2) PATCH {route} error (company credentials): Key '{key}' not in response; {content}")   
        for key in ["name", "collect_days", "donation"]:
            self.assertEquals(body[key], content[key], 
                msg=f"3) PATCH {route} error (company credentials): content doesn't match; {content}")   
                
                

    # PATH /api/companies/<int:id>/discards/

    def superuser_get_company_discards(self):

        random_id = random.randint(0, 9)
        route = f"/api/companies/{self.random_company[random_id].id}/discards/"
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


    def random_usercompany_get_company_discards(self):
        
        random_id = random.randint(0, 9)
        valid_status_code = status.HTTP_200_OK
        route = f"/api/companies/{self.random_company[random_id].id}/discards/" 
                
        token = self.client.post(
            '/api/login/',
            {'username': f"usercompany{random_id+1}", 'password': f"UserCompany{random_id+1}Password123@"},
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
        
        random_id = random.randint(0, 9)
        route = f"/api/companies/{self.random_company[random_id].id}/discards/"
        valid_status_code = status.HTTP_201_CREATED
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']

        body = {
            "address": "New Discard's Address",
            "city": "New Discard's City",
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
         

    def random_usercompany_get_company_discard_id(self):

        random_id = random.randint(0, 9)
        route = f"/api/companies/{self.random_company[random_id].id}/discards/{self.random_discard[random_id].id}/"
        valid_status_code = status.HTTP_200_OK
        
        token = self.client.post(
            '/api/login/',
            {'username': f"usercompany{random_id+1}", 'password': f"UserCompany{random_id+1}Password123@"},
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
            msg=f"1) GET {route} error (random company): {content}")
        for key in ["id", "address", "city", "quantity", "companies"]:
                self.assertTrue(key in content, 
                msg=f"2) GET {route} error (random company): Key '{key}' not in response; {content}")   
         
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

