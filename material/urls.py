from django.urls import include, path

from material.views import ListCreateMaterialView,RetrieverUpdateProductView


urlpatterns = [
    path('materials/',ListCreateMaterialView.as_view()),
    path('materials/<id>/', RetrieverUpdateProductView.as_view()),
]