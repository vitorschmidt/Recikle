from accumulation_points.views import (
    AccumulationPointDetailsView,
    AccumulationPointView,
)
from django.urls import path
from info_collects.views import (
    MaterialInfoCollectionDetailsView,
    MaterialInfoCollectionView,
)
from schedule_collects.views import ScheduleDetailsView, ScheduleView

from materials.views import ListCreateMaterialView, RetrieverUpdateProductView

urlpatterns = [
    path("materials/", ListCreateMaterialView.as_view()),
    path("materials/<int:id>/", RetrieverUpdateProductView.as_view()),
    path("materials/<int:id>/accumulation_point/", AccumulationPointView.as_view()),
    path(
        "materials/<int:id>/accumulation_point/<int:accumulation_point_id>/",
        AccumulationPointDetailsView.as_view(),
    ),
    path("materials/<int:id>/info_collection/", MaterialInfoCollectionView.as_view()),
    path(
        "materials/<int:id>/info_collection/<int:info_id>/",
        MaterialInfoCollectionDetailsView.as_view(),
    ),
    path(
        "materials/<int:id>/schedule/",
        ScheduleView.as_view(),
    ),
    path(
        "materials/<int:id>/schedule/<int:schedule_id>/",
        ScheduleDetailsView.as_view(),
    ),
]
