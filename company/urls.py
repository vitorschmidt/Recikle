from django.urls import path

from . import views

urlpatterns = [
    path("companies/", views.CompanyView.as_view()),
    path("companies/<int:id>/", views.CompanyDetailsView.as_view()),
]
