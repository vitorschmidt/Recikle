from django.urls import include, path

from materials.views import ListCreateMaterialView,RetrieverUpdateProductView
from accumulation_points.views import AccumulationPointDetailsView,AccumulationPointView


urlpatterns = [
    path('materials/',ListCreateMaterialView.as_view()),
    path('materials/<int:id>/', RetrieverUpdateProductView.as_view()),
    path('materials/<int:id>/accumulation_point/',AccumulationPointView.as_view()),
    path('materials/<int:id>/accumulation_point/<int:accumulation_point_id>/',AccumulationPointDetailsView.as_view()),

]