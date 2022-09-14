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

# from uuid import UUID



# def is_valid_uuid(uuid_to_test, version=4):
#     try:
#         uuid_obj = UUID(uuid_to_test, version=version)
#     except ValueError:
#         return False
#     return str(uuid_obj) == uuid_to_test

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


    # PATH /api/login/

    def superuser_login(self):
        
        route = "/api/login/"
        valid_status_code = status.HTTP_200_OK
        
        body = {
            "username": self.profiles["Superuser"]["username"],
            "password": self.profiles["Superuser"]["password"]
        }
        response = self.client.post(
            route, 
            body, 
            format='json', 
            HTTP_ACCEPT='application/json'
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) POST {route} error (superuser credentials): {content}")
        for key in ["refresh", "access"]:
            self.assertTrue(key in content, 
                msg=f"2) POST {route} error (superuser credentials): Key '{key}' not in response: {content}")   


    def person_login(self):
        
        route = "/api/login/"
        valid_status_code = status.HTTP_200_OK
        
        body = {
            "username": self.profiles["Person"]["username"],
            "password": self.profiles["Person"]["password"]
        }
        response = self.client.post(
            route, 
            body, 
            content_type='application/json',
            HTTP_ACCEPT='application/json'
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) POST {route} error (person credentials): {content}")
        for key in ["refresh", "access"]:
            self.assertTrue(key in content, 
                msg=f"2) POST {route} error (person credentials): Key '{key}' not in response: {content}")   
                

    def company_login(self):
        
        route = "/api/login/"
        valid_status_code = status.HTTP_200_OK
        
        body = {
            "username": self.profiles["Company"]["username"],
            "password": self.profiles["Company"]["password"]
        }
        response = self.client.post(
            route, 
            body, 
            content_type='application/json',
            HTTP_ACCEPT='application/json'
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) POST {route} error (company credentials): {content}")
        for key in ["refresh", "access"]:
            self.assertTrue(key in content, 
                msg=f"2) POST {route} error (company credentials): Key '{key}' not in response: {content}")   

    
    # PATH /api/register/

    # def newsuperuser_register(self):
        
    #     route = "/api/register/"
    #     valid_status_code = status.HTTP_201_CREATED

    #     for code in range(10):
    #         user = {
    #             "username": f"newuser{code}",
    #             "first_name": f"Newuser{code}",
    #             "last_name": "Kenzie",
    #             "city": f"Newuser{code}'s City",
    #             "email": f"newuser{code}@kenzie.com",
    #             "is_company": False,
    #             "password": f"NewUser{code}Password123@",
    #             "is_superuser": False
    #         }
    #         response = self.client.post(
    #             route,
    #             user,
    #             content_type='application/json',
    #             HTTP_ACCEPT='application/json'
    #             )
    #         content = response.json()
    #         self.assertEquals(response.status_code, valid_status_code,
    #             msg=f"1) POST {route} error (person): {content}")
    #         for key in ["password"]:
    #             self.assertFalse(key in content, 
    #                 msg=f"2) POST {route} error (company credentials): Key '{key}' in response: {content}")   

    #         login_route = "/admin/"
    #         login_valid_status_code = status.HTTP_200_OK
    #         login_body = {
    #             "username": user["username"],
    #             "password": user["password"]
    #         }
    #         login_response = self.client.post(
    #             login_route, 
    #             login_body, 
    #             content_type='application/json',
    #             HTTP_ACCEPT='application/json'
    #         )
    #         login_content = login_response.json()
    #         self.assertEquals(login_response.status_code, login_valid_status_code,
    #             msg=f"3) POST {login_route} error ({user['username']}): {login_content}")


    def newuser_register(self):
        
        route = "/api/register/"
        valid_status_code = status.HTTP_201_CREATED

        for code in range(10):
            user = {
                "username": f"newuser{code}",
                "first_name": f"Newuser{code}",
                "last_name": "Kenzie",
                "city": f"Newuser{code}'s City",
                "email": f"newuser{code}@kenzie.com",
                "is_company": (code % 2 == 0),
                "password": f"NewUser{code}Password123@",
            }
            response = self.client.post(
                route,
                user,
                content_type='application/json',
                HTTP_ACCEPT='application/json'
                )
            content = response.json()
            self.assertEquals(response.status_code, valid_status_code,
                msg=f"1) POST {route} error (new user): {content}")
            for key in ["password"]:
                self.assertFalse(key in content, 
                    msg=f"2) POST {route} error (new user): Key '{key}' in response: {content}")   

            login_route = "/api/login/"
            login_valid_status_code = status.HTTP_200_OK
            login_body = {
                "username": user["username"],
                "password": user["password"]
            }
            login_response = self.client.post(
                login_route, 
                login_body, 
                content_type='application/json',
                HTTP_ACCEPT='application/json'
            )
            login_content = login_response.json()
            self.assertEquals(login_response.status_code, login_valid_status_code,
                msg=f"3) POST {login_route} error ({user['username']}): {login_content}")

    
    # PATH /api/users/
    
    def superuser_get_users(self):

        route = "/api/users/"
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

    
    def person_get_users(self):
    
        route = "/api/users/"
        valid_status_code = status.HTTP_403_FORBIDDEN

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

    
    def company_get_users(self):
    
        route = "/api/users/"
        valid_status_code = status.HTTP_403_FORBIDDEN

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

    
    def anonymous_get_users(self):

        route = "/api/users/"
        valid_status_code = status.HTTP_401_UNAUTHORIZED

        response = self.client.get(
            route,
            HTTP_ACCEPT='application/json',
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (anonymous): {content}")


    def invalid_get_users(self):
    
        route = "/api/users/"
        valid_status_code = status.HTTP_401_UNAUTHORIZED

        response = self.client.get(
            route,
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer INVALID'
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (anonymous): {content}")

            
    # PATH /api/user/<user_id>/
    
    def superuser_get_superuserid(self):

        route = f"/api/user/{self.superuser.id}/"
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
        for key in ["password"]:
            self.assertFalse(key in content, 
                msg=f"2) GET {route} error (superuser credentials): Key '{key}' in response: {content}")   


    def superuser_get_personid(self):

        route = f"/api/user/{self.person.id}/"
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
        for key in ["password"]:
            self.assertFalse(key in content, 
                msg=f"2) GET {route} error (superuser credentials): Key '{key}' in response: {content}")   


    def superuser_get_companyid(self):

        route = f"/api/user/{self.company.id}/"
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
        for key in ["password"]:
            self.assertFalse(key in content, 
                msg=f"2) GET {route} error (superuser credentials): Key '{key}' in response: {content}")   


    def person_get_superuserid(self):

        route = f"/api/user/{self.superuser.id}/"
        valid_status_code = status.HTTP_403_FORBIDDEN

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


    def person_get_personid(self):

        route = f"/api/user/{self.person.id}/"
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
        for key in ["password"]:
            self.assertFalse(key in content, 
                msg=f"2) GET {route} error (superuser credentials): Key '{key}' in response: {content}")   


    def person_get_companyid(self):

        route = f"/api/user/{self.company.id}/"
        valid_status_code = status.HTTP_403_FORBIDDEN

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


    def company_get_superuserid(self):

        route = f"/api/user/{self.superuser.id}/"
        valid_status_code = status.HTTP_403_FORBIDDEN

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
    

    def company_get_personid(self):

        route = f"/api/user/{self.person.id}/"
        valid_status_code = status.HTTP_403_FORBIDDEN

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
        

    def company_get_companyid(self):

        route = f"/api/user/{self.company.id}/"
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
        for key in ["password"]:
            self.assertFalse(key in content, 
                msg=f"2) GET {route} error (company credentials): Key '{key}' in response: {content}")   


    def anonymous_get_userid(self):

        for user in [self.superuser, self.person, self.company]:
            route = f"/api/user/{user.id}/"
            valid_status_code = status.HTTP_401_UNAUTHORIZED

            response = self.client.get(
                route,
                HTTP_ACCEPT='application/json',
            )
            content = response.json()
            self.assertEquals(response.status_code, valid_status_code,
                msg=f"1) GET {route} error (anonymous): {content}")
        

    def invalid_get_userid(self):

        for user in [self.superuser, self.person, self.company]:
            route = f"/api/user/{user.id}/"
            valid_status_code = status.HTTP_401_UNAUTHORIZED

            response = self.client.get(
                route,
                HTTP_ACCEPT='application/json',
                HTTP_AUTHORIZATION='Bearer INVALID'
            )
            content = response.json()
            self.assertEquals(response.status_code, valid_status_code,
                msg=f"1) GET {route} error (invalid token): {content}")


    def superuser_patch_userid(self):
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']
        
        patch_superuser_response = self.client.patch(
            f"/api/user/{self.superuser.id}/",
            {"city": "New City"},
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        patch_superuser_content = patch_superuser_response.json()

        patch_person_response = self.client.patch(
            f"/api/user/{self.person.id}/",
            {"city": "New City"},
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        patch_person_content = patch_person_response.json()

        patch_company_response = self.client.patch(
            f"/api/user/{self.company.id}/",
            {"city": "New City"},
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        patch_company_content = patch_company_response.json()

        self.assertEquals(patch_superuser_response.status_code, status.HTTP_200_OK,
            msg=f"1) PATCH /api/user/<superuser>/ (superuser credentials) error {patch_superuser_content}")
        self.assertEquals(patch_person_response.status_code, status.HTTP_200_OK,
            msg=f"2) PATCH /api/user/<person>/ (superuser credentials) error {patch_person_content}")
        self.assertEquals(patch_company_response.status_code, status.HTTP_200_OK,
            msg=f"3) PATCH /api/user/<company>/ (superuser credentials) error {patch_company_content}")


    def person_patch_userid(self):

        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Person"]["username"], 'password': self.profiles["Person"]["password"]},
            format='json'
        ).json()['access']

        patch_superuser_response = self.client.patch(
            f"/api/user/{self.superuser.id}/",
            {"city": "New City"},
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        patch_superuser_content = patch_superuser_response.json()

        patch_person_response = self.client.patch(
            f"/api/user/{self.person.id}/",
            {"city": "New City"},
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        patch_person_content = patch_person_response.json()

        patch_company_response = self.client.patch(
            f"/api/user/{self.company.id}/",
            {"city": "New City"},
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        patch_company_content = patch_company_response.json()

        self.assertEquals(patch_superuser_response.status_code, status.HTTP_403_FORBIDDEN,
            msg=f"1) PATCH /api/user/<superuser>/ (person credentials) error {patch_superuser_content}")
        self.assertEquals(patch_person_response.status_code, status.HTTP_200_OK,
            msg=f"2) PATCH /api/user/<person>/ (person credentials) error {patch_person_content}")
        self.assertEquals(patch_company_response.status_code, status.HTTP_403_FORBIDDEN,
            msg=f"3) PATCH /api/user/<company>/ (person credentials) error {patch_company_content}")


    def company_patch_userid(self):

        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Company"]["username"], 'password': self.profiles["Company"]["password"]},
            format='json'
        ).json()['access']

        patch_superuser_response = self.client.patch(
            f"/api/user/{self.superuser.id}/",
            {"city": "New City"},
            format='json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        patch_superuser_content = patch_superuser_response.json()

        patch_person_response = self.client.patch(
            f"/api/user/{self.person.id}/",
            {"city": "New City"},
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        patch_person_content = patch_person_response.json()

        patch_company_response = self.client.patch(
            f"/api/user/{self.company.id}/",
            {"city": "New City"},
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        patch_company_content = patch_company_response.json()

        self.assertEquals(patch_superuser_response.status_code, status.HTTP_403_FORBIDDEN,
            msg=f"1) PATCH /api/user/<superuser>/ (company credentials) error {patch_superuser_content}")
        self.assertEquals(patch_person_response.status_code, status.HTTP_403_FORBIDDEN,
            msg=f"2) PATCH /api/user/<person>/ (company credentials) error {patch_person_content}")
        self.assertEquals(patch_company_response.status_code, status.HTTP_200_OK,
            msg=f"3) PATCH /api/user/<company>/ (company credentials) error {patch_company_content}")


    def anonymous_patch_userid(self):

        patch_superuser_response = self.client.patch(
            f"/api/user/{self.superuser.id}/",
            {"city": "New City"},
            format='json',
            HTTP_ACCEPT='application/json')
        patch_superuser_content = patch_superuser_response.json()

        patch_person_response = self.client.patch(
            f"/api/user/{self.person.id}/",
            {"city": "New City"},
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json')
        patch_person_content = patch_person_response.json()

        patch_company_response = self.client.patch(
            f"/api/user/{self.company.id}/",
            {"city": "New City"},
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json')
        patch_company_content = patch_company_response.json()

        self.assertEquals(patch_superuser_response.status_code, status.HTTP_401_UNAUTHORIZED,
            msg=f"1) PATCH /api/user/<superuser>/ (anonymous) error {patch_superuser_content}")
        self.assertEquals(patch_person_response.status_code, status.HTTP_401_UNAUTHORIZED,
            msg=f"2) PATCH /api/user/<person>/ (anonymous) error {patch_person_content}")
        self.assertEquals(patch_company_response.status_code, status.HTTP_401_UNAUTHORIZED,
            msg=f"3) PATCH /api/user/<company>/ (anonymous) error {patch_company_content}")


    def invalid_patch_userid(self):

        patch_superuser_response = self.client.patch(
            f"/api/user/{self.superuser.id}/",
            {"city": "New City"},
            format='json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer INVALID')
        patch_superuser_content = patch_superuser_response.json()

        patch_person_response = self.client.patch(
            f"/api/user/{self.person.id}/",
            {"city": "New City"},
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer INVALID')
        patch_person_content = patch_person_response.json()

        patch_company_response = self.client.patch(
            f"/api/user/{self.company.id}/",
            {"city": "New City"},
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer INVALID')
        patch_company_content = patch_company_response.json()

        self.assertEquals(patch_superuser_response.status_code, status.HTTP_401_UNAUTHORIZED,
            msg=f"1) PATCH /api/user/<superuser>/ (invalid token) error {patch_superuser_content}")
        self.assertEquals(patch_person_response.status_code, status.HTTP_401_UNAUTHORIZED,
            msg=f"2) PATCH /api/user/<person>/ (invalid token) error {patch_person_content}")
        self.assertEquals(patch_company_response.status_code, status.HTTP_401_UNAUTHORIZED,
            msg=f"3) PATCH /api/user/<company>/ (invalid token) error {patch_company_content}")


    def superuser_patch_invalid_data_userid(self):
        
        token = self.client.post(
            '/api/login/',
            {'username': self.profiles["Superuser"]["username"], 'password': self.profiles["Superuser"]["password"]},
            format='json'
        ).json()['access']
        
        patch_superuser_response = self.client.patch(
            f"/api/user/{self.superuser.id}/",
            {"city": None},
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        patch_superuser_content = patch_superuser_response.json()

        patch_person_response = self.client.patch(
            f"/api/user/{self.person.id}/",
            {"city": None},
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        patch_person_content = patch_person_response.json()

        patch_company_response = self.client.patch(
            f"/api/user/{self.company.id}/",
            {"city": None},
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        patch_company_content = patch_company_response.json()

        self.assertEquals(patch_superuser_response.status_code, status.HTTP_400_BAD_REQUEST,
            msg=f"1) PATCH /api/user/<superuser>/ invalid data (superuser credentials) error {patch_superuser_content}")
        self.assertEquals(patch_person_response.status_code, status.HTTP_400_BAD_REQUEST,
            msg=f"2) PATCH /api/user/<person>/ invalid data (superuser credentials) error {patch_person_content}")
        self.assertEquals(patch_company_response.status_code, status.HTTP_400_BAD_REQUEST,
            msg=f"3) PATCH /api/user/<company>/ invalid data (superuser credentials) error {patch_company_content}")


    # PATH /api/users/<id>/schedules/

    def superuser_get_user_schedules(self):

        route = f"/api/users/{self.random_usercompany[random.randint(0, 9)].id}/schedules/"
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
        # self.assertIsInstance(content["results"], list,
        #     msg=f"2) GET {route} error (superuser credentials); response is not list: {content}")


    def randomuser_get_own_schedules(self):

        random_id = random.randint(0, 9)
        route = f"/api/users/{self.random_usercompany[random_id].id}/schedules/"
        valid_status_code = status.HTTP_200_OK

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


    def anonymous_get_schedules(self):

        random_id = random.randint(0, 9)
        route = f"/api/users/{self.random_usercompany[random_id].id}/schedules/"
        valid_status_code = status.HTTP_401_UNAUTHORIZED

        response = self.client.get(
            route,
            HTTP_ACCEPT='application/json',
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (anonymous): {content}")


    def invalid_get_schedules(self):

        random_id = random.randint(0, 9)
        route = f"/api/users/{self.random_usercompany[random_id].id}/schedules/"
        valid_status_code = status.HTTP_401_UNAUTHORIZED

        response = self.client.get(
            route,
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer INVALID'
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (invalid token): {content}")


    # PATH /api/users/<id>/info_collection/

    def superuser_get_user_infocollection(self):

        route = f"/api/users/{self.random_usercompany[random.randint(0, 9)].id}/info_collection/"
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
        # self.assertIsInstance(content["results"], list,
        #     msg=f"2) GET {route} error (superuser credentials); response is not list: {content}")


    def randomuser_get_own_infocollection(self):

        random_id = random.randint(0, 9)
        route = f"/api/users/{self.random_usercompany[random_id].id}/info_collection/"
        valid_status_code = status.HTTP_200_OK

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
            msg=f"1) GET {route} error (random user): {content}")
        self.assertIsInstance(content["results"], list,
            msg=f"2) GET {route} error (random user); response is not list: {content}")


    def anonymous_get_infocollection(self):

        random_id = random.randint(0, 9)
        route = f"/api/users/{self.random_usercompany[random_id].id}/info_collection/"
        valid_status_code = status.HTTP_401_UNAUTHORIZED

        response = self.client.get(
            route,
            HTTP_ACCEPT='application/json',
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (anonymous): {content}")


    def invalid_get_infocollection(self):

        random_id = random.randint(0, 9)
        route = f"/api/users/{self.random_usercompany[random_id].id}/info_collection/"
        valid_status_code = status.HTTP_401_UNAUTHORIZED

        response = self.client.get(
            route,
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer INVALID'
        )
        content = response.json()
        self.assertEquals(response.status_code, valid_status_code,
            msg=f"1) GET {route} error (invalid token): {content}")


    # PATH /api/users/<id>/info_collection/<info_id>/

    def superuser_get_user_infocollection_id(self):

        random_id = random.randint(0, 9)
        route = f"/api/users/{self.random_usercompany[random_id].id}/info_collection/{self.random_infocollect[random_id].id}/"
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
        # self.assertIsInstance(content["results"], list,
        #     msg=f"2) GET {route} error (superuser credentials); response is not list: {content}")


    def randomuser_get_own_infocollection_id(self):

        random_id = random.randint(0, 9)
        route = f"/api/users/{self.random_usercompany[random_id].id}/info_collection/{self.random_infocollect[random_id].id}/"
        valid_status_code = status.HTTP_200_OK

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
            msg=f"1) GET {route} error (random user): {content}")
        # self.assertIsInstance(content["results"], list,
        #     msg=f"2) GET {route} error (random user); response is not list: {content}")
