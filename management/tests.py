from accumulation_points.tests import AccumulationPointModelTestCase
from companies.tests import CompanyModelTestCase, CompanyViewTestCase
from discards.tests import DiscardModelTestCase
from discards.tests.test_views import DiscardViewTestCase
from django.test import TestCase
from info_collects.tests import InfoCollectModelTestCase
from info_companies.tests import (InfoCompanyModelTestCase,
                                  InfoCompanyViewTestCase)
from materials.tests import MaterialModelTestCase, MaterialViewTestCase
from schedule_collects.tests import (ScheduleCollectModelTestCase,
                                     ScheduleCollectViewTestCase)
from users.tests import UserModelTestCase, UserViewTestCase

# class TestA1(UserModelTestCase):
    
#     def test_A101(self):
#         """USER MODEL: Check user model attributes"""
#         self.user_model_attributes()

#     def test_A102(self):
#         """USER MODEL: Check user type"""
#         self.user_type()
 
# class TestA2(UserViewTestCase):

    # def test_A201(self):
    #     """USER VIEW: POST /api/login/ (superuser credentials)"""
    #     self.superuser_login()

    # def test_A202(self):
    #     """USER VIEW: POST /api/login/ (person credentials)"""
    #     self.person_login()

    # def test_A203(self):
    #     """USER VIEW: POST /api/login/ (company credentials)"""
    #     self.company_login()

    # def test_A204(self):
    #     """USER VIEW: POST /api/register/ (new users)"""
    #     self.newuser_register()

    # def test_A205(self):
    #     """USER VIEW: GET /api/users/ (superuser credentials)"""
    #     self.superuser_get_users()

    # def test_A206(self):
    #     """USER VIEW: GET /api/users/ (person credentials)"""
    #     self.person_get_users()

    # def test_A207(self):
    #     """USER VIEW: GET /api/users/ (company credentials)"""
    #     self.company_get_users()

    # def test_A208(self):
    #     """USER VIEW: GET /api/users/ (anonymous)"""
    #     self.anonymous_get_users()

    # def test_A209(self):
    #     """USER VIEW: GET /api/users/ (invalid token)"""
    #     self.invalid_get_users()

    # def test_A210(self):
    #     """USER VIEW: GET /api/user/<user_id>/ (superuser > superuser_id)"""
    #     self.superuser_get_superuserid()

    # def test_A211(self):
    #     """USER VIEW: GET /api/user/<user_id>/ (superuser > person_id)"""
    #     self.superuser_get_personid()

    # def test_A212(self):
    #     """USER VIEW: GET /api/user/<user_id>/ (superuser > company_id)"""
    #     self.superuser_get_companyid()

    # def test_A213(self):
    #     """USER VIEW: GET /api/user/<user_id>/ (person > superuser_id)"""
    #     self.person_get_superuserid()

    # def test_A214(self):
    #     """USER VIEW: GET /api/user/<user_id>/ (person > person_id)"""
    #     self.person_get_personid()

    # def test_A215(self):
    #     """USER VIEW: GET /api/user/<user_id>/ (person > company_id)"""
    #     self.person_get_companyid()

    # def test_A216(self):
    #     """USER VIEW: GET /api/user/<user_id>/ (company > superuser_id)"""
    #     self.company_get_superuserid()

    # def test_A217(self):
    #     """USER VIEW: GET /api/user/<user_id>/ (company > person_id)"""
    #     self.company_get_personid()

    # def test_A218(self):
    #     """USER VIEW: GET /api/user/<user_id>/ (company > company_id)"""
    #     self.company_get_companyid()

    # def test_A219(self):
    #     """USER VIEW: GET /api/user/<user_id>/ (anonymous > anyone)"""
    #     self.anonymous_get_userid()

    # def test_A220(self):
    #     """USER VIEW: GET /api/user/<user_id>/ (invalid token > anyone)"""
    #     self.invalid_get_userid()

    # def test_A221(self):
    #     """USER VIEW: PATCH /api/user/<user_id>/ (superuser credentials > anyone)"""
    #     self.superuser_patch_userid()

    # def test_A222(self):
    #     """USER VIEW: PATCH /api/user/<user_id>/ (person credentials > anyone)"""
    #     self.person_patch_userid()

    # def test_A223(self):
    #     """USER VIEW: PATCH /api/user/<user_id>/ (company credentials > anyone)"""
    #     self.company_patch_userid()

    # def test_A224(self):
    #     """USER VIEW: PATCH /api/user/<user_id>/ (anonymous > anyone)"""
    #     self.anonymous_patch_userid()

    # def test_A225(self):
    #     """USER VIEW: PATCH /api/user/<user_id>/ (invalid token > anyone)"""
    #     self.invalid_patch_userid()

    # def test_A226(self):
    #     """USER VIEW: PATCH /api/user/<user_id>/ invalid data (superuser > anyone)"""
    #     self.superuser_patch_invalid_data_userid()

    # def test_A227(self):
    #     """USER VIEW: GET /api/users/<id>/schedules/ (superuser > random user's)"""
    #     self.superuser_get_user_schedules()

    # def test_A228(self):
    #     """USER VIEW: GET /api/users/<id>/schedules/ (random user's own)"""
    #     self.randomuser_get_own_schedules()

    # def test_A229(self):
    #     """USER VIEW: GET /api/users/<id>/schedules/ (anonymous > random user's)"""
    #     self.anonymous_get_schedules()

    # def test_A230(self):
    #     """USER VIEW: GET /api/users/<id>/schedules/ (invalid token > random user's)"""
    #     self.invalid_get_schedules()

    # def test_A231(self):
    #     """USER VIEW: GET /api/users/<id>/info_collection/ (superuser > random user's)"""
    #     self.superuser_get_user_infocollection()

    # def test_A232(self):
    #     """USER VIEW: GET /api/users/<id>/info_collection/ (random user's own)"""
    #     self.randomuser_get_own_infocollection()

    # def test_A233(self):
    #     """USER VIEW: GET /api/users/<id>/info_collection/ (anonymous > random user's)"""
    #     self.anonymous_get_infocollection()

    # def test_A234(self):
    #     """USER VIEW: GET /api/users/<id>/info_collection/ (invalid token > random user's)"""
    #     self.invalid_get_infocollection()

    # def test_A235(self):
    #     """USER VIEW: GET /api/users/<id>/info_collection/<info_id>/ (superuser > random user's)"""
    #     self.superuser_get_user_infocollection_id()

    # def test_A236(self):
    #     """USER VIEW: GET /api/users/<id>/info_collection/<info_id>/ (random user's own)"""
    #     self.randomuser_get_own_infocollection_id()


# class TestB1(CompanyModelTestCase):
    
#     def test_B101(self):
#         """COMPANY MODEL: Check company model attributes"""
#         self.company_model_attributes()

#     def test_B102(self):
#         """COMPANY MODEL: Check company instance contents"""
#         self.company_field_contents()

# class TestB2(CompanyViewTestCase):
    
    # def test_B201(self):
    #     """COMPANY VIEW: GET /api/companies/ (superuser credentials)"""
    #     self.superuser_get_companies()

    # def test_B202(self):
    #     """COMPANY VIEW: GET /api/companies/ (person credentials)"""
    #     self.person_get_companies()

    # def test_B203(self):
    #     """COMPANY VIEW: GET /api/companies/ (company credentials)"""
    #     self.company_get_companies()

    # def test_B204(self):
    #     """COMPANY VIEW: GET /api/companies/ (anonymous)"""
    #     self.anonymous_get_companies()

    # def test_B205(self):
    #     """COMPANY VIEW: GET /api/companies/ (invalid credentials)"""
    #     self.invalid_get_companies()

    # def test_B206(self):
    #     """COMPANY VIEW: POST /api/companies/ (superuser credentials)"""
    #     self.superuser_post_company()

    # def test_B207(self):
    #     """COMPANY VIEW: POST /api/companies/ (person credentials)"""
    #     self.person_post_company()

    # def test_B208(self):
    #     """COMPANY VIEW: POST /api/companies/ (company credentials)"""
    #     self.company_post_company()

    # def test_B209(self):
    #     """COMPANY VIEW: POST /api/companies/ (anonymous)"""
    #     self.anonymous_post_company()

    # def test_B210(self):
    #     """COMPANY VIEW: POST /api/companies/ (invalid credentials)"""
    #     self.invalid_post_company()

    # def test_B211(self):
    #     """COMPANY VIEW: POST /api/company/ duplicate data (superuser credentials)"""
    #     self.superuser_post_duplicate_company()

    # def test_B212(self):
    #     """COMPANY VIEW: POST /api/company/ invalid data (superuser credentials)"""
    #     self.superuser_post_invalid_company()

    # def test_B213(self):
    #     """COMPANY VIEW: GET /api/company/<int:id>/ own company (superuser credentials)"""
    #     self.superuser_get_own_companyid()

    # def test_B214(self):
    #     """COMPANY VIEW: GET /api/company/<int:id>/ other's company (superuser credentials)"""
    #     self.superuser_get_others_companyid()

    # def test_B215(self):
    #     """COMPANY VIEW: GET /api/company/<int:id>/ company's own company (company credentials)"""
    #     self.company_get_own_companyid()

    # def test_B216(self):
    #     """COMPANY VIEW: GET /api/company/<int:id>/ (person credentials)"""
    #     self.person_get_companyid()

    # def test_B217(self):
    #     """COMPANY VIEW: GET /api/company/<int:id>/ (anonymous)"""
    #     self.anonymous_get_companyid()

    # def test_B218(self):
    #     """COMPANY VIEW: GET /api/company/<int:id>/ (invalid credentials)"""
    #     self.invalid_get_companyid()

    # def test_B219(self):
    #     """COMPANY VIEW: PATCH /api/company/<int:id>/ (superuser credentials)"""
    #     self.superuser_patch_company_id()

    # def test_B220(self):
    #     """COMPANY VIEW: PATCH /api/company/<int:id>/ duplicate (superuser credentials)"""
    #     self.superuser_patch_duplicate_company_id()

    # def test_B221(self):
    #     """COMPANY VIEW: PATCH /api/company/<int:id>/ (random user)"""
    #     self.random_usercompany_patch_company_id()

    # def test_B222(self):
    #     """COMPANY VIEW: PATCH /api/company/<int:id>/ invalid data (random user)"""
    #     self.random_usercompany_patch_invalid_company_id()

    # def test_B223(self):
    #     """COMPANY VIEW: GET /api/company/<int:id>/discards/ (random company's)"""
    #     self.random_usercompany_get_company_discards()
        
    # def test_B224(self):
    #     """COMPANY VIEW: GET /api/company/<int:id>/discards/ (superuser credentials)"""
    #     self.superuser_get_company_discards()

    # def test_B225(self):
    #     """COMPANY VIEW: POST /api/company/<int:id>/discards/ (superuser credentials)"""
    #     self.superuser_post_company_discard()

    # def test_B226(self):
    #     """COMPANY VIEW: POST /api/company/<int:id>/discards/ (random company's)"""
    #     self.random_usercompany_post_own_company_discard()

    # def test_B227(self):
    #     """COMPANY VIEW: POST /api/company/<int:id>/discards/ invalid data (random company's)"""
    #     self.random_usercompany_post_own_company_invalid_discard()

    # def test_B228(self):
    #     """COMPANY VIEW: GET /api/company/<int:id>/discards/<int:discard_id>/ (superuser credentials)"""
    #     self.superuser_get_company_discard_id()

    # def test_B229(self):
    #     """COMPANY VIEW: GET /api/company/<int:id>/discards/<int:discard_id>/ (random company)"""
    #     self.random_usercompany_get_company_discard_id()

    # def test_B230(self):
    #     """COMPANY VIEW: PATCH /api/company/<int:id>/discards/<int:discard_id>/ (superuser credentials)"""
    #     self.superuser_patch_company_discard_id()

    # def test_B231(self):
    #     """COMPANY VIEW: GET /api/company/<int:id>/materials/ (superuser credentials)"""
    #     self.superuser_get_company_materials()

    # def test_B232(self):
    #     """COMPANY VIEW: POST /api/company/<int:id>/materials/ (superuser credentials)"""
    #     self.superuser_post_company_material()

    # def test_B233(self):
    #     """COMPANY VIEW: GET /api/company/<int:id>/materials/<int:material_id>/ (superuser credentials)"""
    #     self.superuser_get_company_material_id()

    # def test_B234(self):
    #     """COMPANY VIEW: GET /api/company/<int:id>/materials/<int:material_id>/ (random company)"""
    #     self.random_usercompany_get_company_material_id()

#     def test_B235(self):
#         """COMPANY VIEW: PATCH /api/company/<int:id>/materials/<int:material_id>/ (superuser credentials)"""
#         self.superuser_patch_company_material_id()

    # def test_B236(self):
    #     """COMPANY VIEW: GET /api/company/<int:id>/info_collection/ (superuser credentials)"""
    #     self.superuser_get_company_infocollection()

    # def test_B237(self):
    #     """COMPANY VIEW: GET /api/company/<int:id>/info_company/ (superuser credentials)"""
    #     self.superuser_get_company_infocompany()


# class TestC1(InfoCompanyModelTestCase):
    
#     def test_C101(self):
#         """INFOCOMPANY MODEL: Check info_company model attributes"""
#         self.info_company_model_attributes()

#     def test_C102(self):
#         """INFOCOMPANY MODEL: Check info_company instance contents"""
#         self.info_company_field_contents()


# class TestC2(InfoCompanyViewTestCase):
    
#     def test_C201(self):
#         """INFOCOMPANY VIEW: GET /api/info_company/ (superuser credentials)"""
#         self.superuser_get_infocompany()

#     def test_C202(self):
#         """INFOCOMPANY VIEW: GET /api/info_company/ (person credentials)"""
#         self.person_get_infocompany()

#     def test_C203(self):
#         """INFOCOMPANY VIEW: GET /api/info_company/ (company credentials)"""
#         self.company_get_infocompany()

#     def test_C204(self):
#         """INFOCOMPANY VIEW: GET /api/info_company/ (anonymous)"""
#         self.anonymous_get_infocompany()

#     def test_C205(self):
#         """INFOCOMPANY VIEW: GET /api/info_company/ (invalid)"""
#         self.invalid_get_infocompany()

#     def test_C206(self):
#         """INFOCOMPANY VIEW: POST /api/info_company/ (superuser credentials)"""
#         self.superuser_post_infocompany()

#     def test_C207(self):
#         """INFOCOMPANY VIEW: POST /api/info_company/ (random user's own company)"""
#         self.random_usercompany_post_infocompany()

#     def test_C208(self):
#         """INFOCOMPANY VIEW: POST /api/info_company/ invalid data (random user's own company)"""
#         self.random_usercompany_post_invalid_body_infocompany()

#     def test_C209(self):
#         """INFOCOMPANY VIEW: GET /api/info_company/<int:id>/ (superuser credentials)"""
#         self.superuser_get_infocompany_id()

#     def test_C210(self):
#         """INFOCOMPANY VIEW: GET /api/info_company/<int:id>/ (person credentials)"""
#         self.person_get_infocompany_id()

#     def test_C211(self):
#         """INFOCOMPANY VIEW: GET /api/info_company/<int:id>/ (anonymous)"""
#         self.anonymous_get_infocompany_id()

#     def test_C212(self):
#         """INFOCOMPANY VIEW: PATCH /api/info_company/<int:id>/ (superuser credentials)"""
#         self.superuser_patch_infocompany_id()

#     def test_C213(self):
#         """INFOCOMPANY VIEW: PATCH /api/info_company/<int:id>/ (random user's own company)"""
#         self.random_usercompany_patch_infocompany_id()

#     def test_C214(self):
#         """INFOCOMPANY VIEW: DELETE /api/info_company/<int:id>/ (superuser credentials)"""
#         self.superuser_delete_infocompany_id()

#     def test_C215(self):
#         """INFOCOMPANY VIEW: DELETE /api/info_company/<int:id>/ (random user's own company)"""
#         self.random_usercompany_delete_infocompany_id()

#     def test_C216(self):
#         """INFOCOMPANY VIEW: PATCH /api/info_company/<int:id>/ invalid body (random user's own company)"""
#         self.random_usercompany_patch_invalid_body_infocompany_id()


# class TestD1(MaterialModelTestCase):
    
#     def test_D101(self):
#         """MATERIAL MODEL: Check material model attributes"""
#         self.material_model_attributes()

#     def test_D102(self):
#         """MATERIAL MODEL: Check material instance contents"""
#         self.material_field_contents()


class TestD2(MaterialViewTestCase):
    
    def test_D201(self):
        """MATERIAL VIEW: GET /api/materials/ (superuser credentials)"""
        self.superuser_get_materials()

    def test_D202(self):
        """MATERIAL VIEW: GET /api/materials/ (person credentials)"""
        self.person_get_materials()

    def test_D203(self):
        """MATERIAL VIEW: POST /api/materials/ (superuser credentials)"""
        self.superuser_post_material()

# #     def test_D203(self):
# #         """MATERIAL VIEW: GET /api/materials/<int:id>/ (superuser credentials)"""
# #         self.superuser_get_materials_id()

# #     def test_D204(self):
# #         """MATERIAL VIEW: PATCH /api/materials/<int:id>/ (superuser credentials)"""
# #         self.superuser_patch_material_id()

# #     def test_D205(self):
# #         """MATERIAL VIEW: GET /api/materials/<int:id>/accumulation_point/ (superuser credentials)"""
# #         self.superuser_get_material_accumulationpoint()

# #     def test_D206(self):
# #         """MATERIAL VIEW: POST /api/materials/<int:id>accumulation_point/ (superuser credentials)"""
# #         self.superuser_post_material_accumulationpoint()

# #     def test_D207(self):
# #         """MATERIAL VIEW: GET /api/materials/<int:id>/accumulation_point/<int:accumulation_point_id>/ (superuser credentials)"""
# #         self.superuser_get_material_accumulationpoint_id()

# #     def test_D208(self):
# #         """MATERIAL VIEW: PATCH /api/materials/<int:id>/accumulation_point/<int:accumulation_point_id>/ (superuser credentials)"""
# #         self.superuser_patch_material_accumulationpoint_id()

# #     def test_D209(self):
# #         """MATERIAL VIEW: GET /api/materials/<int:id>/info_collection/ (superuser credentials)"""
# #         self.superuser_get_material_infocollection()

# #     def test_D210(self):
# #         """MATERIAL VIEW: POST /api/materials/<int:id>/info_collection/ (superuser credentials)"""
# #         self.superuser_post_material_infocollection()

# #     def test_D211(self):
# #         """MATERIAL VIEW: GET /api/materials/<int:id>/info_collection/<int:info_id>/ (superuser credentials)"""
# #         self.superuser_get_material_infocollection_id()

# #     def test_D212(self):
# #         """MATERIAL VIEW: PATCH /api/materials/<int:id>/info_collection/<int:info_id>/ (superuser credentials)"""
# #         self.superuser_patch_material_infocollection_id()

# class TestE1(AccumulationPointModelTestCase):
    
#     def test_E101(self):
#         """ACCUMULATION_POINT MODEL: Check accumulation_point model attributes"""
#         self.accumulation_point_model_attributes()

#     def test_E102(self):
#         """ACCUMULATION_POINT MODEL: Check accumulation_point instance contents"""
#         self.accumulation_point_field_contents()

# class TestF1(InfoCollectModelTestCase):
    
#     def test_F101(self):
#         """INFO_COLLECT MODEL: Check info_collect model attributes"""
#         self.info_collect_model_attributes()

#     def test_F102(self):
#         """INFO_COLLECT MODEL: Check info_collect instance contents"""
#         self.info_collect_field_contents()


# class TestG1(ScheduleCollectModelTestCase):
    
#     def test_G101(self):
#         """SCHEDULE_COLLECT MODEL: Check schedule_collect model attributes"""
#         self.schedule_collect_model_attributes()

#     def test_G102(self):
#         """SCHEDULE_COLLECT MODEL: Check schedule_collect instance contents"""
#         self.schedule_collect_field_contents()


# class TestG2(ScheduleCollectViewTestCase):
    
#     def test_G201(self):
#         """SCHEDULE_COLLECT VIEW: GET /api/schedules/ (superuser credentials)"""
#         self.superuser_get_schedules()

#     def test_G202(self):
#         """SCHEDULE_COLLECT VIEW: GET /api/schedules/ (person credentials)"""
#         self.person_get_schedules()

#     def test_G203(self):
#         """SCHEDULE_COLLECT VIEW: GET /api/schedules/ (anonymous)"""
#         self.anonymous_get_schedules()

#     def test_G204(self):
#         """SCHEDULE_COLLECT VIEW: GET /api/schedules/ (invalid token)"""
#         self.invalid_get_schedules()

#     def test_G205(self):
#         """SCHEDULE_COLLECT VIEW: GET /api/schedules/<int:id>/ (superuser credentials)"""
#         self.superuser_get_schedules_id()

#     def test_G206(self):
#         """SCHEDULE_COLLECT VIEW: GET /api/schedules/<int:id>/ (person credentials)"""
#         self.person_get_schedules_id()

#     def test_G207(self):
#         """SCHEDULE_COLLECT VIEW: GET /api/schedules/<int:id>/ (anonymous)"""
#         self.anonymous_get_schedules_id()

#     def test_G208(self):
#         """SCHEDULE_COLLECT VIEW: GET /api/schedules/<int:id>/ (invalid token)"""
#         self.invalid_get_schedules_id()

# class TestH1(DiscardModelTestCase):
    
#     def test_H101(self):
#         """DISCARD MODEL: Check discard model attributes"""
#         self.discard_model_attributes()

#     def test_H102(self):
#         """DISCARD MODEL: Check discard instance contents"""
#         self.discard_field_contents()

# class TestH2(DiscardViewTestCase):

#     def test_H201(self):
#         """DISCARD MODEL: GET /api/discards/ (superuser credentials)"""
#         self.superuser_get_discards()
            
#     def test_H202(self):
#         """DISCARD MODEL: GET /api/discards/ (person credentials)"""
#         self.person_get_discards()

#     def test_H203(self):
#         """DISCARD MODEL: GET /api/discards/ (anonymous)"""
#         self.anonymous_get_discards()

#     def test_H204(self):
#         """DISCARD MODEL: GET /api/discards/ (invalid token)"""
#         self.invalid_get_discards()
