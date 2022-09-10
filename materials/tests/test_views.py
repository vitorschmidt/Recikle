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

class MaterialViewTestCase(TestCase):
    
    def setUp(self):
   
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

    # POST /api/materials/

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

''' 
    def test_B(self):
        """B) Check POST /api/materials/ (material creation)"""
        self.material_register("B")

    def test_C(self):
        """C) Check POST /api/materials/ (duplicate material creation)"""
        self.duplicate_material_register("C")

    def test_D(self):
        """D) Check GET /api/materials/ (list materials)"""
        self.material_list("D") '''

