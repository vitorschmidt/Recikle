from discards.views import DiscardCompanyView, DiscardDetailsView
from django.urls import path

from . import views

urlpatterns = [
    path("companies/", views.CompanyView.as_view()),
    path("companies/<int:id>/", views.CompanyDetailsView.as_view()),
    path("companies/<int:id>/discards/", DiscardCompanyView.as_view()),
    path("companies/<int:id>/discards/<int:discard_id>/", DiscardDetailsView.as_view()),
]
