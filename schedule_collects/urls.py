from django.urls import include, path

from schedule_collects.views import ScheduleDetailsView,ScheduleView

urlpatterns = [
    path("schedule/",ScheduleView.as_view()),
    path('schedule/materials/<int:id>/',ScheduleView.as_view()),
    path('schedule/materials/<int:id>/<int:schedule_id>/',ScheduleDetailsView.as_view()),

]