from accumulation_points.tests import AccumulationPointModelTestCase
from companies.tests import CompanyModelTestCase, CompanyViewTestCase
from discards.tests import DiscardModelTestCase
from django.test import TestCase
from info_collects.tests import InfoCollectModelTestCase
from info_companies.tests import (InfoCompanyModelTestCase,
                                  InfoCompanyViewTestCase)
from materials.tests import MaterialModelTestCase
from schedule_collects.tests import ScheduleCollectModelTestCase
from users.tests import UserModelTestCase, UserViewTestCase


class TestA1(UserModelTestCase):
    
    def test_A101(self):
        """USER MODEL: Check user model attributes"""
        self.user_model_attributes()

    def test_A102(self):
        """USER MODEL: Check user type"""
        self.user_type()
 
# class TestA2(UserViewTestCase):
    
#     def test_03(self):
#         """USER VIEW: Check POST /api/login/ (user login and response tokens)"""
#         self.user_login("3")

#     def test_04(self):
#         """USER VIEW: Check POST /api/register/ (random users)"""
#         self.user_register("4")
        
#     def test_05(self):
#         """USER VIEW: Check GET/PATCH /api/user/<int:user_id>/ (superuser credentials)"""
#         self.superuser_get_patch_user_detail("5")        

#     def test_06(self):
#         """USER VIEW: Check GET/PATCH /api/user/<int:user_id>/ (person credentials)"""
#         self.person_get_patch_user_detail("6")        

#     def test_07(self):
#         """USER VIEW: Check GET/PATCH /api/user/<int:user_id>/ (company credentials)"""
#         self.company_get_patch_user_detail("7")        


class TestB1(CompanyModelTestCase):
    
    def test_B101(self):
        """COMPANY MODEL: Check company model attributes"""
        self.company_model_attributes()

    def test_B102(self):
        """COMPANY MODEL: Check company instance contents"""
        self.company_field_contents()

class TestB2(CompanyViewTestCase):
    
    def test_B201(self):
        """COMPANY VIEW: GET /api/company/ (superuser credentials)"""
        self.superuser_get_company()

    def test_B202(self):
        """COMPANY VIEW: GET /api/company/ (person credentials)"""
        self.person_get_company()

    def test_B203(self):
        """COMPANY VIEW: GET /api/company/ (company credentials)"""
        self.company_get_company()

    def test_B204(self):
        """COMPANY VIEW: POST /api/company/ (superuser credentials)"""
        self.superuser_post_company()

    def test_B205(self):
        """COMPANY VIEW: POST /api/company/ (person credentials)"""
        self.person_post_company()

    def test_B206(self):
        """COMPANY VIEW: POST /api/company/ (company credentials)"""
        self.company_post_company()

    def test_B207(self):
        """COMPANY VIEW: POST /api/company/ duplicate (superuser credentials)"""
        self.superuser_post_duplicate_company()

    def test_B208(self):
        """COMPANY VIEW: POST /api/company/ invalid body (superuser credentials)"""
        self.superuser_post_invalid_company()

    def test_B209(self):
        """COMPANY VIEW: GET /api/company/<int:id> (superuser credentials)"""
        self.superuser_get_company_id()

    def test_B210(self):
        """COMPANY VIEW: PATCH /api/company/<int:id> (superuser credentials)"""
        self.superuser_patch_company_id()

    def test_B211(self):
        """COMPANY VIEW: PATCH /api/company/<int:id> duplicate (superuser credentials)"""
        self.superuser_patch_duplicate_company_id()

class TestC1(InfoCompanyModelTestCase):
    
    def test_C101(self):
        """INFOCOMPANY MODEL: Check info_company model attributes"""
        self.info_company_model_attributes()

    def test_C102(self):
        """INFOCOMPANY MODEL: Check info_company instance contents"""
        self.info_company_field_contents()


class TestC2(InfoCompanyViewTestCase):
    
    def test_C201(self):
        """INFOCOMPANY VIEW: GET /api/info_company/ (superuser credentials)"""
        self.superuser_get_infocompany()

    def test_C202(self):
        """INFOCOMPANY VIEW: GET /api/info_company/ (person credentials)"""
        self.person_get_infocompany()

    def test_C203(self):
        """INFOCOMPANY VIEW: GET /api/info_company/ (company credentials)"""
        self.company_get_infocompany()

    def test_C204(self):
        """INFOCOMPANY VIEW: POST /api/info_company/ (superuser credentials)"""
        self.superuser_post_infocompany()

    def test_C205(self):
        """INFOCOMPANY VIEW: GET /api/info_company/<int:id> (superuser credentials)"""
        self.superuser_get_infocompany_id()

    def test_C206(self):
        """INFOCOMPANY VIEW: PATCH /api/info_company/<int:id> (superuser credentials)"""
        self.superuser_patch_infocompany_id()

    def test_C207(self):
        """INFOCOMPANY VIEW: PATCH /api/info_company/<int:id> invalid body (superuser credentials)"""
        self.superuser_patch_invalid_body_infocompany_id()


class TestD1(MaterialModelTestCase):
    
    def test_D101(self):
        """MATERIAL MODEL: Check material model attributes"""
        self.material_model_attributes()

    def test_D102(self):
        """MATERIAL MODEL: Check material instance contents"""
        self.material_field_contents()


class TestE1(AccumulationPointModelTestCase):
    
    def test_E101(self):
        """ACCUMULATION_POINT MODEL: Check accumulation_point model attributes"""
        self.accumulation_point_model_attributes()

    def test_E102(self):
        """ACCUMULATION_POINT MODEL: Check accumulation_point instance contents"""
        self.accumulation_point_field_contents()

class TestF1(InfoCollectModelTestCase):
    
    def test_F101(self):
        """INFO_COLLECT MODEL: Check info_collect model attributes"""
        self.info_collect_model_attributes()

    def test_F102(self):
        """INFO_COLLECT MODEL: Check info_collect instance contents"""
        self.info_collect_field_contents()


class TestG1(ScheduleCollectModelTestCase):
    
    def test_G101(self):
        """SCHEDULE_COLLECT MODEL: Check schedule_collect model attributes"""
        self.schedule_collect_model_attributes()

    def test_G102(self):
        """SCHEDULE_COLLECT MODEL: Check schedule_collect instance contents"""
        self.schedule_collect_field_contents()


class TestH1(DiscardModelTestCase):
    
    def test_H101(self):
        """DISCARD MODEL: Check discard model attributes"""
        self.discard_model_attributes()

    def test_H102(self):
        """DISCARD MODEL: Check discard instance contents"""
        self.discard_field_contents()

