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

        self.random_company = []
        self.random_discard = []
        self.random_material = []
        self.random_accumulationpoint = []
        self.random_infocompany = []
        self.random_infocollect = []
        self.random_schedulecollect = []

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
                    "cep": 10000000+i,
                    "address": f"Random Company {i} InfoCollect's Address",
                    "reference_point": f"Random Company {i} InfoCollect's Address",
                    "company": self.random_company[i-1]
                }))
                self.random_infocollect[i-1].materials.sets = self.random_material[i-1]
                self.random_infocollect[i-1].user_id.sets = self.superuser
                self.random_accumulationpoint.append(AccumulationPoint.objects.create(**{
                    "address": f"Random Company {i} Accumulation Point's Address"
                }))
                self.random_accumulationpoint[i-1].materials.sets = self.random_material[i-1]
                self.random_schedulecollect.append(ScheduleCollect.objects.create(**{
                    "days": 5,
                    "scheduling": make_aware(datetime.now()),
                    "city": f"Random Company {i} Schedule Collect' Address",
                    "user": self.superuser
                }))
                self.random_schedulecollect[i-1].materials.sets = self.random_material[i-1]

                
                
        except Exception as e:
            print(e)
            

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
