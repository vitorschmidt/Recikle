from django.urls import path

from . import views

urlpatterns = [
    path("info_company/", views.InfoCompanyView.as_view()),
    path("info_company/<int:id>/", views.InfoCompanyDetailsView.as_view()),
]
