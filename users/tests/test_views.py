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

    def newsuperuser_register(self):
        
        route = "/api/register/"
        valid_status_code = status.HTTP_201_CREATED

        for code in range(10):
            user = {
                "username": f"newuser{code}",
                "first_name": f"Newuser{code}",
                "last_name": "Kenzie",
                "city": f"Newuser{code}'s City",
                "email": f"newuser{code}@kenzie.com",
                "is_company": False,
                "password": f"NewUser{code}Password123@",
                "is_superuser": False
            }
            response = self.client.post(
                route,
                user,
                content_type='application/json',
                HTTP_ACCEPT='application/json'
                )
            content = response.json()
            self.assertEquals(response.status_code, valid_status_code,
                msg=f"1) POST {route} error (person): {content}")
            for key in ["password"]:
                self.assertFalse(key in content, 
                    msg=f"2) POST {route} error (company credentials): Key '{key}' in response: {content}")   

            login_route = "/admin/"
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
                msg=f"1) POST {route} error (anonymous): {content}")
            for key in ["password"]:
                self.assertFalse(key in content, 
                    msg=f"2) POST {route} error (anonymous): Key '{key}' in response: {content}")   

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


    def newcompany_register(self):
        
        route = "/api/register/"
        valid_status_code = status.HTTP_201_CREATED

        for code in range(10):
            user = {
                "username": f"newcompany{code}",
                "first_name": f"Newcompany{code}",
                "last_name": "Kenzie",
                "city": f"Newcompany{code}'s City",
                "email": f"newcompany{code}@kenzie.com",
                "is_company": False,
                "password": f"NewCompany{code}Password123@",
            }
            response = self.client.post(route, user, format='json', HTTP_ACCEPT='application/json')
            content = response.json()
            self.assertEquals(response.status_code, valid_status_code,
                msg=f"1) POST {route} error (company): {content}")
            for key in ["password"]:
                self.assertFalse(key in content, 
                    msg=f"2) POST {route} error (company credentials): Key '{key}' in response: {content}")   

            login_route = "/api/login/"
            login_valid_status_code = status.HTTP_200_OK
            login_body = {"username": user["username"], "password": user["password"]}
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
        self.assertEquals(content, {'detail': 'You do not have permission to perform this action.'},
            msg=f"2) GET {route} error (person credentials); invalid response message: {content}")

    
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
        self.assertEquals(content, {'detail': 'You do not have permission to perform this action.'},
            msg=f"2) GET {route} error (person credentials); invalid response message: {content}")

    
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
        self.assertEquals(content, {'detail': 'Authentication credentials were not provided.'},
            msg=f"2) GET {route} error (anonymous); invalid response message: {content}")


            
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
        self.assertEquals(content, {'detail': 'You do not have permission to perform this action.'},
            msg=f"2) GET {route} error (person credentials); invalid response message: {content}")


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
        self.assertEquals(content, {'detail': 'You do not have permission to perform this action.'},
            msg=f"2) GET {route} error (person credentials); invalid response message: {content}")


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
        self.assertEquals(content, {'detail': 'You do not have permission to perform this action.'},
            msg=f"2) GET {route} error (company credentials); invalid response message: {content}")
    

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
        self.assertEquals(content, {'detail': 'You do not have permission to perform this action.'},
            msg=f"2) GET {route} error (company credentials); invalid response message: {content}")
        

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
        self.assertEquals(content, {'detail': 'Authentication credentials were not provided.'},
            msg=f"2) GET {route} error (anonymous); invalid response message: {content}")
        

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
