from django.urls import include, path

from schedule_collects.views import ListSchedulesDetailsView, ListSchedulesView

urlpatterns = [
    path("schedules/", ListSchedulesView.as_view()),
    path("schedules/<int:id>/", ListSchedulesDetailsView.as_view()),
]
