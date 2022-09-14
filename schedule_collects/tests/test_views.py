import random
from datetime import datetime

from accumulation_points.models import AccumulationPoint
from companies.models import Company
from discards.models import Discard
from django.test import TestCase
from django.utils.timezone import make_aware
from info_collects.models import InfoCollect
from info_companies.models import InfoCompany
from materials.models import Material, Recomendation
from rest_framework import status
from schedule_collects.models import ScheduleCollect
from users.models import User


class ScheduleCollectViewTestCase(TestCase):
    
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


    # PATH /api/schedules/

    def superuser_get_schedules(self):

        route = "/api/schedules/"
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


    def person_get_schedules(self):

        route = "/api/schedules/"
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


    def anonymous_get_schedules(self):

        route = "/api/schedules/"
        valid_status_code = status.HTTP_200_OK

        response = self.client.get(
            route,
            HTTP_ACCEPT='application/json',
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (anonymous): {content}")
        self.assertIsInstance(content["results"], list,
            msg=f"2) GET {route} error (anonymous); response is not list: {content}")


    def invalid_get_schedules(self):

        route = "/api/schedules/"
        valid_status_code = status.HTTP_401_UNAUTHORIZED

        response = self.client.get(
            route,
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer INVALID'
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (invalid token): {content}")


    # PATH /api/schedules/<int:id>/

    def superuser_get_schedules_id(self):
        
        route = f"/api/schedules/{self.random_schedulecollect[random.randint(0, 9)].id}/"
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


    def person_get_schedules_id(self):
        
        route = f"/api/schedules/{self.random_schedulecollect[random.randint(0, 9)].id}/"
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


    def anonymous_get_schedules_id(self):
        
        route = f"/api/schedules/{self.random_schedulecollect[random.randint(0, 9)].id}/"
        valid_status_code = status.HTTP_200_OK

        response = self.client.get(
            route,
            HTTP_ACCEPT='application/json',
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (anonymous): {content}")
        self.assertIsInstance(content["results"], list,
            msg=f"2) GET {route} error (anonymous); response is not list: {content}")


    def invalid_get_schedules_id(self):
        
        route = f"/api/schedules/{self.random_schedulecollect[random.randint(0, 9)].id}/"
        valid_status_code = status.HTTP_401_UNAUTHORIZED

        response = self.client.get(
            route,
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer INVALID'
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (invalid token): {content}")
