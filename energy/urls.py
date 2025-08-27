from django.urls import path
from . import views

urlpatterns = [
    path("collect/", views.collect_data_view, name="collect_data"),
    path("readings/", views.readings_list, name="readings"),
]
