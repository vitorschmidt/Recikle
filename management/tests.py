from accumulation_points.tests import AccumulationPointModelTestCase
from companies.tests import CompanyModelTestCase, CompanyViewTestCase
from discards.tests import DiscardModelTestCase
from django.test import TestCase
from info_collects.tests import InfoCollectModelTestCase
from info_companies.tests import InfoCompanyModelTestCase
from materials.tests import MaterialModelTestCase
from schedule_collects.tests import ScheduleCollectModelTestCase
from users.tests import UserModelTestCase, UserViewTestCase


class TestA1(UserModelTestCase):
    
    def test_A101(self):
        """USER MODEL: Check user model attributes"""
        self.user_model_attributes("A101")

    def test_A102(self):
        """USER MODEL: Check user type"""
        self.user_type("A102")
 
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
        self.company_model_attributes("B101")

    def test_B102(self):
        """COMPANY MODEL: Check company instance contents"""
        self.company_field_contents("B102")


class TestC1(InfoCompanyModelTestCase):
    
    def test_C101(self):
        """INFOCOMPANY MODEL: Check info_company model attributes"""
        self.info_company_model_attributes("C101")

    def test_C102(self):
        """INFOCOMPANY MODEL: Check info_company instance contents"""
        self.info_company_field_contents("C102")



# class TestB2(CompanyViewTestCase):
    
#     def test_10(self):
#         """COMPANY VIEW: Check company creation"""
#         self.post_company("10")

#     def test_11(self):
#         """COMPANY VIEW: Check company retrieval"""
#         self.get_company("11")

#     def test_12(self):
#         """COMPANY VIEW: Check detailed company retrieval"""
#         self.get_company("12")


class TestD1(MaterialModelTestCase):
    
    def test_D101(self):
        """MATERIAL MODEL: Check material model attributes"""
        self.material_model_attributes("D101")

    def test_D102(self):
        """MATERIAL MODEL: Check material instance contents"""
        self.material_field_contents("D102")


class TestE1(AccumulationPointModelTestCase):
    
    def test_E101(self):
        """ACCUMULATION_POINT MODEL: Check accumulation_point model attributes"""
        self.accumulation_point_model_attributes("E101")

    def test_E102(self):
        """ACCUMULATION_POINT MODEL: Check accumulation_point instance contents"""
        self.accumulation_point_field_contents("E102")

class TestF1(InfoCollectModelTestCase):
    
    def test_F101(self):
        """INFO_COLLECT MODEL: Check info_collect model attributes"""
        self.info_collect_model_attributes("F101")

    def test_F102(self):
        """INFO_COLLECT MODEL: Check info_collect instance contents"""
        self.info_collect_field_contents("F102")


class TestG1(ScheduleCollectModelTestCase):
    
    def test_G101(self):
        """SCHEDULE_COLLECT MODEL: Check schedule_collect model attributes"""
        self.schedule_collect_model_attributes("G101")

    def test_G102(self):
        """SCHEDULE_COLLECT MODEL: Check schedule_collect instance contents"""
        self.schedule_collect_field_contents("G102")


class TestH1(DiscardModelTestCase):
    
    def test_H101(self):
        """DISCARD MODEL: Check discard model attributes"""
        self.discard_model_attributes("H101")

    def test_H102(self):
        """DISCARD MODEL: Check discard instance contents"""
        self.discard_field_contents("H102")

