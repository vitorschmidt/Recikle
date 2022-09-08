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

    # POST User Login

    def user_login(self, order):
        
        route = "/api/login/"
        valid_status_code = status.HTTP_200_OK
        
        for profile in self.profiles:
            body = {"username": self.profiles[profile]["username"], "password": self.profiles[profile]["password"]}
            response = self.client.post(route, body, format='json', HTTP_ACCEPT='application/json')
            content = response.json()
            self.assertEquals(response.status_code, valid_status_code,
                msg=f"{order}.1) User View - POST {route}: {profile} login error {content}")
            for key in ["refresh", "access"]:
                    self.assertTrue(key in content, 
                    msg=f"{order}.2) User View - POST {route}: Key '{key}' not in {profile} response: {content}")   
                
    # POST User Register

    def user_register(self, order):
        
        route = "/api/register/"
        valid_status_code = status.HTTP_201_CREATED

        for code in range(20):
            user = {
                "username": f"user{code}",
                "first_name": f"User{code}",
                "last_name": "Kenzie",
                "city": f"User{code}'s City",
                "email": f"user{code}@kenzie.com",
                "is_company": False,
                "password": f"User{code}Password123@",
            }
            response = self.client.post(route, user, format='json', HTTP_ACCEPT='application/json')
            content = response.json()
            self.assertEquals(response.status_code, valid_status_code,
                msg=f"{order}.1) User View - POST {route}: {user} register error {content}")

            def test_user_login(self):
                """Check POST /api/login/ (random users)"""
                login_route = "/api/login/"
                login_valid_status_code = status.HTTP_200_OK
                login_body = {"username": user["username"], "password": user["password"]}
                login_response = self.client.post(login_route, login_body, format='json', HTTP_ACCEPT='application/json')
                login_content = response.json()
                self.assertEquals(response.status_code, valid_status_code,
                    msg=f"{order}.2) User View - POST {login_route}: {user['username']} login error {login_content}")

    # GET/PATCH User Detail

    def superuser_get_patch_user_detail(self, order):
        
        login_route = "/api/login/"
        login_valid_status_code = status.HTTP_200_OK

        login_response = self.client.post(
            login_route,
            {"username": self.profiles["Superuser"]["username"], "password": self.profiles["Superuser"]["password"]},
            format='json',
            HTTP_ACCEPT='application/json' )
        self.assertEquals(login_response.status_code, login_valid_status_code,
            msg=f"{order}.1) Superuser login error {login_response.json()}")
        
        token = login_response.json()["access"]

        #GET User detail (Superuser credentials)

        get_superuser_response = self.client.get(
            f"/api/user/{self.superuser.id}/",
            format='json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        get_superuser_content = get_superuser_response.json()

        get_person_response = self.client.get(
            f"/api/user/{self.person.id}/",
            format='json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        get_person_content = get_person_response.json()

        get_company_response = self.client.get(
            f"/api/user/{self.company.id}/",
            format='json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        get_company_content = get_company_response.json()

        self.assertEquals(get_superuser_response.status_code, status.HTTP_200_OK,
            msg=f"{order}.2) GET /api/user/<superuser>/ (superuser credentials) error {get_superuser_content}")
        self.assertEquals(get_person_response.status_code, status.HTTP_200_OK,
            msg=f"{order}.3) GET /api/user/<person>/ (superuser credentials) error {get_person_content}")
        self.assertEquals(get_company_response.status_code, status.HTTP_200_OK,
            msg=f"{order}.4) GET /api/user/<company>/ (superuser credentials) error {get_company_content}")

        # PATCH User detail (Superuser credentials)

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
            msg=f"{order}.5) PATCH /api/user/<superuser>/ (superuser credentials) error {patch_superuser_content}")
        self.assertEquals(patch_person_response.status_code, status.HTTP_200_OK,
            msg=f"{order}.6) PATCH /api/user/<person>/ (superuser credentials) error {patch_person_content}")
        self.assertEquals(patch_company_response.status_code, status.HTTP_200_OK,
            msg=f"{order}.7) PATCH /api/user/<company>/ (superuser credentials) error {patch_company_content}")


    def person_get_patch_user_detail(self, order):

        login_route = "/api/login/"
        login_valid_status_code = status.HTTP_200_OK
        
        login_response = self.client.post(
            login_route,
            {"username": self.profiles["Person"]["username"], "password": self.profiles["Person"]["password"]},
            format='json',
            HTTP_ACCEPT='application/json' )
        self.assertEquals(login_response.status_code, login_valid_status_code,
            msg=f"{order}.1) Person login error {login_response.json()}")
        
        token = login_response.json()["access"]

        # GET User detail (Person credentials)
        
        get_superuser_response = self.client.get(
            f"/api/user/{self.superuser.id}/",
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        get_superuser_content = get_superuser_response.json()

        get_person_response = self.client.get(
            f"/api/user/{self.person.id}/",
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        get_person_content = get_person_response.json()

        get_company_response = self.client.get(
            f"/api/user/{self.company.id}/",
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        get_company_content = get_company_response.json()

        self.assertEquals(get_superuser_response.status_code, status.HTTP_200_OK,
            msg=f"5.2) GET /api/user/<superuser>/ (person credentials) error {get_superuser_content}")
        self.assertEquals(get_person_response.status_code, status.HTTP_200_OK,
            msg=f"5.3) GET /api/user/<person>/ (person credentials) error {get_person_content}")
        self.assertEquals(get_company_response.status_code, status.HTTP_200_OK,
            msg=f"5.4) GET /api/user/<company>/ (person credentials) error {get_company_content}")

        # PATCH User detail (Person credentials)

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
            msg=f"5.5) PATCH /api/user/<superuser>/ (person credentials) error {patch_superuser_content}")
        self.assertEquals(patch_person_response.status_code, status.HTTP_200_OK,
            msg=f"5.6) PATCH /api/user/<person>/ (person credentials) error {patch_person_content}")
        self.assertEquals(patch_company_response.status_code, status.HTTP_403_FORBIDDEN,
            msg=f"5.7) PATCH /api/user/<company>/ (person credentials) error {patch_company_content}")


    def company_get_patch_user_detail(self, order):

        login_route = "/api/login/"
        login_valid_status_code = status.HTTP_200_OK

        login_response = self.client.post(
            login_route,
            {"username": self.profiles["Company"]["username"], "password": self.profiles["Company"]["password"]},
            format='json',
            HTTP_ACCEPT='application/json' )
        self.assertEquals(login_response.status_code, login_valid_status_code,
            msg=f"{order}.1) Company login error {login_response.json()}")
        
        token = login_response.json()["access"]

        # GET User detail (Company credentials)

        get_superuser_response = self.client.get(
            f"/api/user/{self.superuser.id}/",
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        get_superuser_content = get_superuser_response.json()

        get_person_response = self.client.get(
            f"/api/user/{self.person.id}/",
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        get_person_content = get_person_response.json()

        get_company_response = self.client.get(
            f"/api/user/{self.company.id}/",
            format='json',
            content_type='application/json',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        get_company_content = get_company_response.json()

        self.assertEquals(get_superuser_response.status_code, status.HTTP_200_OK,
            msg=f"{order}.2) GET /api/user/<superuser>/ (company credentials) error {get_superuser_content}")
        self.assertEquals(get_person_response.status_code, status.HTTP_200_OK,
            msg=f"{order}.3) GET /api/user/<person>/ (company credentials) error {get_person_content}")
        self.assertEquals(get_company_response.status_code, status.HTTP_200_OK,
            msg=f"{order}.4) GET /api/user/<company>/ (company credentials) error {get_company_content}")

        # PATCH User detail (Company credentials)

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
            msg=f"{order}.5) PATCH /api/user/<superuser>/ (company credentials) error {patch_superuser_content}")
        self.assertEquals(patch_person_response.status_code, status.HTTP_403_FORBIDDEN,
            msg=f"{order}.6) PATCH /api/user/<person>/ (company credentials) error {patch_person_content}")
        self.assertEquals(patch_company_response.status_code, status.HTTP_200_OK,
            msg=f"{order}.7) PATCH /api/user/<company>/ (company credentials) error {patch_company_content}")
''' 
    def test_C(self):
        """C) Check POST /api/login/ (user login and response tokens)"""
        self.user_login("C")

    def test_D(self):
        """D) Check POST /api/register/ (random users)"""
        self.user_register("D")
        
    def test_E(self):
        """E) Check GET/PATCH /api/user/<int:user_id>/ (superuser credentials)"""
        self.superuser_get_patch_user_detail("E")        

    def test_F(self):
        """F) Check GET/PATCH /api/user/<int:user_id>/ (person credentials)"""
        self.person_get_patch_user_detail("F")        

    def test_G(self):
        """G) Check GET/PATCH /api/user/<int:user_id>/ (company credentials)"""
        self.company_get_patch_user_detail("G")        
 '''
