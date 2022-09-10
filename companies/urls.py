from discards.views import DiscardCompanyView, DiscardDetailsView
from django.urls import path
from info_companies.views import CompanyInfosView
from materials.views import CompanyMaterialsDetailsView, CompanyMaterialsView

from . import views

urlpatterns = [
    path("companies/", views.CompanyView.as_view()),
    path("companies/<int:id>/", views.CompanyDetailsView.as_view()),
    path("companies/<int:id>/discards/", DiscardCompanyView.as_view()),
    path("companies/<int:id>/discards/<int:discard_id>/", DiscardDetailsView.as_view()),
    path("companies/<int:id>/materials/", CompanyMaterialsView.as_view()),
    path(
        "companies/<int:id>/materials/<int:material_id>/",
        CompanyMaterialsDetailsView.as_view(),
    ),
    path(
        "companies/<int:id>/info_collection/",
        views.ListInfoCollectionCompany.as_view(),
    ),
    path("companies/<int:id>/info_company/", CompanyInfosView.as_view()),
]
