from django.urls import path

from discards.views import DiscardsView

urlpatterns = [
    path("discards/", DiscardsView.as_view()),
]
